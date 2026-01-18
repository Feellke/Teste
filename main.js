const QUESTIONS = {
  "4-7": [
    {
      question: "Quem João Batista disse ser o Cordeiro de Deus?",
      options: ["Jesus", "Pedro", "André", "João"],
      answer: 0,
    },
    {
      question: "Dois discípulos seguiram Jesus. Um deles se chamava?",
      options: ["André", "Filipe", "Tomé", "Tiago"],
      answer: 0,
    },
    {
      question: "André foi contar a boa notícia para quem?",
      options: ["Seu irmão Simão", "Seu pai", "Sua mãe", "Seu primo"],
      answer: 0,
    },
    {
      question: "Qual novo nome Jesus deu a Simão?",
      options: ["Pedro", "Mateus", "Paulo", "Elias"],
      answer: 0,
    },
    {
      question: "Quem Jesus chamou dizendo: \"Siga-me\"?",
      options: ["Filipe", "Judas", "Bartolomeu", "Lucas"],
      answer: 0,
    },
    {
      question: "Filipe contou a Natanael sobre quem?",
      options: ["Jesus", "Moisés", "Davi", "Noé"],
      answer: 0,
    },
  ],
  "8-12": [
    {
      question: "O que os dois discípulos perguntaram a Jesus ao segui-lo?",
      options: [
        "Mestre, onde moras?",
        "Mestre, quem és tu?",
        "Mestre, por que vieste?",
        "Mestre, o que farás?",
      ],
      answer: 0,
    },
    {
      question: "O que Jesus respondeu quando perguntaram onde ele morava?",
      options: ["Vinde e vede", "Esperem aqui", "Voltem amanhã", "Sigam João"],
      answer: 0,
    },
    {
      question: "Qual era a cidade de Filipe?",
      options: ["Betsaida", "Belém", "Nazaré", "Cafarnaum"],
      answer: 0,
    },
    {
      question:
        "Quando Natanael duvidou, ele disse que algo bom poderia vir de qual lugar?",
      options: ["Nazaré", "Jerusalém", "Belém", "Samaria"],
      answer: 0,
    },
    {
      question: "Jesus viu Natanael debaixo de quê?",
      options: ["Uma figueira", "Uma oliveira", "Uma palmeira", "Uma videira"],
      answer: 0,
    },
    {
      question: "Que título Natanael disse sobre Jesus?",
      options: [
        "Filho de Deus e Rei de Israel",
        "Profeta e líder",
        "Rei dos reis e sacerdote",
        "Mestre e escriba",
      ],
      answer: 0,
    },
  ],
};

const POSITIVE = [
  "Muito bem! Você é um explorador da Bíblia!",
  "Acertou! Você está indo super bem!",
  "Excelente! Continue assim!",
  "Uau! Resposta certa!",
];

const ENCOURAGING = [
  "Quase! Você está aprendendo!",
  "Tudo bem errar, vamos tentar a próxima!",
  "Boa tentativa! Você consegue!",
  "Não foi dessa vez, mas você está indo bem!",
];

const HOME_PRAISE = [
  "Você é incrível! Continue brincando e aprendendo!",
  "Mandou bem! Jesus te ama muito!",
  "Que alegria ver você aprendendo!",
  "Muito bom! Vamos para a próxima!",
];

const HOME_ENCOURAGE = [
  "Não tem problema, vamos tentar de novo!",
  "Você consegue! Vamos juntos!",
  "Respira fundo e tenta outra vez!",
  "A próxima vai ser ainda melhor!",
];

const screens = {
  start: document.getElementById("screen-start"),
  how: document.getElementById("screen-how"),
  play: document.getElementById("screen-play"),
  result: document.getElementById("screen-result"),
};

const levelButtons = document.querySelectorAll("[data-level]");
const startGameButton = document.getElementById("start-game");
const toggleClassroomButton = document.getElementById("toggle-classroom");
const toggleHomeButton = document.getElementById("toggle-home");
const goHowButton = document.getElementById("go-how");
const backStartButton = document.getElementById("back-start");
const playAgainButton = document.getElementById("play-again");
const repeatLevelButton = document.getElementById("repeat-level");
const goStartButton = document.getElementById("go-start");
const questionTitle = document.getElementById("question-title");
const optionsContainer = document.getElementById("options");
const feedback = document.getElementById("feedback");
const nextQuestionButton = document.getElementById("next-question");
const revealAnswerButton = document.getElementById("reveal-answer");
const levelLabel = document.getElementById("level-label");
const progressLabel = document.getElementById("progress-label");
const resultText = document.getElementById("result-text");
const classroomStatus = document.getElementById("classroom-status");
const classroomScore = document.getElementById("classroom-score");
const homeStatus = document.getElementById("home-status");

let currentLevel = "4-7";
let currentQuestions = [];
let currentIndex = 0;
let score = 0;
let locked = false;
let classroomMode = false;
let selectedIndex = null;
let collectiveScore = 0;
let homeMode = false;

const shuffle = (array) => {
  const clone = [...array];
  for (let i = clone.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [clone[i], clone[j]] = [clone[j], clone[i]];
  }
  return clone;
};

const showScreen = (name) => {
  Object.values(screens).forEach((screen) => {
    screen.classList.remove("screen--active");
  });
  screens[name].classList.add("screen--active");
};

const updateLevelButtons = () => {
  levelButtons.forEach((button) => {
    const isActive = button.dataset.level === currentLevel;
    button.classList.toggle("active", isActive);
    button.setAttribute("aria-checked", isActive ? "true" : "false");
    button.tabIndex = isActive ? 0 : -1;
  });
};

const updateProgress = () => {
  levelLabel.textContent = `Nível ${currentLevel}`;
  progressLabel.textContent = `Pergunta ${currentIndex + 1} de ${currentQuestions.length}`;
};

const updateClassroomUI = () => {
  toggleClassroomButton.textContent = classroomMode
    ? "Modo Sala de Aula: ligado"
    : "Modo Sala de Aula: desligado";
  toggleClassroomButton.setAttribute("aria-pressed", classroomMode ? "true" : "false");
  classroomStatus.hidden = !classroomMode;
  revealAnswerButton.hidden = !classroomMode;
  revealAnswerButton.disabled = !classroomMode || selectedIndex === null;
  revealAnswerButton.setAttribute(
    "aria-disabled",
    revealAnswerButton.disabled ? "true" : "false"
  );
  classroomScore.textContent = collectiveScore;
};

const updateHomeUI = () => {
  toggleHomeButton.textContent = homeMode
    ? "Modo Em casa: ligado"
    : "Modo Em casa: desligado";
  toggleHomeButton.setAttribute("aria-pressed", homeMode ? "true" : "false");
  homeStatus.hidden = !homeMode;
  repeatLevelButton.hidden = !homeMode;
};

const renderQuestion = () => {
  const current = currentQuestions[currentIndex];
  questionTitle.textContent = current.question;
  optionsContainer.innerHTML = "";
  feedback.textContent = "";
  nextQuestionButton.disabled = true;
  locked = false;
  selectedIndex = null;

  current.options.forEach((option, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "option-btn";
    button.textContent = option;
    button.addEventListener("click", () => handleAnswer(index, button));
    optionsContainer.appendChild(button);
  });

  updateProgress();
  updateClassroomUI();
  updateHomeUI();
};

const handleAnswer = (index, button) => {
  if (locked) return;

  const current = currentQuestions[currentIndex];
  const buttons = optionsContainer.querySelectorAll(".option-btn");

  if (classroomMode) {
    buttons.forEach((optionButton) =>
      optionButton.classList.remove("wrong", "correct", "selected")
    );
    buttons.forEach((optionButton, optionIndex) => {
      optionButton.classList.toggle("selected", optionIndex === index);
    });
    selectedIndex = index;
    feedback.textContent = "Resposta escolhida! Aguarde o professor revelar. 👩‍🏫";
    feedback.style.color = "var(--muted)";
    nextQuestionButton.disabled = true;
    updateClassroomUI();
    return;
  }

  locked = true;
  const isCorrect = index === current.answer;

  buttons.forEach((optionButton, optionIndex) => {
    if (optionIndex === current.answer) {
      optionButton.classList.add("correct");
    } else if (optionIndex === index) {
      optionButton.classList.add("wrong");
    }
  });

  if (isCorrect) {
    score += 1;
    feedback.textContent = POSITIVE[Math.floor(Math.random() * POSITIVE.length)];
    feedback.style.color = "var(--success)";
    if (homeMode) {
      feedback.textContent = `${feedback.textContent} ${HOME_PRAISE[Math.floor(Math.random() * HOME_PRAISE.length)]}`;
    }
  } else {
    feedback.textContent = ENCOURAGING[Math.floor(Math.random() * ENCOURAGING.length)];
    feedback.style.color = "var(--warning)";
    if (homeMode) {
      feedback.textContent = `${feedback.textContent} ${HOME_ENCOURAGE[Math.floor(Math.random() * HOME_ENCOURAGE.length)]}`;
    }
  }

  nextQuestionButton.disabled = false;
};

const revealAnswer = () => {
  if (locked || selectedIndex === null) return;
  locked = true;
  const current = currentQuestions[currentIndex];
  const buttons = optionsContainer.querySelectorAll(".option-btn");
  const isCorrect = selectedIndex === current.answer;

  buttons.forEach((optionButton, optionIndex) => {
    if (optionIndex === current.answer) {
      optionButton.classList.add("correct");
    } else if (optionIndex === selectedIndex) {
      optionButton.classList.add("wrong");
    }
  });

  if (isCorrect) {
    score += 1;
    collectiveScore += 1;
    feedback.textContent = "Muito bem, turma! Resposta certa! 🎉";
    feedback.style.color = "var(--success)";
  } else {
    feedback.textContent = "Boa tentativa! Vamos para a próxima. 💛";
    feedback.style.color = "var(--warning)";
  }

  updateClassroomUI();
  nextQuestionButton.disabled = false;
};

const goToNext = () => {
  currentIndex += 1;
  if (currentIndex >= currentQuestions.length) {
    resultText.textContent = classroomMode
      ? `A turma acertou ${collectiveScore} de ${currentQuestions.length} perguntas!`
      : `Você acertou ${score} de ${currentQuestions.length} perguntas!`;
    showScreen("result");
    return;
  }
  renderQuestion();
};

const startGame = () => {
  currentQuestions = shuffle(QUESTIONS[currentLevel]);
  currentIndex = 0;
  score = 0;
  collectiveScore = 0;
  showScreen("play");
  renderQuestion();
};

levelButtons.forEach((button) => {
  button.addEventListener("click", () => {
    currentLevel = button.dataset.level;
    updateLevelButtons();
  });
});

startGameButton.addEventListener("click", startGame);
toggleClassroomButton.addEventListener("click", () => {
  classroomMode = !classroomMode;
  if (classroomMode) {
    homeMode = false;
  }
  updateClassroomUI();
  updateHomeUI();
});
toggleHomeButton.addEventListener("click", () => {
  homeMode = !homeMode;
  if (homeMode) {
    classroomMode = false;
  }
  updateClassroomUI();
  updateHomeUI();
});

nextQuestionButton.addEventListener("click", goToNext);
revealAnswerButton.addEventListener("click", revealAnswer);
repeatLevelButton.addEventListener("click", startGame);

goHowButton.addEventListener("click", () => showScreen("how"));
backStartButton.addEventListener("click", () => showScreen("start"));
playAgainButton.addEventListener("click", startGame);
goStartButton.addEventListener("click", () => showScreen("start"));

updateLevelButtons();
updateClassroomUI();
updateHomeUI();
