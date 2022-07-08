<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-07 17:23:48
 * @LastEditTime: 2022-07-07 17:51:44
-->
<template>
    <div>
        this is bar page
    </div>
    <p>{{store.state.test}}</p>
</template>
<script setup>
    import{
        useStore
    } from 'vuex'
    const store = useStore()
</script>
<style>
</style>