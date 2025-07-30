<template>
  <div class="container d-flex justify-content-center align-items-center flex-column" style="min-height: 100vh;">
    <h1 class="mb-4 fw-bold">Quiz Master</h1>
    <div class="card p-4" style="width: 100%; max-width: 400px;">
      <h3 class="text-center mb-3">Login</h3>
      
      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <input v-model="username" type="text" class="form-control" placeholder="Username" required/>
        </div>
        
        <div class="mb-3">
          <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
        </div>
        
        <button type="submit" class="btn btn-primary w-100">Login</button>
        
        <div v-if="error" class="text-danger text-center mt-2">{{ error }}</div>
      </form>
    </div>

    <p>
        New here? 
        <router-link to="/register">Click here to register</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

async function loginUser() {
  if (!username.value || !password.value) {
    error.value = 'Both fields are required';
    return;
  }

  try {
    const res = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/users/login`,
      { username: username.value, password: password.value }
    );
    localStorage.setItem('token', res.data.access_token);
    localStorage.setItem('user_id', res.data.user_id);
    localStorage.setItem('first_name', res.data.first_name);
    localStorage.setItem('user_role', res.data.role)
    router.push('/dashboard');
  } catch (err) {
    if (err.response?.data?.message) {
      error.value = err.response.data.message;;
    } else {
      error.value = 'Something went wrong. Please try again.';
    }
  }
}
</script>
