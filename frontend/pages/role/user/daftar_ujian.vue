<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const config = useRuntimeConfig();
const apiUrl = config.public.apiBase;

const router = useRouter();
const exams = ref([]);
const isAuthenticated = ref(false);

const fetchExams = async () => {
  try {
    const response = await fetch(`${apiUrl}/exam`);
    const data = await response.json();
    exams.value = data;
  } catch (error) {
    console.error("Gagal mengambil data ujian:", error);
  }
};  

const startExam = (examId) => {
  router.push(`/exam/${examId}/form_exam`);
};

onMounted(() => {
  const token = localStorage.getItem("token");
  if (!token) router.push("/login");
  else {
    isAuthenticated.value = true;
    fetchExams();
  }
});

definePageMeta({
  middleware: "auth",
});
</script>

<template>
  <div v-if="isAuthenticated" class="p-8">
    <h1 class="text-2xl font-bold mb-4">Daftar Ujian</h1>

    <!-- Scrollable table wrapper -->
    <div class="overflow-auto">
      <table class="min-w-full border-collapse border text-center">
        <thead>
          <tr class="bg-gray-200">
            <th class="border p-2">No</th>
            <th class="border p-2">Nama Ujian</th>
            <th class="border p-2">Durasi</th>
            <th class="border p-2">Jumlah Soal</th>
            <th class="border p-2">Opsi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(exam, index) in exams" :key="exam.id">
            <td class="border p-2">{{ index + 1 }}</td>
            <td class="border p-2">{{ exam.nama_ujian }}</td>
            <td class="border p-2">{{ exam.durasi }}</td>
            <td class="border p-2">{{ exam.jumlah_soal }}</td>
            <td class="border p-2">
              <button
                @click="startExam(exam.id)"
                class="bg-blue-500 text-white py-1 px-3 rounded-lg hover:bg-blue-400"
              >
                Kerjakan
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
