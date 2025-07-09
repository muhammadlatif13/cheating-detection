<template>
  <div v-if="isAuthenticated" class="min-h-screen bg-gray-50 p-6">
    <div
      class="mb-8 bg-white rounded-xl shadow p-4 flex justify-between items-center"
    >
      <div class="flex items-center">
        <div class="bg-indigo-600 p-2 rounded-lg mr-3">
          <i class="fas fa-user-shield text-white text-lg"></i>
        </div>
        <h1 class="text-2xl font-bold text-gray-800">Dashboard Admin</h1>
      </div>
      <div class="flex items-center space-x-4">
        <button
          @click="openModal('add')"
          class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg shadow-sm flex items-center"
        >
          <i class="fas fa-plus mr-2"></i>
          Tambah Ujian
        </button>
        <div class="relative">
          <button
            @click="toggleNotifications"
            class="relative bg-gray-200 hover:bg-gray-300 p-2 rounded-lg"
          >
            <i class="fas fa-bell text-gray-600"></i>
            <span
              v-if="unreadNotifications.length"
              class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center"
            >
              {{ unreadNotifications.length }}
            </span>
          </button>
          <div
            v-if="showNotifications"
            class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg p-4 z-50"
          >
            <h3 class="text-sm font-semibold mb-2">Notifikasi</h3>
            <div
              v-if="notifications.length === 0"
              class="text-sm text-gray-500"
            >
              Tidak ada notifikasi
            </div>
            <div v-else class="max-h-64 overflow-y-auto">
              <div
                v-for="notification in notifications"
                :key="notification.id"
                class="p-2 border-b last:border-b-0 hover:bg-gray-50"
                :class="{ 'bg-gray-100': !notification.read }"
              >
                <div class="flex justify-between items-start">
                  <div>
                    <p class="text-sm font-medium text-red-600">
                      {{ notification.fraud_type }}
                    </p>
                    <p class="text-xs text-gray-600">
                      {{ notification.description }}
                    </p>
                    <p class="text-xs text-gray-500">
                      {{
                        new Date(notification.timestamp).toLocaleString("id-ID")
                      }}
                    </p>
                    <p class="text-xs text-gray-500">
                      Kepercayaan: {{ notification.confidence_percentage }}%
                    </p>
                  </div>
                  <button
                    v-if="!notification.read"
                    @click="markAsRead(notification.id)"
                    class="text-blue-600 hover:text-blue-800 text-xs"
                  >
                    Tandai Dibaca
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="newNotification"
      class="fixed top-4 right-4 bg-red-600 text-white p-4 rounded-lg shadow-lg max-w-sm z-50"
    >
      <div class="flex justify-between items-center">
        <div>
          <h3 class="text-lg font-semibold">
            {{ newNotification.fraud_type }}
          </h3>
          <p class="text-sm">{{ newNotification.description }}</p>
          <p class="text-xs mt-1">
            {{ new Date(newNotification.timestamp).toLocaleString("id-ID") }}
          </p>
          <p class="text-xs">
            Kepercayaan: {{ newNotification.confidence_percentage }}%
          </p>
        </div>
        <button
          @click="closeNotification"
          class="text-white hover:text-gray-200"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>

    <!-- Statistics cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="bg-white rounded-xl shadow p-6 flex items-center">
        <div class="bg-blue-100 p-3 rounded-lg">
          <i class="fas fa-file-alt text-blue-600 text-xl"></i>
        </div>
        <div class="ml-4">
          <h3 class="text-sm font-medium text-gray-500">Total Ujian</h3>
          <p class="text-2xl font-bold text-gray-800">{{ exams.length }}</p>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow p-6 flex items-center">
        <div class="bg-green-100 p-3 rounded-lg">
          <i class="fas fa-question-circle text-green-600 text-xl"></i>
        </div>
        <div class="ml-4">
          <h3 class="text-sm font-medium text-gray-500">Total Soal</h3>
          <p class="text-2xl font-bold text-gray-800">
            {{ calculateTotalQuestions() }}
          </p>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow p-6 flex items-center">
        <div class="bg-purple-100 p-3 rounded-lg">
          <i class="fas fa-clock text-purple-600 text-xl"></i>
        </div>
        <div class="ml-4">
          <h3 class="text-sm font-medium text-gray-500">Rata-rata Durasi</h3>
          <p class="text-2xl font-bold text-gray-800">
            {{ calculateAverageDuration() }} menit
          </p>
        </div>
      </div>
    </div>

    <!-- Search and filter -->
    <div class="bg-white rounded-xl shadow mb-6 p-4">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="relative flex-grow">
          <div
            class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
          >
            <i class="fas fa-search text-gray-400"></i>
          </div>
          <input
            type="text"
            v-model="searchTerm"
            placeholder="Cari nama ujian..."
            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 p-2.5"
          />
        </div>
        <button
          @click="clearSearch"
          v-if="searchTerm"
          class="bg-gray-200 hover:bg-gray-300 text-gray-700 py-2 px-4 rounded-lg"
        >
          Reset
        </button>
      </div>
    </div>

    <!-- Exam list -->
    <div class="bg-white rounded-xl shadow overflow-hidden">
      <div class="sm:hidden px-4 py-3 border-b">
        <label for="sortSelect" class="text-sm font-medium text-gray-700"
          >Urut berdasarkan</label
        >
        <select
          id="sortSelect"
          v-model="sortBy"
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
        >
          <option value="nama">Nama Ujian</option>
          <option value="durasi">Durasi</option>
          <option value="soal">Jumlah Soal</option>
        </select>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                No
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                @click="toggleSort('nama')"
              >
                <div class="flex items-center">
                  Nama Ujian
                  <i class="fas fa-sort ml-1 text-gray-400"></i>
                </div>
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                @click="toggleSort('durasi')"
              >
                <div class="flex items-center">
                  Durasi
                  <i class="fas fa-sort ml-1 text-gray-400"></i>
                </div>
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                @click="toggleSort('soal')"
              >
                <div class="flex items-center">
                  Jumlah Soal
                  <i class="fas fa-sort ml-1 text-gray-400"></i>
                </div>
              </th>
              <th
                scope="col"
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Aksi
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredExams.length === 0">
              <td
                colspan="5"
                class="px-6 py-4 text-center text-sm text-gray-500"
              >
                <div class="flex flex-col items-center justify-center py-12">
                  <i class="fas fa-search text-gray-300 text-4xl mb-3"></i>
                  <p class="text-lg text-gray-500 font-medium">
                    Tidak ada ujian ditemukan
                  </p>
                  <p class="text-gray-400">
                    Coba dengan pencarian yang berbeda atau tambahkan ujian baru
                  </p>
                </div>
              </td>
            </tr>
            <template v-else>
              <tr
                v-for="(exam, index) in filteredExams"
                :key="exam.id"
                class="hover:bg-gray-50"
              >
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ index + 1 }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900">
                    {{ exam.nama_ujian }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <i class="fas fa-clock text-gray-400 mr-2"></i>
                    <span class="text-sm text-gray-900"
                      >{{ exam.durasi }} menit</span
                    >
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <i class="fas fa-question-circle text-gray-400 mr-2"></i>
                    <span class="text-sm text-gray-900">{{
                      exam.jumlah_soal
                    }}</span>
                  </div>
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2"
                >
                  <div class="flex flex-col sm:flex-row gap-2">
                    <button
                      @click="openModal('view', exam)"
                      class="text-blue-600 hover:text-blue-800 bg-blue-100 hover:bg-blue-200 rounded-md px-3 py-1 transition"
                    >
                      <i class="fas fa-eye mr-1"></i>
                      <span class="hidden sm:inline">Lihat</span>
                    </button>
                    <button
                      @click="openModal('edit', exam)"
                      class="text-amber-600 hover:text-amber-800 bg-amber-100 hover:bg-amber-200 rounded-md px-3 py-1 transition"
                    >
                      <i class="fas fa-edit mr-1"></i>
                      <span class="hidden sm:inline">Edit</span>
                    </button>
                    <button
                      @click="goToAddQuestion(exam.id)"
                      class="text-purple-600 hover:text-purple-800 bg-purple-100 hover:bg-purple-200 rounded-md px-3 py-1 transition"
                    >
                      <i class="fas fa-plus-circle mr-1"></i>
                      <span class="hidden sm:inline">Soal</span>
                    </button>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination (placeholder) -->
    <div class="mt-4 flex items-center justify-between">
      <div class="flex-1 flex justify-between sm:hidden">
        <button
          class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          Sebelumnya
        </button>
        <button
          class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          Selanjutnya
        </button>
      </div>
      <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
        <div>
          <p class="text-sm text-gray-700">
            Menampilkan
            <span class="font-medium">{{ filteredExams.length }}</span> dari
            <span class="font-medium">{{ exams.length }}</span> ujian
          </p>
        </div>
        <div>
          <nav
            class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
            aria-label="Pagination"
          >
            <button
              class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
            >
              <span class="sr-only">Previous</span>
              <i class="fas fa-chevron-left text-xs"></i>
            </button>
            <button
              class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              1
            </button>
            <button
              class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
            >
              <span class="sr-only">Next</span>
              <i class="fas fa-chevron-right text-xs"></i>
            </button>
          </nav>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-50"
    >
      <div class="bg-white p-6 rounded-xl shadow-lg w-[90%] max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold text-gray-800">{{ modalTitle }}</h2>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <!-- View Mode -->
        <div v-if="modalType === 'view'">
          <div class="space-y-4">
            <div class="bg-gray-50 p-4 rounded-lg">
              <p class="text-sm text-gray-500">Nama Ujian</p>
              <p class="text-lg font-medium">{{ newExam.nama_ujian }}</p>
            </div>
            <div class="bg-gray-50 p-4 rounded-lg">
              <p class="text-sm text-gray-500">Durasi</p>
              <p class="text-lg font-medium">{{ newExam.durasi }} menit</p>
            </div>
            <div class="bg-gray-50 p-4 rounded-lg">
              <p class="text-sm text-gray-500">Jumlah Soal</p>
              <p class="text-lg font-medium">{{ newExam.jumlah_soal }}</p>
            </div>
          </div>
          <div class="flex justify-end mt-6">
            <button
              @click="closeModal"
              class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg transition"
            >
              Tutup
            </button>
          </div>
        </div>

        <!-- Form Tambah/Edit -->
        <form
          v-else
          @submit.prevent="modalType === 'add' ? addExam() : updateExam()"
        >
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Nama Ujian</label
              >
              <input
                v-model="newExam.nama_ujian"
                type="text"
                class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Masukkan nama ujian"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Durasi (menit)</label
              >
              <input
                v-model="newExam.durasi"
                type="number"
                class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Masukkan durasi ujian"
                min="1"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Jumlah Soal</label
              >
              <input
                v-model="newExam.jumlah_soal"
                type="number"
                class="w-full border border-gray-300 rounded-lg p-2.5 focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="Masukkan jumlah soal"
                min="1"
                required
              />
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button
              type="button"
              @click="closeModal"
              class="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg transition"
            >
              Batal
            </button>
            <button
              type="submit"
              class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition"
            >
              {{ modalType === "add" ? "Tambah" : "Simpan" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted } from "vue";
import { useRouter } from "vue-router";

const config = useRuntimeConfig();
const apiUrl = config.public.apiBase;

const router = useRouter();
const exams = ref([]);
const isAuthenticated = ref(false);
const isModalOpen = ref(false);
const modalTitle = ref("");
const modalType = ref("");
const searchTerm = ref("");
const sortBy = ref("nama");
const sortDirection = ref("asc");
const notifications = ref([]);
const showNotifications = ref(false);
const newNotification = ref(null);
let notificationInterval = null;

const newExam = ref({
  id: null,
  nama_ujian: "",
  durasi: "",
  jumlah_soal: "",
});

// Computed properties
const filteredExams = computed(() => {
  let result = [...exams.value];

  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase();
    result = result.filter((exam) =>
      exam.nama_ujian.toLowerCase().includes(term)
    );
  }

  result.sort((a, b) => {
    let valA, valB;

    if (sortBy.value === "nama") {
      valA = a.nama_ujian.toLowerCase();
      valB = b.nama_ujian.toLowerCase();
    } else if (sortBy.value === "durasi") {
      valA = parseInt(a.durasi);
      valB = parseInt(b.durasi);
    } else if (sortBy.value === "soal") {
      valA = parseInt(a.jumlah_soal);
      valB = parseInt(b.jumlah_soal);
    }

    if (sortDirection.value === "asc") {
      return valA > valB ? 1 : -1;
    } else {
      return valA < valB ? 1 : -1;
    }
  });

  return result;
});

const unreadNotifications = computed(() => {
  return notifications.value.filter((n) => !n.read);
});

const fetchExams = async () => {
  try {
    const response = await fetch(`${apiUrl}/exam`);
    const data = await response.json();
    exams.value = data;
  } catch (error) {
    console.error("Gagal mengambil data ujian:", error);
  }
};

const fetchNotifications = async () => {
  try {
    const response = await fetch(`${apiUrl}/api/notifications`);
    const data = await response.json();
    const newNotifications = data.notifications;

    // Check for new notifications
    const latestNotification = newNotifications[newNotifications.length - 1];
    if (
      latestNotification &&
      !notifications.value.some((n) => n.id === latestNotification.id)
    ) {
      newNotification.value = latestNotification;
      setTimeout(() => {
        newNotification.value = null;
      }, 5000); // Auto-close after 5 seconds
    }

    notifications.value = newNotifications;
  } catch (error) {
    console.error("Gagal mengambil notifikasi:", error);
  }
};

const markAsRead = async (notificationId) => {
  try {
    const response = await fetch(
      `${apiUrl}/api/notifications/${notificationId}/mark-read`,
      {
        method: "POST",
      }
    );
    if (response.ok) {
      notifications.value = notifications.value.map((n) =>
        n.id === notificationId ? { ...n, read: true } : n
      );
    }
  } catch (error) {
    console.error("Gagal menandai notifikasi sebagai dibaca:", error);
  }
};

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value;
};

const closeNotification = () => {
  newNotification.value = null;
};

const addExam = async () => {
  try {
    const response = await fetch(`${apiUrl}/exam`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newExam.value),
    });

    if (response.ok) {
      closeModal();
      fetchExams();
    }
  } catch (error) {
    console.error("Gagal menambahkan ujian:", error);
  }
};

const updateExam = async () => {
  try {
    const response = await fetch(`${apiUrl}/exam/${newExam.value.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nama_ujian: newExam.value.nama_ujian,
        durasi: newExam.value.durasi,
        jumlah_soal: newExam.value.jumlah_soal,
      }),
    });

    if (response.ok) {
      closeModal();
      fetchExams();
    } else {
      const errorData = await response.json();
      console.error("Gagal mengupdate ujian:", errorData);
    }
  } catch (error) {
    console.error("Terjadi kesalahan saat update ujian:", error);
  }
};

const goToAddQuestion = (examId) => {
  if (!examId) {
    console.error("Exam ID tidak ditemukan!", examId);
    return;
  }

  router.push(`/exam/${examId}/questions`);
};

const openModal = (type, exam = null) => {
  modalType.value = type;
  isModalOpen.value = true;

  if (type === "add") {
    modalTitle.value = "Tambah Ujian";
    newExam.value = { id: null, nama_ujian: "", durasi: "", jumlah_soal: "" };
  } else if (type === "edit") {
    modalTitle.value = "Edit Ujian";
    newExam.value = { ...exam };
  } else if (type === "view") {
    modalTitle.value = "Detail Ujian";
    newExam.value = { ...exam };
  }
};

const closeModal = () => {
  isModalOpen.value = false;
  newExam.value = { id: null, nama_ujian: "", durasi: "", jumlah_soal: "" };
};

const toggleSort = (field) => {
  if (sortBy.value === field) {
    sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
  } else {
    sortBy.value = field;
    sortDirection.value = "asc";
  }
};

const clearSearch = () => {
  searchTerm.value = "";
};

const calculateTotalQuestions = () => {
  return exams.value.reduce(
    (sum, exam) => sum + parseInt(exam.jumlah_soal || 0),
    0
  );
};

const calculateAverageDuration = () => {
  if (exams.value.length === 0) return 0;
  const totalDuration = exams.value.reduce(
    (sum, exam) => sum + parseInt(exam.durasi || 0),
    0
  );
  return Math.round(totalDuration / exams.value.length);
};

onMounted(() => {
  const token = localStorage.getItem("token");
  if (!token) router.push("/login");
  else {
    isAuthenticated.value = true;
    fetchExams();
    fetchNotifications();
    notificationInterval = setInterval(fetchNotifications, 5000); // Poll every 5 seconds
  }
});

onUnmounted(() => {
  if (notificationInterval) {
    clearInterval(notificationInterval);
  }
});

definePageMeta({
  middleware: "auth",
});
</script>
