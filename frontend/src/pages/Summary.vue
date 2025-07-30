<script setup>
import { ref, onMounted } from 'vue'
import AdminSummary from '@/components/AdminSummary.vue'
import UserSummary from '@/components/UserSummary.vue'

const userRole = ref('')

onMounted(() => {
  userRole.value = localStorage.getItem('user_role') || 'user'
})
</script>

<template>
  <AdminSummary v-if="userRole === 'admin'" />
  <UserSummary v-else />
</template>