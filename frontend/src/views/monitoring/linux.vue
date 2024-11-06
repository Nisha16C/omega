 
<template>
   
  <div class="pr-5 " >
    <n-card >
      <div class="panel-card">

      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730005180833&to=1730091580833&theme=light&panelId=323" width="190" height="140" ></iframe>

      

      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730005418618&to=1730091818619&theme=light&panelId=20" width="190" height="140" frameborder="0"></iframe>
      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730021743290&to=1730108143290&theme=light&panelId=155" width="190" height="140" frameborder="0"></iframe>


      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730005418618&to=1730091818619&theme=light&panelId=21" width="190" height="140" frameborder="0"></iframe>

      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730021641601&to=1730108041601&theme=light&panelId=16" width="190" height="140" frameborder="0"></iframe>

      
      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730021579616&to=1730107979617&theme=light&panelId=154" width="190" height="140" frameborder="0"></iframe>
      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730021824341&to=1730108224342&theme=light&panelId=14" width="190" height="140" frameborder="0"></iframe>
      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730021891058&to=1730108291062&theme=light&panelId=15" width="150" height="140" frameborder="0"></iframe>
    </div>
    </n-card>
    <n-card >
      <div class="panel-card">

  
      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730006375871&to=1730092775871&theme=light&panelId=77" width="800" height="300" frameborder="0"></iframe>
      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730021984045&to=1730108384045&theme=light&panelId=78" width="800" height="300" frameborder="0"></iframe>
    </div>
    </n-card>
    <n-card >
      <div class="panel-card">

  
      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730006375871&to=1730092775871&theme=light&panelId=74" width="800" height="300" frameborder="0"></iframe>
      <iframe src="http://172.16.1.119:3000/d-solo/rYdddlPWk/node-exporter-full?orgId=1&refresh=1m&from=1730021984045&to=1730108384045&theme=light&panelId=152" width="800" height="300" frameborder="0"></iframe>
    </div>
    </n-card>

    
  
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useOsTheme } from 'naive-ui';

const iframeSrc = ref('');

const orgId = ref(null);
const theme = ref(true);
const ip = ref(null);
const dashboard_id = ref(null);
const froms = ref(null);
const tos = ref(null);

function getIframeSrc(isDark) {
  const baseSrc = `http://172.16.1.119:3000/d/fdongibf4r7r4d/kub-cluster-overview?orgId=1refresh=1m&from=now-15m&to=now&theme=light&kiosk=1`;
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
/* .panel-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
} */

.panel-card {
  /* width: fit-content; */
  display: flex;
  gap: 16px;


}
</style>
