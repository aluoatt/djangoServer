$(document).ready(() => {

    window.myTable = $('#myTable').DataTable({
        "orderClasses": false,
        "responsive": true,
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
        'user', 'email', 'phone', 'jobTitle',
        'ClassRoomName', 'amwayDD', 'auditStatus', 'acceptBtn'
    ]
    myTableHeadChinese = [
        '姓名', '信箱', '電話', '職務',
        '教室', '上手白金', '狀態', '操作'
    ]
    $.ajax({
        'url': location.origin + "/managerPages/getTempUserAccount",
        'method': 'GET',
        'processData': false,
        'contentType': false,
        'headers': { 'X-CSRFToken': getCookie('csrftoken') },
        'success': (res) => {
            data = JSON.parse(res)

            for (i in data) {
                fields = data[i]
                userid = fields['id']
                tempRow = myTable.row.add([
                    fields['user'],
                    fields['email'],
                    fields['phone'],
                    fields['jobTitle'],
                    fields['ClassRoomName'],
                    fields['amwayDD'],
                    fields['auditStatus'],
                    `<a id="${userid}_acceptBtn" data-toggle="modal"
                        data-target="#auditConfirmAccept"
                        class="button_modified h4 btn btn-outline-success btn-sm">
                        ${fields['auditStatus'] === '已寄信' ? "重送" : "同意"}
                    </a>
                    <a id="${userid}_removeBtn" class="button_remove h4 btn btn-outline-success btn-sm" data-toggle="modal"
                        data-target="#auditConfirmRemove">
                        移除
                    </a>`
                ])
                tempRow.node().id = `${userid}_tr`
                tempRow.nodes().to$()
                    .find('td')
                    .each(function (index) {
                        if (index > 6) {
                            return
                        }
                        $(this).attr('id', userid + "_" + myTableHead[index]);
                    });

                gender = fields['gender']
                amwayAward = fields['amwayAward']
                amwayNumber = fields['amwayNumber']
                //insert data for modify perpose
                moHTML = `
                    <td style="display:none" id = "${userid}_amwayNumber" data-th="會員編號">
                        ${amwayNumber}
                    </td>
                    <td style="display:none" id = "${userid}_gender"  data-th="性別">
                        ${gender}
                    </td>
                    <td style="display:none" id = "${userid}_amwayAward" data-th="獎銜">
                        ${amwayAward}
                    </td>
                `
                $(moHTML).appendTo($("#hiddenData"));
            }

            myTable.columns().every(function (index) {
                if (index > 6) {
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
        id = id.split("_")[0];

        document.getElementById("modal_user").innerHTML = ("<mark style=\"color: red\">姓名:</mark>"
            + document.getElementById(id + "_user").innerHTML)

        document.getElementById("modal_amwayNumber").innerHTML = ("<mark style=\"color: red\">會員編號:</mark>"
            + document.getElementById(id + "_amwayNumber").innerHTML)

        document.getElementById("modal_jobTitle").innerHTML = ("<mark style=\"color: red\">職務:</mark>"
            + document.getElementById(id + "_jobTitle").innerHTML)

        document.getElementById("modal_amwayAward").innerHTML = ("<mark style=\"color: red\">獎銜:</mark>"
            + document.getElementById(id + "_amwayAward").innerHTML)

        document.getElementById("modal_gender").innerHTML = ("<mark style=\"color: red\">性別:</mark>"
            + document.getElementById(id + "_gender").innerHTML)
        document.getElementById("modal_amwayDD").innerHTML = ("<mark style=\"color: red\">上手白金:</mark>"
            + document.getElementById(id + "_amwayDD").innerHTML)

        document.getElementById("auditAcceptCurrentId").value = id
    });

    $("#myTable").on("click", ".button_remove", (event) => {
        id = $(event.target)[0].id;
        id = id.split("_")[0];

        document.getElementById("Remove_modal_user").innerHTML = ("<mark style=\"color: red\">姓名:</mark>"
            + document.getElementById(id + "_user").innerHTML)

        document.getElementById("Remove_modal_amwayNumber").innerHTML = ("<mark style=\"color: red\">會員編號:</mark>"
            + document.getElementById(id + "_amwayNumber").innerHTML)

        document.getElementById("Remove_modal_jobTitle").innerHTML = ("<mark style=\"color: red\">職務:</mark>"
            + document.getElementById(id + "_jobTitle").innerHTML)

        document.getElementById("Remove_modal_amwayAward").innerHTML = ("<mark style=\"color: red\">獎銜:</mark>"
            + document.getElementById(id + "_amwayAward").innerHTML)

        document.getElementById("Remove_modal_amwayDD").innerHTML = ("<mark style=\"color: red\">上手白金:</mark>"
            + document.getElementById(id + "_amwayDD").innerHTML)

        document.getElementById("auditRemoveCurrentId").value = id
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

function auditFinalRemove(csrftoken) {
    var requestURL = '/managerPages/removeAuditAccount';
    var curId = $('#auditRemoveCurrentId').val();
    var dataJSON = { "id": $('#auditRemoveCurrentId').val(), };
    $.ajax({
        url: requestURL,
        data: JSON.stringify(dataJSON),
        headers: { 'X-CSRFToken': csrftoken },
        type: "POST",
        method: "POST",
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        success: function (returnData) {
            if (returnData.status) {
                window.myTable.row('#' + curId + '_tr').remove().draw();
            }
            else {
                document.getElementById(curId + "_auditStatus").innerHTML = "發生錯誤，請重整頁面"

            }
        },
        error: function (xhr, ajaxOptions, thrownError) {

            document.getElementById(curId + "_auditStatus").innerHTML = "發生錯誤，請重整頁面"


        }
    });
}

function auditFinalAccept(csrftoken) {
    var requestURL = '/managerPages/AcceptAuditAccount';

    var curId = $('#auditAcceptCurrentId').val();
    document.getElementById(curId + "_auditStatus").innerHTML = "處理中"
    var dataJSON = { "id": $('#auditAcceptCurrentId').val(), };
    $.ajax({
        url: requestURL,
        data: JSON.stringify(dataJSON),
        headers: { 'X-CSRFToken': csrftoken },
        type: "POST",
        method: "POST",
        dataType: "json",
        async: true,
        contentType: "application/json;charset=utf-8",
        success: function (returnData) {
            if (returnData.status) {
                document.getElementById(curId + "_auditStatus").innerHTML = "已寄信"
                document.getElementById(curId + "_acceptBtn").innerHTML = "重送"
                document.getElementById(curId + "_acceptBtn").setAttribute("class", "button_modified h4 btn btn-outline-primary btn-sm");
            }
            else {
                document.getElementById(curId + "_auditStatus").innerHTML = "發生錯誤，請重整頁面"

            }
        },
        error: function (xhr, ajaxOptions, thrownError) {

            document.getElementById(curId + "_auditStatus").innerHTML = "發生錯誤，請重整頁面"


        }
    });

}