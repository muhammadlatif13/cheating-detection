<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center px-4">
    <div class="bg-white rounded-3xl shadow-lg w-full max-w-md p-8 sm:p-10">
      <h2 class="text-3xl font-bold text-gray-800 text-center mb-6">
        Masuk ke Akunmu
      </h2>
      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label class="text-sm text-gray-600 font-medium mb-1 block"
            >Username</label
          >
          <input
            v-model="username"
            type="text"
            placeholder="Username"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
            required
          />
        </div>
        <div>
          <label class="text-sm text-gray-600 font-medium mb-1 block"
            >Password</label
          >
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full px-4 py-2.5 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 transition"
            required
          />
        </div>
        <button
          type="submit"
          class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2.5 rounded-xl transition duration-200"
        >
          Log in
        </button>
        <p
          v-if="errorMessage"
          class="text-center text-red-500 text-sm font-medium"
        >
          {{ errorMessage }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useState } from "#app";

const config = useRuntimeConfig();
const apiUrl = config.public.apiBase;

const router = useRouter();
const username = ref("");
const password = ref("");
const errorMessage = ref("");
const token = useState("token", () => null);

const handleLogin = async () => {
  try {
    const response = await fetch(`${apiUrl}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    const data = await response.json();
    if (response.ok) {
      token.value = data.token;

      if (process.client) {
        localStorage.setItem("token", data.token);
        localStorage.setItem("role", data.role);
      }

      if (data.role === "admin") {
        router.push("/role/admin/admin-dashboard");
      } else {
        router.push("/role/user/user-dashboard");
      }
    } else {
      errorMessage.value = data.detail;
    }
  } catch (error) {
    errorMessage.value = "Terjadi kesalahan, coba lagi!";
  }
};
</script>
