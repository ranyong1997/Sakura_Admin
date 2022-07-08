<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-07 17:17:22
 * @LastEditTime: 2022-07-07 18:10:56
-->

<script setup>
  import {
    useRouter
  } from 'vue-router'
  const router = useRouter()

  function toFoo() {
    router.push({
      path: '/foo'
    })
  }

  function toBar() {
    router.push({
      path: '/bar'
    })
  }
</script>

<template>
  <div>
    <img alt="Vue logo" src="./assets/logo.png" />
  </div>
  <button @click="toFoo">to foo</button>
  <button @click="toBar">to bar</button>
  <rout-link to="/bar">zzzz</rout-link>
  <router-view></router-view>
</template>

<style>
  #app {
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>