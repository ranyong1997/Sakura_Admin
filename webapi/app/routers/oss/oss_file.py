#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 11:39
# @Author  : 冉勇
# @Site    : 
# @File    : oss_file.py
# @Software: PyCharm
# @desc    : oss文件
from fastapi import APIRouter, File, Depends, UploadFile
from webapi.app.crud.auth.UserDao import UserDao
from webapi.app.crud.oss.SakuraOssDao import SakuraOssDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.middleware.oss import OssClient
from webapi.app.models.oss_file import SakuraOssFile
from webapi.app.routers import Permission, get_session
from webapi.config import Config

router = APIRouter(prefix="/oss")


@router.post('/upload')
async def create_oss_file(filepath: str, file: UploadFile = File(...),
                          session=Depends(get_session),
                          user_info=Depends(Permission(Config.MEMBER))):
    try:
        file_content = await file.read()
        client = OssClient.get_oss_client()
        # oss上传 警告:可能存在数据不同步的问题,oss成功 本地失败
        file_url, file_size = await client.create_file(filepath, file_content)
        # 本地数据也要备份一份
        model = SakuraOssFile(user_info['id'], filepath, file_url, SakuraOssFile.get_size(file_size))
        record = await SakuraOssDao.query_record(filepath=filepath, deleted_at=0)
        if record is not None:
            record.file_path = filepath
            record.view_url = file_url
            record.file_size = file_size
            await SakuraOssDao.update_record_by_id(user_info['id'], record)
        else:
            await SakuraOssDao.insert_record(model, True)
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(f"上传失败:{e}")


@router.post("/avatar", summary="上传用户头像")
async def upload_avatar(file: UploadFile = File(...), user_info=Depends(Permission(Config.MEMBER))):
    try:
        file_content = await file.read()
        suffix = file.filename.split('.')[-1]
        filepath = f"user_{user_info['id']}.{suffix}"
        client = OssClient.get_oss_client()
        file_url, _ = await client.create_file(filepath, file_content, base_path="avatar")
        await UserDao.update_avatar(user_info['id'], file_url)
        return SakuraResponse.success(file_url)
    except Exception as e:
        return SakuraResponse.failed(f"上传用户头像失败:{e}")


@router.get('/list')
async def list_oss_file(filepath: str = '', _=Depends(Permission(Config.MEMBER))):
    try:
        records = await SakuraOssDao.list_record(condition=[SakuraOssFile.file_path.like(f"%{filepath}%")])
        return SakuraResponse.records(records)
    except Exception as e:
        return SakuraResponse.failed(f"获取失败:{e}")


@router.get('/delete')
async def delete_oss_file(filepath: str, user_info=Depends(Permission(Config.MEMBER)), session=Depends(get_session)):
    try:
        # 先获取到本地的记录,拿到sha值
        record = await SakuraOssDao.query_record(filepath=filepath, delete_at=0)
        if record is None:
            raise Exception("文件不存在或已被删除")
        await SakuraOssDao.delete_by_id(session, user_info['id'], record, log=True)
        client = OssClient.get_oss_client()
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(f"删除失败:{e}")


@router.get("/download")
async def download_oss_file(filepath: str):
    """
    更新oss文件,路径不能变化
    :param filepath:
    :return:
    """
    try:
        client = OssClient.get_oss_client()
        # 切割获取文件名
        path, filename = await client.download_file(filepath)
        return SakuraResponse.file(path, filename)
    except Exception as e:
        return SakuraResponse.failed(f"下载失败:{e}")
