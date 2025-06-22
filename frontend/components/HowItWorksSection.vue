<template>
  <section id="how-it-works" class="bg-indigo-50 py-16">
    <div class="container mx-auto px-6 text-center">
      <h3 class="text-3xl font-extrabold mb-12 text-indigo-900">
        How It Works
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="p-6 bg-white text-indigo-600 rounded-xl shadow-lg hover:bg-gray-100 hover:shadow-xl transition-all transform hover:scale-105"
        >
          <p class="text-lg text-gray-600">{{ step }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "HowItWorksSection",
  data() {
    return {
      steps: [
        "Set up your exam environment using Proctorly's web dashboard.",
        "Enable real-time monitoring to detect suspicious behavior.",
        "Get instant alerts and reports on potential fraud cases.",
        "Use face recognition to verify the identity of exam participants.",
        "Monitor facial expressions to detect signs of boredom or drowsiness.",
        "Track head movements to ensure the participant stays focused on the exam.",
      ],
    };
  },
};
</script>
