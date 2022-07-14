<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-12 17:18:19
 * @LastEditTime: 2022-07-13 10:55:34
-->
<template>
    <Shops />
    <Cars />
</template>

<script>
import Shops from '../components/shop/Shops.vue'
import Cars from '../components/shop/Cars.vue'
export default {
    components: { Cars, Shops },
}
</script>