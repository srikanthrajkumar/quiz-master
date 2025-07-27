<template>
  <div class="container mt-4">
    <h2>New Question</h2>
    <form @submit.prevent="createQuestion">
      <div class="mb-3">
        <label class="form-label">Question Statement</label>
        <textarea v-model="question.question_statement" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Option 1</label>
        <input v-model="question.option1" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Option 2</label>
        <input v-model="question.option2" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Option 3</label>
        <input v-model="question.option3" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Option 4</label>
        <input v-model="question.option4" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Correct Option</label>
        <input v-model="question.correct_option_index" type="number" class="form-control" min="1" max="4" />
      </div>
      <div class="mb-3">
        <label class="form-label">Photo</label>
        <textarea v-model="question.photoURL" class="form-control" />
      </div>
      <button type="submit" class="btn btn-success">Create Question</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const quizId = route.params.id

const question = ref({
  question_statement: '',
  option1: '',
  option2: '',
  option3: '',
  option4: '',
  correct_option_index: '',
  photoURL: ''
})

async function createQuestion() {
  try {
    const token = localStorage.getItem('token')
    await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/quizzes/${quizId}/questions`,
      question.value,
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )
    router.push('/quizview')
  } catch (err) {
    console.error('Failed to create question:', err)
  }
}
</script>
