document.addEventListener("DOMContentLoaded", 

    function(e) {

        const usernameInput = document.querySelector('input[name="username"]');
        const passwordInput = document.querySelector('input[name="password"]');
        const confirmPasswordInput = document.querySelector('input[name="Confirm_Password"]');
        const form = document.getElementById('box');
        const usernameErrorDiv = createErrorDiv('usernameError');
        const passwordErrorDiv = createErrorDiv('passwordError');
        const confirmPasswordErrorDiv = createErrorDiv('confirmPasswordError');

        usernameInput.addEventListener('input', () => validateInput(usernameInput, usernameErrorDiv, /^[a-zA-Z0-9]{8,}$/, "유효한 사용자 아이디를 입력해주세요(8자 이상의 영문과 특수문자만)"));
        passwordInput.addEventListener('input', () => validateInput(passwordInput, passwordErrorDiv, /^[a-zA-Z0-9!@#$%^&*()_+]{8,}$/, "유효한 비밀번호를 입력해주세요(8자 이상의 영문, 특수문자, 숫자)"));
        confirmPasswordInput.addEventListener('input', () => matchPasswords(passwordInput, confirmPasswordInput, confirmPasswordErrorDiv, "비밀번호가 일치하지 않습니다"));

        form.addEventListener('submit', function(event) {
            const isUsernameValid = validateInput(usernameInput, usernameErrorDiv, /^[a-zA-Z0-9]{8,}$/, "유효한 사용자 아이디를 입력해주세요(8자 이상의 영문과 특수문자만)");
            const isPasswordValid = validateInput(passwordInput, passwordErrorDiv, /^[a-zA-Z0-9!@#$%^&*()_+]{8,}$/, "유효한 비밀번호를 입력해주세요(8자 이상의 영문, 특수문자, 숫자)");
            const arePasswordsMatching = matchPasswords(passwordInput, confirmPasswordInput, confirmPasswordErrorDiv, "비밀번호가 일치하지 않습니다");

            if (!isUsernameValid || !isPasswordValid || !arePasswordsMatching) {
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

        function matchPasswords(passwordInput, confirmPasswordInput, errorDiv, errorMessage) {
            if (passwordInput.value !== confirmPasswordInput.value) {
                errorDiv.textContent = errorMessage;
                if (!document.getElementById(errorDiv.id)) {
                    confirmPasswordInput.after(errorDiv);
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