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
        'reporter', 'reason', 'rewardList', 'recordDate',
        'confirm', 'deleteReport'
    ]
    myTableHeadChinese = [
        '請求者', '獎勵原因', '獎勵名單', '請求日期',
        '審核', '刪除'
    ]

    // 取得待處理列表
    $.ajax({
        'url': location.origin + "/managerPages/getRewardReport/waiting",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                reportID = fields['id']
                //需要取得的資料最好都埋在自己的ID裡，因為datatable的響應式會破壞既有的 dom 結構
                tempRow = reportTable.row.add([
                    fields['reporter'],
                    fields['reason'],
                    fields['rewardList'],
                    fields['recordDate'],
                    `<a id="${reportID}_confirm" class="button_confirm h4 btn btn-outline-success btn-sm">
                        審核
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
        'url': location.origin + "/managerPages/getRewardReport/finish",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                tempRow = finishTable.row.add([
                    fields['reporter'],
                    fields['reason'],
                    fields['rewardList'],
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
        'url': location.origin + "/managerPages/getRewardReport/discard",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                tempRow = discardTable.row.add([
                    fields['reporter'],
                    fields['reason'],
                    fields['rewardList'],
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

    $("#reportTable").on("click", ".button_confirm", (event) => {
        id = $(event.target)[0].id;
        reportID = id.split("_")[0];
        action = id.split("_")[1];
        if (action === "confirm") {

            reason = $("#" + reportID + "_reason").text()
            rewardList = $("#" + reportID + "_rewardList").text()
            messageGroup = $("<div>")

            reasonDiv = $("<div>", { class: "form-group" });
            reasonDiv.append($("<label>", { text: "獎勵原因" }));
            reasonDiv.append($("<textarea>", {html:reason, class:"bg-light text-dark form-control", style:"resize:none", disabled:true}))
            rewardListDiv = $("<div>", { class: "form-group" });
            rewardListDiv.append($("<label>", { text: "獎勵名單" }));
            rewardListDiv.append($("<textarea>", {html:rewardList, class:"bg-light text-dark form-control", style:"resize:none", disabled:true}))
            
            messageGroup.append(reasonDiv)
            messageGroup.append(rewardListDiv)

            formInput = "";
            formInput = $("<form>", { id: "rewardPointForm" });
            pointDiv = $("<div>", { class: "form-group" });
            pointDiv.append($("<label>", { text: "請填寫要獎賞的點數:" }));
            pointDiv.append($("<input>", { type: "number", name: "point", class: "form-control", placeholder: "Enter point" }));
            formInput.append(pointDiv);
            
            messageGroup.append(formInput);

            bootbox.confirm({
                closeButton: false,
                backdrop: true,
                scrollable: true,
                title: "提醒:請確認名單和獎賞原因, 並填寫點數!!",
                message: messageGroup,
                locale: "zh_TW",
                container: "body",
                className: "modal-dialog-centered",
                centerVertical: true,
                callback: (res) => {
                    if (!res)
                        return;
                    formData = new FormData($("#rewardPointForm")[0]);
                    formData.append("reportID", reportID)
                    $.ajax({
                        'url': location.origin + "/managerPages/confirmRewardReport",
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
        }
    });

    $("#reportTable").on("click", ".button_deleteReport", (event) => {
        id = $(event.target)[0].id;
        reportID = id.split("_")[0];
        action = id.split("_")[1];
        reporter = $(`#${reportID}_reporter`).html();
        title = `確認要刪除【${reporter}】的獎勵請求?`
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

                discardReason = formData.get("discardReason")
                if(discardReason === ""){
                    bootbox.alert({
                        closeButton: false,
                        message: "請填寫無效原因!",
                        locale: "zh_TW",
                        centerVertical: true,
                    });
                    return;
                }
                formData.append("reportID", reportID)
                $.ajax({
                    'url': location.origin + "/managerPages/discardRewardReport",
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
