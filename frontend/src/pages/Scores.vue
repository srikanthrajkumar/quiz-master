<template>
  <div>
    <NavBar />
    
    <div class="container mt-4">
      <h2>Score Dashboard</h2>

      <div class="mb-3">
        <button @click="exportCSV" class="btn btn-primary">Export Scores to CSV</button>
        <div v-if="downloadLink" class="mt-2">
          <a :href="downloadLink" target="_blank" class="btn btn-outline-success">Download CSV</a>
        </div>
      </div>
      
      <hr/>

      <div v-if="!scores || scores.length === 0" class="text-muted">
        No scores found.
      </div>

      <table v-else class="table table-striped">
        <thead>
          <tr>
            <th style="width: 20%">Score ID</th>
            <th style="width: 20%">Quiz ID</th>
            <th style="width: 30%">Time Stamp</th>
            <th style="width: 15%">Score</th>
            <th style="width: 15%">Redo</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="score in scores" :key="score.id">
            <td>{{ score.id }}</td>
            <td>{{ score.quiz_id }}</td>
            <td>{{ formatDate(score.time_stamp_of_attempt) }}</td>
            <td><b>{{ score.total_scored }}%</b></td>
            <td>  
              <router-link :to="`/attempt/${score.quiz_id}`" class="btn btn-sm btn-success">Redo</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { formatDate } from '@/utils/dateFormatter';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

const scores = ref([]);
const downloadLink = ref(null);

onMounted(async () => {
  try {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');
    
    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/users/${userId}/scores`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    scores.value = res.data;
  } catch (err) {
    console.error('Failed to fetch quiz data:', err);
  }
});

const exportCSV = async () => {
  try {
    const token = localStorage.getItem('token');
    
    const startRes = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/export_csv`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    const jobId = startRes.data.job_id;
    
    const pollForCompletion = async () => {
      const statusRes = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/export_status/${jobId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (statusRes.data.status === 'completed') {
        downloadLink.value = `${import.meta.env.VITE_API_BASE_URL}${statusRes.data.download_url}`;
        return;
      } else if (statusRes.data.status === 'failed') {
        throw new Error('Export failed: ' + statusRes.data.error);
      } else {
        setTimeout(pollForCompletion, 2000);
      }
    };
    
    pollForCompletion();
  } catch (err) {
    console.error('CSV export failed:', err);
    alert('CSV export failed. Please try again.');
  }
};

</script>