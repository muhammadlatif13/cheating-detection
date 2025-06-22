<template>
  <section id="fraud-logs" class="py-8">
    <div class="container mx-auto px-4">
      <div class="mb-6 flex flex-col md:flex-row justify-between items-center">
        <h3 class="text-2xl md:text-3xl font-extrabold text-indigo-900">
          Fraud Logs
        </h3>

        <!-- Control panel -->
        <div class="flex flex-wrap gap-3 mt-4 md:mt-0">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search logs..."
              class="pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-300 focus:border-indigo-500 outline-none transition"
            />
            <span class="absolute left-3 top-2.5 text-gray-400">
              <i class="fas fa-search mr-1"></i>
            </span>
          </div>

          <select
            v-model="filterType"
            class="px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-300 focus:border-indigo-500 outline-none transition"
          >
            <option value="">All Types</option>
            <option v-for="type in uniqueFraudTypes" :key="type" :value="type">
              {{ type }}
            </option>
          </select>

          <button
            @click="refreshLogs"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition flex items-center gap-2"
          >
            <i class="fas fa-refresh"></i>
            Refresh
          </button>
        </div>
      </div>

      <!-- Stats cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div
          class="bg-white p-4 rounded-xl shadow-md border-l-4 border-indigo-500"
        >
          <div class="flex justify-between">
            <div>
              <p class="text-gray-500 text-sm">Total Logs</p>
              <p class="text-2xl font-bold">{{ logs.length }}</p>
            </div>
            <div class="bg-indigo-100 p-3 rounded-lg">
              <i class="fas fa-file h-6 w-6 text-indigo-600 text-center"></i>
            </div>
          </div>
        </div>

        <div
          class="bg-white p-4 rounded-xl shadow-md border-l-4 border-yellow-500"
        >
          <div class="flex justify-between">
            <div>
              <p class="text-gray-500 text-sm">Last 24 Hours</p>
              <p class="text-2xl font-bold">{{ last24HoursCount }}</p>
            </div>
            <div class="bg-yellow-100 p-3 rounded-lg">
              <i class="fas fa-clock h-6 w-6 text-yellow-600 text-center"></i>
            </div>
          </div>
        </div>

        <div
          class="bg-white p-4 rounded-xl shadow-md border-l-4 border-green-500"
        >
          <div class="flex justify-between">
            <div>
              <p class="text-gray-500 text-sm">With Evidence</p>
              <p class="text-2xl font-bold">{{ logsWithImages }}</p>
            </div>
            <div class="bg-green-100 p-3 rounded-lg">
              <i class="fas fa-image h-6 w-6 text-green-600 text-center"></i>
            </div>
          </div>
        </div>

        <div
          class="bg-white p-4 rounded-xl shadow-md border-l-4 border-green-500"
        >
          <div class="flex justify-between">
            <div>
              <p class="text-gray-500 text-sm">Detected Cheating</p>
              <p class="text-2xl font-bold">{{ DetectedCheatingCount }}</p>
            </div>
            <div class="bg-purple-100 p-3 rounded-lg">
              <i class="fas fa-robot h-6 w-6 text-purple-600 text-center"></i>
            </div>
          </div>
        </div>
      </div>

      <div
        class="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200"
      >
        <!-- Table container -->
        <div class="overflow-x-auto max-h-[600px]">
          <table class="table-auto w-full border-collapse">
            <thead class="bg-indigo-600 text-white sticky top-0 z-10">
              <tr>
                <th
                  class="px-4 py-3 cursor-pointer select-none"
                  @click="sortBy('id')"
                >
                  <div class="flex items-center">
                    No
                    <span v-if="sortField === 'id'" class="ml-1">
                      {{ sortDirection === "asc" ? "↑" : "↓" }}
                    </span>
                  </div>
                </th>
                <th
                  class="px-4 py-3 cursor-pointer select-none"
                  @click="sortBy('created_at')"
                >
                  <div class="flex items-center">
                    Time
                    <span v-if="sortField === 'created_at'" class="ml-1">
                      {{ sortDirection === "asc" ? "↑" : "↓" }}
                    </span>
                  </div>
                </th>
                <th class="px-4 py-3">Description</th>
                <th
                  class="px-4 py-3 cursor-pointer select-none"
                  @click="sortBy('fraud_type')"
                >
                  <div class="flex items-center">
                    Type
                    <span v-if="sortField === 'fraud_type'" class="ml-1">
                      {{ sortDirection === "asc" ? "↑" : "↓" }}
                    </span>
                  </div>
                </th>
                <th
                  class="px-4 py-3 cursor-pointer select-none"
                  @click="sortBy('fraud_count')"
                >
                  <div class="flex items-center">
                    Amount
                    <span v-if="sortField === 'fraud_count'" class="ml-1">
                      {{ sortDirection === "asc" ? "↑" : "↓" }}
                    </span>
                  </div>
                </th>
                <th class="px-4 py-3">Detection</th>
                <th class="px-4 py-3">Confidence</th>
                <th class="px-4 py-3">Capture</th>
                <th class="px-4 py-3">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="log in filteredAndSortedLogs"
                :key="log.id"
                class="hover:bg-gray-50 transition border-b"
              >
                <td class="px-4 py-3 text-center">{{ log.id }}</td>
                <td class="px-4 py-3">{{ formatDate(log.created_at) }}</td>
                <td class="px-4 py-3">
                  <div class="max-w-md truncate">{{ log.description }}</div>
                </td>
                <td class="px-4 py-3">
                  <span
                    class="px-2 py-1 rounded-full text-xs font-medium"
                    :class="getTypeClass(log.fraud_type)"
                  >
                    {{ log.fraud_type }}
                  </span>
                </td>
                <td class="px-4 py-3 text-center">{{ log.fraud_count }}</td>
                <td class="px-4 py-3">
                  <span
                    class="px-2 py-1 rounded-full text-xs font-medium"
                    :class="getDetectionClass(log.classification_result)"
                  >
                    {{ log.classification_result || "N/A" }}
                  </span>
                </td>
                <td class="px-4 py-3 text-center">
                  <div
                    v-if="log.confidence_percentage"
                    class="w-full bg-gray-200 rounded-full h-2.5"
                  >
                    <div
                      class="bg-indigo-600 h-2.5 rounded-full"
                      :style="{ width: log.confidence_percentage * 100 + '%' }"
                      :title="
                        (log.confidence_percentage * 100).toFixed(1) + '%'
                      "
                    ></div>
                    <span class="text-xs text-gray-600">
                      {{ (log.confidence_percentage * 100).toFixed(1) }}%
                    </span>
                  </div>
                  <span v-else class="text-gray-400 text-sm italic">N/A</span>
                </td>
                <td class="px-4 py-3">
                  <div class="flex justify-center">
                    <img
                      v-if="log.image_data"
                      :src="'data:image/png;base64,' + log.image_data"
                      alt="Fraud Evidence"
                      class="w-12 h-12 rounded object-cover shadow cursor-pointer hover:opacity-80 transition-all"
                      @click="openModal(log)"
                    />
                    <span v-else class="text-gray-400 text-sm italic"
                      >No image</span
                    >
                  </div>
                </td>
                <td class="px-4 py-3">
                  <div class="flex justify-center space-x-2">
                    <button
                      @click="viewDetails(log)"
                      class="p-1.5 bg-indigo-100 text-indigo-700 rounded hover:bg-indigo-200 transition"
                      title="View Details"
                    >
                      <i class="fas fa-eye text-center"></i>
                    </button>
                    <button
                      @click="markReviewed(log.id)"
                      class="p-1.5 bg-green-100 text-green-700 rounded hover:bg-green-200 transition"
                      title="Mark as Reviewed"
                    >
                      <i class="fas fa-check text-green-700 text-center"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Empty state -->
        <div
          v-if="filteredAndSortedLogs.length === 0 && !isLoading"
          class="text-center py-12 text-gray-500"
        >
          <i
            class="fas fa-minus-circle h-16 w-16 mx-auto text-gray-300 text-center mb-4"
          ></i>
          <p class="text-xl font-semibold">No fraud logs found</p>
          <p class="mt-1 text-gray-400">Try adjusting your search or filters</p>
        </div>

        <!-- Loading state -->
        <div v-if="isLoading" class="text-center py-12">
          <div
            class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"
          ></div>
          <p class="mt-4 text-gray-600 font-medium">Loading fraud logs...</p>
        </div>

        <!-- Pagination -->
        <div
          v-if="filteredAndSortedLogs.length > 0 && !isLoading"
          class="flex justify-between items-center px-6 py-4 bg-gray-50 border-t"
        >
          <div class="text-sm text-gray-500">
            Showing {{ startIndex + 1 }} to
            {{ Math.min(endIndex, filteredLogs.length) }} of
            {{ filteredLogs.length }} logs
          </div>
          <div class="flex space-x-2">
            <button
              @click="prevPage"
              :disabled="currentPage === 1"
              class="px-3 py-1 rounded border"
              :class="
                currentPage === 1
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-white hover:bg-gray-50'
              "
            >
              Previous
            </button>
            <button
              @click="nextPage"
              :disabled="currentPage >= totalPages"
              class="px-3 py-1 rounded border"
              :class="
                currentPage >= totalPages
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-white hover:bg-gray-50'
              "
            >
              Next
            </button>
          </div>
        </div>
      </div>

      <!-- Modal -->
      <transition name="fade">
        <div
          v-if="showModal"
          class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-75 z-50"
          @click.self="closeModal"
        >
          <div
            class="bg-white rounded-xl shadow-2xl max-w-4xl w-full mx-4 overflow-hidden"
          >
            <div class="flex justify-between items-center p-4 border-b">
              <h3 class="text-xl font-bold text-indigo-900">
                Fraud Evidence Details
              </h3>
              <button
                class="text-gray-500 hover:text-gray-700 text-2xl focus:outline-none"
                @click="closeModal"
              >
                &times;
              </button>
            </div>

            <div class="p-4 md:flex gap-6">
              <div class="md:w-1/2">
                <img
                  v-if="selectedLog && selectedLog.image_data"
                  :src="'data:image/png;base64,' + selectedLog.image_data"
                  alt="Fraud Evidence"
                  class="w-full object-contain rounded-md max-h-[50vh]"
                />
              </div>

              <div class="md:w-1/2 mt-4 md:mt-0">
                <div v-if="selectedLog" class="space-y-4">
                  <div>
                    <h4 class="text-sm font-semibold text-gray-500">ID</h4>
                    <p>{{ selectedLog.id }}</p>
                  </div>

                  <div>
                    <h4 class="text-sm font-semibold text-gray-500">
                      Timestamp
                    </h4>
                    <p>{{ formatDate(selectedLog.created_at) }}</p>
                  </div>

                  <div>
                    <h4 class="text-sm font-semibold text-gray-500">Warning</h4>
                    <p>
                      <span
                        class="px-2 py-1 rounded-full text-xs font-medium"
                        :class="getTypeClass(selectedLog.fraud_type)"
                      >
                        {{ selectedLog.fraud_type }}
                      </span>
                    </p>
                  </div>

                  <div>
                    <h4 class="text-sm font-semibold text-gray-500">
                      Description
                    </h4>
                    <p>{{ selectedLog.description }}</p>
                  </div>

                  <div>
                    <h4 class="text-sm font-semibold text-gray-500">Amount</h4>
                    <p>{{ selectedLog.fraud_count }}</p>
                  </div>
                  <div>
                    <p>
                      <span
                        class="px-2 py-1 rounded-full text-xs font-medium"
                        :class="
                          getDetectionClass(selectedLog.classification_result)
                        "
                      >
                        {{ selectedLog.classification_result || "N/A" }}
                      </span>
                    </p>
                  </div>

                  <div>
                    <h4 class="text-sm font-semibold text-gray-500">
                      Confidence Level
                    </h4>
                    <div class="flex items-center gap-2">
                      <div class="w-full bg-gray-200 rounded-full h-2.5">
                        <div
                          class="bg-indigo-600 h-2.5 rounded-full"
                          :style="{
                            width:
                              selectedLog.confidence_percentage * 100 + '%',
                          }"
                        ></div>
                      </div>
                      <span class="text-sm text-gray-600">
                        {{
                          (selectedLog.confidence_percentage * 100).toFixed(1)
                        }}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="flex justify-end gap-3 p-4 border-t bg-gray-50">
              <button
                @click="closeModal"
                class="px-4 py-2 border rounded-lg hover:bg-gray-100"
              >
                Close
              </button>
              <button
                @click="
                  markReviewed(selectedLog.id);
                  closeModal();
                "
                class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
              >
                Mark as Reviewed
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const config = useRuntimeConfig();
const apiUrl = config.public.apiBase;
const logs = ref([]);
const selectedLog = ref(null);
const showModal = ref(false);
const isLoading = ref(true);
const searchQuery = ref("");
const filterType = ref("");
const sortField = ref("created_at");
const sortDirection = ref("desc");
const currentPage = ref(1);
const pageSize = ref(10);

const startIndex = computed(() => (currentPage.value - 1) * pageSize.value);
const endIndex = computed(() => startIndex.value + pageSize.value);

const uniqueFraudTypes = computed(() => {
  const types = [...new Set(logs.value.map((log) => log.fraud_type))];
  return types.sort();
});

const filteredLogs = computed(() => {
  return logs.value.filter((log) => {
    const matchesSearch = searchQuery.value
      ? log.description
          .toLowerCase()
          .includes(searchQuery.value.toLowerCase()) ||
        log.fraud_type
          .toLowerCase()
          .includes(searchQuery.value.toLowerCase()) ||
        log.id.toString().includes(searchQuery.value)
      : true;

    const matchesType = filterType.value
      ? log.fraud_type === filterType.value
      : true;

    return matchesSearch && matchesType;
  });
});

const filteredAndSortedLogs = computed(() => {
  const sorted = [...filteredLogs.value].sort((a, b) => {
    let aValue = a[sortField.value];
    let bValue = b[sortField.value];

    if (sortField.value === "created_at") {
      aValue = new Date(aValue);
      bValue = new Date(bValue);
    }

    if (aValue < bValue) {
      return sortDirection.value === "asc" ? -1 : 1;
    }
    if (aValue > bValue) {
      return sortDirection.value === "asc" ? 1 : -1;
    }
    return 0;
  });

  return sorted.slice(startIndex.value, endIndex.value);
});

const totalPages = computed(() => {
  return Math.ceil(filteredLogs.value.length / pageSize.value);
});

const last24HoursCount = computed(() => {
  const oneDayAgo = new Date();
  oneDayAgo.setDate(oneDayAgo.getDate() - 1);

  return logs.value.filter((log) => {
    const logDate = new Date(log.created_at);
    return logDate >= oneDayAgo;
  }).length;
});

const logsWithImages = computed(() => {
  return logs.value.filter((log) => log.image_data).length;
});

const DetectedCheatingCount = computed(() => {
  return logs.value.filter((log) => log.classification_result === "Cheating")
    .length;
});

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  return date.toLocaleString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
};

const getTypeClass = (type) => {
  const typeMap = {
    "Payment Fraud": "bg-red-100 text-red-700",
    "Account Takeover": "bg-purple-100 text-purple-700",
    "Fake Account": "bg-yellow-100 text-yellow-700",
    "Identity Theft": "bg-orange-100 text-orange-700",
    "Phishing Attempt": "bg-blue-100 text-blue-700",
  };
  return typeMap[type] || "bg-gray-100 text-gray-700";
};

const getDetectionClass = (result) => {
  const resultMap = {
    Cheating: "bg-red-100 text-red-700",
    Normal: "bg-green-100 text-green-700",
  };
  return resultMap[result] || "bg-gray-100 text-gray-700";
};

const fetchLogs = async () => {
  isLoading.value = true;
  try {
    const data = await $fetch(`${apiUrl}/api/fraud_logs`);
    logs.value = data;
  } catch (err) {
    console.error("Error fetching logs:", err);
    alert("Failed to load fraud logs. Please try again later.");
  } finally {
    isLoading.value = false;
  }
};

const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === "asc" ? "desc" : "asc";
  } else {
    sortField.value = field;
    sortDirection.value = "asc";
  }
};

const openModal = (log) => {
  selectedLog.value = log;
  showModal.value = true;
};

const closeModal = () => {
  selectedLog.value = null;
  showModal.value = false;
};

const viewDetails = (log) => {
  openModal(log);
};

const refreshLogs = () => {
  fetchLogs();
};

const markReviewed = async (id) => {
  alert(`Log #${id} marked as reviewed.`);
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

onMounted(() => {
  fetchLogs();
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
