$(document).ready(() => {

    myTable = $('#myArticleTable').DataTable({
        dom: '<"row"lfr>tip',
        "orderClasses": false,
        "responsive": true,
        "autoWidth": true,
        "columnDefs": [
            { "width": "10%", "targets": 4 },
            { "width": "20%", "targets": 5 },
            { "width": "10%", "targets": 0 },
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
        'title','DBClass' ,'mainClass','secClass', 'keyword',
        'describe','point','visible', "modify", "modifyHistory"
    ]
    myTableHeadChinese = [
        '標題','分類','主類','次類', '關鍵字',
        '描述','點數','可見', "編輯", "歷史"
    ]
    $.ajax({
        'url': location.origin + "/managerPages/getFileDataInfo",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)
            for (i in data) {
                fields = data[i]
                articleID = fields['id']
                myTable.row.add([
                    `<a target="_blank" href="${location.origin}/viewFilePage/${articleID}">${fields['title']}</a>`,
                    fields['DBClassCode'],
                    fields['mainClass'],
                    fields['secClass'],
                    fields['keyword'],
                    fields['describe'],
                    fields['point'],
                    fields['visible'],
                    `<a id="${articleID}_modify" class="button_modified h4 btn btn-outline-success btn-sm">
                        修改
                    </a>`,
                    `<a id="${articleID}_getModifyHistory" class="button_history h4 btn btn-outline-success btn-sm" data-toggle="modal"
                        data-target="#articleHistoryModal">
                        查看
                    </a>`
                ]).nodes().to$()
                .find('td')
                .each(function(index) {
                    $(this).attr('id', articleID +"_" + myTableHead[index] );
                });
            }
            myTable.columns().every( function (index) {
                if(myTableHeadChinese[index] !== "分類" &&
                    myTableHeadChinese[index] !== "主類" &&
                    myTableHeadChinese[index] !== "次類" &&
                    myTableHeadChinese[index] !== "點數" &&
                    myTableHeadChinese[index] !== "可見"){
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
                    .appendTo( $("#colSearch") );

                select.find("select").on( 'change', function () {
                    var val = $.fn.dataTable.util.escapeRegex(
                        $(this).val()
                    );

                    column
                        .search( val ? '^'+val+'$' : '', true, false )
                        .draw();
                } );
 
                column.data().unique().sort().each( function ( d, j ) {
                    select.find("select").append( '<option value="'+d+'">'+d+'</option>' )
                } );
            } );
            
            setTimeout(function(){
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
    
    $("#myArticleTable").on("click", ".button_modified",(event) => {

        id = $(event.target)[0].id;
        articleID = id.split("_")[0];
        action = id.split("_")[1];
        if (action === "modify") {
            formInput=""
            formInput = $("<form>", { id: "article_modify" });

            title = $(`#${articleID}_title`).html();
            DBClass = $(`#${articleID}_DBClass`).html();
            mainClass = $(`#${articleID}_mainClass`).html();
            secClass = $(`#${articleID}_secClass`).html();
            keyword = $(`#${articleID}_keyword`).html();
            describe = $(`#${articleID}_describe`).html();
            point = $(`#${articleID}_point`).html();
            visible = $(`#${articleID}_visible`).html();
            groupRow = $("<div>", {class:"form-row"});

            formInput.append($("<input>", {style:"display:none;", value:articleID, name:"id"}))
            pointDiv = $("<div>", { class: "form-group  col-md-3" });
            pointDiv.append($("<label>", { text: "資料庫類別", class: "form-check-label", for: "DBClass"}));
            pointDiv.append($("<input>", { type: "text", name: "DBClass", class: "form-control form-control-sm rounded  text-dark", value: DBClass, id: "DBClass", readonly:true, disabled: true}));
            groupRow.append(pointDiv);

            pointDiv = $("<div>", { class: "form-group col" });
            pointDiv.append($("<label>", { text: "標題", class: "form-check-label", for: "title"}));
            pointDiv.append($("<input>", { type: "text", name: "title", class: "form-control form-control-sm rounded bg-white text-dark", value: title, id: "title"}));
            groupRow.append(pointDiv);

            formInput.append(groupRow);

            groupRow = $("<div>", {class:"form-row"});

            pointDiv = $("<div>", { class: "form-group col" });
            pointDiv.append($("<label>", { text: "主類別", class: "form-check-label", for: "mainClass"}));
            pointDiv.append($("<select>", { name: "mainClass", class: "form-control custom-select", id: "mainClass"}));
            mainClassList.forEach((element, index) => {
                if (element === "無")
                    return;
                $(pointDiv).find("#mainClass").append($("<option>", {text:element}))
            });
            $(pointDiv).find("#mainClass").val(mainClass);
            groupRow.append(pointDiv);

            pointDiv = $("<div>", { class: "form-group col" });
            pointDiv.append($("<label>", { text: "次類別", class: "form-check-label", for: "secClass"}));
            pointDiv.append($("<select>", { name: "secClass", class: "form-control custom-select", id: "secClass"}));
            secClassList.forEach((element, index) => {
                if (element === "無")
                    return;
                $(pointDiv).find("#secClass").append($("<option>", {text:element}))
            });
            $(pointDiv).find("#secClass").val(secClass);
            groupRow.append(pointDiv);
            
            formInput.append(groupRow);
            
            if (window.aritclePointManage){
                pointDiv = $("<div>", { class: "form-group col" });
                pointDiv.append($("<label>", { text: "消耗點數", class: "form-check-label", for: "point"}));
                pointDiv.append($("<input>", { type: "text", name: "point", class: "form-control form-control-sm  rounded bg-white text-dark round", value: point, id: "point"}));
                groupRow.append(pointDiv);
            }
            

            pointDiv = $("<div>", { class: "form-group col" });
            pointDiv.append($("<label>", { text: "是否可見", class: "form-check-label", for: "visible"}));
            pointDiv.append($("<select>", { type: "text", name: "visible", class: "form-control", value: visible, id: "visible"}));
            $(pointDiv).find("#visible").append($("<option>", {text:"true"}))
            $(pointDiv).find("#visible").append($("<option>", {text:"false"}))
            $(pointDiv).find("#visible").val(visible);
            groupRow.append(pointDiv);
            
            formInput.append(groupRow);

            pointDiv = $("<div>", { class: "form-group" });
            pointDiv.append($("<label>", { text: "關鍵字", class: "form-check-label", for: "keyword"}));
            pointDiv.append($("<textarea>", { type: "text", name: "keyword", class: "form-control", text: keyword, id: "keyword"}));
            formInput.append(pointDiv);

            pointDiv = $("<div>", { class: "form-group" });
            pointDiv.append($("<label>", { text: "描述", class: "form-check-label", for: "describe"}));
            pointDiv.append($("<textarea>", { type: "text", name: "describe", class: "form-control", text: describe, id: "describe"}));
            formInput.append(pointDiv);

            bootbox.confirm({
                closeButton: false,
                backdrop: true,
                scrollable: true,
                title: "提醒:您正在修改文章資料!",
                message: formInput,
                locale: "zh_TW",
                container: "body",
                className:"modal-dialog-centered",
                centerVertical: true,
                callback: (res) => {
                    if (!res)
                        return;
                    formData = new FormData($("#article_modify")[0]);
                    $.ajax({
                        'url': location.origin + "/managerPages/updateFileDataInfo",
                        'method': 'POST',
                        'processData': false,
                        'contentType': false,
                        'data': formData,
                        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
                        'success': (res) => {
                            res = JSON.parse(res);
                            $(`#${articleID}_title`).html(formData.get("title"));
                            $(`#${articleID}_mainClass`).html(formData.get("mainClass"));
                            $(`#${articleID}_secClass`).html(formData.get("secClass"));
                            $(`#${articleID}_keyword`).html(formData.get("keyword"));
                            $(`#${articleID}_describe`).html(formData.get("describe"));
                            $(`#${articleID}_point`).html(formData.get("point"));
                            $(`#${articleID}_visible`).html(formData.get("visible"));
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

    window.t = $('#articleHistoryTable').DataTable({
        dom: '<"row"lfBr>tip',
        buttons: [
            {
                extend:'excel',
                title: "點數歷史紀錄",
                className: 'btn btn-sm btn-warning'
            },
            {
                extend:'print',
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

    $("#myArticleTable").on("click", ".button_history", (event) => {
        var counter = 1;
        t.clear().draw();
        $(".dataTables_empty").addClass("table-warning text-dark font-weight-bold");
        $(".dataTables_empty").text("目前沒有紀錄");
        id = $(event.target)[0].id;
        articleID = id.split("_")[0];
        action = id.split("_")[1];
        formData = new FormData();
        formData.append("id", articleID)
        $.ajax({
            'url': location.origin + "/managerPages/getArticleHistory",
            'method': 'POST',
            'processData': false,
            'contentType': false,
            'data': formData,
            'headers': { 'X-CSRFToken': getCookie('csrftoken') },
            'success': (res) => {
                data = JSON.parse(res)
                for (i in data) {
                    fields = data[i]
                    t.row.add([
                        fields['modifier'],
                        fields['recordDate'],
                        fields['title'],
                        fields['mainClass'],
                        fields['secClass'],
                        fields['keyword'],
                        fields['describe'],
                        fields['point'],
                        fields['visible'],
                    ]).draw(true);
                }
                
                setTimeout(function(){
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
