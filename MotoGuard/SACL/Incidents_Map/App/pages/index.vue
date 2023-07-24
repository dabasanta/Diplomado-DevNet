<template>
  <div class="h-screen bg-green-200 py-20">
    <div class="px-6 py-6 bg-white rounded-lg m-auto w-1/4 flex shadow-lg">
      <form class="w-full">
        <div class="grid gap-4">
          <h3 class="font-bold text-gray-500 text-xl">Login</h3>
          <hr class="opacity-50" />
          <input type="text" name="username" placeholder="Username" class="px-6 py-2 text-sm outline-none rounded-sm bg-gray-200" v-model="usernameInput" />
          <input type="password" name="password" placeholder="Password" class="px-6 py-2 text-sm outline-none rounded-sm bg-gray-200" v-model="passwordInput" />
          <div>
            <button type="button" class="bg-emerald-500 px-6 py-2 rounded-sm text-white hover:bg-emerald-700 duration-400 w-full" @click="submitHandler()">Login</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import {ref } from 'vue';
import { authStore } from '@/stores/auth'
let usernameInput = ref("");
let passwordInput = ref("");
const auth = authStore();
const submitHandler = async () => {
if (usernameInput.value == "admin" && passwordInput.value == "password123."){
  auth.loggedIn();
  await navigateTo('/map');
}
else {
  alert('Invalid credentials')
}
}
</script>