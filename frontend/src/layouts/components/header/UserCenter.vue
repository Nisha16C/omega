<script setup lang="ts">
import { useAuthStore } from '@/store'
import { renderIcon } from '@/utils/icon'
import IconBookOpen from '~icons/icon-park-outline/book-open'
import IconGithub from '~icons/icon-park-outline/github'
import IconLogout from '~icons/icon-park-outline/logout'
import IconUser from '~icons/icon-park-outline/user'
import {useKeycloak} from '@/plugins/keycloak.js'
import IconAddUser from '~icons/icon-park-outline/add-user' // Add an icon for creating a new user
import {UI_URL} from "/home/ubuntu/omega-code/frontend/api-config.js";



const { t } = useI18n()

const { userInfo, logout } = useAuthStore()
const router = useRouter()

const options = computed(() => {
  return [
    {
      label: t('app.userCenter'),
      key: 'userCenter',
      icon: () => h(IconUser),
    },
    {
      type: 'divider',
      key: 'd1',
    },
    {
      type: 'divider',
      key: 'd1',
    },
    { type: 'divider', key: 'd3' },
    {
      label: t('app.loginOut'),
      key: 'loginOut',
      icon: () => h(IconLogout),
    },
    
  ]
})
function handleSelect(key: string | number) {
  if (key === 'loginOut') {
    window.$dialog?.info({
      title: t('app.loginOutTitle'),
      content: t('app.loginOutContent'),
      positiveText: t('common.confirm'),
      negativeText: t('common.cancel'),
      onPositiveClick: () => {
        logoutFromUIAndKeycloak();
      },
    })
  }
  if (key === 'userCenter')
    router.push('/userCenter')

  if (key === 'guthub')
    window.open('https://github.com/chansee97/nova-admin')

  if (key === 'gitee')
    window.open('https://gitee.com/chansee97/nova-admin')

  if (key === 'docs')
    window.open('https://nova-admin-docs.pages.dev/')
}

function logoutFromUIAndKeycloak() {
  // Call the UI logout (your store's logout function)
  console.log("Logging out from the UI...");
  logout();
  console.log("User has been logged out from the frontend.");

  // Call Keycloak logout
  const keycloak = useKeycloak(); // Assuming you have a Keycloak store or service
  console.log("Initiating Keycloak logout...");
  keycloak.logout({
    redirectUri: `${UI_URL}`,  // Redirect the user to the desired page after Keycloak logout
  }).then(() => {
    console.log("User has been logged out from Keycloak.");
  }).catch(error => {
    console.error("Error logging out from Keycloak:", error);
  });
}

</script>

<template>
  <n-dropdown
    trigger="click"
    :options="options"
    @select="handleSelect"
  >
    <n-avatar
      round

      :src="userInfo?.avatar"
    >
      <template #fallback>
        <div class="wh-full flex-center">
          <icon-park-outline-user />
        </div>
      </template>
    </n-avatar>
  </n-dropdown>
</template>

<style scoped></style>
