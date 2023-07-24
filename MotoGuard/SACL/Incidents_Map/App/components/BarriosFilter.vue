<script setup>
const getData = async () => {
  const { data, error, execute, pending, refresh } = await useFetch(
    `${config.baseURL}/municipios/1/barrios/`,
    {
      onRequest({ request, options }) {},
      onRequestError({ request, options, error }) {},
      async onResponse({ request, response, options }) {
        // Process the response data
        console.log("Data is ", response);
      },
      onResponseError({ request, response, options }) {},
    }
  );
};

onBeforeMount(() => {
  getData();
});
</script>

<template>
  <div>hola</div>
</template>
