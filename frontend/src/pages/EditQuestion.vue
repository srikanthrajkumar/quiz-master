<template>
  <NavBar />
  
  <div class="container d-flex justify-content-center align-items-center flex-column" style="min-height: 140vh;">
    <div class="card p-4" style="width: 100%; max-width: 600px;">
        <h3 class="text-center mb-3">Edit Question</h3>
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
            <button type="submit" class="btn btn-primary w-100">Save Changes</button>
        </form> 
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import NavBar from '@/components/NavBar.vue';

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
    router.push('/quiz')
  } catch (err) {
    console.error('Failed to update question:', err)
  }
}
</script>
