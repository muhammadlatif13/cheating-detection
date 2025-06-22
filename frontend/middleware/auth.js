export default defineNuxtRouteMiddleware((to, from) => {
  if (process.client) {
    const role = localStorage.getItem("role");

    if (to.path.startsWith("/admin-dashboard") && role !== "admin") {
      return navigateTo("/user-dashboard");
    }
    if (to.path.startsWith("/user-dashboard") && role !== "user") {
      return navigateTo("/admin-dashboard");
    }
  }
});
