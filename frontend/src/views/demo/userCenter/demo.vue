<script setup lang="ts">
import { ref } from 'vue'
import { useMessage } from 'naive-ui'
import axios from 'axios'
import { useAuthStore } from '@/store'
import {BASE_URL_1} from "../../api-config.js";


const authStore = useAuthStore()
const { userInfo } = authStore

// Form references and values
const formRef = ref()
const formValue = ref({
  user: {
    name: '',
    age: '',
  },
  Nickname: '',
  email: '',
  password: '',
})
const isLoading = ref(false)
const message = useMessage()

// Validation rules
const rules = {
  user: {
    name: {
      required: true,
      message: 'Please enter a name',
      trigger: 'blur',
    },
    age: {
      required: true,
      message: 'Please enter an age',
      trigger: ['input', 'blur'],
    },
  },
  Nickname: {
    required: true,
    message: 'Please enter a nickname',
    trigger: ['input'],
  },
  email: {
    required: true,
    message: 'Please enter an email',
    trigger: ['input', 'blur'],
  },
  password: {
    required: true,
    message: 'Please enter a password',
    trigger: 'blur',
  },
}

// Function to create user in your system (e.g., using your Django API)
async function createUser(userData) {
  try {
    // Send the form data to the backend API (replace this URL with your actual user creation API)
    const response = await axios.post(`${BASE_URL_1}/api/v6/create-keycloak-user/`, userData, {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,  // Include the token for authentication if required
        'Content-Type': 'application/json',
      }
    })
    if (response.status === 201) {
      message.success("User created successfully")
      // Optionally clear the form after success
      formValue.value = {
        user: { name: '', age: '' },
        Nickname: '',
        email: '',
        password: '',
      }
    }
  } catch (error) {
    console.error("Error creating user:", error)
    message.error("Failed to create user")
  } finally {
    isLoading.value = false
  }
}

// Handle form validation and submission
function handleValidateClick() {
  formRef.value?.validate((errors) => {
    if (!errors) {
      const userData = {
        username: formValue.value.user.name,
        email: formValue.value.email,
        nickname: formValue.value.Nickname,
        age: formValue.value.user.age,
        password: formValue.value.password,
        enabled: true,  // Assuming you want to activate the user immediately
      }
      isLoading.value = true
      createUser(userData)
    } else {
      message.error('Validation failed')
    }
  })
}
</script>

<template>
  <n-space vertical>
    <n-card title="User Management">
      <n-space size="large">
        <n-avatar round :size="128" :src="userInfo?.avatar" />

        <n-descriptions label-placement="left" :column="2" :title="`Good evening, ${userInfo?.nickname}`">
          <n-descriptions-item label="ID">
            {{ userInfo?.id }}
          </n-descriptions-item>
          <n-descriptions-item label="Username">
            {{ userInfo?.userName }}
          </n-descriptions-item>
          <n-descriptions-item label="Real Name">
            {{ userInfo?.nickname }}
          </n-descriptions-item>
          <n-descriptions-item label="Role">
            {{ userInfo?.role }}
          </n-descriptions-item>
        </n-descriptions>
      </n-space>
    </n-card>

    <n-card title="Create New User">
      <n-space justify="center">
        <n-form ref="formRef" class="w-500px" :label-width="100" :model="formValue" :rules="rules">
          <n-form-item label="Name" path="user.name">
            <n-input v-model:value="formValue.user.name" placeholder="Enter username" />
          </n-form-item>
          <n-form-item label="Age" path="user.age">
            <n-input v-model:value="formValue.user.age" placeholder="Enter age" />
          </n-form-item>
          <n-form-item label="Nick Name" path="Nickname">
            <n-input v-model:value="formValue.Nickname" placeholder="Enter your nickname" />
          </n-form-item>
          <n-form-item label="Email" path="email">
            <n-input v-model:value="formValue.email" type="email" placeholder="Enter email" />
          </n-form-item>
          <n-form-item label="Password" path="password">
            <n-input v-model:value="formValue.password" type="password" placeholder="Enter password" />
          </n-form-item>
          <n-form-item>
            <n-button type="primary" :loading="isLoading" block @click="handleValidateClick">
              Create New User
            </n-button>
          </n-form-item>
        </n-form>
      </n-space>
    </n-card>
  </n-space>
</template>

<style scoped>
.w-500px {
  width: 500px;
}
</style>
