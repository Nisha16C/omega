<template>
  <n-card class="bordered" :shadow="'always'" size="large">
    
    <n-space vertical>
      <n-text type="success" class="text-2xl font-bold">
        Welcome OMEGA User {{ username }}
      </n-text>
      <n-text class="text-lg font-medium">
        Streamline your observability journey with OMEGA: Advanced monitoring and analytics in one platform.
      </n-text>
    </n-space>
  </n-card>
</template>

<script setup>
const username = 'Aastha Gupta'; // Replace with your actual data source
</script>

<style scoped>
/* Add any additional styling here if needed */
</style>
