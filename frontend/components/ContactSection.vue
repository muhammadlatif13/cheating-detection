<template>
  <section id="contact" class="bg-indigo-50 py-16">
    <div class="container mx-auto px-6 text-center">
      <h3 class="text-3xl font-extrabold mb-8 text-indigo-900">Contact Us</h3>
      <p class="text-lg text-gray-600 mb-6">
        Have questions? Reach out to us using the form below!
      </p>

      <!-- Contact Form -->
      <form
        @submit.prevent="handleSubmit"
        class="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-lg"
      >
        <div class="mb-6">
          <label for="name" class="block text-gray-700 font-semibold mb-2"
            >Your Name</label
          >
          <input
            type="text"
            id="name"
            v-model="form.name"
            placeholder="Your Name"
            class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-600"
            required
          />
        </div>

        <div class="mb-6">
          <label for="email" class="block text-gray-700 font-semibold mb-2"
            >Your Email</label
          >
          <input
            type="email"
            id="email"
            v-model="form.email"
            placeholder="Your Email"
            class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-600"
            required
          />
        </div>

        <div class="mb-6">
          <label for="message" class="block text-gray-700 font-semibold mb-2"
            >Your Message</label
          >
          <textarea
            id="message"
            v-model="form.message"
            placeholder="Type your message here"
            rows="4"
            class="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-600"
            required
          ></textarea>
        </div>

        <button
          type="submit"
          class="w-full bg-indigo-600 text-white font-semibold py-3 rounded-lg hover:bg-indigo-700 transition-all"
        >
          Send Message
        </button>
      </form>

      <p class="mt-8 text-lg text-gray-200">
        Or email us directly at
        <a href="mailto:support@proctorly.com" class="text-indigo-300"
          >support@proctorly.com</a
        >
      </p>
    </div>
  </section>
</template>

<script>
export default {
  name: "ContactSection",
  data() {
    return {
      form: {
        name: "",
        email: "",
        message: "",
      },
    };
  },
  methods: {
    handleSubmit() {
      // Here you would typically handle form submission
      console.log("Form submitted", this.form);
      // You can add an API call or other logic to process the form data.
      alert("Your message has been sent!");
      this.form.name = "";
      this.form.email = "";
      this.form.message = "";
    },
  },
};
</script>
