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
        'user', 'point', 'amwayNumber', 'jobTitle', 'amwayAward',
        'addPoint', 'reducePoint', 'addReducePointByUser', 'getPointHistory'
    ]
    myTableHeadChinese = [
        '姓名', '點數', '直銷商編號', '職務', '獎銜',
        '增點', '扣點', '增扣點', '查看歷史'
    ]
    $.ajax({
        'url': location.origin + "/pointManage/allUserAccount",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            window.allUser = data
            for (i in data) {
                fields = data[i]
                username = fields['username']
                myTable.row.add([
                    fields['user'],
                    fields['point'],
                    fields['amwayNumber'],
                    fields['jobTitle'],
                    fields['amwayAward'],
                    `<a id="${username}_addPoint" class="button_modified h4 btn btn-outline-success btn-sm">+10</a>`,
                    `<a id="${username}_reducePoint" class="button_modified h4 btn btn-outline-success btn-sm">-1</a>`,
                    `<a id="${username}_addReducePointByUser" class="button_modified h4 btn btn-outline-success btn-sm">自定義</a>`,
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
                if (index > 4) {
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
             $(".dataTables_empty").text("此功能異常,請聯繫系統人員");
        }
    });

    $("#myTable").on("click", ".button_modified", (event) => {

        id = $(event.target)[0].id;
        username = id.split("_")[0];
        user = $("#" + username + "_user").html();
        action = id.split("_")[1];
        if (action === "addPoint" || action === "reducePoint" ||
            action === "addReducePointByUser") {
            msg = ""
            if (action === "addPoint")
            {
                title = "提醒"
                msg = "將為\"" + user + "\"增加 10 點"
            }
            else if (action === "reducePoint")
            {
                title = "提醒"
                msg = "將為\"" + user + "\"減少 1 點"
            }
            else if (action === "addReducePointByUser")
            {
                title = "請輸入您要給予的點數"
                msg = $("<form>", { id: "addPointForm" });
                pointDiv = $("<div>", { class: "form-group" });
                pointDiv.append($("<label>", { text: "點數" }));
                pointDiv.append($("<input>", { type: "number", name: "point", class: "form-control", placeholder: "Enter point" }));
                msg.append(pointDiv);
            }

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
                    if(action === "addReducePointByUser"){
                        formData = new FormData($("#addPointForm")[0]);
                        formData.append("username", username)
                    }else{
                        formData = new FormData();
                        formData.append("username", username)
                    }
                    
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
                alert("此功能異常,請聯繫系統人員")
            }
        });

    });

    $(".addPointByOption").on("click", addPointByOption);

    function addPointByOption (event) {
        id = $(event.target)[0].id;
        if (id === "addPointByAll" || id === "addPointByJobTitle" ||
            id === "addPointByAmwayAward" || id === "addPointByExcel" ||
            id === "addPointByCondition"  || id === "addPointByMonth") {
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
                pointDiv.append($("<label>", { text: "請選擇獎銜區間起點", for: "amwayAwardStart" }));
                pointDiv.append($("<select>", { name: "amwayAwardStart", class: "form-control custom-select", id: "amwayAwardStart" }));
                amwayAwardList.forEach((element, index) => {
                    $(pointDiv).find("#amwayAwardStart").append($("<option>", { text: element }))
                });
                pointDiv.append($("<label>", { text: "請選擇獎銜區間終點", for: "amwayAwardEnd" }));
                pointDiv.append($("<select>", { name: "amwayAwardEnd", class: "form-control custom-select", id: "amwayAwardEnd" }));
                amwayAwardList.forEach((element, index) => {
                    $(pointDiv).find("#amwayAwardEnd").append($("<option>", { text: element }))
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
            } else if (id === "addPointByCondition") {
                //僅先實作小於某點數重置到特定點數的功能
                title = "請確認要給予的點數規則"
                formInput = "";
                formInput = $("<form>", { id: "addPointForm" });
                pointDiv = $("<div>", { class: "form-group" });
                pointDiv.append($("<label>", { text: "請妥善選擇條件", for: "conditionType" }));
                pointDiv.append($("<select>", { name: "condition", class: "form-control custom-select", id: "conditionType" }));
                $(pointDiv).find("#conditionType").append($("<option>", { text: "大於" }))
                $(pointDiv).find("#conditionType").append($("<option>", { text: "小於" }))
                $(pointDiv).find("#conditionType").append($("<option>", { text: "等於" }))
                $(pointDiv).find("#conditionType").append($("<option>", { text: "大於或等於" }))
                $(pointDiv).find("#conditionType").append($("<option>", { text: "小於或等於" }))
                formInput.append(pointDiv);
                pointDiv = $("<div>", { class: "form-group" });
                pointDiv.append($("<label>", { text: "目標點數" }));
                pointDiv.append($("<input>", { type: "number", name: "conditionPoint", class: "form-control", placeholder: "目標點數" }));
                formInput.append(pointDiv);
                pointDiv = $("<div>", { class: "form-group" });
                pointDiv.append($("<label>", { text: "重置後的點數" }));
                pointDiv.append($("<input>", { type: "number", name: "resultPoint", class: "form-control", placeholder: "重置後的點數" }));
                formInput.append(pointDiv);
            } else if (id === "addPointByMonth"){
                title = "請確認要給予的點數規則"
                formInput = "";
                formInput = $("<form>", { id: "addPointForm" });

                // 特殊名單
                groupRow = $("<div>", {class:"form-row"});
                pointDiv = $("<div>", { class: "form-group col-md-4" });
                pointDiv.append($("<label>", { text: "對象" }));
                groupRow.append(pointDiv);
                pointDiv = $("<div>", { class: "form-group col-md-4" });
                pointDiv.append($("<label>", { text: "點數" }));
                groupRow.append(pointDiv);
                pointDiv = $("<div>", { class: "form-group col-md-4" });
                pointDiv.append($("<label>", { text: "移除", for: "amwayAwardEnd" }));
                groupRow.append(pointDiv)
                formInput.append(groupRow);

                if(window.monthResult["peopleList"] &&
                    Object.keys( window.monthResult["peopleList"] ).length > 0) {
                    // 存取上一次的紀錄
                    peopleList = monthResult["peopleList"];
                    peopleList.forEach((element, index) => {
                        defaultUsername = `${element["user"]} ${element["username"]}`;
                        groupRow = $("<div>", {class:"form-row"});
                        pointDiv = $("<div>", { class: "form-group col-md-4" });
                        pointDiv.append($("<select>", { name: "people[]", class: "form-control", id: "conditionType"}));
                        for (i in window.allUser) {
                            fields = window.allUser[i]
                            username = fields['username']
                            chineseName = fields['user']
                            $(pointDiv).find("#conditionType").append($("<option>", { text: `${chineseName} ${username}` }))
                        }
                        $(pointDiv).find("#conditionType").selectpicker({
                            style:'',
                            styleBase:'form-control',
                            container: 'body',
                            size:'3',
                            liveSearch: true
                        });
                        $(pointDiv).find("#conditionType").val(defaultUsername);
                        $(pointDiv).find("#conditionType").selectpicker('refresh');
                        groupRow.append(pointDiv);

                        pointDiv = $("<div>", { class: "form-group col-md-4" });
                        pointDiv.append($("<input>", { type: "number", name: "peoplePoint[]", class: "form-control", value: element["point"] }));
                        groupRow.append(pointDiv);

                        pointDiv = $("<div>", { class: "form-group col-md-4" });
                        delDiv = $("<a>", { class: "btn  btn-info", type:"button", id: "deleteItem", html:"移除"});
                        $(delDiv).on("click", deleteItemButton);
                        pointDiv.append(delDiv);
                        groupRow.append(pointDiv);

                        formInput.append(groupRow);
                    });

                }
                addDiv = $("<a>", { class: "btn btn-info", id: "addItemByPeople", html:"新增"});
                $(addDiv).on("click", addItemPeopleButton);
                formInput.append(addDiv);

                formInput.append($("<hr>", {style:"height:2px;border-width:0;color:gray;background-color:gray"}))

                // 高獎銜範圍

                groupRow = $("<div>", {class:"form-row"});

                pointDiv = $("<div>", { class: "form-group col" });
                pointDiv.append($("<label>", { text: "請選擇獎銜區間起點", for: "amwayAwardStart" }));

                groupRow.append(pointDiv);
                pointDiv = $("<div>", { class: "form-group col" });
                pointDiv.append($("<label>", { text: "請選擇獎銜區間終點", for: "amwayAwardEnd" }));
                
                groupRow.append(pointDiv);
                pointDiv = $("<div>", { class: "form-group col" });
                pointDiv.append($("<label>", { text: "點數", for: "amwayAwardEnd" }));
                groupRow.append(pointDiv);

                pointDiv = $("<div>", { class: "form-group col" });
                pointDiv.append($("<label>", { text: "移除", for: "amwayAwardEnd" }));
                groupRow.append(pointDiv)

                formInput.append(groupRow);

                if(window.monthResult["awardList"] &&
                    Object.keys( window.monthResult["awardList"] ).length > 0) {
                    // 存取上一次的紀錄
                    awardList = monthResult["awardList"]
                    awardList.forEach((element, index) => {
                        amwayAwardStart = element['awardStart']
                        amwayAwardEnd = element['awardEnd']
                        awardPoint = element['point']
                        groupRow = $("<div>", {class:"form-row"});

                        pointDiv = $("<div>", { class: "form-group col" });
                        pointDiv.append($("<select>", { name: "amwayAwardStart[]", class: "form-control custom-select", id: "amwayAwardStart" }));
                        amwayAwardList.forEach((element, index) => {
                            $(pointDiv).find("#amwayAwardStart").append($("<option>", { text: element }))
                        });
                        $(pointDiv).find("#amwayAwardStart").val(amwayAwardStart);

                        groupRow.append(pointDiv);
                        pointDiv = $("<div>", { class: "form-group col" });
                        pointDiv.append($("<select>", { name: "amwayAwardEnd[]", class: "form-control custom-select", id: "amwayAwardEnd" }));
                        amwayAwardList.forEach((element, index) => {
                            $(pointDiv).find("#amwayAwardEnd").append($("<option>", { text: element }))
                        });
                        $(pointDiv).find("#amwayAwardEnd").val(amwayAwardEnd);
                        groupRow.append(pointDiv);
                        pointDiv = $("<div>", { class: "form-group col" });
                        pointDiv.append($("<input>", { type: "number", name: "awardPoint[]", class: "form-control", placeholder: "目標點數", value:awardPoint}));
                        groupRow.append(pointDiv);

                        pointDiv = $("<div>", { class: "form-group col" });

                        delDiv = $("<a>", { class: "btn  btn-info", type:"button", id: "deleteItem", html:"移除"});
                        $(delDiv).on("click", deleteItemButton);
                        pointDiv.append(delDiv)
                        groupRow.append(pointDiv)

                        formInput.append(groupRow);
                    });

                }

                addDiv = $("<a>", { class: "btn btn-info", id: "addItemByAward", html:"新增"});
                $(addDiv).on("click", addItemAwardButton);
                formInput.append(addDiv);
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
                size: "large",
                callback: (res) => {
                    if (!res)
                        return;
                    formData = new FormData($("#addPointForm")[0]);
                    for (var pair of formData.entries()) {
                        console.log(pair[0]+ ', ' + pair[1]); 
                    }
                    if (action !== "addPointByExcel" && 
                        action !== "addPointByCondition" &&
                        action !== "addPointByMonth") {
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
                    if(action === "addPointByAmwayAward"){
                        amwayAwardStart = formData.get("amwayAwardStart")
                        amwayAwardEnd = formData.get("amwayAwardEnd")
                        if (amwayAwardList.indexOf(amwayAwardStart) > amwayAwardList.indexOf(amwayAwardEnd)) {
                            bootbox.alert({
                                closeButton: false,
                                message: "起始獎銜請勿大於獎銜終點",
                                locale: "zh_TW",
                                centerVertical: true,
                            });
                            return;
                        }
                    }

                    if (action === "addPointByCondition") {
                        conditionPoint = formData.get("conditionPoint");
                        resultPoint = formData.get("resultPoint");
                        warningMessage = "";
                        if (conditionPoint <= 0 ||
                            resultPoint <= 0) {
                            warningMessage = "請輸入大於零的點數"
                        }
                        if(warningMessage !== ""){
                            bootbox.alert({
                                closeButton: false,
                                message: warningMessage,
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

    function addItemPeopleButton(){
        groupRow = $("<div>", {class:"form-row"});

        pointDiv = $("<div>", { class: "form-group col-md-4" });
        pointDiv.append($("<select>", { name: "people[]", class: "form-control", id: "conditionType"}));
        for (i in window.allUser) {
            fields = window.allUser[i]
            username = fields['username']
            chineseName = fields['user']
            $(pointDiv).find("#conditionType").append($("<option>", { text: `${chineseName} ${username}` }))
        }
        $(pointDiv).find("#conditionType").selectpicker({
            style:'',
            styleBase:'form-control',
            container: 'body',
            size:'3',
            liveSearch: true
        });
        groupRow.append(pointDiv);
        pointDiv = $("<div>", { class: "form-group col-md-4" });
        pointDiv.append($("<input>", { type: "number", name: "peoplePoint[]", class: "form-control", placeholder: "目標點數" }));
        groupRow.append(pointDiv);

        pointDiv = $("<div>", { class: "form-group col-md-4" });
        delDiv = $("<a>", { class: "btn  btn-info", type:"button", id: "deleteItem", html:"移除"});
        $(delDiv).on("click", deleteItemButton);
        pointDiv.append(delDiv)
        groupRow.append(pointDiv)

        $("#addItemByPeople").before(groupRow)
    }

    function addItemAwardButton(){
        groupRow = $("<div>", {class:"form-row"});
        pointDiv = $("<div>", { class: "form-group col" });
        pointDiv.append($("<select>", { name: "amwayAwardStart[]", class: "form-control custom-select", id: "amwayAwardStart" }));
        amwayAwardList.forEach((element, index) => {
            $(pointDiv).find("#amwayAwardStart").append($("<option>", { text: element }))
        });

        groupRow.append(pointDiv);
        pointDiv = $("<div>", { class: "form-group col" });
        pointDiv.append($("<select>", { name: "amwayAwardEnd[]", class: "form-control custom-select", id: "amwayAwardEnd" }));
        amwayAwardList.forEach((element, index) => {
            $(pointDiv).find("#amwayAwardEnd").append($("<option>", { text: element }))
        });
        groupRow.append(pointDiv);
        pointDiv = $("<div>", { class: "form-group col" });
        pointDiv.append($("<input>", { type: "number", name: "awardPoint[]", class: "form-control", placeholder: "目標點數" }));
        groupRow.append(pointDiv);

        pointDiv = $("<div>", { class: "form-group col" });

        delDiv = $("<a>", { class: "btn  btn-info", type:"button", id: "deleteItem", html:"移除"});
        $(delDiv).on("click", deleteItemButton);
        pointDiv.append(delDiv)
        groupRow.append(pointDiv)

        formInput.append(groupRow);

        $("#addItemByAward").before(groupRow)
    }

    function deleteItemButton(e){
        $(e.target).parent().parent().remove();
    }
});
