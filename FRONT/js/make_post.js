document.addEventListener('DOMContentLoaded', function () {
    const videoContainer = document.getElementById('video-container');
    const video = document.getElementById('video');
    const takePicBtn = document.getElementById('take_pic');
    const capturedPhoto = document.getElementById('captured-photo');
    const captureBtn = document.getElementById('capture-btn');
    const imageUploadInput = document.getElementById('image-upload');
    const uploadLabel = document.getElementById('upload-label');

    let isFileUploadHandled = false;

    // "사진 찍기" 버튼 클릭 이벤트 처리
    takePicBtn.addEventListener('click', async function (event) {
        // 이벤트의 기본 동작 중지
        event.preventDefault();

        try {
            // 비디오 스트림 가져오기
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });

            // 비디오 요소에 스트림 설정
            video.srcObject = stream;

            // 비디오 컨테이너를 보이도록 설정
            videoContainer.style.display = 'block';
        } catch (error) {
            console.error('카메라 액세스 오류:', error);
        }
    });

    // "사진 찍기" 버튼 클릭 시 이미지 캡처 및 표시
    captureBtn.addEventListener('click', function (event) {
        // 이벤트의 기본 동작 중지
        event.preventDefault();

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // 캡처된 이미지를 이미지 요소에 표시
        capturedPhoto.src = canvas.toDataURL('image/png');

        // 비디오 스트림 중지
        video.srcObject.getTracks().forEach(track => track.stop());

        // 비디오 컨테이너를 숨기도록 설정
        videoContainer.style.display = 'none';

        // Blob으로 변환
        canvas.toBlob(function (blob) {
            // Blob으로부터 File 객체 생성
            const file = new File([blob], 'captured_image.png', { type: 'image/png' });

            // 파일 업로드 input에 파일 추가
            imageUploadInput.files = [file];
        }, 'image/png');
    });

    // 이미지 업로드 처리
    imageUploadInput.addEventListener('change', function () {
        if (!isFileUploadHandled) {
            const file = imageUploadInput.files[0];
            if (file) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    // 업로드된 이미지를 이미지 요소에 표시
                    capturedPhoto.src = e.target.result;
                };

                reader.readAsDataURL(file);

                // 이미지 업로드가 발생할 때마다 플래그 초기화
                isFileUploadHandled = true;
                imageUploadInput.value = ''; // 파일 선택 초기화
            }
        }
    });
});