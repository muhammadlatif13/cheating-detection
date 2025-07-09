<script setup>
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";

const config = useRuntimeConfig();
const apiUrl = config.public.apiBase;

const router = useRouter();
const exams = ref([]);
const isAuthenticated = ref(false);

// Refs untuk sorting
const sortField = ref("id"); // Kolom default untuk diurutkan
const sortDirection = ref("asc"); // Arah default

const fetchExams = async () => {
  try {
    // Menambahkan id sementara pada data fetch untuk sorting
    const response = await fetch(`${apiUrl}/exam`);
    let data = await response.json();
    // Beri nomor id agar bisa di-sort berdasarkan nomor urut
    exams.value = data.map((exam, index) => ({ ...exam, no: index + 1 }));
  } catch (error) {
    console.error("Gagal mengambil data ujian:", error);
  }
};

const startExam = (examId) => {
  router.push(`/exam/${examId}/form_exam`);
};

// Fungsi untuk mengubah kriteria sorting
const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
  } else {
    sortField.value = field;
    sortDirection.value = "asc";
  }
};

// Computed property untuk mengurutkan ujian
const sortedExams = computed(() => {
  return [...exams.value].sort((a, b) => {
    let aValue = a[sortField.value];
    let bValue = b[sortField.value];

    if (aValue === undefined || bValue === undefined) return 0;

    let modifier = 1;
    if (sortDirection.value === "desc") {
      modifier = -1;
    }

    if (aValue < bValue) return -1 * modifier;
    if (aValue > bValue) return 1 * modifier;
    return 0;
  });
});

onMounted(() => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
  } else {
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
    <h1 class="text-2xl font-bold mb-6 text-gray-800">Daftar Ujian</h1>

    <div class="overflow-x-auto max-h-[650px] shadow-lg rounded-lg">
      <table class="table-auto w-full border-collapse">
        <thead class="bg-indigo-600 text-white sticky top-0 z-10">
          <tr>
            <th
              class="px-4 py-3 cursor-pointer select-none text-left"
              @click="sortBy('no')"
            >
              <div class="flex items-center">
                No
                <span v-if="sortField === 'no'" class="ml-2">
                  {{ sortDirection === "asc" ? "↑" : "↓" }}
                </span>
              </div>
            </th>
            <th
              class="px-4 py-3 cursor-pointer select-none text-left"
              @click="sortBy('nama_ujian')"
            >
              <div class="flex items-center">
                Nama Ujian
                <span v-if="sortField === 'nama_ujian'" class="ml-2">
                  {{ sortDirection === "asc" ? "↑" : "↓" }}
                </span>
              </div>
            </th>
            <th
              class="px-4 py-3 cursor-pointer select-none"
              @click="sortBy('durasi')"
            >
              <div class="flex items-center justify-center">
                Durasi (menit)
                <span v-if="sortField === 'durasi'" class="ml-2">
                  {{ sortDirection === "asc" ? "↑" : "↓" }}
                </span>
              </div>
            </th>
            <th
              class="px-4 py-3 cursor-pointer select-none"
              @click="sortBy('jumlah_soal')"
            >
              <div class="flex items-center justify-center">
                Jumlah Soal
                <span v-if="sortField === 'jumlah_soal'" class="ml-2">
                  {{ sortDirection === "asc" ? "↑" : "↓" }}
                </span>
              </div>
            </th>
            <th class="px-4 py-3 text-center">Opsi</th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr
            v-for="exam in sortedExams"
            :key="exam.id"
            class="hover:bg-gray-50 transition border-b border-gray-200"
          >
            <td class="px-4 py-3 text-gray-700">{{ exam.no }}</td>
            <td class="px-4 py-3 font-medium text-gray-800">
              {{ exam.nama_ujian }}
            </td>
            <td class="px-4 py-3 text-center text-gray-700">
              {{ exam.durasi }}
            </td>
            <td class="px-4 py-3 text-center text-gray-700">
              {{ exam.jumlah_soal }}
            </td>
            <td class="px-4 py-3 text-center">
              <button
                @click="startExam(exam.id)"
                class="bg-indigo-500 text-white py-2 px-4 rounded-lg hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50 transition-colors"
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
