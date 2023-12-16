document.addEventListener("DOMContentLoaded",

    function(e) {
        
        const deleteLink = document.getElementById("delete");

            deleteLink.addEventListener("click", function(e) {
                e.preventDefault();

                const confirmation = confirm("진짜로 방을 삭제하시겠습니까?");

                if (confirmation) {

                    window.location.href = "삭제하려는 실제 URL";
                }
            });



    }
)