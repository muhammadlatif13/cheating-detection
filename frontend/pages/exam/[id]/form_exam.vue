<template>
  <div class="flex h-screen bg-white text-gray-900 p-6">
    <!-- Bagian Soal -->
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

    <!-- Sidebar Kamera & Status Ujian -->
    <div
      class="w-1/4 ml-6 bg-white shadow-lg p-4 rounded-lg border flex flex-col items-center"
    >
      <!-- Kamera -->
      <div class="w-full border rounded-lg overflow-hidden mb-4">
        <img
          v-if="videoStreamUrl"
          :src="videoStreamUrl"
          alt="Webcam Stream"
          class="w-full h-full object-cover"
        />
        <p v-else class="text-gray-600 text-sm">Menghubungkan kamera...</p>
      </div>

      <!-- Pilih Kamera -->
      <div class="w-full mb-4">
        <label
          for="camera-select"
          class="block text-start text-gray-700 font-semibold mb-2"
        >
          Pilih Kamera:
        </label>
        <select
          id="camera-select"
          v-model="selectedCamera"
          @change="updateCamera"
          class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 text-gray-700"
        >
          <option
            v-for="(camera, index) in cameras"
            :key="index"
            :value="camera.deviceId"
          >
            {{ camera.label }}
          </option>
        </select>
      </div>

      <!-- Status Jawaban -->
      <p class="text-center mb-3 text-gray-700">
        {{ answeredCount }} dari {{ questions.length }} soal terjawab
      </p>

      <!-- Nomor Soal -->
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const examId = route.params.id;

const config = useRuntimeConfig();
const apiUrl = config.public.apiBase;

const questions = ref([]);
const currentIndex = ref(0);
const currentQuestion = ref({});
const selectedAnswer = ref(null);
const selectedCamera = ref("");
const cameras = ref([]);
const videoStreamUrl = ref("");

// Fetch cameras
const fetchCameras = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/get_cameras`);
    cameras.value = await response.json();
    if (cameras.value.length > 0) {
      selectedCamera.value = cameras.value[0].deviceId;
      updateCamera();
    }
  } catch (error) {
    console.error("Gagal mengambil kamera:", error);
  }
};

const updateCamera = () => {
  videoStreamUrl.value = `${apiUrl}/video_feed?camera_id=${selectedCamera.value}`;
};

const fetchQuestions = async () => {
  try {
    const response = await fetch(`${apiUrl}/add_questions/${examId}`);
    const data = await response.json();

    console.log(
      "Isi tiap soal:",
      data.map((q) => q.question)
    );
    console.log("Data soal dari backend:", data); // cek isi data

    watch(selectedAnswer, (newValue) => {
      questions.value[currentIndex.value].selected = newValue;
      if (newValue !== null) {
        questions.value[currentIndex.value].answered = true;
      }
    });

    questions.value = data.map((q, index) => ({
      number: index + 1,
      text: q.question.question_text,
      options: q.question.options,
      selected: null,
      answered: false,
    }));

    updateCurrentQuestion();
  } catch (error) {
    console.error("Gagal mengambil soal:", error);
  }
};

const answeredCount = computed(
  () => questions.value.filter((q) => q.answered).length
);

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
    updateCurrentQuestion();
  }
};

const nextQuestion = () => {
  if (selectedAnswer.value !== null) {
    questions.value[currentIndex.value].answered = true;
  }
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++;
    updateCurrentQuestion();
  }
};

const finishExam = () => {
  // Kamu bisa kirim data jawaban ke backend di sini
  const hasilJawaban = questions.value.map((q) => ({
    number: q.number,
    selected: q.selected,
  }));

  console.log("Jawaban akhir:", hasilJawaban);

  // Redirect ke halaman lain atau tampilkan notifikasi
  alert("Ujian telah diselesaikan. Terima kasih!");
  // Misal redirect ke halaman hasil
  // router.push('/exam/hasil');
};

const goToQuestion = (index) => {
  currentIndex.value = index;
  updateCurrentQuestion();
};

const updateCurrentQuestion = () => {
  currentQuestion.value = questions.value[currentIndex.value];
  selectedAnswer.value = currentQuestion.value.selected;
};

onMounted(() => {
  fetchQuestions();
  fetchCameras();
});
</script>
