document.addEventListener("DOMContentLoaded",

    function(e) {
        

        const RoomNameInput = document.querySelector('input[name="request_room_alias"]');
        const RoomIdInput = document.querySelector('input[name="request_room_name"]');
        const form = document.getElementById('box');
        const RoomNameErrorDiv = createErrorDiv('RoomNameError');
        const RoomIdErrorDiv = createErrorDiv('RoomIdError');

        RoomNameInput.addEventListener('input', () => validateInput(RoomNameInput, RoomNameErrorDiv, /^[a-zA-Z가-힣0-9]{1,5}$/, "유효한 방 이름을 입력해주세요 (5자 이하의 한국어, 숫자)"));
        
        RoomIdInput.addEventListener('input', () => validateInput(RoomIdInput, RoomIdErrorDiv, /^[a-zA-Z0-9]{1,16}$/, "유효한 방 아이디를 입력해주세요 (16자 이하의 영문, 숫자)"));

        form.addEventListener('submit', function(event) {
            const isRoomNameValid = validateInput(RoomNameInput, RoomNameErrorDiv, /^[a-zA-Z가-힣0-9]{1,5}$/, "유효한 방 이름을 입력해주세요 (5자 이하의 한국어, 숫자)");
            const isRoomIdValid = validateInput(RoomIdInput, RoomIdErrorDiv, /^[a-zA-Z0-9]{1,16}$/, "유효한 방 아이디를 입력해주세요 (16자 이하의 영문, 숫자)");

            if (!isRoomNameValid || !isRoomIdValid) {
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