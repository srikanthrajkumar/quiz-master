<template>
  <div>
    <NavBar />
    
    <div class="container mt-4">
      <h2>User Summary</h2>
      <hr/>
      
      <h4>Details</h4>

      <div v-if="!subjects || subjects.length === 0" class="text-muted">
        No summary found.
      </div>

      <table v-else class="table table-striped">
        <thead>
          <tr>
            <th style="width: 20%">Subject</th>
            <th style="width: 15%">Total Quizzes</th>
            <th style="width: 15%">Pending/Upcoming</th>
            <th style="width: 20%">Average</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="subject in subjects" :key="subject.id">
            <td>{{ subject.subject_name }}</td>
            <td>{{ subject.quiz_count }}</td>
            <td>{{ subject.pending }}</td>
            <td><b>{{ subject.average_score }}%</b></td>
          </tr>
        </tbody>
      </table>
      <hr/>
    </div>

    <div class="container mt-5">
      <div class="d-flex justify-content-between mt-5">
        <div style="width: 32%;">
          <h5>Total Quizzes</h5>
            <BarChart
            :labels="subjectLabels"
            :data="quizCounts"
            label="Total Quizzes"
            backgroundColor="#66BB6A"
          />
        </div>

        <div style="width: 32%;">
          <h5>Pending/Upcoming</h5>
            <BarChart
            :labels="subjectLabels"
            :data="pending"
            label="Pending/Upcoming"
            backgroundColor="#EF5350"
          />
        </div>

        <div style="width: 32%;">
          <h5>Average (%)</h5>
            <PercentageChart
            :labels="subjectLabels"
            :data="averages"
            label="Average Score"
            backgroundColor="#42A5F5"
         />
        </div>
      </div>
        <hr/>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';
import BarChart from '@/components/BarChart.vue';
import PercentageChart from '@/components/PercentageChart.vue';

const subjects = ref([]);

const subjectLabels = computed(() => subjects.value.map(s => s.subject_name));
const quizCounts = computed(() => subjects.value.map(s => s.quiz_count));
const pending = computed(() => subjects.value.map(s => s.pending));
const averages = computed(() => subjects.value.map(s => s.average_score));


onMounted(async () => {
  try {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');
    
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/users/summary/${userId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    subjects.value = res.data;
  } catch (err) {
    console.error('Failed to fetch quiz data:', err);
  }
});
</script>