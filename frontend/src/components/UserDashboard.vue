<template>
  <div>
    <NavBar />
    
    <div class="container mt-4">
      <h2 align="center">User Dashboard</h2>
      
      <div v-if="quizzes.length === 0" class="text-muted">
        No quizzes found.
      </div>

      <div v-else>
        <table class="table table-striped">
          <thead>
            <tr>
              <th style="width: 10%">Quiz Id</th>
              <th style="width: 30%">Quiz Name</th>
              <th style="width: 15%">No. of Questions</th>
              <th style="width: 15%">Duration</th>
              <th style="width: 15%">View</th>
              <th style="width: 15%">Start</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in quizzes" :key="quiz.id">
              <td>{{ quiz.id }}</td>
              <td>{{ quiz.name }}</td>
              <td>{{ quiz.num_questions || 0 }}</td>
              <td>{{ quiz.time_duration }}</td>
              <td>
                <router-link :to="`/quizzes/${quiz.id}`" class="btn btn-sm btn-primary">View</router-link>
              </td>
              <td>  
                <router-link :to="`/attempt/${quiz.id}`" class="btn btn-sm btn-success">Start</router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

const quizzes = ref([]);

onMounted(async () => {
  try {
    const token = localStorage.getItem('token');

    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/user/quizzes`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    quizzes.value = res.data;
  } catch (err) {
    console.error('Failed to fetch quizzes:', err);
  }
});
</script>