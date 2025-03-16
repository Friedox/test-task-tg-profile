<template>
  <router-view v-if="ready" />
  <div v-else class="flex items-center justify-center h-screen">
    <p class="text-xl">Loading...</p>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useUserStore } from './store/user'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const store = useUserStore()

  const ready = ref(false)

  onMounted(async () => {
  const initData = window.Telegram?.WebApp?.initData ?? '';

  if (!initData || initData === '') {
    window.location.href = 'https://t.me/BirthdayProfileBot';
    return;
  }

  window.Telegram.WebApp.ready?.();

  const telegramUser = window.Telegram.WebApp.initDataUnsafe?.user;
  const startParam = window.Telegram.WebApp.initDataUnsafe?.start_param;

  if (startParam) {
    await store.fetchUser(Number(startParam));
    router.replace(`/share/${startParam}`);
  } else if (telegramUser?.id) {
    await store.fetchUser(telegramUser.id);
    router.replace('/profile');
  } else {
    router.replace('/');
  }

  ready.value = true;
  }
 );
</script>
