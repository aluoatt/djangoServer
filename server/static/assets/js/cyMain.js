

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
            document.getElementById(curId+"_acceptBtn").innerHTML = "重送"
            document.getElementById("_acceptBtn").setAttribute("class","primary");
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

function auditFilter() {
  var amwayNumbers, amwayAwards, chainYenClasses, registerDDs, registerDims;
  var amwayNumbersValue,amwayAwardsValue,chainYenClassesValue,registerDDsValue,registerDimsValue
  var amwayNumbers_input = document.getElementById("amwayNumbers_input").value.toUpperCase();
  var amwayAwards_input = document.getElementById("amwayAwards_input").value.toUpperCase();
  var chainYenClasses_input = document.getElementById("chainYenClasses_input").value.toUpperCase();
  var registerDDs_input = document.getElementById("registerDDs_input").value.toUpperCase();
  var registerDims_input = document.getElementById("registerDims_input").value.toUpperCase();

  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  for (i = 0; i < tr.length; i++) {
    amwayNumbers = tr[i].getElementsByTagName("td")[1];
    amwayAwards = tr[i].getElementsByTagName("td")[6];
    chainYenClasses = tr[i].getElementsByTagName("td")[7];
    registerDDs = tr[i].getElementsByTagName("td")[8];
    registerDims = tr[i].getElementsByTagName("td")[9];

      if (amwayNumbers) {
          amwayNumbersValue = amwayNumbers.textContent || amwayNumbers.innerText;
          amwayAwardsValue = amwayAwards.textContent || amwayAwards.innerText;
          chainYenClassesValue = chainYenClasses.textContent || chainYenClasses.innerText;
          registerDDsValue = registerDDs.textContent || registerDDs.innerText;
          registerDimsValue = registerDims.textContent || registerDims.innerText;

          if (amwayNumbersValue.toUpperCase().indexOf(amwayNumbers_input) > -1
              && amwayAwardsValue.toUpperCase().indexOf(amwayAwards_input) > -1
              && chainYenClassesValue.toUpperCase().indexOf(chainYenClasses_input) > -1
              && registerDDsValue.toUpperCase().indexOf(registerDDs_input) > -1
              && registerDimsValue.toUpperCase().indexOf(registerDims_input) > -1
          ) {
              tr[i].style.display = "";
          } else {
              tr[i].style.display = "none";
          }
      }
  }
}

function accountManagerFilter() {
    var amwayNumbers, amwayAwards, chainYenClasses, registerDDs, registerDims;
    var amwayNumbersValue, amwayAwardsValue, chainYenClassesValue, registerDDsValue, registerDimsValue
    var user, jobtitles,jobtitlesValue,userValue
    var amwayNumbers_input = document.getElementById("amwayNumbers_input").value.toUpperCase();
    var user_input = document.getElementById("user_input").value.toUpperCase();
    var jobtitles_input = document.getElementById("jobtitles_input").value.toUpperCase();
    var amwayAwards_input = document.getElementById("amwayAwards_input").value.toUpperCase();
    var chainYenClasses_input = document.getElementById("chainYenClasses_input").value.toUpperCase();
    var registerDDs_input = document.getElementById("registerDDs_input").value.toUpperCase();
    var registerDims_input = document.getElementById("registerDims_input").value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        user = tr[i].getElementsByTagName("td")[0];
        amwayNumbers = tr[i].getElementsByTagName("td")[1];
        jobtitles = tr[i].getElementsByTagName("td")[4];
        amwayAwards = tr[i].getElementsByTagName("td")[5];
        chainYenClasses = tr[i].getElementsByTagName("td")[6];
        registerDDs = tr[i].getElementsByTagName("td")[7];
        registerDims = tr[i].getElementsByTagName("td")[8];


        if (amwayNumbers) {
            amwayNumbersValue = amwayNumbers.textContent || amwayNumbers.innerText;
            amwayAwardsValue = amwayAwards.textContent || amwayAwards.innerText;
            chainYenClassesValue = chainYenClasses.textContent || chainYenClasses.innerText;
            registerDDsValue = registerDDs.textContent || registerDDs.innerText;
            registerDimsValue = registerDims.textContent || registerDims.innerText;
            jobtitlesValue = jobtitles.textContent || jobtitles.innerText;
            userValue = user.textContent || user.innerText;

            if (amwayNumbersValue.toUpperCase().indexOf(amwayNumbers_input) > -1
                && amwayAwardsValue.toUpperCase().indexOf(amwayAwards_input) > -1
                && chainYenClassesValue.toUpperCase().indexOf(chainYenClasses_input) > -1
                && registerDDsValue.toUpperCase().indexOf(registerDDs_input) > -1
                && registerDimsValue.toUpperCase().indexOf(registerDims_input) > -1
                && jobtitlesValue.toUpperCase().indexOf(jobtitles_input) > -1
                && userValue.toUpperCase().indexOf(user_input) > -1
            ) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function setEmptyByTagId(TagId) {

    document.getElementById(TagId).value = ""
    auditFilter()
}