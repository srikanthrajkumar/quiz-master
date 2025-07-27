<template>
  <div class="container mt-4">
    <h2>Add New Quiz</h2>
    
    <form @submit.prevent="submitQuiz" class="mt-3">
      <div class="mb-3">
        <label class="form-label">Quiz Name</label>
        <input v-model="quiz.name" type="text" class="form-control" required />
      </div>

      <select v-model="quiz.chapter_id" class="form-select" required>
        <option disabled value="">Select Chapter</option>
        <option v-for="chapter in chapters" :key="chapter.id" :value="chapter.id">
            {{ chapter.name }}
        </option>
      </select>

      <div class="mb-3">
        <label class="form-label">Date of Quiz (DD/MM/YYYY)</label>
        <input v-model="quiz.date_of_quiz" type="text" class="form-control" placeholder="19/07/2025" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Time Duration (HH:MM:SS)</label>
        <input v-model="quiz.time_duration" type="text" class="form-control" placeholder="01:30:00" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Remarks (Optional)</label>
        <textarea v-model="quiz.remarks" class="form-control" rows="2"></textarea>
      </div>

      <button type="submit" class="btn btn-success">Submit</button>
    </form>

    <p class="text-danger mt-2" v-if="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const quiz = ref({
  name: '',
  date_of_quiz: '',
  time_duration: '',
  remarks: '',
  chapter_id: ''
});

const error = ref('');
const router = useRouter();
const route = useRoute();

const chapters = ref([]);

onMounted(async () => {
  const token = localStorage.getItem('token');
  const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/chapters`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  chapters.value = res.data;
});


async function submitQuiz() {
  try {
    const token = localStorage.getItem('token');

    await axios.post(`${import.meta.env.VITE_API_BASE_URL}/chapters/${quiz.value.chapter_id}/quizzes`,
     {
      name: quiz.value.name,
      date_of_quiz: quiz.value.date_of_quiz,
      time_duration: quiz.value.time_duration,
      remarks: quiz.value.remarks,
     },
     { headers: { Authorization: `Bearer ${token}` } }
    );


    router.push('/quizview');
  } catch (err) {
    error.value = err.response?.data?.message || 'Something went wrong.';
  }
}
</script>
