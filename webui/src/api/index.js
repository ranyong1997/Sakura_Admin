/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-08 09:37:06
 * @LastEditTime: 2022-07-08 09:55:57
 */
import ApiManager from "../api/apiManager";
const apiManager = ApiManager.getApiHost("", "");

export function userLogin(data) {
    return apiManager.post('你的baseURL' + '你的接口路径', data)
}