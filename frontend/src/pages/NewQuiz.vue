<template>
  <NavBar />
  
  <div class="container d-flex justify-content-center align-items-center flex-column" style="min-height: 100vh;">
    <div class="card p-4" style="width: 100%; max-width: 600px;">
        <h3 class="text-center mb-3">Add Quiz</h3>
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
                <label class="form-label">Start Date of Quiz (DD/MM/YYYY)</label>
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

            <button type="submit" class="btn btn-success w-100">Create Quiz</button>
            <div v-if="error" class="text-danger text-center mt-2">{{ error }}</div> 
        </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

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


    router.push('/quiz');
  } catch (err) {
    error.value = err.response?.data?.message || 'Something went wrong.';
  }
}
</script>
