import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/pages/Login.vue';
import Dashboard from '@/pages/Dashboard.vue';
import Register from '@/pages/Register.vue';
import EditChapter from '../pages/EditChapter.vue';
import NewChapter from '../pages/NewChapter.vue';
import NewSubject from '../pages/NewSubject.vue';
import NewQuiz from '../pages/NewQuiz.vue';
import NewQuestion from '../pages/NewQuestion.vue';
import QuizView from '../pages/QuizView.vue';
import EditQuestion from '../pages/EditQuestion.vue';
import QuizAttempt from '../pages/QuizAttempt.vue';


const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  { path: '/dashboard', component: Dashboard },
  { path: '/quizview', component: QuizView },
  { path: '/register', component: Register },
  { path: '/chapters/:id/edit', component: EditChapter},
  { path: '/questions/:id/edit', component: EditQuestion},
  { path: '/subjects/new', component: NewSubject},
  { path: '/subjects/:subject_id/chapters/new', component: NewChapter},
  { path: '/quizzes/new', component: NewQuiz},
  { path: '/quizzes/:id/questions/new', component: NewQuestion },
  { path: '/attempt/:quizId', component: QuizAttempt }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router;
