<script setup lang="ts">
const { wFull } = defineProps<{
  type?: string;
  name?: string;
  placeholder: string;
  wFull: boolean;
}>();
</script>

<template>
  <input
    :type="type"
    :name="name"
    :placeholder="placeholder"
    class="bg-gray-100 border border-gray-300 px-2 py-1 rounded-lg outline-none focus:border-blue-300 focus:border duration-600 text-gray-600"
    v-bind:class="{ 'w-full': wFull }"
  />
</template>
