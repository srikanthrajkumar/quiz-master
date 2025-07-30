import { ref, computed } from 'vue'

export function useQuizTimer() {
  const timeRemaining = ref(0)
  const timeExpired = ref(false)
  let timerInterval = null

  const displayTime = computed(() => {
    const minutes = Math.floor(timeRemaining.value / 60)
    const seconds = timeRemaining.value % 60
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  })

  const startTimer = (onTimeExpired) => {
    timerInterval = setInterval(() => {
      if (timeRemaining.value > 0) {
        timeRemaining.value--
      } else {
        timeExpired.value = true
        clearInterval(timerInterval)
        onTimeExpired()
      }
    }, 1000)
  }

  const cleanup = () => {
    if (timerInterval) {
      clearInterval(timerInterval)
    }
  }

  return {
    timeRemaining,
    timeExpired,
    displayTime,
    startTimer,
    cleanup
  }
}