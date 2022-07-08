<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-07 17:23:54
 * @LastEditTime: 2022-07-07 17:52:36
-->
<template>
    <div>
        this is foo page
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