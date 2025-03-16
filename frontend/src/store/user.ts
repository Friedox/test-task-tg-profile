import { defineStore } from 'pinia'
import axios from 'axios'

interface User {
  id: number
  telegram_id: number
  first_name: string
  last_name?: string
  username?: string
  photo_url?: string
  birthday: string
  countdown?: string
}

const API_URL = import.meta.env.VITE_API_URL

export const useUserStore = defineStore('user', {
  state: (): { user: User | null } => ({ user: null }),
  actions: {
    async createUser(userData: Omit<User, 'id' | 'countdown'> & { birthday: string }) {
      const { data } = await axios.post(`${API_URL}/users/`, userData)
      this.user = { ...userData, ...data }
    },

    async fetchUser(telegram_id: number) {
      try {
        const { data } = await axios.get(`${API_URL}/users/telegram/${telegram_id}`)
        this.user = data
      } catch (error: any) {
        if (error.response && error.response.status === 404) {
          this.user = null
        } else {
          console.error('Ошибка загрузки пользователя:', error)
        }
      }
    }
  },
})
