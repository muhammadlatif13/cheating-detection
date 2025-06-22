<template>
  <section
    class="bg-gradient-to-r from-indigo-600 to-indigo-500 text-white py-32 w-full"
  >
    <div class="container mx-auto px-6 text-start max-w-2xl">
      <h2 class="text-4xl md:text-5xl font-extrabold mb-6 leading-tight">
        Enhance Your Online Exam Security with
        <span
          class="underline decoration-gray-300 decoration-4 underline-offset-4"
          >Proctorly</span
        >
      </h2>
      <p class="text-lg md:text-xl mb-8 leading-relaxed">
        Proctorly revolutionizes online exam monitoring by leveraging advanced
        AI and secure technologies to ensure a fair, transparent, and cheat-free
        exam environment. Whether you're an educational institution or a
        corporate training provider, Proctorly offers a seamless solution to
        safeguard the integrity of your exams.
      </p>

      <!-- Call to Action Button -->
      <NuxtLink
        href="menu/detection"
        class="bg-white text-indigo-600 font-semibold py-3 px-8 rounded-lg shadow-lg hover:bg-gray-100 flex items-center space-x-3 transition-transform transform hover:scale-105"
      >
        <span>Try Proctorly</span>
        <i class="fas fa-arrow-right"></i>
      </NuxtLink>
    </div>
  </section>
</template>

<script>
export default {
  name: "HeroSection",
};
</script>
