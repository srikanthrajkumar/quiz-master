<template>
  <NavBar />

  <div class="container d-flex justify-content-center align-items-center flex-column" style="min-height: 90vh;">
    <div class="card p-4" style="width: 100%; max-width: 600px;">
       <h3 class="text-center mb-3">Add Chapter</h3>
        <form @submit.prevent="updateChapter">
            <div class="mb-3">
                <label class="form-label">Name</label>
                <input v-model="chapter.name" type="text" class="form-control" />
            </div>
            <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="chapter.description" class="form-control" />
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
