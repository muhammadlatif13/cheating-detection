<template>
  <div
    v-if="!shouldHideSidebar"
    class="h-screen sticky top-0 w-64 bg-gray-800 text-white flex flex-col shadow-lg transition-all duration-300"
    :class="{ 'w-20': isCollapsed }"
  >
    <!-- Header with collapsible toggle -->
    <div
      class="px-6 py-4 flex items-center justify-between border-b border-gray-700"
    >
      <div v-if="!isCollapsed" class="text-xl font-bold truncate">
        {{ isAdmin ? "Admin Panel" : "User Panel" }}
      </div>
      <div v-else class="text-xl font-bold mx-auto">
        {{ isAdmin ? "A" : "U" }}
      </div>
      <button
        @click="toggleSidebar"
        class="text-gray-400 hover:text-white focus:outline-none"
        :title="isCollapsed ? 'Expand' : 'Collapse'"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            v-if="isCollapsed"
            fill-rule="evenodd"
            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
            clip-rule="evenodd"
          />
          <path
            v-else
            fill-rule="evenodd"
            d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
            clip-rule="evenodd"
          />
        </svg>
      </button>
    </div>

    <!-- User profile section -->
    <div class="px-4 py-3 border-b border-gray-700 flex items-center">
      <div class="rounded-full bg-gray-600 flex-shrink-0">
        <img
          v-if="userAvatar"
          :src="userAvatar"
          alt="User avatar"
          class="w-10 h-10 rounded-full object-cover"
        />
        <div
          v-else
          class="w-10 h-10 rounded-full flex items-center justify-center bg-blue-500 text-white font-bold"
        >
          {{ userInitials }}
        </div>
      </div>
      <div v-if="!isCollapsed" class="ml-3 overflow-hidden">
        <div class="text-sm font-medium truncate">{{ userName }}</div>
        <div class="text-xs text-gray-400 truncate">
          {{ isAdmin ? "Administrator" : "Regular User" }}
        </div>
      </div>
    </div>

    <!-- Navigation section -->
    <nav class="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
      <!-- Admin Menu -->
      <template v-if="isAdmin">
        <div class="mb-4">
          <div
            v-if="!isCollapsed"
            class="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2"
          >
            Main
          </div>

          <NuxtLink
            to="/role/admin/admin-dashboard"
            class="flex items-center px-3 py-2 rounded-lg transition-colors"
            :class="[
              activePath === '/role/admin/admin-dashboard'
                ? 'bg-blue-600 text-white'
                : 'text-gray-300 hover:bg-gray-700',
            ]"
          >
            <i class="fas fa-house"></i>
            <span v-if="!isCollapsed" class="ml-3">Dashboard</span>
          </NuxtLink>

          <NuxtLink
            to="/role/admin/logs"
            class="flex items-center px-3 py-2 rounded-lg transition-colors mt-1"
            :class="[
              activePath === '/role/admin/logs'
                ? 'bg-blue-600 text-white'
                : 'text-gray-300 hover:bg-gray-700',
            ]"
          >
            <i class="fas fa-book"></i>
            <span v-if="!isCollapsed" class="ml-3">Fraud Logs</span>
          </NuxtLink>
        </div>
      </template>

      <!-- User Menu -->
      <template v-else>
        <div class="mb-4">
          <div
            v-if="!isCollapsed"
            class="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2"
          >
            Menu
          </div>

          <NuxtLink
            to="/role/user/user-dashboard"
            class="flex items-center px-3 py-2 rounded-lg transition-colors"
            :class="[
              activePath === '/role/user/user-dashboard'
                ? 'bg-blue-600 text-white'
                : 'text-gray-300 hover:bg-gray-700',
            ]"
          >
            <i class="fas fa-house"></i>
            <span v-if="!isCollapsed" class="ml-3">Dashboard</span>
          </NuxtLink>
        </div>
      </template>
    </nav>

    <!-- Footer with logout button -->
    <div class="px-4 py-4 border-t border-gray-700">
      <button
        @click="logout"
        class="w-full flex items-center justify-center bg-red-600 hover:bg-red-500 px-4 py-2 rounded text-white transition-colors"
      >
        <i class="fas fa-sign-out"></i>
        <span v-if="!isCollapsed" class="ml-2">Logout</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from "vue-router";
import { ref, computed, onMounted } from "vue";

const router = useRouter();
const route = useRoute();

const isAdmin = ref(localStorage.getItem("role") === "admin");
const userName = ref(localStorage.getItem("userName") || "User");
const userAvatar = ref(localStorage.getItem("userAvatar") || null);

const userInitials = computed(() => {
  const nameParts = userName.value.split(" ");
  if (nameParts.length >= 2) {
    return (nameParts[0][0] + nameParts[1][0]).toUpperCase();
  }
  return userName.value.substring(0, 2).toUpperCase();
});

const isCollapsed = ref(localStorage.getItem("sidebarCollapsed") === "true");
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
  localStorage.setItem("sidebarCollapsed", isCollapsed.value.toString());
};

const hiddenRoutes = ["/", "/menu/login", "/menu/detection", "/menu/register"];

const shouldHideSidebar = computed(() => {
  return hiddenRoutes.includes(route.path);
});

const activePath = computed(() => route.path);

const logout = () => {
  if (confirm("Are you sure you want to logout?")) {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("userName");
    localStorage.removeItem("userAvatar");

    router.push("/menu/login");
  }
};

onMounted(() => {
  const token = localStorage.getItem("token");

  if (!token && !hiddenRoutes.includes(route.path)) {
    router.push("/menu/login");
  }
});
</script>

<style scoped>
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style>
