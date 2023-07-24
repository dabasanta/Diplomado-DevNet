<template>
  <div
    class="absolute left-2 top-2 z-50 bg-white/90 p-2 rounded-lg shadow-sm text-sm w-1/4"
  >
    <div>
      <Icon
        name="uil:search"
        class="absolute right-4 top-4 text-gray-400 font-bold"
      />
      <Input type="text" name="search" placeholder="Búsqueda" :wFull="true" />
    </div>
  </div>
</template>

<script setup>
import Input from "@/components/Input";
</script>
