$(document).ready(() => {

    blackListTable = $('#blackListTable').DataTable({
        "orderClasses": false,
        "responsive": true,
        "autoWidth": true,
        "language": {
            url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
        },
        "createdRow": function (row, data, dataIndex) {
            $(row).addClass('table-primary');
            $(row).addClass('text-dark');
            $(row).addClass('font-weight-bold');
        }
    });
    myTableHead = [
        'name', 'gender', 'phone', 'amwayNumber',
        'id4', 'editInfo', 'deleteInfo'
    ]
    myTableHeadChinese = [
        '姓名', '性別', '手機', '直銷商編號',
        '身份證後四碼', '編輯', '刪除'
    ]

    // 取得待處理列表
    $.ajax({
        'url': location.origin + "/managerPages/getBlackList",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]['fields']
                blackID = data[i]['pk']
                tempRow = blackListTable.row.add([
                    fields['name'],
                    fields['gender'],
                    fields['phone'],
                    fields['amwayNumber'],
                    fields['id4'],
                    `<a id="${blackID}_editInfo" class="button_editInfo h4 btn btn-outline-success btn-sm">
                        編輯
                    </a>`,
                    `<a id="${blackID}_deleteInfo" class="button_deleteInfo h4 btn btn-outline-success btn-sm">
                        刪除
                    </a>`
                ]);
                tempRow.node().id = `${blackID}_tr`;
                tempRow.nodes().to$()
                    .find('td')
                    .each(function (index) {
                        $(this).attr('id', blackID + "_" + myTableHead[index]);
                    });
            }

            setTimeout(function () {
                blackListTable.draw(true);
                blackListTable.columns.adjust().draw();
                blackListTable.responsive.recalc().columns.adjust();
                if (data.length == 0) {
                    $(".dataTables_empty").text("目前沒有資料");
                }
            }, 10);
        },
        'error': (res) => {
            $(".dataTables_empty").text("此功能異常,請聯繫系統人員");
        }
    });

    blackRequestTable = $('#blackRequestTable').DataTable({
        dom: '<"row"lfr>tip',
        "orderClasses": false,
        "responsive": true,
        "autoWidth": true,
        "language": {
            url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
        },
        "createdRow": function (row, data, dataIndex) {
            $(row).addClass('table-primary');
            $(row).addClass('text-dark');
            $(row).addClass('font-weight-bold');
        }
    });

    // 取得黑名單註冊的列表
    $.ajax({
        'url': location.origin + "/managerPages/getBlackRequestList",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]['fields']
                tempRow = blackRequestTable.row.add([
                    fields['registerDate'],
                    fields['name'],
                    fields['gender'],
                    fields['phone'],
                    fields['amwayDD'],
                    fields['amwayNumber'],
                    fields['id4'],
                    fields['ChainYenClass'],
                ]);
            }
            setTimeout(function () {
                blackRequestTable.draw(true);
                blackRequestTable.columns.adjust().draw();
                blackRequestTable.responsive.recalc().columns.adjust();
                if (data.length == 0) {
                    $(".dataTables_empty").text("目前沒有資料");
                }
            }, 10);
        },
        'error': (res) => {
            $(".dataTables_empty").text("此功能異常,請聯繫系統人員");
        }
    });

    $("#blackListTable").on("click", ".button_deleteInfo", (event) => {
        id = $(event.target)[0].id;
        blackID = id.split("_")[0];
        action = id.split("_")[1];
        infoName = $(`#${blackID}_name`).html();
        title = `提醒!!!`
        msg = `確認要刪除黑名單的【${infoName}】?`


        bootbox.confirm({
            closeButton: false,
            backdrop: true,
            scrollable: true,
            title: title,
            message: msg,
            locale: "zh_TW",
            container: "body",
            centerVertical: true,
            callback: (res) => {
                if (!res)
                    return;
                $.ajax({
                    'url': location.origin + "/managerPages/deleteBlackInfo/" + blackID,
                    'method': 'GET',
                    'processData': false,
                    'contentType': false,
                    'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                    'success': (res) => {
                        window.blackListTable.row('#' + blackID + '_tr').remove().draw();

                        bootbox.alert({
                            closeButton: false,
                            message: "成功",
                            locale: "zh_TW",
                            centerVertical: true,
                        });
                    },
                    'error': (res) => {
                        alert("此功能異常,請聯繫系統人員")
                    }
                });
            }
        });


    });

    $("#blackListTable").on("click", ".button_editInfo", (event) => {

        id = $(event.target)[0].id;
        blackID = id.split("_")[0];
        action = id.split("_")[1];
        if (action === "editInfo") {
            formInput = ""
            formInput = $("<form>", { id: "blackInfoModify" });

            infoName = $(`#${blackID}_name`).html();
            gender = $(`#${blackID}_gender`).html();
            phone = $(`#${blackID}_phone`).html();
            amwayNumber = $(`#${blackID}_amwayNumber`).html();
            id4 = $(`#${blackID}_id4`).html();

            groupRow = $("<div>", { class: "form-row" });

            pointDiv = $("<div>", { class: "form-group  col-md-3" });
            pointDiv.append($("<label>", { text: "姓名", class: "form-check-label", for: "DBClass" }));
            pointDiv.append($("<input>", { type: "text", name: "name",value:infoName, class: "form-control form-control-sm rounded bg-white text-dark", id: "name" }));
            groupRow.append(pointDiv);

            pointDiv = $("<div>", { class: "form-group  col-md-3" });
            pointDiv.append($("<label>", { text: "性別", class: "form-check-label", for: "gender" }));
            pointDiv.append($("<select>", { name: "gender", class: "form-control custom-select", id: "gender" }));
            $(pointDiv).find("select").append($("<option>", { text: "男" }))
            $(pointDiv).find("select").append($("<option>", { text: "女" }))
            $(pointDiv).find("#gender").val(gender);
            groupRow.append(pointDiv);

            pointDiv = $("<div>", { class: "form-group col" });
            pointDiv.append($("<label>", { text: "電話", class: "form-check-label", for: "title" }));
            pointDiv.append($("<input>", { type: "text", name: "phone", value:phone, class: "form-control form-control-sm rounded bg-white text-dark", id: "phone" }));
            groupRow.append(pointDiv);

            formInput.append(groupRow);

            groupRow = $("<div>", { class: "form-row" });

            pointDiv = $("<div>", { class: "form-group  col-md-3" });
            pointDiv.append($("<label>", { text: "直銷商編號", class: "form-check-label", for: "amwayNumber" }));
            pointDiv.append($("<input>", { type: "text", name: "amwayNumber", value:amwayNumber, class: "form-control form-control-sm rounded bg-white text-dark", id: "amwayNumber" }));
            groupRow.append(pointDiv);

            pointDiv = $("<div>", { class: "form-group col" });
            pointDiv.append($("<label>", { text: "身份證後四碼", class: "form-check-label", for: "id4" }));
            pointDiv.append($("<input>", { type: "text", name: "id4", value:id4, class: "form-control form-control-sm rounded bg-white text-dark", id: "id4" }));
            groupRow.append(pointDiv);

            formInput.append(groupRow);

            bootbox.confirm({
                closeButton: false,
                backdrop: true,
                scrollable: true,
                title: "提醒:您正在修改文章資料!",
                message: formInput,
                locale: "zh_TW",
                container: "body",
                className: "modal-dialog-centered",
                centerVertical: true,
                callback: (res) => {
                    if (!res)
                        return;
                    formData = new FormData($("#blackInfoModify")[0]);
                    $.ajax({
                        'url': location.origin + "/managerPages/updateBlackInfo/" + blackID,
                        'method': 'POST',
                        'processData': false,
                        'contentType': false,
                        'data': formData,
                        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                        'success': (res) => {
                            $(`#${blackID}_name`).html(formData.get("name"));
                            $(`#${blackID}_gender`).html(formData.get("gender"));
                            $(`#${blackID}_phone`).html(formData.get("phone"));
                            $(`#${blackID}_amwayNumber`).html(formData.get("amwayNumber"));
                            $(`#${blackID}_id4`).html(formData.get("id4"));
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
        }
    });

    $(".actionBlackList").on("click", actionBlackList);

    function actionBlackList(event) {
        id = $(event.target)[0].id;
        if (id === "addBlackInfo") {
            action = id;
            formInput = "";
            formInput = $("<form>", { id: "blackInfoForm" });
            title = "請輸入黑名單資訊";
            if (action === "addBlackInfo") {
                groupRow = $("<div>", { class: "form-row" });

                pointDiv = $("<div>", { class: "form-group  col-md-3" });
                pointDiv.append($("<label>", { text: "姓名", class: "form-check-label", for: "DBClass" }));
                pointDiv.append($("<input>", { type: "text", name: "name", class: "form-control form-control-sm rounded bg-white text-dark", id: "name" }));
                groupRow.append(pointDiv);

                pointDiv = $("<div>", { class: "form-group  col-md-3" });
                pointDiv.append($("<label>", { text: "性別", class: "form-check-label", for: "gender" }));
                pointDiv.append($("<select>", { name: "gender", class: "form-control custom-select", id: "gender" }));
                $(pointDiv).find("select").append($("<option>", { text: "男" }))
                $(pointDiv).find("select").append($("<option>", { text: "女" }))
                groupRow.append(pointDiv);

                pointDiv = $("<div>", { class: "form-group col" });
                pointDiv.append($("<label>", { text: "電話", class: "form-check-label", for: "title" }));
                pointDiv.append($("<input>", { type: "text", name: "phone", class: "form-control form-control-sm rounded bg-white text-dark", id: "phone" }));
                groupRow.append(pointDiv);

                formInput.append(groupRow);

                groupRow = $("<div>", { class: "form-row" });

                pointDiv = $("<div>", { class: "form-group  col-md-3" });
                pointDiv.append($("<label>", { text: "直銷商編號", class: "form-check-label", for: "amwayNumber" }));
                pointDiv.append($("<input>", { type: "text", name: "amwayNumber", class: "form-control form-control-sm rounded bg-white text-dark", id: "amwayNumber" }));
                groupRow.append(pointDiv);

                pointDiv = $("<div>", { class: "form-group col" });
                pointDiv.append($("<label>", { text: "身份證後四碼", class: "form-check-label", for: "id4" }));
                pointDiv.append($("<input>", { type: "text", name: "id4", class: "form-control form-control-sm rounded bg-white text-dark", id: "id4" }));
                groupRow.append(pointDiv);

                formInput.append(groupRow);
            }

            bootbox.confirm({
                closeButton: false,
                backdrop: true,
                scrollable: true,
                title: title,
                message: formInput,
                locale: "zh_TW",
                container: "body",
                centerVertical: true,
                className: "modal-dialog-centered",
                callback: (res) => {
                    if (!res)
                        return;
                    formData = new FormData($("#blackInfoForm")[0]);
                    if (action === "addBlackInfo") {
                        infoName = formData.get("name");
                        if (infoName === "") {
                            bootbox.alert({
                                closeButton: false,
                                message: "請輸入姓名",
                                locale: "zh_TW",
                                centerVertical: true,
                            });
                            return;
                        }
                        infoPhone = formData.get("phone");
                        if (infoPhone === "") {
                            bootbox.alert({
                                closeButton: false,
                                message: "請輸入手機",
                                locale: "zh_TW",
                                centerVertical: true,
                            });
                            return;
                        }
                        infoGender = formData.get("gender");
                        if (infoGender === "") {
                            bootbox.alert({
                                closeButton: false,
                                message: "請輸入性別",
                                locale: "zh_TW",
                                centerVertical: true,
                            });
                            return;
                        }
                    }

                    $.ajax({
                        url: location.origin + "/managerPages/" + action,
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
                            msg = "此功能異常,請聯繫系統人員"
                            if (res.status == 400) {
                                msg = res.responseText
                            }
                            bootbox.alert({
                                closeButton: false,
                                message: msg,
                                locale: "zh_TW",
                                centerVertical: true,
                            });
                        }
                    });

                }
            });
        }

    }

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
