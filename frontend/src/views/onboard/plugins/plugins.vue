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
            :class="{ 'selected-card': selectedCards.includes(card) }"
            @click="toggleCard(card)"
          >
          </n-card>
        </div>
      </n-card>

      <!-- Second Box: Details -->
      <n-card class="p-4 w-full md:w-4/4 shadow-md rounded-lg">
        <n-text class="text-lg font-bold"> Details </n-text>
        <div class="mt-2">
          <!-- Content inside Details box -->
          <p>Add your details-related content here.</p>
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

          <!-- Activate/Deactivate Button -->
          <n-button
            :type="isActivated ? 'info' : 'warning'"
            ghost
            @click="toggleActivateDeactivate"
          >
            {{ isActivated ? "Deactivate" : "Activate" }}
          </n-button>
        </div>
      </n-card>
    </div>
  </template>

  <script setup>
  import { ref } from "vue";

  // State variables for buttons
  const isEnabled = ref(false); // Track Enable/Disable state
  const isActivated = ref(false); // Track Activate/Deactivate state

  // List of cards
  const cards = ref(['SOC Wazuh', 'Wazuh2', 'Wazuh3']);

  // Selected cards
  const selectedCards = ref([]);

  // Toggle card selection
  const toggleCard = (card) => {
    if (selectedCards.value.includes(card)) {
      // If card is already selected, remove it
      selectedCards.value = selectedCards.value.filter((c) => c !== card);
    } else {
      // If card is not selected, add it
      selectedCards.value.push(card);
    }
  };

  // Toggle logic for Enable/Disable
  const toggleEnableDisable = () => {
    isEnabled.value = !isEnabled.value;
  };

  // Toggle logic for Activate/Deactivate
  const toggleActivateDeactivate = () => {
    isActivated.value = !isActivated.value;
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

  </style>
