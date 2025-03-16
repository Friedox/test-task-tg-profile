<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
    <div v-if="user" class="bg-white p-6 rounded-lg shadow-lg text-center w-80">
      <img
        v-if="user.photo_url"
        :src="user.photo_url"
        class="rounded-full w-24 h-24 mx-auto mb-4"
      />

      <h2 class="text-xl font-semibold">{{ user.first_name }} {{ user.last_name }}</h2>
      <p class="text-gray-500">@{{ user.username }}</p>

      <!-- Новый отсчет -->
      <div v-if="countdownText" class="mt-4 text-lg font-semibold text-blue-600 flex flex-col items-center">
        🎉
        <span v-if="isOwner">
          Твой день рождения через
        </span>
        <span v-else>
          День рождения {{ user.first_name }} через
        </span>

        <!-- Сам отсчет -->
        <span class="mt-1 text-2xl">{{ countdownText }}</span>
      </div>

      <!-- Кнопки -->
      <button
        v-if="isOwner"
        @click="share"
        class="mt-6 bg-green-500 text-white px-4 py-2 rounded w-full"
      >
        Поделиться
      </button>

      <button
        v-else
        @click="goBack"
        class="mt-6 bg-gray-500 text-white px-4 py-2 rounded w-full"
      >
        В Свой Профиль
      </button>
    </div>

    <div v-else class="text-center text-lg">
      Данные не найдены
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '../store/user'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const store = useUserStore()
const route = useRoute()
const router = useRouter()

const telegramUser = window.Telegram.WebApp.initDataUnsafe.user
const currentTelegramId = ref<number>(
  route.params.telegram_id ? Number(route.params.telegram_id) : telegramUser.id
)

const isOwner = computed(() => telegramUser.id === currentTelegramId.value)
const user = computed(() => store.user)
const API_URL = import.meta.env.VITE_API_URL

// Счетчик обратного отсчета
const countdownText = ref('')
let countdownInterval: number | undefined

const startCountdown = () => {
  if (!user.value?.birthday) return

  const updateCountdown = () => {
    const now = new Date()
    const birthDate = new Date(user.value!.birthday)
    birthDate.setFullYear(now.getFullYear())

    // Если ДР в этом году прошло, берем следующий год
    if (birthDate < now) {
      birthDate.setFullYear(now.getFullYear() + 1)
    }

    const diffMs = birthDate.getTime() - now.getTime()

    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
    const diffHours = Math.floor((diffMs / (1000 * 60 * 60)) % 24)
    const diffMinutes = Math.floor((diffMs / (1000 * 60)) % 60)

    countdownText.value = `${diffDays} дн. ${diffHours} ч. ${diffMinutes} мин.`
  }

  updateCountdown()

  // Очищаем, чтобы не дублировать интервал
  if (countdownInterval) clearInterval(countdownInterval)

  countdownInterval = setInterval(updateCountdown, 60000) // обновлять каждую минуту
}

const fetchAndCheckUser = async () => {
  await store.fetchUser(currentTelegramId.value)

  if (!store.user) {
    if (isOwner.value) {
      router.replace('/')
    } else {
      router.replace('/profile')
    }
  } else {
    startCountdown() // запускаем отсчет после загрузки пользователя
  }
}

onMounted(fetchAndCheckUser)

watch(() => route.params.telegram_id, async (newId) => {
  currentTelegramId.value = newId ? Number(newId) : telegramUser.id
  await fetchAndCheckUser()
})

// Очистка при уничтожении компонента
onUnmounted(() => {
  if (countdownInterval) clearInterval(countdownInterval)
})

const share = async () => {
  try {
    const res = await axios.post(`${API_URL}/share_message/${telegramUser.id}`)
    const messageId = res.data.prepared_message_id

    if (window.Telegram.WebApp.shareMessage) {
      window.Telegram.WebApp.shareMessage(messageId, (success: boolean) => {
        if (success) {
          alert('✅ Сообщение успешно отправлено!')
        } else {
          alert('❌ Не удалось отправить сообщение.')
        }
      })
    } else {
      alert('❌ Ваш Telegram не поддерживает эту функцию.')
    }
  } catch (error) {
    console.error('Ошибка при создании prepared message:', error)
    alert('❌ Не удалось создать сообщение для отправки.')
  }
}

const goBack = async () => {
  currentTelegramId.value = telegramUser.id
  await store.fetchUser(telegramUser.id)

  if (store.user) {
    router.replace('/profile')
  } else {
    router.replace('/')
  }
}
</script>
