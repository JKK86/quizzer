document.addEventListener("DOMContentLoaded", function () {

    (function () {
        /**
         * AJAX - get the questions and answers for the quiz
         */
        let startButton = $("#start-quiz");
        let quizContent = document.querySelector("#quiz-content");

        function slugify(text) {
            return text
                .toLowerCase()
                .replace(/ /g, '-')
                .replace(/[^\w-]+/g, '');
        }


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
                                id="${slugify(question)}-${slugify(answer)}" 
                                value="${answer}">
                                <label for="${slugify(question)}-${slugify(answer)}">${answer}</label>
                                </div>
                                `;
                    });
                }
            });
        }

        const url = window.location.href;

        startButton.on("click", evt => {
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

        let buttonSubmit = $('#button-submit')

        startButton.on("click", evt => {
            startButton.hide();
            buttonSubmit.show();
        })

        /**
         * Ajax - send results to the server
         */

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const csrftoken = getCookie('csrftoken');

        function prepareData() {
            const data = {};
            const answers = $(".answer");
            answers.each(function(index, el) {
                let that = $(el)
                if (that.is (':checked')) {
                    data[that.attr('name')] = that.attr('value');
                } else {
                    if (!data[that.attr(name)]) {
                        data[that.attr(name)] = null;
                    }
                }
            })
            return data;
        }

        const quizResults = $('#quiz-results')

        function showResults(data) {
            const results = data.results;
            const score = data.score;
            const total_score = $('#total-score')

            total_score.text(score)
            total_score.parent().show()

            results.forEach(el => {
                for (const [question, ans] of Object.entries(el)) {

                    const selected = ans["selected_answer"]
                    const correct = ans["correct_answer"]
                    console.log(selected);
                    console.log(correct);

                    const selectedAnswer =
                        (selected === "Brak odpowiedzi") ? null : $(`#${slugify(question)}-${slugify(selected)}`)
                    const correctAnswer = $(`#${slugify(question)}-${slugify(correct)}`)

                    if (selected === correct) {
                        selectedAnswer.parent().addClass("success")
                    } else if (selected === 'Brak odpowiedzi') {
                        correctAnswer.parent().addClass("info")
                    } else {
                        selectedAnswer.parent().addClass("mistake")
                        correctAnswer.parent().addClass("info")
                    }
                }
            });
        }

        buttonSubmit.on("click", evt => {
            evt.preventDefault()

            const data = prepareData();

            timerDisplay.parent().hide();
            timeLeft = 0;

            const csrftoken = getCookie('csrftoken');

            $(".answer").attr("disabled", true);

            $.ajax({
                url: `${url}save`,
                method: "POST",
                data: data,
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                success: showResults,
                error: function (error) {
                    console.log(error);
                }
            });
        });

    })();
});
