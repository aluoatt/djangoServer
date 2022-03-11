$(document).ready(() => {
    rThead = $("#replayCalendar").find("th");
    today = moment()
    monDay = today.subtract(today.day()-1, "days")
    for(i = 0; i< 5; i=i+1){
        dateString = monDay.format("l")
        newHead = $("<th>", { text: dateString });
        rThead.after(newHead);
        rThead =  newHead;
        monDay.add(1, "days")
    }
    
    replayTable = $('#replayCalendar').DataTable({
        "orderClasses": false,
        "responsive": true,
        "paging": false,
        "ordering": false,
        "info": false,
        "searching": false,
        "language": {
            url: location.origin + '/static/assets/i18n/datatable/zh_Hant.json'
        },
        "createdRow": function (row, data, dataIndex) {
            $(row).addClass('table-warning');
            $(row).addClass('text-dark');
            $(row).addClass('font-weight-bold');
        }
    });
    classRoomList = ["CYP", "CYL", "CYZ", "CYJ1",
        "CYJ2", "CYN1", "CYN2",
        "CYK"]
    
    classRoomList.forEach((classRoom, index) => {
        tmp = []
        if(window.weekVideo[classRoom] == undefined){
            for(i=0;i<5;i=i+1){
                tmp[i] = ""
            } 
        } else {
            //TODO: set date to relative
            for(i=0;i<5;i=i+1){
                if(window.weekVideo[classRoom][i] != ""){
                    title = window.weekVideo[classRoom][i]['title'].split("_")[2]
                    fileid = window.weekVideo[classRoom][i]['id']
                    tmp[i] = `<a target="_blank" href="${location.origin}/courseReplay/viewFilePage/${fileid}">${title}</a>`
                } else {
                    tmp[i] = ""
                }
            }
        }
        
        replayTable.row.add([
            classRoom,
            tmp[0],
            tmp[1],
            tmp[2],
            tmp[3],
            tmp[4],
        ])
    });

})

function confirmViewFile(id, title, costpoint, userpoint) {
    document.getElementById("fileCheckTitle").innerHTML = "兌換【" + title + "】" + "需點數" + costpoint + "點";
    // document.getElementById("needPoint").innerHTML = "需點數" + costpoint + "點";
    document.getElementById("userpoint").innerHTML = "目前剩餘點數:" + userpoint;
    document.getElementById("fileViewID").value = id;
    document.getElementById("fileIDModal").action = "/acceptRecord/" + id;
}

function confirmViewFileSubmit() {
    document.fileIDModal.submit();
}

function searPageViewFileSubmit(id) {
    document.getElementById("fileIDModal").action = "/viewFilePage/" + id;
    document.getElementById("fileIDModal").submit();
}


function ViewFileSubmit(id) {
    document.getElementById("fileIDview").action = "/viewFilePage/" + id;
    document.getElementById("fileIDview").submit();
}

