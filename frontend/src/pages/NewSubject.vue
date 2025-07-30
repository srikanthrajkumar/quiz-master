<template>
  <NavBar />

  <div class="container d-flex justify-content-center align-items-center flex-column" style="min-height: 90vh;">
    <div class="card p-4" style="width: 100%; max-width: 600px;">
       <h3 class="text-center mb-3">Add Subject</h3>
       <form @submit.prevent="createSubject">
          <div class="mb-3">
            <label for="name" class="form-label">Subject Name</label>
            <input v-model="name" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea v-model="description" class="form-control" rows="3" />
          </div>
          <button type="submit" class="btn btn-success w-100">Create Subject</button>
          <div v-if="error" class="text-danger text-center mt-2">{{ error }}</div>           
       </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

const router = useRouter();

const name = ref('');
const description = ref('');
const error = ref('');

async function createSubject() {
  try {
    const token = localStorage.getItem('token');
    await axios.post(`${import.meta.env.VITE_API_BASE_URL}/subjects`, {
      name: name.value,
      description: description.value,
    }, {
      headers: { Authorization: `Bearer ${token}` },
    });

    router.push('/dashboard');
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to create subject';
  }
}
</script>
