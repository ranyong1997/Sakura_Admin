<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-12 17:20:13
 * @LastEditTime: 2022-07-12 17:45:41
-->
<template>
    <ul v-if="!isLoading">
        <li v-for="item in foods" :key="item.id">
            <span>{{ item.title }}</span>
            <span>单价{{ item.price }}</span>
            <span>数量{{ item.nums }}</span>
            <button @click="addToCar(item.id)" :disabled="item.nums === 0">加入购物车</button>
        </li>
    </ul>
    <p v-if="isLoading">加载中</p>
</template>

<script>
import { shopStore } from '../../store/Shops'
import { carStore } from '../../store/Car'
export default {
    setup() {
        const shops = shopStore();
        shops.loadFoods()
        const car = carStore()
        const addToCar = (id) => {
            car.addToCar(id)
        }
        return {
            shops,
            addToCar
        }
    },
    computed: {
        foods() {
            return this.shops.foods
        },
        isLoading() {
            return this.shops.isLoading
        }
    }
}
</script>

<style>
</style>