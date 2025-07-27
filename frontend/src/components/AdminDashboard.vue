<template>
  <div>
    <NavBar />
    
    <div class="container mt-4">
      <h2 align="center">Admin Dashboard</h2>
      
      <div class="d-flex justify-content-center">
        <router-link :to="`/subjects/new` "class="btn btn-success btn-sm mt-2">+ Add Subject</router-link>
      </div>
      
      <div v-if="subjects.length === 0" class="text-muted">
        No subjects found.
      </div>

      <div v-for="subject in subjects" :key="subject.id" class="mb-4">
        <hr class="my-2" />
        <h4>{{ subject.name }}</h4>
        <i>{{ subject.description }}</i>
        <hr class="my-2" />
        
        <div v-if="!subject.chapters || subject.chapters.length === 0" class="text-muted">
          No chapters found for this subject.
        </div>
        
        <table v-else class="table table-striped">
          <thead>
            <tr>
              <th style="width: 15%">Chapter</th>
              <th style="width: 45%">Description</th>
              <th style="width: 10%">No. of Quizzes</th>
              <th style="width: 15%">Edit</th>
              <th style="width: 15%">Delete</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="chapter in subject.chapters" :key="chapter.id">
              <td>{{ chapter.name }}</td>
              <td>{{ chapter.description }}</td>
              <td>{{ chapter.num_quizzes }}</td>
              <td>
                <router-link :to="`/chapters/${chapter.id}/edit`" class="btn btn-sm btn-primary me-2">Edit</router-link>
              </td>
              <td>
                <template v-if="deletingChapterId === chapter.id">
                  <button class="btn btn-sm btn-danger me-1" @click="confirmDelete(chapter.id)">Confirm</button>
                  <button class="btn btn-sm btn-secondary" @click="cancelDelete">Cancel</button>
                </template>
                <template v-else>
                  <button class="btn btn-sm btn-danger" @click="startDelete(chapter.id)">Delete</button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
        <router-link :to="`/subjects/${subject.id}/chapters/new` "class="btn btn-success btn-sm mt-2">+ Add Chapter</router-link>
        <hr class="my-4" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';

const subjects = ref([]);
const deletingChapterId = ref(null);

onMounted(async () => {
  try {
    const token = localStorage.getItem('token');

    const res = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/admin/dashboard`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    subjects.value = res.data;
  } catch (err) {
    console.error('Failed to fetch dashboard data:', err);
  }
});


function startDelete(chapterId) {
  deletingChapterId.value = chapterId;
}

function cancelDelete() {
  deletingChapterId.value = null;
}

async function confirmDelete(chapterId) {
  const token = localStorage.getItem('token');
  try {
    await axios.delete(`${import.meta.env.VITE_API_BASE_URL}/chapters/${chapterId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    subjects.value = subjects.value.map(subject => ({
      ...subject,
      chapters: subject.chapters.filter(ch => ch.id !== chapterId)
    }));
  } catch (err) {
    console.error('Failed to delete chapter:', err);
  } finally {
    deletingChapterId.value = null;
  }
}

</script>

