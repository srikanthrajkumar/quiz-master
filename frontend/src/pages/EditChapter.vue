<template>
  <div class="container mt-4">
    <h2>Edit Chapter</h2>
    <form @submit.prevent="updateChapter">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input v-model="chapter.name" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea v-model="chapter.description" class="form-control" />
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
const chapterId = route.params.id
const chapter = ref({ name: '', description: '' })

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/chapters/${chapterId}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    chapter.value = res.data
  } catch (err) {
    console.error('Failed to fetch chapter:', err)
  }
})

async function updateChapter() {
  try {
    const token = localStorage.getItem('token')
    await axios.put(`${import.meta.env.VITE_API_BASE_URL}/chapters/${chapterId}`, chapter.value, {
      headers: { Authorization: `Bearer ${token}` },
    })
    router.push('/dashboard')
  } catch (err) {
    console.error('Failed to update chapter:', err)
  }
}
</script>
