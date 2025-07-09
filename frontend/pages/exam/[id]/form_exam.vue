<template>
  <div class="flex h-screen bg-white text-gray-900 p-6">
    <div class="w-3/4 p-6 bg-white shadow-lg rounded-lg border">
      <p class="mb-6 text-lg font-semibold">
        {{ currentQuestion.number }}. {{ currentQuestion.text }}
      </p>

      <div
        v-for="(option, index) in currentQuestion.options"
        :key="index"
        class="mb-3"
      >
        <label
          class="flex items-center p-3 border rounded-lg cursor-pointer transition-all"
          :class="{
            'bg-blue-100 border-blue-500': selectedAnswer === index,
            'hover:bg-gray-100': selectedAnswer !== index,
          }"
        >
          <input
            type="radio"
            :value="index"
            v-model="selectedAnswer"
            class="hidden"
          />
          <span
            class="w-4 h-4 border rounded-full flex items-center justify-center mr-3"
            :class="{ 'bg-blue-500': selectedAnswer === index }"
          ></span>
          {{ option }}
        </label>
      </div>

      <div class="flex justify-between mt-6">
        <button
          @click="prevQuestion"
          class="bg-gray-500 text-white px-4 py-2 rounded-lg"
        >
          ← Kembali
        </button>
        <button
          v-if="currentIndex < questions.length - 1"
          @click="nextQuestion"
          class="bg-blue-500 text-white px-4 py-2 rounded-lg"
        >
          Simpan & Lanjutkan →
        </button>
        <button
          v-else
          @click="finishExam"
          class="bg-green-600 text-white px-4 py-2 rounded-lg"
        >
          Selesaikan Ujian ✅
        </button>
      </div>
    </div>

    <ProctoringSidebar>
      <p class="text-center mb-3 text-gray-700">
        {{ answeredCount }} dari {{ questions.length }} soal terjawab
      </p>

      <div class="grid grid-cols-4 gap-2 w-full">
        <button
          v-for="(q, index) in questions"
          :key="index"
          class="w-10 h-10 rounded-lg text-sm font-medium transition-all"
          :class="{
            'bg-green-500 text-white': q.answered,
            'bg-red-500 text-white':
              q.number === currentQuestion.number && q.answered,
            'bg-gray-200': !q.answered,
            'hover:bg-gray-300': true,
          }"
          @click="goToQuestion(index)"
        >
          {{ q.number }}
        </button>
      </div>
    </ProctoringSidebar>
  </div>
</template>

<script setup>
import { useRoute } from "vue-router";
import { useExam } from "~/composables/useExam";
import ProctoringSidebar from "~/components/ProctoringSidebar.vue";

definePageMeta({
  layout: "exam-layout",
});

const route = useRoute();
const examId = route.params.id;

const {
  questions,
  currentIndex,
  currentQuestion,
  selectedAnswer,
  answeredCount,
  prevQuestion,
  nextQuestion,
  goToQuestion,
  finishExam,
} = useExam(examId);
</script>
