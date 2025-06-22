<script lang="ts" setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { menuList } from "~/assets/ts/headerMenu";

const route = useRoute();

// Pastikan ada slash di depan path
const isLoginPage = computed(() => route.path === "/menu/login");

const isDetectionOrLogsPage = computed(() =>
  ["/detection", "/logs"].includes(route.path)
);

const isLoggedIn = computed(() => !!localStorage.getItem("token"));
</script>

<template>
  <header class="bg-white sticky top-0 z-10 p-5 shadow-lg">
    <nav class="flex items-center justify-between">
      <!-- Brand -->
      <NuxtLink to="/">
        <h1 class="text-2xl font-bold text-indigo-600">Proctorly</h1>
      </NuxtLink>

      <!-- Menu hanya muncul di halaman detection dan logs -->
      <ul v-if="isDetectionOrLogsPage" class="flex space-x-6">
        <li v-for="(menu, index) in menuList" :key="index">
          <NuxtLink
            :to="menu.link"
            class="text-gray-700 hover:text-indigo-600"
            exact-active-class="font-bold text-indigo-600 border-b-2 border-indigo-600"
          >
            {{ menu.name }}
          </NuxtLink>
        </li>
      </ul>

      <!-- Button Login -->
      <div class="flex space-x-6">
        <NuxtLink
          v-if="!isLoggedIn && !isLoginPage"
          to="/menu/login"
          class="bg-indigo-600 text-white font-semibold py-2 px-6 rounded-lg shadow hover:bg-indigo-700"
        >
          Log in
        </NuxtLink>
      </div>
    </nav>
  </header>
</template>
