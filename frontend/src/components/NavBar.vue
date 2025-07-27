<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const firstName = ref('');
const role = ref('guest');

onMounted(() => {
  firstName.value = localStorage.getItem('first_name') || '';
  role.value = localStorage.getItem('user_role') || 'guest';
});

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('first_name');
  router.push('/login');
}
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <router-link to="/dashboard" class="navbar-brand">Quiz Master</router-link>
      
      <div class="navbar-nav me-auto">
        <router-link to="/dashboard" class="nav-link">Home</router-link>
        <router-link v-if="role === 'admin'" to="/quizview" class="nav-link">Quiz</router-link>
        <router-link v-else-if="role === 'user'" to="/scores" class="nav-link">Scores</router-link>
        <router-link to="/summary" class="nav-link">Summary</router-link>
      </div>
      
      <div class="d-flex align-items-center">
        <input type="text" class="form-control me-3" placeholder="Search..." style="width: 200px;">
        <span class="text-light me-3">Welcome {{ firstName }}</span>
        <button @click="logout" class="btn btn-outline-light btn-sm">Logout</button>
      </div>
    </div>
  </nav>
</template>