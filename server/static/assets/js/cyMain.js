

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