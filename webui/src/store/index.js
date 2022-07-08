/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-07 17:46:35
 * @LastEditTime: 2022-07-07 17:50:01
 */
import {createStore} from 'vuex';

export default createStore({
    state:{
        test:0
    },
    mutations:{
        add(state){
            state.test++;
        },
        min(state){
            state.test--;
        },
        set99(state,payload){
            state.test = payload
        }
    },
    actions:{
        change(context,payload){
            setTimeout(()=>{
                context.commit('set99',payload)
            },1500)
        }
    }
});