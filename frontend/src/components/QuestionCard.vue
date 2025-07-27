<template>
  <div class="card p-3 mb-3">
    <h5>{{ question.question_statement }}</h5>

    <label class="form-check-label d-block">
      <input
        class="form-check-input me-2"
        type="radio"
        value="0"
        v-model="selected"
        @change="emitAnswer"
      />
      {{ question.option1 }}
    </label>

    <label class="form-check-label d-block">
      <input
        class="form-check-input me-2"
        type="radio"
        value="1"
        v-model="selected"
        @change="emitAnswer"
      />
      {{ question.option2 }}
    </label>

    <label class="form-check-label d-block">
      <input
        class="form-check-input me-2"
        type="radio"
        value="2"
        v-model="selected"
        @change="emitAnswer"
      />
      {{ question.option3 }}
    </label>

    <label class="form-check-label d-block">
      <input
        class="form-check-input me-2"
        type="radio"
        value="3"
        v-model="selected"
        @change="emitAnswer"
      />
      {{ question.option4 }}
    </label>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  question: Object,
  modelValue: Number,
})

const emit = defineEmits(['update:modelValue'])

const selected = ref(props.modelValue)

watch(
  () => props.modelValue,
  (newVal) => {
    selected.value = newVal
  }
)

function emitAnswer() {
  const isCorrect = Number(selected.value) === props.question.correct_option_index ? 1 : 0
  emit('update:modelValue', isCorrect)
}
</script>
