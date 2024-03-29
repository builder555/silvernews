import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useStore = defineStore('counter', () => {
  const isDark = ref(false)
  function toggleTheme() {
    isDark.value = !isDark.value
    const body = document.querySelector('body')
    if (isDark.value) {
      body.classList.add('dark')
    } else {
      body.classList.remove('dark')
    }
  }

  return { isDark, toggleTheme }
})
