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
import { useQuizTimer } from '@/utils/useQuizTimer'

const route = useRoute()
const router = useRouter()
const quizId = parseInt(route.params.quizId)

const quiz = ref(null)
const answers = ref([])
const isSubmitting = ref(false)

const { timeRemaining, timeExpired, displayTime, startTimer, cleanup } = useQuizTimer()

const currentScore = computed(() => {
  if (!quiz.value || !quiz.value.questions || quiz.value.questions.length === 0) return 0
  
  const totalScore = answers.value.reduce((total, score) => {
    return total + (score || 0)
  }, 0)
  
  const totalQuestions = quiz.value.questions.length
  return Math.round((totalScore / totalQuestions) * 100)
})

async function loadQuiz() {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(
      `${import.meta.env.VITE_API_BASE_URL}/user/attempt`,
      { headers: { Authorization: `Bearer ${token}` } }
    )

    const foundQuiz = response.data.find(q => q.id === quizId)
    if (foundQuiz) {
      quiz.value = foundQuiz
      answers.value = Array(foundQuiz.questions.length).fill(null)
      timeRemaining.value = foundQuiz.time_duration
      startTimer(submitQuiz)
    }
  } catch (error) {
    console.error('Failed to load quiz:', error)
  }
}

async function submitQuiz() {
  if (isSubmitting.value) return;

  isSubmitting.value = true;
  cleanup();

  try {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');
    const totalScore = currentScore.value;

    await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/users/${userId}/scores`,
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
    if (error.response && error.response.status === 409) {
      try {
        const token = localStorage.getItem('token');
        const userId = localStorage.getItem('user_id');
        const totalScore = currentScore.value;

        await axios.put(
          `${import.meta.env.VITE_API_BASE_URL}/users/${userId}/scores`,
          {
            quiz_id: quizId,
            total_scored: totalScore
          },
          {
            headers: { Authorization: `Bearer ${token}` }
          }
        );

        router.push('/dashboard');
      } catch (putError) {
        console.error('Failed to update score:', putError);
        isSubmitting.value = false;
      }
    } else {
      console.error('Failed to submit score:', error);
      isSubmitting.value = false;
    }
  }
}

onMounted(loadQuiz)
onUnmounted(cleanup)
</script>