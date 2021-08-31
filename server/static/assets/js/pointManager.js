$(document).ready(()=>{
    $("button").on("click", (event)=>{
        id = $(event.target).parent()[0].id;
        username = id.split("_")[0];
        action   = id.split("_")[1];
        if(action === "addPoint" || action === "reducePoint"){
            formData = new FormData();
            formData.append("username", username)
            $.ajax({
                'url': location.origin + "/pointManage/" + action,
                'method': 'POST',
                'processData': false,
                'contentType': false,
                'data': formData,
                'headers': {'X-CSRFToken': getCookie('csrftoken')},
                'success': (res) => {
                    $("#" + username + "_point").html(res);
                },
                'error': (res) => {
                    $("#" + username + "_point").html(res);
                }
            });

        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
