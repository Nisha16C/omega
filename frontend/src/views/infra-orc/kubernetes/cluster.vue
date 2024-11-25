<template>
  <div class="pr-5">
    <iframe
      :src="iframeSrc"
      width="100%"
      height="100%"
      frameborder="0"
      allowfullscreen
      class="m-5 dashboard-iframe"
    ></iframe>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useOsTheme } from "naive-ui";

const iframeSrc = ref("");

function getIframeSrc(isDark) {
  const baseSrc = `http://10.0.35.220:3000/d/bbfd65c0-2de8-4348-8f61-9b1fb2981ed1/kub-cluster-container-details?orgId=1&from=1731450716196&to=1731472316197&theme=light`;

  return baseSrc;
}

const osTheme = useOsTheme();
iframeSrc.value = getIframeSrc(osTheme.value === "dark");

watch(
  () => osTheme.value,
  (newTheme) => {
    iframeSrc.value = getIframeSrc(newTheme === "dark");
  }
);
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
}

#app {
  height: 100%;
}

.p-6 {
  height: calc(100vh - 12px); /* Adjusting for padding or other elements */
}

.dashboard-iframe {
  height: calc(100vh - 52px);
}

.overlay-text {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100px;
  text-align: center;
  background-color: white;
  z-index: 2;
}

.dark-overlay {
  position: absolute;
  top: 0%;
  left: 0%;
  width: 99.5%;
  height: 9.5%;
  text-align: center;
  color: white;
  background-color: rgb(15, 15, 15);
  padding: 10px;
  border-radius: 8px;
  z-index: 2;
}
</style>
