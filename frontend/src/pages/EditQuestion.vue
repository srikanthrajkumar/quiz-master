<template>
  <div class="container mt-4">
    <h2>Edit Question</h2>
    <form @submit.prevent="updateQuestion">
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
        <input v-model="question.correct_option_index" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Photo</label>
        <textarea v-model="question.photoURL" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Save Changes</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const questionId = route.params.id
const question = ref({ question_statement: '', option1: '', option2: '', option3: '', option4: '', correct_option_index: '', photoURL: ''})

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/questions/${questionId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    question.value = res.data
  } catch (err) {
    console.error('Failed to fetch question:', err)
  }
})

async function updateQuestion() {
  try {
    const token = localStorage.getItem('token')
    await axios.put(`${import.meta.env.VITE_API_BASE_URL}/questions/${questionId}`, question.value, {
      headers: { Authorization: `Bearer ${token}` },
    })
    router.push('/quizview')
  } catch (err) {
    console.error('Failed to update question:', err)
  }
}
</script>
