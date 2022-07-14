/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-12 17:14:14
 * @LastEditTime: 2022-07-12 17:15:47
 */
import { defineStore } from 'pinia';
import { shopStore } from './Shops';
export const carStore = defineStore('car', {
    state: () => {
        return {
            cars: {},
            price: 0,
        };
    },
    getters: {
        /**
         * 对象转数组 便于展示
         */
        carsList() {
            let cars = [];
            if (!this.cars) {
                return [];
            }
            for (var key in this.cars) {
                if (this.cars.hasOwnProperty(key)) {
                    cars.push(this.cars[key]);
                }
            }
            return cars;
        },
        /**
         * 计算总价
         */
        totalPrice() {
            let cars = this.carsList;
            let total = cars.reduce((all, item) => {
                return all + item.price * item.nums;
            }, 0);
            return total;
        },
    },
    actions: {
        /**
         * 添加到购物车
         * @param id
         */
        addToCar(id) {
            const shop = shopStore();
            // 获取商品
            let foods = shop.getShopObj;
            if (foods[id].nums <= 0) {
                return;
            }
            // 商品数量减少
            shop.joinCard(id);
            // 购物车如果存在商品 数量加1 否则新增
            if (this.cars[id]) {
                this.cars[id].nums++;
            }
            else {
                // 简单深拷贝
                this.cars[id] = JSON.parse(JSON.stringify(foods[id]));
                this.cars[id].nums = 1;
            }
        },
        /**
         * 从购物车减少
         * @param id
         */
        cudCar(id) {
            const shop = shopStore();
            // 如果只剩下一个就移除 否则就减少一个
            if (this.cars[id].nums === 1) {
                Reflect.deleteProperty(this.cars, id);
            }
            else {
                this.cars[id].nums--;
            }
            // 商品数量加1
            shop.cardToShop(id);
        },
    },
});