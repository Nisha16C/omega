<template>
    <div>
      <h1>Dynamic HTML Renderer</h1>
      <div v-html="htmlContent"></div>
    </div>
  </template>
  
  <script lang="ts">
  import { ref, onMounted } from 'vue';
  
  export default {
    setup() {
      const htmlContent = ref<string>(''); // Define the type as string
  
      onMounted(async () => {
        try {
          const response = await fetch('/home/ubuntu/omega/frontend/public/index.html');
          htmlContent.value = await response.text();
        } catch (error) {
          console.error('Error fetching HTML file:', error);
        }
      });
  
      return { htmlContent };
    },
  };
  </script>
  