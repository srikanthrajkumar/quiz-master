<template>
  <div class="regsiter">
    <h2>Register</h2>
    <form @submit.prevent="loginUser">
      <input v-model="first_name" placeholder="First Name" />
      <input v-model="last_name" placeholder="Last Name" />
      <input v-model="username" placeholder="Username" />
      <input v-model="qualification" placeholder="Qualification" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
      <p v-if="error">{{ error }}</p>
    </form>

    <p>
      Already a member?
      <router-link to="/login">Login</router-link>
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
  try {
    const res = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/users/register`,
      { username: username.value, password: password.value }
    );
    localStorage.setItem('token', res.data.access_token);
    router.push('/dashboard');
  } catch (err) {
    error.value = 'Invalid credentials';
  }
}
</script>
