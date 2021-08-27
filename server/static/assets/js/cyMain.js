

function confirmViewFile(id,title,costpoint,userpoint){
    document.getElementById("fileCheckTitle").innerHTML = "兌換【" + title + "】"+"需點數" + costpoint + "點";
    // document.getElementById("needPoint").innerHTML = "需點數" + costpoint + "點";
    document.getElementById("userpoint").innerHTML = "目前剩餘點數:" + userpoint;
    document.getElementById("fileViewID").value = id;
    document.getElementById("fileIDModal").action = "/exchangeOption/"+id;
}

function confirmViewFileSubmit(){
    document.fileIDModal.submit();
}

function searPageViewFileSubmit(id){
    document.getElementById("fileIDModal").action = "/viewFilePage/"+id;
    document.getElementById("fileIDModal").submit();
}


function ViewFileSubmit(id){
    document.getElementById("fileIDview").action = "/viewFilePage/"+id;
    document.getElementById("fileIDview").submit();
}

function registerCheckDD(csrftoken){


    var requestURL = "/checkRegDD";
    var dataJSON = {"num":$('#amwayDD').val(),};
    $.ajax({
        url: requestURL,
        data: JSON.stringify(dataJSON),
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        method: "POST",
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        success: function (returnData) {
        if (!returnData.status){

            document.getElementById("DDnotExist").style.display = "";
            document.getElementById("amwayDiamond").value = ""
            document.getElementById("DDnotExist").innerHTML = "該白金不存在"
            document.getElementById("DDnotExist").style.color = "red";
        }
        else{
            document.getElementById("DDnotExist").style.display = "";
            document.getElementById("DDnotExist").innerHTML = returnData.DDname
            document.getElementById("DDnotExist").style.color = "#EBEB00";
            document.getElementById("amwayDiamond").value = returnData.diamond

        }
        },
        error: function (xhr, ajaxOptions, thrownError) {



        }
    });
}


function auditConfirmAccept(id){
    document.getElementById("modal_user").innerHTML = ("<mark style=\"color: red\">姓名:</mark>"
                                                            + document.getElementById(id+"_user").innerHTML)

    document.getElementById("modal_amwayNumber").innerHTML = ("<mark style=\"color: red\">會員編號:</mark>"
                                                            + document.getElementById(id+"_amwayNumber").innerHTML)

    document.getElementById("modal_jobTitle").innerHTML = ("<mark style=\"color: red\">職務:</mark>"
                                                            + document.getElementById(id+"_jobTitle").innerHTML)

    document.getElementById("modal_amwayAward").innerHTML = ("<mark style=\"color: red\">獎銜:</mark>"
                                                            + document.getElementById(id+"_amwayAward").innerHTML)

    document.getElementById("modal_amwayDD").innerHTML = ("<mark style=\"color: red\">上手白金:</mark>"
                                                            + document.getElementById(id+"_amwayDD").innerHTML)

    document.getElementById("auditAcceptCurrentId").value = id
}

function auditFinalAccept(csrftoken){
    var requestURL = '/managerPages/AcceptAuditAccount';
    var curId = $('#auditAcceptCurrentId').val();
    var dataJSON = {"id":$('#auditAcceptCurrentId').val(),};
    $.ajax({
        url: requestURL,
        data: JSON.stringify(dataJSON),
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        method: "POST",
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        success: function (returnData) {
        if (returnData.status){
            document.getElementById(curId+"_auditStatus").innerHTML ="確認中"
            document.getElementById(curId+"_acceptBtn").disabled = true
        }
        else{
            document.getElementById(curId+"_auditStatus").innerHTML ="發生錯誤，請重整頁面"

        }
        },
        error: function (xhr, ajaxOptions, thrownError) {

            document.getElementById(curId+"_auditStatus").innerHTML ="發生錯誤，請重整頁面"


        }
    });

}

function auditConfirmRemove(id){
    document.getElementById("Remove_modal_user").innerHTML = ("<mark style=\"color: red\">姓名:</mark>"
                                                            + document.getElementById(id+"_user").innerHTML)

    document.getElementById("Remove_modal_amwayNumber").innerHTML = ("<mark style=\"color: red\">會員編號:</mark>"
                                                            + document.getElementById(id+"_amwayNumber").innerHTML)

    document.getElementById("Remove_modal_jobTitle").innerHTML = ("<mark style=\"color: red\">職務:</mark>"
                                                            + document.getElementById(id+"_jobTitle").innerHTML)

    document.getElementById("Remove_modal_amwayAward").innerHTML = ("<mark style=\"color: red\">獎銜:</mark>"
                                                            + document.getElementById(id+"_amwayAward").innerHTML)

    document.getElementById("Remove_modal_amwayDD").innerHTML = ("<mark style=\"color: red\">上手白金:</mark>"
                                                            + document.getElementById(id+"_amwayDD").innerHTML)

    document.getElementById("auditRemoveCurrentId").value = id
}

function auditFinalRemove(csrftoken){
    var requestURL = '/managerPages/removeAuditAccount';
    var curId = $('#auditRemoveCurrentId').val();
    var dataJSON = {"id":$('#auditRemoveCurrentId').val(),};
    $.ajax({
        url: requestURL,
        data: JSON.stringify(dataJSON),
        headers: {'X-CSRFToken': csrftoken},
        type: "POST",
        method: "POST",
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        success: function (returnData) {
        if (returnData.status){
            $('#'+curId+'_tr').remove();
        }
        else{
            document.getElementById(curId+"_auditStatus").innerHTML ="發生錯誤，請重整頁面"

        }
        },
        error: function (xhr, ajaxOptions, thrownError) {

            document.getElementById(curId+"_auditStatus").innerHTML ="發生錯誤，請重整頁面"


        }
    });
}

