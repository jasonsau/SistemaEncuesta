const selectTypeOptions = document.querySelector('#type_question');
const addQuestionButton = document.querySelector('#add_question');
const numberOptions = document.querySelector('#number_options');
const questions = document.querySelector('#questions');
const titleQuestion = document.querySelector('#question');
const namePoll = document.querySelector('#name_poll');
const objectivePoll = document.querySelector('#objetive_poll');
const instructionsPoll = document.querySelector('#instructions_poll');
const dateStartPoll = document.querySelector('#date_start_poll');
const dateEndPoll = document.querySelector('#date_end_poll');
const limitSamplePoll = document.querySelector('#limit_sample_poll');
const savePoll = document.querySelector('#save-poll');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]');
const messageAlert = document.querySelector('#message_alert');
const toast = document.querySelector('#toast');


let options = '';
let templateHtml = '';
let idQuestions = '';
let nameQuestion = '';
let jsonPoll = {};
jsonPoll.general = {
    name_poll: "",
    objective_poll: "",
    instructions_poll: "",
    date_start_poll: "",
    date_end_poll: "",
    limit_sample_poll: 0,
}
jsonPoll.questions = [];

savePoll.addEventListener('click', (e) => {
    savePollRequest();
})
namePoll.addEventListener('input', (e) => {
    console.log(namePoll.value)
    jsonPoll.general.name_poll = e.target.value;
    localStorage.setItem('poll', JSON.stringify(jsonPoll));
});

objectivePoll.addEventListener('input', (e) => {
    jsonPoll.general.objective_poll = e.target.value;
    localStorage.setItem('poll', JSON.stringify(jsonPoll));
});

instructionsPoll.addEventListener('input', (e) => {
    jsonPoll.general.instructions_poll = e.target.value;
    localStorage.setItem('poll', JSON.stringify(jsonPoll));
});

dateStartPoll.addEventListener('input', (e) => {
    jsonPoll.general.date_start_poll = e.target.value;
    localStorage.setItem('poll', JSON.stringify(jsonPoll));
});

dateEndPoll.addEventListener('input', () => {
    jsonPoll.general.date_end_poll = dateEndPoll.value;
    localStorage.setItem('poll', JSON.stringify(jsonPoll));
});

limitSamplePoll.addEventListener('input', () => {
    jsonPoll.general.limit_sample_poll = parseInt(limitSamplePoll.value);
    localStorage.setItem('poll', JSON.stringify(jsonPoll));
});




let typeQuestion = '';
fetch('/get-type-questions')
    .then(response => response.json())
    .then(response => {
        if(response.status === 'Success') {
            console.log(response)
            const data = response.data;
            data.forEach(typeQuestion => {
                const option = document.createElement('option');
                option.value = typeQuestion.id_type_question;
                option.textContent = typeQuestion.name_type_question;
                selectTypeOptions.appendChild(option);
            })
        }
        typeQuestion = selectTypeOptions.value;
    })
    .catch(error => {
        console.log(error)
    })

selectTypeOptions.addEventListener('change', () => {
    typeQuestion = selectTypeOptions.value;
    if(typeQuestion !== '1') {
        document.querySelector('#id_options').style.display = 'block';
    } else {
        document.querySelector('#id_options').style.display = 'none';
    }
});

addQuestionButton.addEventListener('click', () => {
    options = numberOptions.value;
    templateHtml = returnTemplateHtml(typeQuestion, options.split(','), titleQuestion.value);
    questions.innerHTML += templateHtml;
    typeQuestion = selectTypeOptions.value;
    numberOptions.value = '';
    titleQuestion.value = '';
    localStorage.setItem('poll', JSON.stringify(jsonPoll));
});

function returnTemplateHtml(typeQuestion, optionsQuestion, title) {
    let titleQuestion = `
                <div class = "title__question">
                <h3 class = "h5">${title}</h3>
                </div>
            `
    nameQuestion = getInitialsLetterQuestions(title);
    let options = '';
    let q = {
        title_question: title,
        type_question: typeQuestion,
    }
    q.options = [];

    if(typeQuestion === '1') {
        idQuestions = generateUniqueIdRandom(title);
        options = `
                    <div>
                        <input type = "text" id = "${idQuestions}" placeholder = "Escribe tu respuesta aqui" name = "${nameQuestion}" class = "form-control">
                    </div>
                `
        q.options.push({
            "title_option": "",
            "name_option": nameQuestion,
            "value_option": "",
            "id_question": idQuestions,
        });

    } else if(typeQuestion === '2') {
        for(let i = 0; i < optionsQuestion.length; i++) {
            idQuestions = generateUniqueIdRandom(optionsQuestion[i]);
            options += `
                        <div class = "form-check">
                            <input type = "checkbox" id = "${idQuestions}" name = "${nameQuestion}" class = "form-check-input"/>
                            <label for="${idQuestions}" class = "form-check-label">${optionsQuestion[i]}</label>
                        </div>
                    `
            q.options.push({
                "title_option": optionsQuestion[i],
                "name_option": nameQuestion,
                "value_option": "false",
                "id_question": idQuestions,
            });

        }
    } else if(typeQuestion === '3') {
        options = '';
        for(let i = 0; i < optionsQuestion.length; i++) {
            idQuestions = generateUniqueIdRandom(optionsQuestion[i]);
            options += `
                        <div class = "form-check">
                            <input type = "radio" id = "${idQuestions}" name = "${nameQuestion}" class = "form-check-input"/>
                            <label for = "${idQuestions}" class = "form-check-label">${optionsQuestion[i]}</label>
                        </div>
                    `;
            q.options.push({
                "title_option": optionsQuestion[i],
                "name_option": nameQuestion,
                "value_option": "false",
                "id_question": idQuestions,
            });
        }
    } else {
        return ``;
    }
    jsonPoll.questions.push(q);
    console.log(jsonPoll);
    return `<div class = "mt-3 mb-3">${titleQuestion}${options}</div>`;
}

function generateUniqueIdRandom(option) {
    option = option.trim();
    option = option.replaceAll(' ', '');
    console.log(option)
    return option + Math.random().toString(36).substring(2, 9);
}

function getInitialsLetterQuestions(titleQuestion) {
    let initials = '';
    let words = titleQuestion.split(' ');
    for(let i = 0; i < words.length; i++) {
        initials += words[i].charAt(0);
    }
    return initials + Math.random().toString(36).substring(2, 9);
}

function savePollRequest() {
    console.log(csrftoken.value);
    fetch('/save-poll', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken.value,
        },
        mode: 'same-origin',
        body: JSON.stringify(jsonPoll)
    })
        .then(response => response.json())
        .then(data => {
            messageAlert.innerHTML = data.message;
            toast.classList.add('show');
            if(data.status === 'error') {
                if(data.errors) {
                    toast.classList.remove('text-bg-success');
                    toast.classList.add('text-bg-danger');
                    const errors = data.errors;
                    errors.forEach(error => {
                        if(error[error.field].length > 0) {
                            if(error.field === 'questions') {
                                document.querySelector('#question_error').innerHTML = error['questions'][0];
                                document.querySelector('#question_error').style.display = 'block';
                            }
                            document.querySelector(`#${error.field}`).classList.add('is-invalid');
                            document.querySelector(`#${error.field}_error`).innerHTML = error[error.field][0];
                        } else {
                            document.querySelector(`#${error.field}`).classList.remove('is-invalid');
                            document.querySelector(`#${error.field}_error`).innerHTML = ''
                            if(error.field === 'questions') {
                                document.querySelector('#question_error').style.display = 'none';
                            }
                        }
                    });
                }
            }
            if(data.status === 'Succes') {
                toast.classList.remove('text-bg-danger');
                toast.classList.add('text-bg-success');
                savePoll.style.disabled = true;
                setTimeout(() => {
                    window.location.href = '/home';
                }, 2000)
            }
        })
        .catch(error => console.log(error))
        .finally(() => {
            setTimeout(() => {
                toast.classList.remove('show');
            }, 2000)
        })

}
