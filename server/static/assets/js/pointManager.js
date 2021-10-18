$(document).ready(() => {

    myTable = $('#myTable').DataTable({
        dom: '<"row"lfr>tip',
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
        'user', 'point', 'jobTitle', 'amwayAward',
        'addPoint', 'reducePoint', 'getPointHistory'
    ]
    myTableHeadChinese = [
        '姓名', '點數', '職務', '獎銜',
        '加點', '扣點', '查看歷史'
    ]
    $.ajax({
        'url': location.origin + "/pointManage/allUserAccount",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                username = fields['username']
                myTable.row.add([
                    fields['user'],
                    fields['point'],
                    fields['jobTitle'],
                    fields['amwayAward'],
                    `<a id="${username}_addPoint" class="button_modified h4 btn btn-outline-success btn-sm">+10</a>`,
                    `<a id="${username}_reducePoint" class="button_modified h4 btn btn-outline-success btn-sm">-1</a>`,
                    `<a id="${username}_getPointHistory" class="button_history h4 btn btn-outline-success btn-sm" data-toggle="modal"
                        data-target="#pointModal">
                        查看
                    </a>`
                ]).nodes().to$()
                    .find('td')
                    .each(function (index) {
                        $(this).attr('id', username + "_" + myTableHead[index]);
                    });
            }
            myTable.columns().every(function (index) {
                if (index > 3) {
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
                if (data.length == 0 ){

                $(".dataTables_empty").text("目前沒有資料");

             }
            }, 10);
        },
        'error': (res) => {
             $(".dataTables_empty").text("伺服器出狀況,請聯繫系統人員");
        }
    });

    $("#myTable").on("click", ".button_modified", (event) => {

        id = $(event.target)[0].id;
        username = id.split("_")[0];
        user = $("#" + username + "_user").html();
        action = id.split("_")[1];
        if (action === "addPoint" || action === "reducePoint") {
            msg = ""
            if (action === "addPoint")
                msg = "將為\"" + user + "\"增加 10 點"
            else if (action === "reducePoint")
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

    window.t = $('#example').DataTable({
        dom: '<"row"lfBr>tip',
        buttons: [
            {
                extend: 'excel',
                title: "點數歷史紀錄",
                className: 'btn btn-sm btn-warning'
            },
            {
                extend: 'print',
                title: "點數歷史紀錄",

                className: 'btn btn-sm btn-warning'
            }
        ],
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
                    ]).draw(true);
                }

                setTimeout(function () {
                    t.draw(true);
                    t.columns.adjust().draw();
                    t.responsive.recalc().columns.adjust();
                }, 10);
            },
            'error': (res) => {
                alert("伺服器出狀況,請聯繫系統人員")
            }
        });

    });

    $(".addPointByOption").on("click", (event) => {
        id = $(event.target)[0].id;
        if (id === "addPointByAll" || id === "addPointByJobTitle" ||
            id === "addPointByAmwayAward" || id === "addPointByExcel") {
            action = id;
            formInput = "";
            formInput = $("<form>", { id: "addPointForm" });
            pointDiv = $("<div>", { class: "form-group" });
            pointDiv.append($("<label>", { text: "點數" }));
            pointDiv.append($("<input>", { type: "number", name: "point", class: "form-control", placeholder: "Enter point" }));
            formInput.append(pointDiv);
            title = "請輸入您要給予的點數";
            if (action === "addPointByAll") {

            } else if (action === "addPointByJobTitle") {
                pointDiv = $("<div>", { class: "form-group" });
                pointDiv.append($("<label>", { text: "請選擇職務", for: "jobTitle" }));
                pointDiv.append($("<select>", { name: "jobTitle", class: "form-control custom-select", id: "jobTitle" }));
                jobTitleList.forEach((element, index) => {
                    if (element === "無")
                        return;
                    $(pointDiv).find("select").append($("<option>", { text: element }))
                });
                formInput.append(pointDiv);
            } else if (action === "addPointByAmwayAward") {
                pointDiv = $("<div>", { class: "form-group" });
                pointDiv.append($("<label>", { text: "請選擇獎銜", for: "amwayAward" }));
                pointDiv.append($("<select>", { name: "amwayAward", class: "form-control custom-select", id: "amwayAward" }));
                amwayAwardList.forEach((element, index) => {
                    $(pointDiv).find("select").append($("<option>", { text: element }))
                });
                formInput.append(pointDiv);
            } else if (id === "addPointByExcel") {
                title = "請輸入要增加點數的報表清單"
                formInput = "";
                formInput = $("<form>", { id: "addPointForm" });
                pointDiv = $("<div>", { class: "form-group" });
                pointDiv.append($("<label>", { text: "報表檔案" }));
                pointDiv.append($("<input>", { type: "file", name: "excelFile", class: "form-control", placeholder: "Select file" }));
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
                className: "modal-dialog-centered",
                callback: (res) => {
                    if (!res)
                        return;
                    formData = new FormData($("#addPointForm")[0]);
                    if (action !== "addPointByExcel") {
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
                    }
                    $.ajax({
                        url: location.origin + "/pointManage/" + action,
                        'method': 'POST',
                        'processData': false,
                        'contentType': false,
                        'data': formData,
                        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                        'success': (res) => {

                            if (action === "addPointByExcel") {
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
                                            title: "點數報表結果",
                                            className: 'btn btn-sm btn-warning'
                                        },
                                        {
                                            extend: 'print',
                                            title: "點數報表結果",

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
                                    "columns": [{ title: "姓名" }, { title: "編號" }, { title: "結果" }]
                                });
                                result.forEach((ele, index) => {
                                    excelTable.row.add([
                                        ele["user"],
                                        ele["amwayNumber"],
                                        ele["point"]
                                    ])
                                });


                                bootbox.alert({
                                    closeButton: false,
                                    scrollable: true,
                                    className: "modal-dialog-centered",
                                    container: "body",
                                    title: "點數增加清單",
                                    message: message,
                                    locale: "zh_TW",
                                    centerVertical: true,
                                });

                            } else {
                                bootbox.alert({
                                    closeButton: false,
                                    message: "成功",
                                    locale: "zh_TW",
                                    centerVertical: true,
                                });
                            }

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
