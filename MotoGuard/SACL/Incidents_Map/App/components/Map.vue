<script setup>
import { ref } from "vue";
import {
  addMainControls,
} from "@/composables/map/map.composable";
//const layers = layersStore();
const config = useRuntimeConfig();

let lat = 10.985986471629564;
let lng = -74.80175213213752;
let showInfoCard = ref(false);
let logs = ref([]);
/**
 * Get the main municipio data to set the limits
 */

const getLogsData = async () => {
  const { data, error, execute, pending, refresh } = await useFetch(
    `${config.baseURL}/logs`,
    {
      onRequest({ request, options }) {},
      onRequestError({ request, options, error }) {},
      async onResponse({ request, response, options }) {
        logs = await response._data;
      },
      onResponseError({ request, response, options }) {},
    }
  );
};

onBeforeMount(async () => {
  getLogsData();
});

const addMarkers = (map, data) => {
  console.log("daaa", data.length);/* 
  const newData = Array.from(
    new Set(data?.map((a) => a.longitud))
  ).map((Longitud) => {
    return data?.find((a) => a.latitud === Longitud);
  });
  console.log("new data", newData.length); */
  data.splice(100)
  data.map((element) => {

    let popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
      `<div>
        <strong>Alerta: </strong>${element.alerta}<br/>
        <strong>Velocidad: </strong>${element.velocidad}<br/>
        <strong>Fecha: </strong>${element.fecha}<br/>
        </div>`
    )

    new mapboxgl.Marker()
      .setLngLat([element.longitud, element.latitud])
      .setPopup(popup)
      .addTo(map);
  });
};

/* Callback to load after map loads */
useMapbox("map", (map) => {
  /* On load map */
  map.on("load", () => {
    addMainControls(map);

    /* Map on click */
    map.on("click", ["maine", "outline"], (e) => {
      showInfoCard.value = true;
    });

    map.flyTo({
      center: [lng, lat], // Fly to the selected target
      duration: 12000, // Animate over 12 seconds
      essential: true, // This animation is considered essential with
      //respect to prefers-reduced-motion
      zoom: 12,
    });

    addMarkers(map, logs);
  });
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<template>
  <MapboxMap
    map-id="map"
    class="relative top-0 bottom-0 left-0 w-full h-full"
    :options="{
      style: 'mapbox://styles/devjesg/clhkr6hjv007201qnf3di9kxz', // style URL
      center: [lng, lat], // municipality sabanalarga
      zoom: 2, // starting zoom
    }"
  ></MapboxMap>
</template>
