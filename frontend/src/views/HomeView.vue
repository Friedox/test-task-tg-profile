<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-100">
    <h2 class="text-xl font-bold mb-6">Выберите дату рождения</h2>

    <div class="relative w-full max-w-md">
      <div class="flex justify-center bg-gradient-to-r from-purple-700 to-pink-500 p-4 rounded-lg shadow-lg">

        <div class="relative flex-1">
          <div ref="dayRef" class="scroll-container" @scroll="onScroll('day')">
            <div class="spacer"></div>
            <div v-for="(day, index) in days" :key="index" class="picker-item" :class="{ selected: selectedDay === day }">
              {{ day }}
            </div>
            <div class="spacer"></div>
          </div>
        </div>

        <div class="relative flex-1">
          <div ref="monthRef" class="scroll-container" @scroll="onScroll('month')">
            <div class="spacer"></div>
            <div v-for="(month, index) in months" :key="index" class="picker-item" :class="{ selected: selectedMonth === index + 1 }">
              {{ month }}
            </div>
            <div class="spacer"></div>
          </div>
        </div>

        <div class="flex-1">
          <div ref="yearRef" class="scroll-container" @scroll="onScroll('year')">
            <div class="spacer"></div>
            <div v-for="(year, index) in years" :key="year" class="picker-item" :class="{ selected: selectedYear === year }">
              {{ year }}
            </div>
            <div class="spacer"></div>
          </div>
        </div>
      </div>

      <div class="absolute top-1/2 left-0 right-0 pointer-events-none -translate-y-1/2">
        <div class="h-[40px] border-y-2 border-white/50"></div>
      </div>
    </div>

    <button
      @click="submit"
      class="mt-6 bg-green-500 text-white px-6 py-2 rounded w-48 disabled:bg-gray-400"
      :disabled="loading"
    >
      {{ loading ? 'Сохраняем...' : 'Сохранить' }}
    </button>

    <div class="mt-4 text-gray-600">
      Вы выбрали: {{ formattedDate }}
    </div>

    <div v-if="error" class="mt-2 text-red-500">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useUserStore } from '../store/user'
import { useRouter } from 'vue-router'

const store = useUserStore()
const router = useRouter()

const loading = ref(false)
const error = ref('')

const ITEM_HEIGHT = 40
const days = Array.from({ length: 31 }, (_, i) => i + 1)
const months = [
  'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
]
const currentYear = new Date().getFullYear()
const years = Array.from({ length: 100 }, (_, i) => currentYear - i)

const selectedDay = ref(days[0])
const selectedMonth = ref(1)
const selectedYear = ref(years[0])

const formattedDate = computed(() => {
  const monthNum = selectedMonth.value.toString().padStart(2, '0')
  const dayNum = selectedDay.value.toString().padStart(2, '0')
  return `${dayNum}.${monthNum}.${selectedYear.value}`
})

const dayRef = ref<HTMLDivElement | null>(null)
const monthRef = ref<HTMLDivElement | null>(null)
const yearRef = ref<HTMLDivElement | null>(null)

const onScroll = (type: 'day' | 'month' | 'year') => {
  nextTick(() => {
    let container: HTMLDivElement | null
    let items: number[]

    if (type === 'day') {
      container = dayRef.value
      items = days
    } else if (type === 'month') {
      container = monthRef.value
      items = months.map((_, idx) => idx + 1)
    } else {
      container = yearRef.value
      items = years
    }

    if (!container) return

    const children = container.querySelectorAll('.picker-item')
    const containerRect = container.getBoundingClientRect()
    const centerY = containerRect.top + containerRect.height / 2

    let closestIndex = 0
    let closestDistance = Infinity

    children.forEach((el, index) => {
      const rect = el.getBoundingClientRect()
      const elCenterY = rect.top + rect.height / 2
      const distance = Math.abs(centerY - elCenterY)

      if (distance < closestDistance) {
        closestDistance = distance
        closestIndex = index
      }
    })

    const value = items[closestIndex]
    if (value === undefined) return

    if (type === 'day') selectedDay.value = value
    if (type === 'month') selectedMonth.value = value
    if (type === 'year') selectedYear.value = value
  })
}

const scrollToSelected = (container: HTMLDivElement | null, items: number[], value: number) => {
  if (!container) return
  const index = items.indexOf(value)
  container.scrollTop = (index) * ITEM_HEIGHT
}

const submit = async () => {
  loading.value = true
  error.value = ''
  try {
    const telegramUser = window.Telegram.WebApp.initDataUnsafe.user

    await store.createUser({
      telegram_id: telegramUser.id,
      first_name: telegramUser.first_name,
      last_name: telegramUser.last_name,
      username: telegramUser.username,
      photo_url: telegramUser.photo_url,
      birthday: `${selectedYear.value}-${String(selectedMonth.value).padStart(2, '0')}-${String(selectedDay.value).padStart(2, '0')}`
    })

    router.push('/profile')
  } catch (err) {
    error.value = 'Ошибка при сохранении данных'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  nextTick(() => {
    scrollToSelected(dayRef.value, days, selectedDay.value)
    scrollToSelected(monthRef.value, months.map((_, idx) => idx + 1), selectedMonth.value)
    scrollToSelected(yearRef.value, years, selectedYear.value)
  })
})
</script>

<style scoped>
.scroll-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow-y: scroll;
  height: 200px;
  scroll-snap-type: y mandatory;
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.scroll-container::-webkit-scrollbar {
  display: none;
}
.picker-item {
  height: 40px;
  line-height: 40px;
  text-align: center;
  font-size: 16px;
  color: white;
  scroll-snap-align: center;
  transition: all 0.2s;
}
.picker-item.selected {
  font-weight: bold;
  font-size: 20px;
  color: white;
}
.spacer {
  height: 80px;
  flex-shrink: 0;
}
</style>
