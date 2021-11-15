$(document).ready(() => {

    myTable = $('#myTable').DataTable({
        "orderClasses": false,
        "responsive": true,
        "fixedHeader": true,
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
        'user', 'amwayNumber', 'ClassRoomName', 'amwayDD',
        'point', 'accountStatus', 'modify', 'modify_history'
    ]
    myTableHeadChinese = [
        '姓名', '會員編號', '教室', '上手白金',
        '點數', '狀態', '修改', '修改紀錄'
    ]
    $.ajax({
        'url': location.origin + "/managerPages/allUserAccount",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                userid = fields['id']
                myTable.row.add([
                    fields['user'],
                    fields['amwayNumber'],
                    fields['ClassRoomName'],
                    fields['amwayDD'],
                    fields['point'],
                    fields['accountStatus'] === true ? "正常" : "凍結",
                    `<a id="${userid}_modify" data-toggle="modal"
                        data-target="#accountModifyConfirm"
                        class="button_modified h4 btn btn-outline-success btn-sm">
                        修改
                    </a>`,
                    `<a id="${userid}_modify_history" class="button_history h4 btn btn-outline-success btn-sm" data-toggle="modal"
                        data-target="#pointModal">
                        查看
                    </a>`
                ]).nodes().to$()
                    .find('td')
                    .each(function (index) {
                        $(this).attr('id', userid + "_" + myTableHead[index]);
                    });

                amwayDiamond = fields['amwayDiamond']
                gender = fields['gender']
                phone = fields['phone']
                jobTitle = fields['jobTitle']
                amwayAward = fields['amwayAward']
                amwayNumber = fields['amwayNumber']
                amwayDD_number = fields['amwayDD_number']
                dataPermissionsLevel = fields['dataPermissionsLevel']
                //insert data for modify perpose
                moHTML = `
                    <td id="${userid}_gender" style="display:none" data-th="性別">
                        ${gender}
                    </td>
                    　　
                    <td id="${userid}_phone" style="display:none" data-th="電話">
                        ${phone}
                    </td>
                    <td id="${userid}_jobTitle" style="display:none" data-th="職務">
                        ${jobTitle}
                    </td>
                    　　
                    <td id="${userid}_amwayAward" style="display:none" data-th="獎銜">
                        ${amwayAward}
                    </td>
                    <input type="hidden"
                        value="${amwayDD_number}"
                        id="${userid}_amwayDD_number">
                    <input type="hidden" value="${dataPermissionsLevel}"
                        id="${userid}_dataPermissionsLevel">
                    <td id="${userid}_amwayDiamond" style="display:none" data-th="上手鑽石">
                        ${amwayDiamond}
                    </td>
                `
                $(moHTML).appendTo($("#hiddenData"));
            }
            myTable.columns().every(function (index) {
                if (index > 5) {
                    return;
                }
                var column = this;
                selectHTML = `
                <div class="col-auto">
                    <label>${myTableHeadChinese[index]}</label>
                    <select class="custom-select custom-select-md"><option value=""></option></select>
                </div>
                `
                var select = $(selectHTML)
                    .appendTo($("#colSearch"));

                select.find("select").on('change', function () {
                    var val = $.fn.dataTable.util.escapeRegex(
                        $(this).val()
                    );

                    column
                        .search(val ? '^' + val + '$' : '', true, false)
                        .draw();
                });

                column.data().unique().sort().each(function (d, j) {
                    select.find("select").append('<option value="' + d + '">' + d + '</option>')
                });
            });

            setTimeout(function () {
                myTable.draw(true);
                myTable.columns.adjust().draw();
                myTable.responsive.recalc().columns.adjust();
                if (data.length == 0) {

                    $(".dataTables_empty").text("目前沒有資料");

                }

            }, 10);
        },
        'error': (res) => {
            $(".dataTables_empty").text("伺服器出狀況,請聯繫系統人員");
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

    $("#myTable").on("click", ".button_history", (event) => {
        var counter = 1;
        t.clear().draw();
        $(".dataTables_empty").addClass("table-warning text-dark font-weight-bold");
        $(".dataTables_empty").text("目前沒有紀錄");
        id = $(event.target)[0].id;
        username = id.split("_")[0];

        action = "getAccountModifyHistory";
        formData = new FormData();
        formData.append("username", username)
        $.ajax({
            'url': location.origin + "/managerPages/" + action,
            'method': 'POST',
            'processData': false,
            'contentType': false,
            'data': formData,
            'headers': { 'X-CSRFToken': getCookie('csrftoken') },
            'success': (res) => {
                console.log(res)
                data = JSON.parse(res)
                for (i in data) {
                    fields = data[i]['fields']
                    t.row.add([
                        fields['modifier'],
                        fields['recordDate'],
                        fields['modifyFielddName'],
                        fields['originFieldData'],
                        fields['RevisedData'],

                    ]).draw(false);
                }
            },
            'error': (res) => {
                alert("伺服器出狀況,請聯繫系統人員")
            }
        });

    });

    $(".accountStatusBtn").on("click", (e) => {
        action = $(e.target)[0].id;
        if (action === "activateByExcel") {
            title = "請輸入要啟用的帳號清單"
        } else if (action === "freezeByExcel") {
            title = "請輸入要凍結的帳號清單"
        }
        formInput = "";
        formInput = $("<form>", { id: "accountStatusForm" });
        pointDiv = $("<div>", { class: "form-group" });
        pointDiv.append($("<label>", { text: "報表檔案" }));
        pointDiv.append($("<input>", { type: "file", name: "excelFile", class: "form-control", placeholder: "Select file" }));
        formInput.append(pointDiv);

        if (action === "activateByExcel") {
            pointDiv = $("<div>", { class: "form-group" });
            pointDiv.append($("<label>", { text: "點數" }));
            pointDiv.append($("<input>", { type: "number", name: "point", class: "form-control", placeholder: "Enter point" }));
            formInput.append(pointDiv);
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
            className: "modal-dialog-centered text-dark",
            onShow: function(e) {
                $(e.target).find(".modal-content").addClass("bg-dark")
            } ,
            callback: (res) => {
                if (!res)
                    return;
                formData = new FormData($("#accountStatusForm")[0]);
                if (action === "activateByExcel") {
                    formData.append("is_active", 1)
                    point = formData.get("point");
                    if (point < 0) {
                        bootbox.alert({
                            closeButton: false,
                            message: "請輸入大於等於零的點數",
                            locale: "zh_TW",
                            centerVertical: true,
                            onShow: function(e) {
                                $(e.target).find(".modal-content").addClass("bg-dark")
                            } ,
                        });
                        return;
                    }
                } else {
                    formData.append("is_active", 0)
                }
                $.ajax({
                    url: location.origin + "/managerPages/changeStatusByExcel",
                    'method': 'POST',
                    'processData': false,
                    'contentType': false,
                    'data': formData,
                    'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                    'success': (res) => {

                        result = JSON.parse(res);
                        message = $("<table>", {
                            "id": "excelTable",
                            class: "display table-bordered ",
                            style: "width:100%; white-space: nowrap;"
                        });
                        excelTable = $(message).DataTable({
                            dom: '<"row"lfBr>tip',
                            buttons: [
                                {
                                    extend: 'excel',
                                    title: "帳號異動結果",
                                    className: 'btn btn-sm btn-warning'
                                },
                                {
                                    extend: 'print',
                                    title: "帳號異動結果",

                                    className: 'btn btn-sm btn-warning'
                                }
                            ],
                            "orderClasses": false,
                            "responsive": true,
                            "fixedHeader": true,
                            "language": {
                                url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
                            },
                            "createdRow": function (row, data, dataIndex) {
                                $(row).addClass('table-primary');
                                $(row).addClass('text-dark');
                                $(row).addClass('font-weight-bold');
                            },
                            "columns": [{ title: "姓名" }, { title: "編號" }, { title: "點數" }, { title: "狀態" }]
                        });
                        result.forEach((ele, index) => {
                            excelTable.row.add([
                                ele["user"],
                                ele["amwayNumber"],
                                ele["point"],
                                ele["status"],
                            ])
                        });


                        bootbox.alert({
                            closeButton: false,
                            scrollable: true,
                            className: "modal-dialog-centered",
                            container: "body",
                            title: "帳號異動清單",
                            message: message,
                            locale: "zh_TW",
                            centerVertical: true,
                            onShow: function(e) {
                                $(e.target).find(".modal-content").addClass("bg-dark")
                            } ,
                        });

                    },
                    'error': (res) => {
                        bootbox.alert({
                            closeButton: false,
                            message: "伺服器出狀況,請聯繫系統人員",
                            locale: "zh_TW",
                            centerVertical: true,
                            onShow: function(e) {
                                $(e.target).find(".modal-content").addClass("bg-dark")
                            } ,
                        });
                    }
                });

            }
        });
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
