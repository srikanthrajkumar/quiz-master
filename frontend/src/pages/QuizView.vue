<template>
  <div>
    <NavBar />
    
    <div class="container mt-4">
      <h2 align="center">Quiz Dashboard</h2>
      
      <div class="d-flex justify-content-center">
        <router-link :to="`/quizzes/new` "class="btn btn-success btn-sm mt-2">+ Add Quiz</router-link>
      </div>
      
      <div v-if="!quizzes || quizzes.length === 0" class="text-muted">
        No quizzes found.
      </div>

      <div v-for="quiz in quizzes" :key="quiz.id" class="mb-4">
        <hr class="my-2" />
        <h4>{{ quiz.name }}</h4>
        <i>{{ quiz.date_of_quiz }}</i>
        <hr class="my-2" />
        
        <div v-if="!quiz.questions || quiz.questions.length === 0" class="text-muted">
          No questions found for this quiz.
        </div>
        
        <table v-else class="table table-striped">
          <thead>
            <tr>
              <th style="width: 10%">Question Id.</th>
              <th style="width: 40%">Question</th>
              <th style="width: 10%">Option 1</th>
              <th style="width: 10%">Option 2</th>
              <th style="width: 10%">Option 3</th>
              <th style="width: 10%">Option 4</th>
              <th style="width: 10%">Correct Option</th>
              <th style="width: 5%">Edit</th>
              <th style="width: 5%">Delete</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="question in quiz.questions" :key="question.id">
              <td>{{ question.id }}</td>
              <td>{{ question.question_statement }}</td>
              <td>{{ question.option1 }}</td>
              <td>{{ question.option2 }}</td>
              <td>{{ question.option3 }}</td>
              <td>{{ question.option4 }}</td>
              <td>{{ question.correct_option_index }}</td>
              <td>
                <router-link :to="`/questions/${question.id}/edit`" class="btn btn-sm btn-primary me-2">Edit</router-link>
              </td>
              <td>
                <template v-if="deletingQuestionId === question.id">
                  <button class="btn btn-sm btn-danger me-1" @click="confirmDelete(question.id)">Confirm</button>
                  <button class="btn btn-sm btn-secondary" @click="cancelDelete">Cancel</button>
                </template>
                <template v-else>
                  <button class="btn btn-sm btn-danger" @click="startDelete(question.id)">Delete</button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
        <router-link :to="`/quizzes/${quiz.id}/questions/new`" class="btn btn-success btn-sm mt-2">+ Add Question</router-link>
        <hr class="my-4" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

const quizzes = ref([]);
const deletingQuestionId = ref(null);

onMounted(async () => {
  try {
    const token = localStorage.getItem('token');

    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/admin/quizview`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    quizzes.value = res.data;
  } catch (err) {
    console.error('Failed to fetch quiz data:', err);
  }
});


function startDelete(questionId) {
  deletingQuestionId.value = questionId;
}

function cancelDelete() {
  deletingQuestionId.value = null;
}

async function confirmDelete(questionId) {
  const token = localStorage.getItem('token');
  try {
    await axios.delete(`${import.meta.env.VITE_API_BASE_URL}/questions/${questionId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    quizzes.value = quizzes.value.map(quiz => ({
      ...quiz,
      questions: quiz.questions.filter(q => q.id !== questionId)
    }));
  } catch (err) {
    console.error('Failed to delete chapter:', err);
  } finally {
    deletingQuestionId.value = null;
  }
}

</script>

