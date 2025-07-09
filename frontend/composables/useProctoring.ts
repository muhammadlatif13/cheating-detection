import { ref, onMounted, onUnmounted } from 'vue';

export function useProctoring() {
  const config = useRuntimeConfig();
  const apiUrl = config.public.apiBase;

  // State untuk kamera dan proctoring
  const cameras = ref<MediaDeviceInfo[]>([]);
  const selectedCamera = ref<string | null>(null);
  const videoElement = ref<HTMLVideoElement | null>(null);
  const detectionResults = ref<any>({});
  
  let analysisInterval: NodeJS.Timeout | null = null;
  let currentStream: MediaStream | null = null;

  const stopCurrentStream = () => {
    if (currentStream) {
      currentStream.getTracks().forEach(track => track.stop());
    }
    if (videoElement.value) {
      videoElement.value.srcObject = null;
    }
  };

  const startFrameAnalysis = () => {
    if (analysisInterval) clearInterval(analysisInterval);
    analysisInterval = setInterval(sendFrameForAnalysis, 1500);
  };
  
  const sendFrameForAnalysis = async () => {
    if (!videoElement.value || videoElement.value.paused || videoElement.value.ended) {
      return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = videoElement.value.videoWidth;
    canvas.height = videoElement.value.videoHeight;
    const context = canvas.getContext("2d");
    if (!context) return;
    context.drawImage(videoElement.value, 0, 0, canvas.width, canvas.height);
    const imageDataUrl = canvas.toDataURL("image/jpeg");

    try {
      const response = await fetch(`${apiUrl}/api/analyze_frame?threshold_timing=10&fraud_tolerance=3`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageDataUrl }),
      });
      if (!response.ok) throw new Error("Gagal menganalisis frame");
      detectionResults.value = await response.json();
    } catch (error) {
      console.error("Error sending frame for analysis:", error);
    }
  };

  const startCameraStream = async (deviceId?: string) => {
    stopCurrentStream();
    
    const constraints: MediaStreamConstraints = {
        video: deviceId ? { deviceId: { exact: deviceId } } : true,
    };

    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        currentStream = stream;
        if (videoElement.value) {
          videoElement.value.srcObject = stream;
          await videoElement.value.play();
        }
        startFrameAnalysis();
    } catch (error: any) {
        console.error("Gagal memulai stream kamera:", error);
        if (error.name === "NotAllowedError" || error.name === "PermissionDeniedError") {
            alert("Anda harus memberikan izin akses kamera untuk melanjutkan ujian.");
        } else {
            alert("Gagal memulai kamera. Pastikan tidak ada aplikasi lain yang menggunakannya.");
        }
    }
  };

  const initializeCameraAndDevices = async () => {
    if (!navigator.mediaDevices?.enumerateDevices) {
      alert("Browser Anda tidak mendukung enumerasi perangkat media.");
      return;
    }

    // Minta izin dulu untuk mendapatkan label kamera
    await navigator.mediaDevices.getUserMedia({ video: true });

    const devices = await navigator.mediaDevices.enumerateDevices();
    cameras.value = devices.filter(device => device.kind === "videoinput");

    if (cameras.value.length > 0) {
      const defaultCamera = cameras.value[0].deviceId;
      selectedCamera.value = defaultCamera;
      await startCameraStream(defaultCamera);
    } else {
      alert("Tidak ada kamera yang terdeteksi.");
    }
  };
  
  const switchCamera = async () => {
    if (selectedCamera.value) {
      await startCameraStream(selectedCamera.value);
    }
  };

  onMounted(initializeCameraAndDevices);

  onUnmounted(() => {
    if (analysisInterval) clearInterval(analysisInterval);
    stopCurrentStream();
  });

  return {
    videoElement,
    cameras,
    selectedCamera,
    detectionResults,
    switchCamera,
  };
}