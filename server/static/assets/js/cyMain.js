

function confirmViewFile(id,title,costpoint,userpoint){
    document.getElementById("fileCheckTitle").innerHTML = "兌換【" + title + "】";
    document.getElementById("needPoint").innerHTML = "需點數" + costpoint + "點";
    document.getElementById("userpoint").innerHTML = "剩餘點數:" + userpoint;
    document.getElementById("fileViewID").value = id;
    document.getElementById("fileID").action = "/viewFilePage/"+id;
}

function confirmViewFileSubmit(){
    document.fileID.submit();
}
