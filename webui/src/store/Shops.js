/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-12 17:14:17
 * @LastEditTime: 2022-07-12 17:48:54
 */
import { defineStore } from 'pinia';
import getFood from '../api/foods';
export const shopStore = defineStore('shop', {
    state: () => {
        return {
            foods: [],
            isLoading: true,
        };
    },
    getters: {
        /**
         * 数组转对象 方便操作
         * @returns foods:{id:{food}}
         */
        getShopObj() {
            let foods = {};
            this.foods.forEach((item) => {
                foods[item.id] = item;
            });
            return foods;
        },
    },
    actions: {
        /**
         * 异步加载数据
         */
        async loadFoods() {
            this.foods = await getFood();
            this.isLoading = false;
        },
        /**
         * 加入购物车 商品数量减1
         * @param id
         */
        joinCard(id) {
            this.foods.forEach((item, index) => {
                if (item.id === id) {
                    if (this.foods[index].nums > 0) {
                        this.foods[index].nums--;
                    }
                }
            });
        },
        /**
         * 购物车商品减少 商品数量加1
         * @param id
         */
        cardToShop(id) {
            this.foods.forEach((item, index) => {
                if (item.id === id) {
                    this.foods[index].nums++;
                }
            });
        },
    },
});