// src/types/telegram.d.ts

export {}

declare global {
  interface Window {
    Telegram: TelegramNamespace
  }

  interface TelegramNamespace {
    WebApp: TelegramWebApp
  }

  interface TelegramWebApp {
    initDataUnsafe: {
      user: TelegramUser
      start_param?: string
    }

    shareLink?: (params: { url: string }) => void

    shareMessage?: (
      messageId: string,
      callback?: (success: boolean) => void
    ) => void

    ready?: () => void
  }

  interface TelegramUser {
    id: number
    first_name: string
    last_name?: string
    username?: string
    language_code?: string
    birthday: string
    photo_url?: string
  }
}
