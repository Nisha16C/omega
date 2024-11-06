 
<template>
   
  <div class="pr-5 grafana-container">
    
    <iframe
      :src="iframeSrc"
      width="100%"
      height="100%"
      frameborder="0"
      allowfullscreen
      class="m-5 dashboard-iframe"
    ></iframe>
    <!-- <div class="overlay"></div> -->
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useOsTheme } from 'naive-ui';

const iframeSrc = ref('');

function getIframeSrc(isDark) {
  const baseSrc = `http://172.16.1.119:3000/d/fdongibf4r7r4d/kub-cluster-overview?orgId=1&from=1730766653757&to=1730788253762&theme=light`;
  
  
  return baseSrc ;
}

const osTheme = useOsTheme();
iframeSrc.value = getIframeSrc(osTheme.value === 'dark');

watch(
  () => osTheme.value,
  (newTheme) => {
    iframeSrc.value = getIframeSrc(newTheme === 'dark');
  }
);
</script>

<style scoped>
html, body {
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
.grafana-container {
  position: relative;
}
.overlay {
  position: absolute;
  top: 0; /* Adjust to cover only the unwanted parts */
  left: 0;
  width: 100%;
  height: 60px; /* Adjust height based on what you want to hide */
  background: white; /* Or match your app's background */
  z-index: 1;
}
</style>
