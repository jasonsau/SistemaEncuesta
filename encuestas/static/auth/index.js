const buttonOpenModal = document.getElementById('button_open_modal');
const modalRegister = document.getElementById('modal_register');
const btnCloseModal = document.querySelectorAll('.btn-close');
const btnRegisterUser = document.getElementById('btn_register_user');
const namePerson = document.getElementById('name_person');
const birthDatePerson = document.getElementById('birth_date_person');
const genrePerson = document.getElementById('genre_person');
const emailPerson = document.getElementById('email_person');
const registerPassword = document.getElementById('register_password');
const confirmPassword = document.getElementById('confirm_password');
let dataJsonRegister = {};
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]');
const messageAlert = document.querySelector('#message_alert');
const toast = document.querySelector('#toast');
const btnLogin = document.querySelector('#btn_login');
const email = document.querySelector('#email');
const password = document.querySelector('#password');

btnLogin.addEventListener('click', (event) => {
    event.preventDefault();
    dataJsonLogin = {
        'email': email.value,
        'password': password.value,
    }
    fetch('/login-post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken.value,
        },
        body: JSON.stringify(dataJsonLogin),
    })
        .then((response) => response.json())
        .then((data) => {
            toast.classList.add('text-bg-success');
            messageAlert.innerHTML = data.message;
            toast.classList.add('show');
            if (data.status === 'success') {
                btnLogin.style.disabled = true;
                setTimeout(() => {
                    window.location.href = '/home';
                }, 1500);
            } else {
                toast.classList.add('text-bg-danger');
            }
        })
        .catch((error) => {
            console.log(error);
        })
        .finally(() => {
            setTimeout(() => {
                toast.classList.remove('show');
            }, 1000);
        });
});


btnCloseModal.forEach((btn) => {
    btn.addEventListener('click', (event) => {
        event.preventDefault();
        modalRegister.classList.remove('fade', 'show');
        modalRegister.style.display = 'none';
    });
});

buttonOpenModal.addEventListener('click', (event) => {
    event.preventDefault();
    modalRegister.classList.add('fade', 'show');
    modalRegister.style.display = 'block';
});

btnRegisterUser.addEventListener('click', (event) => {
    event.preventDefault();
    dataJsonRegister = {
        'person': {
            'name_person': namePerson.value,
            'birth_date_person': birthDatePerson.value,
            'genre_person': genrePerson.value,
            'email_person': emailPerson.value,
        },
        'user': {
            'password_user': registerPassword.value,
            'confirm_password': confirmPassword.value,
            'username_user': emailPerson.value,
        }
    };
    console.log(dataJsonRegister);
    fetch('/register-user', {
        method: 'POST',
        body: JSON.stringify(dataJsonRegister),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken.value,
        }
    })
        .then(response => response.json())
        .then(data => {
            messageAlert.innerHTML = data.message;
            toast.classList.add('show');
            if(data.status === 'error'){
                if(data.errors) {
                    const errors = data.errors;
                    errors.forEach(error => {
                        if(error[error.field].length > 0) {
                            document.querySelector(`#${error.field}`).classList.add('is-invalid');
                            document.querySelector(`#${error.field}_error`).innerHTML = error[error.field][0];
                        }else {
                            document.querySelector(`#${error.field}`).classList.remove('is-invalid');
                            document.querySelector(`#${error.field}_error`).innerHTML = '';
                        }
                    })
                    toast.classList.add('text-bg-danger');
                    toast.classList.remove('text-bg-success');
                } else {
                    clearErrors();
                }
            }else {
                toast.classList.remove('text-bg-danger');
                toast.classList.add('text-bg-success');
                modalRegister.classList.remove('fade', 'show');
                modalRegister.style.display = 'none';
                cleanCamps()
                clearErrors()
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        })
        .finally(() => {
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);

        });
});

function clearErrors() {
    const errors = document.querySelectorAll('.is-invalid');
    errors.forEach(error => {
        error.classList.remove('is-invalid');
    });
}

function cleanCamps() {
    const camps = document.querySelectorAll('.form-control');
    camps.forEach(camp => {
        camp.value = '';
    });
}
