<template>
  <div v-if="visible" class="bg-red-200 absolute h-screen w-full">
    <image src="@/public/spinner.svg" alt="Spinner"></image>
  </div>
</template>

<script setup lang="ts">
const { visible } = defineProps<{
  visible: boolean;
}>();
</script>
