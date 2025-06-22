<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div class="mb-10">
        <div class="bg-indigo-600 rounded-2xl shadow-lg p-8 text-white">
          <div
            class="flex flex-col md:flex-row md:items-center md:justify-between"
          >
            <div>
              <h1 class="text-3xl font-bold">Halo, Selamat Datang 👋</h1>
              <p class="mt-2 text-indigo-100">
                Lanjutkan perjalanan belajarmu dengan ujian yang tersedia
              </p>
            </div>
            <div class="mt-6 md:mt-0">
              <button
                @click="goToExamList"
                class="bg-white text-indigo-600 px-6 py-3 rounded-lg font-medium hover:bg-indigo-50 transition"
              >
                Kerjakan Ujian
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="mb-10 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-xl shadow p-6 flex items-center">
          <div class="bg-green-100 p-3 rounded-lg">
            <i class="fas fa-check text-green-600 text-xl"></i>
          </div>
          <div class="ml-4">
            <h3 class="text-sm font-medium text-gray-500">Ujian Selesai</h3>
            <p class="text-2xl font-bold text-gray-800">12</p>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow p-6 flex items-center">
          <div class="bg-blue-100 p-3 rounded-lg">
            <i class="fas fa-clock text-blue-600 text-xl"></i>
          </div>
          <div class="ml-4">
            <h3 class="text-sm font-medium text-gray-500">Sisa Ujian</h3>
            <p class="text-2xl font-bold text-gray-800">3</p>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow p-6 flex items-center">
          <div class="bg-purple-100 p-3 rounded-lg">
            <i class="fas fa-star text-purple-600 text-xl"></i>
          </div>
          <div class="ml-4">
            <h3 class="text-sm font-medium text-gray-500">Nilai Rata-rata</h3>
            <p class="text-2xl font-bold text-gray-800">85.7</p>
          </div>
        </div>
      </div>

      <!-- Main Navigation Cards -->
      <h2 class="text-xl font-bold text-gray-800 mb-6">Menu Navigasi</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition cursor-pointer group"
          @click="goToExamList"
        >
          <div
            class="bg-indigo-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:bg-indigo-600 transition"
          >
            <i
              class="fas fa-list text-indigo-600 group-hover:text-white transition"
            ></i>
          </div>
          <h2 class="text-xl font-semibold text-gray-800 mb-2">Daftar Ujian</h2>
          <p class="text-gray-600 text-sm">
            Lihat dan kerjakan ujian yang tersedia untuk kamu.
          </p>
          <div class="mt-4 text-indigo-600 flex items-center">
            <span class="text-sm font-medium">Lihat Ujian</span>
            <i class="fas fa-arrow-right ml-2 text-xs"></i>
          </div>
        </div>

        <div
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition cursor-pointer group"
          @click="goToHistory"
        >
          <div
            class="bg-indigo-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:bg-indigo-600 transition"
          >
            <i
              class="fas fa-history text-indigo-600 group-hover:text-white transition"
            ></i>
          </div>
          <h2 class="text-xl font-semibold text-gray-800 mb-2">
            Riwayat Ujian
          </h2>
          <p class="text-gray-600 text-sm">
            Lihat hasil dan riwayat pengerjaan ujianmu.
          </p>
          <div class="mt-4 text-indigo-600 flex items-center">
            <span class="text-sm font-medium">Cek Riwayat</span>
            <i class="fas fa-arrow-right ml-2 text-xs"></i>
          </div>
        </div>

        <div
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition cursor-pointer group"
          @click="goToProfile"
        >
          <div
            class="bg-indigo-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:bg-indigo-600 transition"
          >
            <i
              class="fas fa-user text-indigo-600 group-hover:text-white transition"
            ></i>
          </div>
          <h2 class="text-xl font-semibold text-gray-800 mb-2">Profil</h2>
          <p class="text-gray-600 text-sm">
            Kelola informasi akun dan ubah password.
          </p>
          <div class="mt-4 text-indigo-600 flex items-center">
            <span class="text-sm font-medium">Edit Profil</span>
            <i class="fas fa-arrow-right ml-2 text-xs"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const goToExamList = () => {
  router.push("/role/user/daftar_ujian");
};

const goToHistory = () => {
  router.push("/exam/history");
};

const goToProfile = () => {
  router.push("/profile");
};
</script>
