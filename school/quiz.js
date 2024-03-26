const quizData = [
    {
      question: "47/29 - 1/29",
      options: ["46/29", "66/93", "48/29", "47/28"],
      answer: "46/29"
    },
    {
      question: "7 / 66/12",
      options: ["462/84", "100/782", "84/462", "782/100"],
      answer: "84/462"
    },
    {
      question: "123+4-5+67-89 = ?",
      options: ["100", "105", "101", "99"],
      answer: "100"
    },
    {
      question: "8 * 44/99",
      options: ["777/1723", "5278/754", "2845/88", "3520/99"],
      answer: "3520/99"
    },
    {
      question: "If 1=3, 2=3, 3=5, 4=4, and 5=4, what is 6=?",
      options: ["-3", "9", "3", "4.6"],
      answer: "3"
    },
    {
      question: "4032 * 445/325",
      options: ["845270984375/234857092834", "009807774/72745", "338778/342", "1794240/1310400"],
      answer: "1794240/1310400"
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

 
