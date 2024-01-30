<template>
  <div id="app">
    <keep-alive :include="['Story']">
      <router-view />
    </keep-alive>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>