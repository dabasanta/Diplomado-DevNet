<script setup lang="ts">
const { visible } = defineProps<{
  visible?: any;
}>();
</script>

<template>
  <div
    v-if="visible"
    class="bg-white/80 px-6 py-4 w-auto rounded-lg shadow-sm z-50 absolute right-2 top-2"
  >
    <slot />
  </div>
</template>
