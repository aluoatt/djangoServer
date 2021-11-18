$(document).ready(()=>{
    $(".button_reportArticle").on("click", (e)=>{
        id = $(e.target)[0].id;
        articleID = id.split("_")[1];
        actionTarget = id.split("_")[0];

        formInput=""
        formInput = $("<form>", { id: "article_report" });

        pointDiv = $("<div>", { class: "form-group" });
        pointDiv.append($("<label>", { text: "回報原因", class: "form-check-label", for: "reason"}));
        pointDiv.append($("<textarea>", { type: "text", name: "reason", class: "form-control", id: "reason"}));
        formInput.append(pointDiv);

        bootbox.confirm({
            closeButton: false,
            backdrop: true,
            scrollable: true,
            title: "提醒:請詳細回報原因!!!",
            message: formInput,
            locale: "zh_TW",
            container: "body",
            className:"modal-dialog-centered",
            centerVertical: true,
            callback: (res) => {
                if (!res)
                    return;
                formData = new FormData($("#article_report")[0]);
                formData.append("articleID", articleID);
                reason = formData.get("reason")
                if(reason === ""){
                    bootbox.alert({
                        closeButton: false,
                        message: "請確實填寫回報原因喔!",
                        locale: "zh_TW",
                        centerVertical: true,
                    });
                    return;
                }
                $.ajax({
                    'url': location.origin + "/managerPages/reportArticle",
                    'method': 'POST',
                    'processData': false,
                    'contentType': false,
                    'data': formData,
                    'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                    'success': (res) => {
                        bootbox.alert({
                            closeButton: false,
                            message: "成功",
                            locale: "zh_TW",
                            centerVertical: true,
                        });
                    },
                    'error': (res) => {
                        alert("此功能異常,請聯繫系統人員");
                    }
                });
            }
        });
    })

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