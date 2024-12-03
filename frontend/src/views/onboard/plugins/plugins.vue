<template>
  <div class="flex flex-wrap gap-4 p-4">
    <!-- First Box: Plugins -->
    <n-card class="p-4 w-full md:w-4/4 shadow-md rounded-lg">
      <n-text class="text-lg font-bold"> Plugins </n-text>

      <div class="card-container mt-4 w-200">
        <n-card
          v-for="card in cards"
          :key="card"
          :title="card"
          class="hover-card"
          :class="{ 'selected-card': selectedCards.includes(card), 'activated-card': activatedPlugins.includes(card) }"
          @click="toggleCard(card)"
        >
        </n-card>
      </div>
    </n-card>

    <!-- Second Box: Details -->
    <n-card class="p-4 w-full md:w-4/4 shadow-md rounded-lg">
      <n-text class="text-lg font-bold"> Details </n-text>
      <div class="mt-2">
        <p>Add your details-related content here.</p>
        <!-- Show the current activation or deactivation message -->
        <p v-if="currentAction && currentPlugin">
          Currently {{ currentAction }}: <strong>{{ currentPlugin }}</strong>
        </p>
      </div>

      <!-- Buttons at the bottom -->
      <div class="flex gap-4 mt-18">
        <!-- Enable/Disable Button -->
        <n-button
          :type="isEnabled ? 'error' : 'success'"
          @click="toggleEnableDisable"
        >
          {{ isEnabled ? "Disable" : "Enable" }}
        </n-button>

        <!-- Activate Button -->
        <n-button
          type="success"
          :disabled="selectedCards.every(card => activatedPlugins.includes(card))"
          @click="activatePlugins"
        >
          Activate
        </n-button>

        <!-- Deactivate Button -->
        <n-button
          type="warning"
          :disabled="selectedCards.every(card => !activatedPlugins.includes(card))"
          @click="deactivatePlugins"
        >
          Deactivate
        </n-button>
      </div>
    </n-card>
  </div>
</template>

<script setup>
import { ref } from "vue";

// List of cards and activated plugins
const cards = ref(['SOC Wazuh', 'Wazuh2', 'Wazuh3']);
const activatedPlugins = ref([]); // Tracks the activated plugins

// Selected cards
const selectedCards = ref([]);

// Track the current plugin being activated or deactivated
const currentPlugin = ref('');
const currentAction = ref('');

// Track the state for Enable/Disable
const isEnabled = ref(false);

// Toggle card selection
const toggleCard = (card) => {
  if (selectedCards.value.includes(card)) {
    selectedCards.value = selectedCards.value.filter((c) => c !== card);
  } else {
    selectedCards.value.push(card);
  }
};

// Enable/Disable functionality
const toggleEnableDisable = () => {
  isEnabled.value = !isEnabled.value;
  console.log(isEnabled.value ? "Enabled" : "Disabled");
};

// Activate selected plugins
const activatePlugins = () => {
  selectedCards.value.forEach((card) => {
    if (!activatedPlugins.value.includes(card)) {
      activatedPlugins.value.push(card);
      console.log(`Activated plugin: ${card}`);
      
      // Set current plugin and action for the UI
      currentPlugin.value = card;
      currentAction.value = 'Activating';
    }
  });
  console.log('Activated plugins:', activatedPlugins.value);
  
  // Clear the selected cards after activation
  selectedCards.value = [];
  
  // Hide the message after activation completes
  setTimeout(() => {
    currentPlugin.value = '';
    currentAction.value = '';
  }, 2000); // Wait for 2 seconds before hiding the message
};

// Deactivate selected plugins and deselect them
const deactivatePlugins = () => {
  selectedCards.value.forEach((card) => {
    const index = activatedPlugins.value.indexOf(card);
    if (index !== -1) {
      activatedPlugins.value.splice(index, 1); // Remove from activated list
      console.log(`Deactivated plugin: ${card}`);
      
      // Set current plugin and action for the UI
      currentPlugin.value = card;
      currentAction.value = 'Deactivating';
    }
  });
  console.log('Activated plugins:', activatedPlugins.value);
  
  // Clear the selection after deactivation
  selectedCards.value = [];
  
  // Hide the message after deactivation completes
  setTimeout(() => {
    currentPlugin.value = '';
    currentAction.value = '';
  }, 2000); // Wait for 2 seconds before hiding the message
};
</script>

<style scoped>
/* Optional custom styles */
.card-container {
  display: flex;
  flex-direction: row;
  gap: 1rem;
}
.hover-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.hover-card:hover {
  transform: translateY(-10px); /* Card ko upar uthata hai */
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3); /* Shadow ko bada karta hai */
}
.selected-card {
  border: 1px solid black;
  background-color: lightgray;
}
.activated-card {
  background-color: pink !important;
}
</style>
