#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 17:24
# @Author  : 冉勇
# @Site    : 
# @File    : crud.py
# @Software: PyCharm
# @desc    :
from sqlalchemy.orm import Session
from app.utils.models import *
from app.utils.schemas import *
from sqlalchemy import or_, and_


# 通过id查找用户
def get_user(db: Session, use_id: int):
    return db.query(User).filter(User.id == use_id, User.status == False).first()


def get_user_username(db: Session, username: str):
    return db.query(User).filter(User.username == username, User.status == False).first()


def get_role_name(db: Session, name: str):
    roles = db.query(Role).filter(Role.name == user.role).first()
    db_user = User(**user.dict())
    db_user.role = roles.id
    db.add(db_user)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_user)  # 刷新
    return db_user


def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id, Message.status == False).first()


def get_pid_message(db: Session, pid: int):
    return db.query(Message).filter(Message.pid == pid, Message.status == False).first()


def get_message_list(db: Session, page: int, limit: int):
    return db.query(Message).filter(
        or_(Message.senduser == userid, Message.acceptusers == userid,
            Message.status == 0)).all()


def db_creat_rebackmessage(db: Session, reback: RebackMessConnet, senduser: int):
    times = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

    reabck = Message(pid=reback.id, context=reback.connect)
    reabck.sendtime = times
    reabck.senduser = senduser
    db.add(reabck)
    db.commit()  # 提交保存到数据库中
    db.refresh(reabck)  # 刷新
    return reabckx


def db_create_course(db: Session, course: Courses, user: int):  # 创建课程
    course = Course(**course.dict())
    course.owner = user
    db.add(course)
    db.commit()  # 提交保存到数据库中
    db.refresh(course)  # 刷新
    return course


def db_get_course_name(db: Session, name: str):
    return db.query(Course).filter(Course.name == name, Course.status == False).first()


def db_get_course_id(db: Session, id: int):
    return db.query(Course).filter(Course.id == id, Course.status == False).first()


def db_get_coursecomment_id(db: Session, id: int):
    return db.query(Commentcourse).filter(Commentcourse.course == id, Commentcourse.status == False).all()


def get_cousecomments(db: Session, id: int):
    return db.query(Commentcourse).filter(Commentcourse.id == id, Commentcourse.status == False).all()


def createcomments(db: Session, cousecoment: Coursecomment, user: id):
    comments = Commentcourse(**cousecoment.dict())
    comments.users = user
    db.add(comments)
    db.commit()
    db.refresh(comments)
    return comments


def get_student(db: Session, couese: int, user: int):
    return db.query(Studentcourse).filter(Studentcourse.course == couese, Studentcourse.students == user,
                                          Studentcourse.status == False).first()


def add_student_course(db: Session, couese: int, user: int):
    studentcourse = Studentcourse(students=couese,
                                  course=user)
    db.add(studentcourse)
    db.commit()
    db.refresh(studentcourse)
    return studentcourse


def rebck_couses(db: Session, student: Studentcourse):
    student.status = True
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def getallcourse(db: Session):
    return db.query(Course).filter(Course.status == True).all()


def get_student_all(db: Session, user: int):
    return db.query(Studentcourse).filter(Studentcourse.students == user,
                                          Studentcourse.status == False).all()


def getlikeCourse(db: Session):
    return db.query(Course).filter(Course.likenum > 500,
                                   Course.onsale == True).all()
