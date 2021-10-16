document.addEventListener("DOMContentLoaded", function () {

    (function () {
        /**
         * AJAX to get the questions and answers for the quiz
         */
        let startButton = document.querySelector("#start-quiz");
        let quizContent = document.querySelector("#quiz-content");

        startButton.addEventListener("click", evt => {
            const url = window.location.href
            $.ajax({
                url: `${url}data`,
                method: "GET",
                success: function (data) {
                    const questions = data.questions
                    questions.forEach((el, i) => {
                        for (const [question, answers] of Object.entries(el)) {
                            quizContent.innerHTML += `
                        <hr>
                        <div class="question">
                        <b>${i+1}. ${question}</b>
                        </div>
                    `
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
                                `
                            })
                        }
                    })
                },
                error: function (error) {
                    console.log(error)
                }
            })
        })
    })()

});