const objetivePoll = document.querySelector('#objetive_poll');
const instructionsPoll = document.querySelector('#instructions_poll');
const titlePoll = document.querySelector('#title_poll');
const titlePollH1 = document.querySelector('#title_poll_h1');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]');
const questions = document.querySelector('#questions');
let tokenPoll = '';
let options = '';

function getDataPoll() {
    tokenPoll = new URL(window.location.href).pathname.split('/')[2];
    console.log(tokenPoll)
    fetch(`/get-data-poll/${tokenPoll}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrftoken.value
        }
    })
        .then(response => response.json())
        .then(data => {
            titlePoll.textContent = data.general.name_poll;
            titlePollH1.textContent = data.general.name_poll;
            objetivePoll.textContent = data.general.objective_poll;
            instructionsPoll.textContent = data.general.instructions_poll;

            console.log("******************8")
            console.log(questions);
            data.questions.forEach(question => {
                questions.innerHTML += returnHtmlTemplate(question.type_question, question.options, question.title_question);
            });
            console.log(data)
        })
        .catch(error => console.log(error))
}

function returnHtmlTemplate(typeQuestion, optionsQuestion, title) {
    console.log("Entra a una funcion")
    console.log(typeQuestion)
    console.log(optionsQuestion)
    options = '';
    let titleQuestion = `<div class = "title_question"><h3 class = "h5">${title}</h3></div>`;
    console.log("titulo de la question")
    console.log(titleQuestion)
    if(typeQuestion === 1) {
        options = `<div><input type = "text" class = "form-control" id = "${optionsQuestion[0].id_question}" name="${optionsQuestion[0].name_option}"></div>`;
    } else if(typeQuestion === 3) {
        for(let i = 0; i < optionsQuestion.length; i++) {
            options += `<div class = "form-check"><input type = "radio" class = "form-check-input" id = "${optionsQuestion[i].id_question}" name="${optionsQuestion[i].name_option}" value = "${optionsQuestion[i].value_option}"><label for = "${optionsQuestion[i].id_question}" class = "form-check-label">${optionsQuestion[i].title_option}</label></div>`;
        }
    } else if(typeQuestion === 2) {
        for(let i = 0; i < optionsQuestion.length; i++) {
            options += `<div class = "form-check"><input type = "checkbox" class = "form-check-input" id = "${optionsQuestion[i].id_question}" name="${optionsQuestion[i].name_option}" value = "${optionsQuestion[i].value_option}"><label for = "${optionsQuestion[i].id_question}" class = "form-check-label">${optionsQuestion[i].title_option}</label></div>`;
        }
    } else {
        return '';
    }
    return `<div class = "mt-3 mb-3">${titleQuestion}${options}</div>`
}

getDataPoll()
