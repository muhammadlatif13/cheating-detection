<template>
  <section id="features" class="bg-indigo-50 py-16">
    <div class="container mx-auto px-6 text-center">
      <h3 class="text-3xl font-extrabold mb-12 text-indigo-900">
        Our Features
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div
          class="p-6 bg-white text-indigo-600 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
        >
          <h4 class="text-xl font-semibold mb-4">Real-Time Monitoring</h4>
          <p class="text-gray-600">
            Monitor students live using advanced AI techniques, including head
            pose and eye tracking.
          </p>
        </div>
        <div
          class="p-6 bg-white text-indigo-600 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
        >
          <h4 class="text-xl font-semibold mb-4">Multi-Modal Detection</h4>
          <p class="text-gray-600">
            Combine head pose, eye gaze, lip movement, and face classification
            for accurate fraud detection.
          </p>
        </div>
        <div
          class="p-6 bg-white text-indigo-600 rounded-xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
        >
          <h4 class="text-xl font-semibold mb-4">Web-Based Dashboard</h4>
          <p class="text-gray-600">
            Easily configure thresholds and tolerances through an intuitive web
            interface.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "FeaturesSection",
};
</script>
