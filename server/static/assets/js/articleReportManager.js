$(document).ready(() => {

    reportTable = $('#reportTable').DataTable({
        dom: '<"row"lfr>tip',
        "orderClasses": false,
        "responsive": true,
        "autoWidth": true,
        "columnDefs": [
            { "width": "25%", "targets": 3 },
        ],
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
        'reporter', 'title', 'mainClass', 'reason',
        'recordDate', 'editArticle', 'deleteReport'
    ]
    myTableHeadChinese = [
        '回報者', '標題', '主類別', '原因',
        '回報日期', '編輯資料', '刪除回報紀錄'
    ]

    // 取得待處理列表
    $.ajax({
        'url': location.origin + "/managerPages/getArticleReport/report",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                reportID = fields['id']
                articleID = fields['articleID']
                //需要取得的資料最好都埋在自己的ID裡，因為datatable的響應式會破壞既有的 dom 結構
                tempRow = reportTable.row.add([
                    fields['reporter'],
                    `<a target="_blank" href="${location.origin}/viewFilePage/${articleID}">${fields['title']}</a>`,
                    fields['mainClass'],
                    fields['reason'],
                    fields['recordDate'],
                    `<a id="${reportID}_${articleID}_editArticle" class="button_editArticle h4 btn btn-outline-success btn-sm">
                        編輯
                    </a>`,
                    `<a id="${reportID}_deleteReport" class="button_deleteReport h4 btn btn-outline-success btn-sm">
                        刪除
                    </a>`
                ]);
                tempRow.node().id = `${reportID}_tr`;
                tempRow.nodes().to$()
                    .find('td')
                    .each(function (index) {
                        $(this).attr('id', reportID + "_" + myTableHead[index]);
                    });

            }
            reportTable.columns().every(function (index) {
                return;
                if (index > 6 || myTableHeadChinese[index] === "描述") {
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
                reportTable.draw(true);
                reportTable.columns.adjust().draw();
                reportTable.responsive.recalc().columns.adjust();
                if (data.length == 0) {

                    $(".dataTables_empty").text("目前沒有資料");

                }
            }, 10);
        },
        'error': (res) => {
            $(".dataTables_empty").text("此功能異常,請聯繫系統人員");
        }
    });

    finishTable = $('#finishTable').DataTable({
        dom: '<"row"lfr>tip',
        "orderClasses": false,
        "responsive": true,
        "autoWidth": true,
        "columnDefs": [
            { "width": "25%", "targets": 3 },
        ],
        "language": {
            url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
        },
        "createdRow": function (row, data, dataIndex) {
            $(row).addClass('table-primary');
            $(row).addClass('text-dark');
            $(row).addClass('font-weight-bold');
        }
    });

    // 取得已完成列表
    $.ajax({
        'url': location.origin + "/managerPages/getArticleReport/finish",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                articleID = fields['articleID']
                tempRow = finishTable.row.add([
                    fields['reporter'],
                    `<a target="_blank" href="${location.origin}/viewFilePage/${articleID}">${fields['title']}</a>`,
                    fields['mainClass'],
                    fields['reason'],
                    fields['recordDate'],
                    fields['handler'],
                    fields['handleDate'],
                ]);
            }
            setTimeout(function () {
                finishTable.draw(true);
                finishTable.columns.adjust().draw();
                finishTable.responsive.recalc().columns.adjust();
                if (data.length == 0) {
                    $(".dataTables_empty").text("目前沒有資料");
                }
            }, 10);
        },
        'error': (res) => {
            $(".dataTables_empty").text("此功能異常,請聯繫系統人員");
        }
    });

    discardTable = $('#discardTable').DataTable({
        dom: '<"row"lfr>tip',
        "orderClasses": false,
        "responsive": true,
        "autoWidth": true,
        "columnDefs": [
            { "width": "25%", "targets": 3 },
        ],
        "language": {
            url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
        },
        "createdRow": function (row, data, dataIndex) {
            $(row).addClass('table-primary');
            $(row).addClass('text-dark');
            $(row).addClass('font-weight-bold');
        }
    });
    
    // 取得無效列表
    $.ajax({
        'url': location.origin + "/managerPages/getArticleReport/discard",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                articleID = fields['articleID']
                tempRow = discardTable.row.add([
                    fields['reporter'],
                    `<a target="_blank" href="${location.origin}/viewFilePage/${articleID}">${fields['title']}</a>`,
                    fields['mainClass'],
                    fields['reason'],
                    fields['recordDate'],
                    fields['handler'],
                    fields['discardReason'],
                    fields['handleDate'],
                ]);
            }
            setTimeout(function () {
                discardTable.draw(true);
                discardTable.columns.adjust().draw();
                discardTable.responsive.recalc().columns.adjust();
                if (data.length == 0) {
                    $(".dataTables_empty").text("目前沒有資料");
                }
            }, 10);
        },
        'error': (res) => {
            $(".dataTables_empty").text("此功能異常,請聯繫系統人員");
        }
    });

    $("#reportTable").on("click", ".button_editArticle", (event) => {
        id = $(event.target)[0].id;
        reportID = id.split("_")[0];
        articleID = id.split("_")[1];
        action = id.split("_")[2];
        if (action === "editArticle") {
            $.ajax({
                'url': location.origin + "/managerPages/getFileDataInfoByID/" + articleID,
                'method': 'GET',
                'processData': false,
                'contentType': false,
                'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                'success': (res) => {
                    res = JSON.parse(res);
                    formInput = ""
                    formInput = $("<form>", { id: "article_modify" });

                    title = res["title"];
                    DBClass = res['DBClassCode'];
                    mainClass = res["mainClass"];
                    secClass = res["secClass"];
                    keyword = res["keyword"];
                    describe = res["describe"];
                    point = res["point"];
                    visible = res["visible"];
                    groupRow = $("<div>", { class: "form-row" });

                    formInput.append($("<input>", { style: "display:none;", value: articleID, name: "id" }))
                    pointDiv = $("<div>", { class: "form-group  col-md-3" });
                    pointDiv.append($("<label>", { text: "資料庫類別", class: "form-check-label", for: "DBClass" }));
                    pointDiv.append($("<input>", { type: "text", name: "DBClass", class: "form-control form-control-sm rounded  text-dark", value: DBClass, id: "DBClass", readonly: true, disabled: true }));
                    groupRow.append(pointDiv);

                    pointDiv = $("<div>", { class: "form-group col" });
                    pointDiv.append($("<label>", { text: "標題", class: "form-check-label", for: "title" }));
                    pointDiv.append($("<input>", { type: "text", name: "title", class: "form-control form-control-sm rounded bg-white text-dark", value: title, id: "title" }));
                    groupRow.append(pointDiv);

                    formInput.append(groupRow);

                    groupRow = $("<div>", { class: "form-row" });

                    pointDiv = $("<div>", { class: "form-group col" });
                    pointDiv.append($("<label>", { text: "主類別", class: "form-check-label", for: "mainClass" }));
                    pointDiv.append($("<select>", { name: "mainClass", class: "form-control custom-select", id: "mainClass" }));
                    mainClassList.forEach((element, index) => {
                        if (element === "無")
                            return;
                        $(pointDiv).find("#mainClass").append($("<option>", { text: element }))
                    });
                    $(pointDiv).find("#mainClass").val(mainClass);
                    groupRow.append(pointDiv);

                    pointDiv = $("<div>", { class: "form-group col" });
                    pointDiv.append($("<label>", { text: "次類別", class: "form-check-label", for: "secClass" }));
                    pointDiv.append($("<select>", { name: "secClass", class: "form-control custom-select", id: "secClass" }));
                    secClassList.forEach((element, index) => {
                        if (element === "無")
                            return;
                        $(pointDiv).find("#secClass").append($("<option>", { text: element }))
                    });
                    $(pointDiv).find("#secClass").val(secClass);
                    groupRow.append(pointDiv);

                    formInput.append(groupRow);

                    if (window.aritclePointManage) {
                        pointDiv = $("<div>", { class: "form-group col" });
                        pointDiv.append($("<label>", { text: "消耗點數", class: "form-check-label", for: "point" }));
                        pointDiv.append($("<input>", { type: "text", name: "point", class: "form-control form-control-sm  rounded bg-white text-dark round", value: point, id: "point" }));
                        groupRow.append(pointDiv);
                    }


                    pointDiv = $("<div>", { class: "form-group col" });
                    pointDiv.append($("<label>", { text: "是否可見", class: "form-check-label", for: "visible" }));
                    pointDiv.append($("<select>", { type: "text", name: "visible", class: "form-control", id: "visible" }));
                    $(pointDiv).find("#visible").append($("<option>", { text: "true" }))
                    $(pointDiv).find("#visible").append($("<option>", { text: "false" }))
                    $(pointDiv).find("#visible").val(String(visible));
                    groupRow.append(pointDiv);

                    formInput.append(groupRow);

                    pointDiv = $("<div>", { class: "form-group" });
                    pointDiv.append($("<label>", { text: "關鍵字", class: "form-check-label", for: "keyword" }));
                    pointDiv.append($("<textarea>", { type: "text", name: "keyword", class: "form-control", text: keyword, id: "keyword" }));
                    formInput.append(pointDiv);

                    pointDiv = $("<div>", { class: "form-group" });
                    pointDiv.append($("<label>", { text: "描述", class: "form-check-label", for: "describe" }));
                    pointDiv.append($("<textarea>", { type: "text", name: "describe", class: "form-control", text: describe, id: "describe" }));
                    formInput.append(pointDiv);

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
                            formData = new FormData($("#article_modify")[0]);
                            formData.append("reportID", reportID)
                            $.ajax({
                                'url': location.origin + "/managerPages/updateFileDataInfo",
                                'method': 'POST',
                                'processData': false,
                                'contentType': false,
                                'data': formData,
                                'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                                'success': (res) => {
                                    res = JSON.parse(res);
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
                },
                'error': (res) => {
                    alert("此功能異常,請聯繫系統人員");
                }
            });

        }
    });


    $("#reportTable").on("click", ".button_deleteReport", (event) => {
        id = $(event.target)[0].id;
        reportID = id.split("_")[0];
        action = id.split("_")[1];
        title = $(`#${reportID}_title`).html();
        reporter = $(`#${reportID}_reporter`).html();
        title = `確認要刪除【${reporter}】回報的【${title}】?`
        msg = $("<form>", { id: "discardForm" });
        pointDiv = $("<div>", { class: "form-group" });
        pointDiv.append($("<label>", { text: "無效原因" }));
        pointDiv.append($("<textarea>", { type: "text", name: "discardReason", class: "form-control", text: "", id: "discardReason", required: true }));
        msg.append(pointDiv);

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
                formData = new FormData($("#discardForm")[0]);
                $.ajax({
                    'url': location.origin + "/managerPages/removeArticleReport/" + reportID,
                    'method': 'POST',
                    'processData': false,
                    'contentType': false,
                    'data': formData,
                    'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                    'success': (res) => {
                        window.reportTable.row('#' + reportID + '_tr').remove().draw();

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
