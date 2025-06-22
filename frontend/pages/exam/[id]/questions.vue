<!--question.vue-->
<template>
  <div class="p-8 max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-6">Tambah Soal untuk {{ examName }}</h1>

    <form @submit.prevent="submitQuestions">
      <div
        v-for="(q, index) in newQuestions"
        :key="index"
        class="mb-8 p-6 border rounded-lg shadow-sm bg-white"
      >
        <label class="block font-semibold text-lg mb-2"
          >Pertanyaan {{ index + 1 }}</label
        >
        <textarea
          v-model="q.question_text"
          class="w-full p-3 border rounded mb-4"
          placeholder="Tulis pertanyaannya di sini"
          required
        ></textarea>

        <label class="block font-semibold mb-2">Pilihan Jawaban</label>
        <p class="text-sm text-gray-600 mb-2">
          Tandai opsi untuk menentukan jawaban benar.
        </p>

        <div
          v-for="(option, optIndex) in q.options"
          :key="optIndex"
          class="flex items-center gap-2 mb-2"
        >
          <input
            type="radio"
            :name="'correct-' + index"
            :value="option"
            v-model="q.correctAnswer"
            class="accent-green-600"
          />
          <input
            v-model="q.options[optIndex]"
            type="text"
            class="flex-1 p-2 border rounded"
            placeholder="Isi opsi jawaban"
            required
          />
          <button
            type="button"
            @click="removeOption(index, optIndex)"
            class="text-red-600 hover:text-red-800"
            v-if="q.options.length > 1"
          >
            &#x2715;
          </button>
        </div>

        <button
          type="button"
          @click="addOption(index)"
          class="bg-green-500 text-white px-3 py-1 rounded mt-1"
        >
          + Tambah Opsi
        </button>

        <div class="flex justify-end gap-2 mt-4">
          <button
            type="button"
            @click="removeQuestion(index)"
            class="bg-red-500 text-white px-4 py-2 rounded"
          >
            Hapus Soal
          </button>
        </div>
      </div>

      <div class="flex gap-4">
        <button
          type="button"
          @click="addNewQuestion"
          class="bg-blue-500 text-white px-6 py-2 rounded"
        >
          + Soal Baru
        </button>
        <button type="submit" class="bg-green-600 text-white px-6 py-2 rounded">
          Simpan Semua Soal
        </button>
      </div>
    </form>

    <h2 class="text-xl font-bold mt-10 mb-4">Daftar Soal Tersimpan</h2>
    <div class="space-y-4">
      <div
        v-for="(q, index) in questions"
        :key="q.id"
        class="p-4 border rounded bg-gray-50 shadow-sm"
      >
        <p class="font-semibold mb-2">
          {{ index + 1 }}. {{ q.question.question_text }}
        </p>
        <div class="ml-4 space-y-1">
          <label
            v-for="(option, optIndex) in q.question.options"
            :key="optIndex"
            class="flex items-center"
          >
            <input
              type="radio"
              :checked="option === q.answer"
              disabled
              class="mr-2"
            />
            {{ option }}
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const config = useRuntimeConfig();
const apiUrl = config.public.apiBase;

const route = useRoute();
const examId = ref(route.params.id);
const examName = ref("");
const questions = ref([]);
const newQuestions = ref([
  { question_text: "", options: [""], correctAnswer: "" },
]);

const fetchExamDetails = async () => {
  try {
    const response = await fetch(`${apiUrl}/exam/${examId.value}`);
    const data = await response.json();
    examName.value = data.nama_ujian;
  } catch (error) {
    console.error("Gagal mengambil data ujian:", error);
  }
};

const fetchQuestions = async () => {
  try {
    const response = await fetch(`${apiUrl}/add_questions/${examId.value}`);
    if (!response.ok)
      throw new Error(`Gagal mengambil soal, status: ${response.status}`);

    const data = await response.json();
    questions.value = data.map((q) => ({
      ...q,
      question:
        typeof q.question === "string" ? JSON.parse(q.question) : q.question,
    }));
  } catch (error) {
    console.error("Gagal mengambil data soal:", error);
  }
};

const addNewQuestion = () => {
  newQuestions.value.push({
    question_text: "",
    options: [""],
    correctAnswer: "",
  });
};

const addOption = (index) => {
  newQuestions.value[index].options.push("");
};

const removeQuestion = (index) => {
  newQuestions.value.splice(index, 1);
};

const removeOption = (qIndex, optIndex) => {
  newQuestions.value[qIndex].options.splice(optIndex, 1);
};

const submitQuestions = async () => {
  try {
    const formattedQuestions = newQuestions.value.map((q) => ({
      exam_id: examId.value,
      question: {
        question_text: q.question_text,
        options: q.options,
        answer: q.correctAnswer,
      },
      answer: q.correctAnswer,
    }));

    const response = await fetch(`${apiUrl}/add_questions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ questions: formattedQuestions }),
    });

    if (response.ok) {
      newQuestions.value = [
        { question_text: "", options: [""], correctAnswer: "" },
      ];
      fetchQuestions();
    } else {
      console.error("Gagal menyimpan soal:", await response.text());
    }
  } catch (error) {
    console.error("Gagal menambahkan soal:", error);
  }
};

onMounted(() => {
  fetchExamDetails();
  fetchQuestions();
});
</script>
