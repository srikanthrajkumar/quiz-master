<script setup>
import { computed, ref, onMounted } from 'vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import UserDashboard from '@/components/UserDashboard.vue'

const userRole = ref('')

onMounted(() => {
  userRole.value = localStorage.getItem('user_role') || 'user'
})
</script>

<template>
  <AdminDashboard v-if="userRole === 'admin'" />
  <UserDashboard v-else />
</template>