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
    classRoomList = ["台北", "中壢", "台中", "嘉義 135",
        "嘉義 245", "永康 135", "永康 245",
        "高雄"]
    weekVideo  = window.weekVideo
    
    classRoomList.forEach((classRoom, index) => {
        if(weekVideo[classRoom] == undefined){
            tmp = []
            for(i=0;i<5;i=i+1){
                tmp[i] = ""
            } 
        } else {
            //TODO: set date to relative
            for(i=0;i<5;i=i+1){
                tmp[i] = weekVideo[classRoom][i]
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
    document.getElementById("fileIDModal").action = "/exchangeOption/" + id;
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

