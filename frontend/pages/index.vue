<template>
  <div class="bg-gray-50 min-h-screen">
    <main>
      <HeroSection />
      <FeatureSection />
      <HowItWorksSection />
      <ContactSection />
    </main>

    <footer class="bg-gray-800 text-white py-6">
      <div class="container mx-auto px-6 text-center">
        <p>&copy; 2025 Proctorly. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import HeroSection from "~/components/HeroSection.vue";
import FeatureSection from "~/components/FeatureSection.vue";
import HowItWorksSection from "~/components/HowItWorksSection.vue";
import ContactSection from "~/components/ContactSection.vue";

export default {
  name: "LandingPage",
  components: {
    HeroSection,
    FeatureSection,
    HowItWorksSection,
    ContactSection,
  },
};
</script>
