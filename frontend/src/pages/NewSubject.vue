<template>
  <div class="container mt-4">
    <h3>Add New Subject</h3>
    <form @submit.prevent="createChapter">
      <div class="mb-3">
        <label for="name" class="form-label">Subject Name</label>
        <input v-model="name" type="text" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea v-model="description" class="form-control" rows="3" />
      </div>
      <button type="submit" class="btn btn-success">Create Subject</button>
    </form>

    <p class="text-danger mt-2" v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

const name = ref('');
const description = ref('');
const error = ref('');

async function createChapter() {
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
