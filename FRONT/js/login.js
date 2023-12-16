document.addEventListener("DOMContentLoaded",

    function(e) {
        

        const usernameInput = document.querySelector('input[name="username"]');
        const passwordInput = document.querySelector('input[name="password"]');
        const form = document.getElementById('box');
        const usernameErrorDiv = createErrorDiv('usernameError');
        const passwordErrorDiv = createErrorDiv('passwordError');

        usernameInput.addEventListener('input', () => validateInput(usernameInput, usernameErrorDiv, /^[a-zA-Z0-9]{8,}$/, "유효한 사용자 이름을 입력해주세요"));
        passwordInput.addEventListener('input', () => validateInput(passwordInput, passwordErrorDiv, /^[a-zA-Z0-9!@#$%^&*()_+]{8,}$/, "유효한 비밀번호를 입력해주세요"));

        form.addEventListener('submit', function(event) {
            const isUsernameValid = validateInput(usernameInput, usernameErrorDiv, /^[a-zA-Z0-9]{8,}$/, "유효한 사용자 이름을 입력해주세요");
            const isPasswordValid = validateInput(passwordInput, passwordErrorDiv, /^[a-zA-Z0-9!@#$%^&*()_+]{8,}$/, "유효한 비밀번호를 입력해주세요");
    
            if (!isUsernameValid || !isPasswordValid) {
                event.preventDefault();
            }
        });

        function validateInput(inputElement, errorDiv, regex, errorMessage) {
            if (!regex.test(inputElement.value)) {
                errorDiv.textContent = errorMessage;
                if (!document.getElementById(errorDiv.id)) {
                    inputElement.after(errorDiv);
                }
                return false;
            } else {
                errorDiv.textContent = '';
                return true;
            }
        }

        function createErrorDiv(id) {
            const div = document.createElement('div');
            div.id = id;
            div.style.color = 'red';
            div.style.margin = '5px';
            return div;
        }


    }
)