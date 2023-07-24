import { env } from "process";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  typescript: {
    strict: true,
  },
  modules: ["@nuxtjs/tailwindcss", "nuxt-mapbox", "nuxt-icon", "@pinia/nuxt"],
  mapbox: {
    accessToken: `${env.MAPBOX_API}`,
  },
  runtimeConfig: {
    public: {
      baseURL: process.env.SERVER_API,
    },
  },
  css: ["@/assets/css/styles.css"],
});
