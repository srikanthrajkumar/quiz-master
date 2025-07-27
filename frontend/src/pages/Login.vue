<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
      <p v-if="error">{{ error }}</p>
    </form>

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
