<template>
  <div>
    <h1>마이페이지</h1>
    <p>User ID: {{ userId }}</p>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref } from 'vue'

const userId = ref(null)

</script>

<style scoped>

</style>