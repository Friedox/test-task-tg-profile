<template>
  <router-view v-if="ready" />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from './store/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useUserStore()
const ready = ref(false)

onMounted(async () => {
  const initData = window.Telegram.WebApp.initDataUnsafe
  const telegramUser = initData.user
  const startParam = initData.start_param

  if (startParam) {
    await store.fetchUser(Number(startParam))
    router.replace(`/share/${startParam}`)
  } else if (telegramUser?.id) {
    await store.fetchUser(telegramUser.id)

    if (store.user) {
      router.replace('/profile')
    } else {
      router.replace('/')
    }
  } else {
    router.replace('/')
  }

  ready.value = true
})
</script>
