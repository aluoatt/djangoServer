$(document).ready(() => {

    myRewardReportTable = $('#myRewardReportTable').DataTable({
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

    myRewardReportTableHead = [
        'reporter', 'reportReason', 'rewardList', 'rewardDate', 'status', 'handleDate',
    ]
    $(".dataTables_empty").html("目前沒有資料");
    $.ajax({
        'url': location.origin + "/personalInfoPage/getSelfRewardReport",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                rewardStatus = ""
                if(fields['status'] == "waiting")
                    rewardStatus = "待審核"
                else if (fields['status'] == "finish")
                    rewardStatus = "通過"
                else if (fields['status'] == "discard")
                    rewardStatus = "無效"
                myRewardReportTable.row.add([
                    fields['reporter'],
                    fields['reason'],
                    fields['rewardList'],
                    fields['recordDate'],
                    fields['handleDate'],
                    rewardStatus,
                ]).draw(true);
            }

            setTimeout(function () {
                myRewardReportTable.draw(true);
                myRewardReportTable.columns.adjust().draw();
                myRewardReportTable.responsive.recalc().columns.adjust();
                if (data.length == 0) {
                    $(".dataTables_empty").html("目前沒有資料");
                }
            }, 10);
        },
        'error': (res) => {
            $(".dataTables_empty").text("此功能異常,請聯繫系統人員");
        }
    });

    $(".rewardReportBtn").on("click", (e) => {
        action = $(e.target)[0].id;
        title = '<div class="text-dark">請輸入要申請獎勵的帳號清單</div>'
        formInput = "";
        formInput = $("<form>", { id: "rewardReportForm" });
        pointDiv = $("<div>", { class: "form-group" });
        pointDiv.append($("<label>", { text: "報表檔案(欄位順序:姓名/編號/後四碼)" }));
        pointDiv.append($("<input>", { type: "file", name: "excelFile", class: "form-control", placeholder: "Select file" }));
        formInput.append(pointDiv);

        pointDiv = $("<div>", { class: "form-group" });
        pointDiv.append($("<label>", { text: "獎勵原因" }));
        pointDiv.append($("<textarea>", { type: "text", name: "reason", class: "form-control", id: "reason"}));
        formInput.append(pointDiv);

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
                formData = new FormData($("#rewardReportForm")[0]);
                excelFile = formData.get("excelFile");
                reason = formData.get("reason");
                if(excelFile["name"] === ""){
                    bootbox.alert({
                        closeButton: false,
                        scrollable: true,
                        className: "modal-dialog-centered",
                        container: "body",
                        title: "提醒",
                        message: "請確實上傳名單!!!",
                        locale: "zh_TW",
                        centerVertical: true,
                        onShow: function(e) {
                            $(e.target).find(".modal-content").addClass("bg-dark")
                        } ,
                    });
                    return;
                }
                if(reason === ""){
                    bootbox.alert({
                        closeButton: false,
                        scrollable: true,
                        className: "modal-dialog-centered",
                        container: "body",
                        title: "提醒",
                        message: "請確實填寫申請獎勵點數的原因!!!",
                        locale: "zh_TW",
                        centerVertical: true,
                        onShow: function(e) {
                            $(e.target).find(".modal-content").addClass("bg-dark")
                        } ,
                    });
                    return;
                }
                $.ajax({
                    url: location.origin + "/personalInfoPage/rewardReportByExcel",
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
                            "orderClasses": false,
                            "responsive": true,
                            "language": {
                                url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
                            },
                            "createdRow": function (row, data, dataIndex) {
                                $(row).addClass('table-primary');
                                $(row).addClass('text-dark');
                                $(row).addClass('font-weight-bold');
                            },
                            "columns": [{ title: '姓名' }, 
                                        { title: '編號' }
                                    ]
                        });
                        result.forEach((ele, index) => {
                            excelTable.row.add([
                                ele["user"],
                                ele["amwayNumber"],
                            ]).draw(true)
                        });
                        


                        bootbox.alert({
                            closeButton: false,
                            scrollable: true,
                            className: "modal-dialog-centered",
                            title: '<div class="text-dark">帳號獎勵清單</div>',
                            message: message,
                            locale: "zh_TW",
                            onShow: function(e) {
                                $(e.target).find(".modal-content").css("color", "black")
                                $(e.target).find(".modal-content").addClass("bg-light")
                                $(e.target).find(".modal-dialog").addClass("modal-lg")
                            } ,
                            onShown: function(e) {
                                $(e.target).find("th").addClass("text-dark")
                                $(e.target).find(".bootbox-body").addClass("container")
                                setTimeout(function () {
                                    excelTable.draw(true);
                                    excelTable.columns.adjust().draw();
                                    excelTable.responsive.recalc().columns.adjust();
                                }, 100);
                            } ,
                        });

                    },
                    'error': (res) => {
                        if(res.status == 404){
                            result = JSON.parse(res.responseText);
                            message = $("<table>", {
                                "id": "excelTable",
                                class: "display table-bordered ",
                                style: "width:100%; white-space: nowrap;"
                            });
                            excelTable = $(message).DataTable({
                                "orderClasses": false,
                                "responsive": true,
                                "language": {
                                    url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
                                },
                                "createdRow": function (row, data, dataIndex) {
                                    $(row).addClass('table-primary');
                                    $(row).addClass('text-dark');
                                    $(row).addClass('font-weight-bold');
                                },
                                "columns": [{ title: "姓名" }, { title: "編號" },{ title: "身份證後四碼" }]
                            });
                            result.forEach((ele, index) => {
                                excelTable.row.add([
                                    ele["user"],
                                    ele["amwayNumber"],
                                    ele["id4"],
                                ])
                            });
                            messageMain = $("<div>", {text:"請修正名單再申請一次", class:"text-dark"})
                            messageMain.append(message) 
    
                            bootbox.alert({
                                closeButton: false,
                                scrollable: true,
                                className: "modal-dialog-centered",
                                container: "body",
                                title: '<div class="text-dark">申請名單錯誤清單</div>',
                                message: message,
                                locale: "zh_TW",
                                centerVertical: true,
                                onShow: function(e) {
                                    $(e.target).find(".modal-content").css("color", "black")
                                    $(e.target).find(".modal-content").addClass("bg-light")
                                    $(e.target).find(".modal-dialog").addClass("modal-lg")
                                } ,
                                onShown: function(e) {
                                    $(e.target).find("th").addClass("text-dark")
                                    $(e.target).find(".bootbox-body").addClass("container")
                                    setTimeout(function () {
                                        excelTable.draw(true);
                                        excelTable.columns.adjust().draw();
                                        excelTable.responsive.recalc().columns.adjust();
                                    }, 100);
                                } ,
                            });
                        } else if(res.status == 400) {
                            bootbox.alert({
                                closeButton: false,
                                message: res.responseText,
                                locale: "zh_TW",
                                centerVertical: true,
                                onShow: function(e) {
                                    $(e.target).find(".modal-content").addClass("bg-dark")
                                } ,
                            });
                        } else {
                            bootbox.alert({
                                closeButton: false,
                                message: "此功能異常,請聯繫系統人員",
                                locale: "zh_TW",
                                centerVertical: true,
                                onShow: function(e) {
                                    $(e.target).find(".modal-content").addClass("bg-dark")
                                } ,
                            });
                        }
                        
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
