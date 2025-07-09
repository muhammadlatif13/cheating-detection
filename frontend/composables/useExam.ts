import { ref, computed, watch } from 'vue';

// Definisikan tipe data agar lebih jelas
interface Question {
  number: number;
  text: string;
  options: string[];
  selected: number | null;
  answered: boolean;
}

export function useExam(examId: string) {
  const config = useRuntimeConfig();
  const apiUrl = config.public.apiBase;

  // State untuk soal ujian
  const questions = ref<Question[]>([]);
  const currentIndex = ref(0);
  const selectedAnswer = ref<number | null>(null);

  // Computed property untuk data yang ditampilkan
  const currentQuestion = computed<Partial<Question>>(() => {
    return questions.value[currentIndex.value] || {};
  });

  const answeredCount = computed(() => {
    return questions.value.filter(q => q.answered).length;
  });

  // Fungsi untuk mengambil data soal
  const fetchQuestions = async () => {
    try {
      const response = await fetch(`${apiUrl}/add_questions/${examId}`);
      const data = await response.json();
      questions.value = data.map((q: any, index: number) => ({
        number: index + 1,
        text: q.question.question_text,
        options: q.question.options,
        selected: null,
        answered: false,
      }));
      updateCurrentQuestion();
    } catch (error) {
      console.error("Gagal mengambil soal:", error);
      // Tambahkan notifikasi error untuk pengguna di sini
    }
  };

  // Fungsi untuk navigasi
  const prevQuestion = () => {
    if (currentIndex.value > 0) {
      currentIndex.value--;
      updateCurrentQuestion();
    }
  };

  const nextQuestion = () => {
    if (currentIndex.value < questions.value.length - 1) {
      currentIndex.value++;
      updateCurrentQuestion();
    }
  };

  const goToQuestion = (index: number) => {
    currentIndex.value = index;
    updateCurrentQuestion();
  };
  
  const finishExam = () => {
    const finalAnswers = questions.value.map(q => ({
      number: q.number,
      selected: q.selected,
    }));
    console.log("Jawaban akhir:", finalAnswers);
    alert("Ujian telah diselesaikan. Terima kasih!");
    // Logika untuk mengirim jawaban ke server bisa ditambahkan di sini
  };
  
  // Helper function
  const updateCurrentQuestion = () => {
    if (questions.value.length > 0) {
      selectedAnswer.value = questions.value[currentIndex.value].selected;
    }
  };

  // Watcher untuk menandai soal sebagai terjawab
  watch(selectedAnswer, (newValue) => {
    const question = questions.value[currentIndex.value];
    if (question) {
      question.selected = newValue;
      if (newValue !== null) {
        question.answered = true;
      }
    }
  });
  
  // Panggil fetchQuestions saat composable digunakan
  fetchQuestions();

  // Expose state dan functions yang dibutuhkan oleh komponen
  return {
    questions,
    currentIndex,
    currentQuestion,
    selectedAnswer,
    answeredCount,
    prevQuestion,
    nextQuestion,
    goToQuestion,
    finishExam,
  };
}