#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 09:31
# @Author  : 冉勇
# @Site    : 
# @File    : address.py
# @Software: PyCharm
# @desc    : 网关地址CRUD
from fastapi import Depends
from webapi.app.crud.config.AddressDao import SakuraGatewayDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.models.address import SakuraGateway
from webapi.app.routers import Permission, get_session
from webapi.app.routers.config.environment import router
from webapi.app.schema.address import SakuraAddressForm
from webapi.config import Config


@router.get("/gateway/list", summary="查询网关地址")
async def list_gateway(name: str = '', gateway: str = '', env: int = None,
                       user_info=Depends(Permission(Config.MEMBER))):
    data = await SakuraGatewayDao.list_record(env=env, gateway=f"{gateway}", name=f"{name}")
    return SakuraResponse.success(data)


@router.post("/gateway/insert", summary="添加网关地址", description="添加网关地址,只有组长可以操作")
async def insert_gateway(form: SakuraAddressForm, user_info=Depends(Permission(Config.MEMBER))):
    model = SakuraGateway(**form.dict(), user_id=user_info['id'])
    model = await SakuraGatewayDao.insert_record(model, True)
    return SakuraResponse.success(model)


@router.post("/gateway/update", summary="编辑网关地址", description="编辑网关地址,只有组长可以操作")
async def update_gateway(form: SakuraAddressForm, user_info=Depends(Permission(Config.MEMBER))):
    model = await SakuraGatewayDao.update_record_by_id(user_info['id'], form, True, log=True)
    return SakuraResponse.success(model)


@router.get("/gateway/delete", summary="删除网关地址", description="根据id删除网关地址,自由组长可以操作")
async def delete_gateway(id: int, user_info: Depends(Permission(Config.MEMBER)), session=Depends(get_session)):
    await SakuraGatewayDao.delete_record_by_id(session, user_info['id'], id)
    return SakuraResponse.success()
