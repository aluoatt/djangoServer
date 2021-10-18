$(document).ready(() => {

    myHistoryTable = $('#myHistoryTable').DataTable({
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
    
    myHistoryTableHead = [
        'modifier', 'recordDate', 'addPoint', 'reducePoint', 'transferPoint',
        'reason', 'resultPoint'
    ]

    $.ajax({
        'url': location.origin + "/pointManage/getSelfPointHistory",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]['fields']
                myHistoryTable.row.add([
                    fields['modifier'],
                    fields['recordDate'],
                    fields['addPoint']+fields['reducePoint']+fields['transferPoint'],
                    fields['reason'],
                    fields['resultPoint'],
                ]).draw(true);
            }

            setTimeout(function () {
                if (data.length == 0 ){

                $(".dataTables_empty").text("目前沒有資料");

             }
                myHistoryTable.draw(true);
                myHistoryTable.columns.adjust().draw();
                myHistoryTable.responsive.recalc().columns.adjust();
            }, 10);
        },
        'error': (res) => {
            $(".dataTables_empty").text("伺服器出狀況,請聯繫系統人員");
        }
    });

    myTransferTable = $('#myTransferTable').DataTable({
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
    
    myTransferTableHead = [
        'user', 'amwayNumber', 'point', 'transferonepoint', 
        'transfertenpoint', 'transferPoint'
    ]

    $.ajax({
        'url': location.origin + "/pointManage/getPersonalTeam",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                username = fields['username']
                myTransferTable.row.add([
                    fields['user'],
                    fields['amwayNumber'],
                    fields['point'],
                    `<a id="${username}_transferonepoint" class="button_transfer h4 btn btn-outline-success btn-sm">+1</a>`,
                    `<a id="${username}_transfertenpoint" class="button_transfer h4 btn btn-outline-success btn-sm">+10</a>`,
                    `<a id="${username}_transferPoint" class="button_transfer h4 btn btn-outline-success btn-sm">轉讓</a>`
                ]).nodes().to$()
                .find('td')
                .each(function(index) {
                    $(this).attr('id', username +"_" + myTransferTableHead[index] );
                });
            }

            setTimeout(function () {
                myTransferTable.draw(true);
                myTransferTable.columns.adjust().draw();
                myTransferTable.responsive.recalc().columns.adjust();
            }, 10);
        },
        'error': (res) => {
            alert("伺服器出狀況,請聯繫系統人員")
        }
    });

    $("#myTransferTable").on("click", ".button_transfer", (event) => {
        id = $(event.target)[0].id;
        username = id.split("_")[0];
        user = $("#" + username + "_user").html();
        action = id.split("_")[1];
        if (action === "transferonepoint" || action === "transfertenpoint") {
            msg = ""
            if (action === "transferonepoint")
                msg = "將轉讓 1 點給\"" + user + "\""
            else if (action === "transfertenpoint")
                msg = "將轉讓 10 點給\"" + user + "\""

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
                    if (action === "transferonepoint")
                        point = 1
                    else
                        point = 10
                    validPoint = Number($(".selfPoint").html());
                    if ((validPoint - point) < 0) {
                        bootbox.alert({
                            closeButton: false,
                            message: "您的點數不足",
                            locale: "zh-TW",
                            centerVertical: true,
                        });
                        return;
                    }

                    formData.append("point", point)
                    $.ajax({
                        'url': location.origin + "/pointManage/transferPoint",
                        'method': 'POST',
                        'processData': false,
                        'contentType': false,
                        'data': formData,
                        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                        'success': (res) => {
                            res = JSON.parse(res);
                            $("#" + res["toUser"] + "_point").html(res["toResultPoint"]);
                            $("#" + res["fromUser"] + "_point").html(res["fromResultPoint"]);
                            bootbox.alert({
                                closeButton: false,
                                message: "成功",
                                className: "text-center",
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


        } else if (action === "transferPoint") {
            bootbox.prompt({
                closeButton: false,
                title: "請輸入您要轉讓的點數",
                inputType: 'number',
                locale: "zh_TW",
                container: "table",
                centerVertical: true,
                callback: (point) => {
                    if (!point)
                        return
                    if (point <= 0) {
                        bootbox.alert({
                            closeButton: false,
                            message: "請輸入大於 0 的數字",
                            locale: "zh_TW",
                            centerVertical: true,
                        }
                        );
                        return;
                    }
                    validPoint = Number($(".selfPoint").html());
                    if ((validPoint - point) < 0) {
                        bootbox.alert({
                            closeButton: false,
                            message: "您的點數不足",
                            locale: "zh_TW",
                            centerVertical: true,
                        });
                        return;
                    }
                    formData = new FormData();
                    formData.append("username", username)
                    formData.append("point", point)
                    $.ajax({
                        'url': location.origin + "/pointManage/transferPoint",
                        'method': 'POST',
                        'processData': false,
                        'contentType': false,
                        'data': formData,
                        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                        'success': (res) => {
                            res = JSON.parse(res);
                            $("#" + res["toUser"] + "_point").html(res["toResultPoint"]);
                            $("#" + res["fromUser"] + "_point").html(res["fromResultPoint"]);
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
        } else {
            //Are you kidding me?
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
