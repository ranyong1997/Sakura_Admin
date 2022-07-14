<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-12 17:20:31
 * @LastEditTime: 2022-07-12 17:49:52
-->
<template>
    <h1>购物车</h1>
    <ul v-if="carList.length > 0">
        <li v-for="item in carList" :key="item.id">
            <span>{{ item.title }}</span>
            <span>单价{{ item.price }}</span>
            <span>数量{{ item.nums }}</span>
            <button @click="addToCar(item.id)">+</button>
            <button @click="cudCar(item.id)">-</button>
        </li>
    </ul>
    <p>总价:{{ total }}</p>
</template>

<script>
import { carStore } from '../../store/Car'
export default {
    setup() {
        const car = carStore()
        const addToCar = (id) => {
            car.addToCar(id)
        }
        const cudCar = (id) => {
            car.cudCar(id)
        }
        return {
            car,
            addToCar, cudCar
        }
    },
    computed: {
        carList() {
            return this.car.carsList
        },
        total() {
            return this.car.totalPrice
        }
    }
}
</script>

<style>
</style>