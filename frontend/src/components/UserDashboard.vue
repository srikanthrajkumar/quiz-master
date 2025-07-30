<template>
  <div>
    <NavBar />
    
    <div class="container mt-4">
      <h2>User Dashboard</h2>

      <hr/>
      
      <div v-if="quizzes.length === 0" class="text-muted">
        No quizzes found.
      </div>

      <div v-else>
        <table class="table table-striped">
          <thead>
            <tr>
              <th style="width: 5%">Quiz ID</th>
              <th style="width: 10%">Subject</th>
              <th style="width: 15%">Chapter</th>
              <th style="width: 30%">Quiz</th>
              <th style="width: 10%">No. of Qs</th>
              <th style="width: 10%">Start Date</th>
              <th style="width: 10%">Duration</th>
              <th style="width: 10%">Start</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="quiz in quizzes" :key="quiz.id">
              <td>{{ quiz.id }}</td>
              <td>{{ quiz.subject_name }}</td>
              <td>{{ quiz.chapter_name }}</td>
              <td><b>{{ quiz.name }}</b></td>
              <td>{{ quiz.num_questions || 0 }}</td>
              <td>{{ quiz.date_of_quiz }}</td>
              <td>{{ quiz.time_duration }}</td>
              <td>
                <template v-if="isUpcoming(quiz.date_of_quiz)">
                  <div class="text-muted">
                    <i>Upcoming...</i>
                  </div> 
                </template>
                <template v-else>
                  <router-link :to="`/attempt/${quiz.id}`" class="btn btn-sm btn-success">Start</router-link>
                </template>
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

const isUpcoming = (quizDate) => {
  const today = new Date()
  
  const [day, month, year] = quizDate.split('/')
  const quiz = new Date(year, month - 1, day)
  
  today.setHours(0, 0, 0, 0)
  quiz.setHours(0, 0, 0, 0)
  
  return quiz > today
}

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