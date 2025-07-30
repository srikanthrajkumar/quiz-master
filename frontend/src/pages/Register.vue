<template>
  <div class="container d-flex justify-content-center align-items-center flex-column" style="min-height: 100vh;">
    <h1 class="mb-4 fw-bold">Quiz Master</h1>
    <div class="card p-4" style="width: 100%; max-width: 400px;">
      <h3 class="text-center mb-3">Register</h3>

      <form @submit.prevent="registerUser">
        <div class="mb-3">
          <input v-model="first_name" type="text" class="form-control" placeholder="First Name" required/>
        </div>
        <div class="mb-3">
          <input v-model="last_name" type="text" class="form-control" placeholder="Last Name" required/>
        </div>
        <div class="mb-3">
          <input v-model="username" type="text" class="form-control" placeholder="Username" required/>
        </div>
        <div class="mb-3">
          <input v-model="qualification" type="text" class="form-control" placeholder="Qualification"/>
        </div>

        <div class="mb-3">
          <input v-model="password" type="password" class="form-control" placeholder="Password" required/>
        </div>

        <button type="submit" class="btn btn-success w-100">Register</button>
        
        <div v-if="error" class="text-danger text-center mt-2">{{ error }}</div>
      </form>
    </div>

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
const first_name = ref('');
const last_name = ref('');
const qualification  = ref('');
const error = ref('');
const router = useRouter();

async function registerUser() {
  try {
    const res = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/users/register`,
      { username: username.value, password: password.value, first_name: first_name.value, last_name: last_name.value, qualification: qualification.value }
    );
    localStorage.setItem('token', res.data.access_token);
    router.push('/login');
  } catch (err) {
    error.value = 'Invalid credentials';
  }
}
</script>
