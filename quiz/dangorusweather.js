const quizData = [
    {
      question: "How does a thunderstorm form?",
      options: ["When moist warm air rises quickly", "How am I supposed to know?!?!?!", "When it rains it creates thunderstorms", "When it rains and it is windy"],
      answer: "When moist warm air rises quickly"
    },
    {
      question: "Thunderstorms always form in the morning",
      options: ["True", "False"],
      answer: "False"
    },
    {
      question: "Thunderstorms form MORE in winter",
      options: ["True", "False"],
      answer: "False"
    },
    {
      question: "How does lightning form",
      options: ["It forms by clouds getting static electricity", "It forms by clouds rubbing up against each other", "When ice and dirt rub against each other", "hen lightning Mcqueen drives"],
      answer: "When ice and dirt rub against each other"
    },
    {
      question: "Ground that is negatively charged forms lightning",
      options: ["True", "False"],
      answer: "False"
    },
    {
      question: "How big can a hurricane get?",
      options: ["845270984375234857092834ft", "100ft", "50ft", "600ft"],
      answer: "600ft"
    },
    {
      question: "Hurricanes form everywhere with water?",
      options: ["True", "Flase"],
      answer: "False"
    },
    {
      question: "How big can a hurricane get?",
      options: ["500", "300", "350", "how am i suppost to know?"],
      answer: "300"
    },
    {
      question: "Are tornados smaller than hurricanes?",
      options: ["Yes", "No"],
      answer: "Yes"
    },
    {
      question: "tornados that form over water are called...",
      options: ["Water we we", "bro thats hurricanes!", "Come On!", "Waterspouts"],
      answer: "Waterspouts"
    },
    {
      question: "Is dangerous weather dangerous?",
      options: ["Yes", "No"],
      answer: "Yes"
    },
  ];
  
  const questionElement = document.getElementById("question");
  const optionsElement = document.getElementById("options");
  const submitButton = document.getElementById("submit");
  var restart = document.getElementById("restart");

     var onButtonClick = function() {
        location.reload();
      }

      restart.addEventListener("click", onButtonClick);

  let currentQuestion = 0;
  let score = 0;
  
  function showQuestion() {
    const question = quizData[currentQuestion];
    questionElement.innerText = question.question;
  
    optionsElement.innerHTML = "";
    question.options.forEach(option => {
      const button = document.createElement("button");
      button.innerText = option;
      optionsElement.appendChild(button);
      button.addEventListener("click", selectAnswer);
    });
  }
  
  function selectAnswer(e) {
    const selectedButton = e.target;
    const answer = quizData[currentQuestion].answer;
  
    if (selectedButton.innerText === answer) {
      score++;
      
    }
  
    currentQuestion++;
  
    if (currentQuestion < quizData.length) {
      showQuestion();
    } else {
      showResult();
    }
  }
  
  function showResult() {
    quiz.innerHTML = `
      <h1>Quiz Completed!</h1>
      <p>Your score: ${score}/${quizData.length}</p>
      <button id="restart"> Restart </button>



      <a href="https://raskattack.github.io">
        <button id="home">Go home</button>
      </a>
      
    `;
        var restart = document.getElementById("restart");

     var onButtonClick = function() {
        location.reload();

         
      }

      restart.addEventListener("click", onButtonClick);

      
      
  }
  
  showQuestion();

 
