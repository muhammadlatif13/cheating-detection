<template>
  <div
    class="w-1/4 ml-6 bg-white shadow-lg p-4 rounded-lg border flex flex-col items-center"
  >
    <div class="w-full border rounded-lg overflow-hidden mb-4 bg-black">
      <video
        ref="videoElement"
        autoplay
        playsinline
        muted
        class="w-full h-full object-cover"
      ></video>
    </div>

    <div class="w-full mb-4 p-2 border rounded-lg text-sm">
      <p>
        <strong>Status:</strong>
        {{ detectionResults.fraud_status || "Memulai..." }}
      </p>
      <p>
        <strong>Pose Kepala:</strong> {{ detectionResults.head_pose || "N/A" }}
      </p>
      <p>
        <strong>Arah Mata:</strong> {{ detectionResults.eye_gaze || "N/A" }}
      </p>
      <p>
        <strong>Pelanggaran:</strong>
        {{ detectionResults.fraud_count || 0 }} kali
      </p>
    </div>

    <div class="w-full mb-4">
      <label
        for="camera-select"
        class="block text-start text-gray-700 font-semibold mb-2"
      >
        Pilih Kamera:
      </label>
      <select
        id="camera-select"
        v-model="selectedCamera"
        @change="switchCamera"
        class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 text-gray-700"
      >
        <option
          v-for="camera in cameras"
          :key="camera.deviceId"
          :value="camera.deviceId"
        >
          {{ camera.label || `Kamera ${cameras.indexOf(camera) + 1}` }}
        </option>
      </select>
    </div>

    <slot></slot>
  </div>
</template>

<script setup>
import { useProctoring } from "~/composables/useProctoring";

// Komponen ini hanya menggunakan logika dari composable
const {
  videoElement,
  cameras,
  selectedCamera,
  detectionResults,
  switchCamera,
} = useProctoring();
</script>
