

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
            document.getElementById("DDnotExist").style.color = "black";
            document.getElementById("amwayDiamond").value = returnData.diamond

        }
        },
        error: function (xhr, ajaxOptions, thrownError) {



        }
    });
}
