<template>
  <div class="container mt-4">
    <div v-if="quiz">
        <h2>{{ quiz.name }}</h2>
        <p><strong>Time: {{ displayTime }}</strong></p>

        <div v-if="timeExpired" class="alert alert-danger">
        <p>Time's up! Quiz submitted automatically.</p>
        </div>

        <form @submit.prevent="submitQuiz" v-if="quiz">
        <div
            v-for="(question, index) in quiz.questions"
            :key="question.id"
            class="mb-3"
        >
            <QuestionCard
            :question="question"
            :model-value="answers[index]"
            @update:model-value="answers[index] = $event"
            :disabled="timeExpired"
            />
        </div>

        <hr />
        <p>Score: {{ currentScore }} / {{ quiz.questions.length }}</p>
        <button type="submit" class="btn btn-primary" :disabled="timeExpired || isSubmitting">
            {{ isSubmitting ? 'Submitting...' : 'Submit Quiz' }}
        </button>

        </form>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import QuestionCard from '@/components/QuestionCard.vue'

const route = useRoute()
const router = useRouter()
const quizId = parseInt(route.params.quizId)
console.log(quizId)

const quiz = ref(null)
const answers = ref([])
const timeRemaining = ref(0)
const timeExpired = ref(false)
const isSubmitting = ref(false)

let timerInterval = null

const displayTime = computed(() => {
  const minutes = Math.floor(timeRemaining.value / 60)
  const seconds = timeRemaining.value % 60
  return `${minutes.toString().padStart(2, '0')}:${seconds
    .toString()
    .padStart(2, '0')}`
})

const currentScore = computed(() => {
  if (!quiz.value) return 0
  return answers.value.reduce((total, score) => {
    return total + (score || 0)
  }, 0)
})

async function loadQuiz() {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(
      `${import.meta.env.VITE_API_BASE_URL}/user/quizzes`,
      { headers: { Authorization: `Bearer ${token}` } }
    )

    console.log('Quiz API data:', response.data)

    const foundQuiz = response.data.find(q => q.id === quizId)
    if (foundQuiz) {
      quiz.value = foundQuiz
      answers.value = Array(foundQuiz.questions.length).fill(null)

      const [hh, mm, ss] = foundQuiz.time_duration.split(':').map(Number)
      timeRemaining.value = hh * 3600 + mm * 60 + ss

      startTimer()
    }
  } catch (error) {
    console.error('Failed to load quiz:', error)
  }
}

function startTimer() {
  timerInterval = setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--
    } else {
      timeExpired.value = true
      clearInterval(timerInterval)
      submitQuiz()
    }
  }, 1000)
}

async function submitQuiz() {
  if (isSubmitting.value) return;

  isSubmitting.value = true;
  clearInterval(timerInterval);

  try {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');
    const totalScore = currentScore.value;

    await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/score/${userId}`,
      {
        quiz_id: quizId,
        total_scored: totalScore
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    );

    router.push('/dashboard');
  } catch (error) {
    console.error('Failed to submit score:', error);
    isSubmitting.value = false;
  }
}


onMounted(loadQuiz)

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
})
</script>
