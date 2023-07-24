<template>
  <div class="h-screen">
    <Map />
  </div>
</template>

<script setup>
import Map from '@/components/Map'
import { authStore } from '@/stores/auth'
const auth = authStore();

onBeforeMount(async () => {
  if (!auth.isLogged){
    navigateTo('/')
  }
})
</script>