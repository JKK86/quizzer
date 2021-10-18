document.addEventListener("DOMContentLoaded", function () {

    (function () {
        /**
         * AJAX to get the questions and answers for the quiz
         */
        let startButton = $("#start-quiz");
        let quizContent = document.querySelector("#quiz-content");

        function showQuestions(data) {
            const questions = data.questions;
            questions.forEach((el, i) => {
                for (const [question, answers] of Object.entries(el)) {
                    quizContent.innerHTML += `
                        <hr>
                        <div class="question">
                        <b>${i + 1}. ${question}</b>
                        </div>
                    `;
                    answers.forEach(answer => {
                        quizContent.innerHTML += `
                                <div>
                                <input type="radio" 
                                class="answer" 
                                name="${question}" 
                                id="${question}-${answer}" 
                                value="${answer}">
                                <label for="${question}-${answer}">${answer}</label>
                                </div>
                                `;
                    });
                }
            });
        }

        startButton.on("click", evt => {
            const url = window.location.href;
            $.ajax({
                url: `${url}data`,
                method: "GET",
                success: showQuestions,
                error: function (error) {
                    console.log(error);
                }
            });
        })

        /**
         * Set quiz timer and start countdown
         */

        let timerDisplay = $("#quiz-time-left");
        let timeLeft = timerDisplay.text();

        function countDown() {

            timerDisplay.parent().show();
            setInterval(function () {
                if (timeLeft <= 0) {
                    clearInterval(timeLeft = 0);
                }
                if (timeLeft === 0) {
                    $(".answer").attr("disabled", true);
                }
                timeLeft--;
                timerDisplay.text(timeLeft);
            }, 1000);
        }

        startButton.on("click", evt => {
            if (timeLeft) {
                countDown();
            }
        });

        /**
         * Hide start button and show submit button
         */

        startButton.on("click", evt => {
            startButton.hide();
            $('#button-submit').show();
        })

    })()
});
