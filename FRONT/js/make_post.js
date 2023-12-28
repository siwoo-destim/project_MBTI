document.addEventListener('DOMContentLoaded', function () {
    var imageInput = document.getElementById("image-upload");
    var previewImage = document.getElementById("previewImage");

    imageInput.addEventListener("change", function () {
        var file = imageInput.files[0];

        if (file) {
            var reader = new FileReader();

            reader.onload = function (e) {
                previewImage.src = e.target.result;
                previewImage.style.display = "block";
            };

            reader.readAsDataURL(file);
        }
    });

    const MbtiNameInput = document.querySelector('input[name="request_mbti_name"]');
    const form = document.getElementById('box');
    const MbtiNameErrorDiv = createErrorDiv('MbtiNameError');


    MbtiNameInput.addEventListener('input', () => validateInput(MbtiNameInput, MbtiNameErrorDiv, /^[a-zA-Z가-힣ㄱ-ㅎㅏ-ㅣ0-9]{1,16}$/, "유효한 이름을 입력해주세요 (16자 이하의 한국어, 영어, 숫자)"));

    form.addEventListener('submit', function(event) {
        const isNameValid = validateInput(MbtiNameInput, MbtiNameErrorDiv, /^[a-zA-Z가-힣ㄱ-ㅎㅏ-ㅣ0-9]{1,16}$/, "유효한 이름을 입력해주세요 (16자 이하의 한국어, 영어, 숫자)");

        // 이미지 업로드 여부 확인
        if (!imageInput.files.length) {
            event.preventDefault(); // 폼 제출 중단
            if (confirm("사진을 찍지 않겠습니까?")) {
                // 사용자가 확인을 눌렀을 때만 폼을 다시 제출
                imageInput.required = true;
                form.submit();
            }
        } else if (!isNameValid) {
            // 이름 입력 검증이 실패했을 경우 폼 제출 중단
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
});
