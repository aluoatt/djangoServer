$(document).ready(() => {
    $(".button_modified").on("click", (event) => {

        id = $(event.target).parent()[0].id;
        username = id.split("_")[0];
        user = $("#" + username +"_user").html();
        action = id.split("_")[1];
        if (action === "addPoint" || action === "reducePoint") {
            msg=""
            if(action === "addPoint")
                msg = "將為\"" + user + "\"增加 10 點"
            else if(action === "reducePoint")
                msg = "將為\"" + user + "\"減少 1 點"

            bootbox.confirm({
                closeButton: false,
                backdrop: true,
                scrollable: true,
                title: "提醒",
                message: msg,
                locale: "zh_TW",
                container: "body",
                centerVertical: true,
                callback: (res) => {
                    if (!res)
                        return;
                    formData = new FormData();
                    formData.append("username", username)
                    $.ajax({
                        'url': location.origin + "/pointManage/" + action,
                        'method': 'POST',
                        'processData': false,
                        'contentType': false,
                        'data': formData,
                        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                        'success': (res) => {
                            $("#" + username + "_point").html(res);
                            bootbox.alert({
                                closeButton: false,
                                message: "成功",
                                locale: "zh_TW",
                                centerVertical: true,
                            });
                        },
                        'error': (res) => {
                            alert("伺服器出狀況,請聯繫系統人員");
                        }
                    });
                }
            });
        }
    });

    var t = $('#example').DataTable({
        "orderClasses": false,
        "responsive": true,
        "language": {
            url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
        },
        "createdRow": function (row, data, dataIndex) {
            $(row).addClass('table-warning');
            $(row).addClass('text-dark');
            $(row).addClass('font-weight-bold');
        }
    });

    $(".button_history").on("click", (event) => {
        var counter = 1;
        t.clear()
        $(".dataTables_empty").addClass("table-warning text-dark font-weight-bold");
        $(".dataTables_empty").text("目前沒有紀錄");
        id = $(event.target).parent()[0].id;
        username = id.split("_")[0];
        action = id.split("_")[1];
        formData = new FormData();
        formData.append("username", username)
        $.ajax({
            'url': location.origin + "/pointManage/" + action,
            'method': 'POST',
            'processData': false,
            'contentType': false,
            'data': formData,
            'headers': { 'X-CSRFToken': getCookie('csrftoken') },
            'success': (res) => {
                data = JSON.parse(res)
                for (i in data) {
                    fields = data[i]['fields']
                    t.row.add([
                        fields['modifier'],
                        fields['recordDate'],
                        fields['addPoint'],
                        fields['reducePoint'],
                        fields['transferPoint'],
                        fields['reason'],
                        fields['resultPoint'],
                    ]).draw(false);
                }
            },
            'error': (res) => {
                alert("伺服器出狀況,請聯繫系統人員")
            }
        });

    });

    $(".addPointByOption").on("click", (event) => {
        id = $(event.target)[0].id;
        if (id === "addPointByAll" || id === "addPointByJobTitle" || id === "addPointByAmwayAward") {
            action = id;
            formInput = "";
            formInput = $("<form>", { id: "addPointForm" });
            pointDiv = $("<div>", { class: "form-group" });
            pointDiv.append($("<label>", { text: "點數" }));
            pointDiv.append($("<input>", { type: "number", name: "point", class: "form-control", placeholder: "Enter email" }));
            formInput.append(pointDiv);
            if (action === "addPointByAll") {

            } else if (action === "addPointByJobTitle") {
                pointDiv = $("<div>", { class: "form-check" });
                pointDiv.append($("<input>", { type: "radio", name: "jobTitle", class: "form-check-input", value: "會長", id: "jobTitle1", checked: true }));
                pointDiv.append($("<label>", { text: "團長", class: "form-check-label", for: "jobTitle1" }));
                formInput.append(pointDiv);
                pointDiv = $("<div>", { class: "form-check" });
                pointDiv.append($("<input>", { type: "radio", name: "jobTitle", class: "form-check-input", value: "團長", id: "jobTitle2" }));
                pointDiv.append($("<label>", { text: "會長", class: "form-check-label", for: "jobTitle2" }));
                formInput.append(pointDiv);
            } else if (action === "addPointByAmwayAward") {
                amwayAwardList.forEach((element, index) => {
                    pointDiv = $("<div>", { class: "form-check" });
                    pointDiv.append($("<input>", { type: "radio", name: "amwayAward", class: "form-check-input", value: element, id: "amwayAward" + index }));
                    pointDiv.append($("<label>", { text: element, class: "form-check-label", for: "amwayAward" + index }));
                    formInput.append(pointDiv);
                });
            }

            bootbox.confirm({
                closeButton: false,
                backdrop: true,
                scrollable: true,
                title: "請輸入您要給予的點數",
                message: formInput,
                locale: "zh_TW",
                container: "body",
                centerVertical: true,
                className: "pt-5",
                callback: (res) => {
                    if (!res)
                        return;
                    formData = new FormData($("#addPointForm")[0]);
                    point = formData.get("point");
                    if (point <= 0) {
                        bootbox.alert({
                            closeButton: false,
                            message: "請輸入大於零的點數",
                            locale: "zh_TW",
                            centerVertical: true,
                        });
                        return;
                    }
                    $.ajax({
                        url: location.origin + "/pointManage/" + action,
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
                            bootbox.alert({
                                closeButton: false,
                                message: "伺服器出狀況,請聯繫系統人員",
                                locale: "zh_TW",
                                centerVertical: true,
                            });
                        }
                    });

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
