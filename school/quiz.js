const quizData = [
    {
      question: "What is 7 * 66/12?",
      options: ["38 1/2", "79", "11 1/8", "7 11/15"],
      answer: "38 1/2"
    },
    {
      question: "What is the highest common factor of the numbers 30 and 132?",
      options: ["2.6", "8", "4.9", "6"],
      answer: "6"
    },
    {
      question: "123+4-5+67-89 = ?",
      options: ["100", "105", "101", "99"],
      answer: "100"
    },
    {
      question: "From the number 0 to the number 1000, the letter “A” appears only in?",
      options: ["100", "3000", "1000", "1050"],
      answer: "1000"
    },
    {
      question: "If 1=3, 2=3, 3=5, 4=4, and 5=4, what is 6=?",
      options: ["-3", "9", "3", "4.6"],
      answer: "3"
    },
    {
      question: "Which number is the equivalent to 3^(4)/3^(2)?",
      options: ["-3", "9", "3.3", "4"],
      answer: "9"
    },
    {
      question: "Using only the process of addition, how to add eight 8’s to get the final number of 1000?",
      options: ["8=1000", "8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8+8=1000", "8888+88+8+88+88=1000", "888+88+8+8+8=1000"],
      answer: "888+88+8+8+8=1000"
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
    `;
        var restart = document.getElementById("restart");

     var onButtonClick = function() {
        location.reload();
      }

      restart.addEventListener("click", onButtonClick);
      
      
  }
  
  showQuestion();

 
