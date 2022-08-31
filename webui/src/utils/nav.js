/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-12 09:28:44
 * @LastEditTime: 2022-07-12 16:21:11
 */
import request from './axios'

export function login(data) {
    data = `username=${data.username}&password=${data.password}`
    return request({
        url: "/auth/login",
        headers: { 'content-type': 'application/x-www-form-urlencoded' },
        method: "post",
        data
    });
}