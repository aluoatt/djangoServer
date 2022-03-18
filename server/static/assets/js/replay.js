$(document).ready(() => {
    rThead = $("#replayCalendar").find("th");
    today = moment()
    monDay = today.subtract(today.day()-1, "days")
    for(i = 0; i< 5; i=i+1){
        dateString = monDay.format("l")
        newHead = $("<th>", { text: `${dateString}(${monDay.format('dddd')})` });
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
    classRoomList = ["CYP", "CYS","CYL", "CYZ", "CYJ1",
        "CYJ2", "CYM", "CYN1", "CYN2",
        "CYK", "CYD"]
    classRoomChinese = {
        "CYP": "台北教室", 
        "CYS": "新竹教室", 
        "CYL": "中壢教室", 
        "CYZ": "台中教室", 
        "CYJ1":"嘉義135",
        "CYJ2":"嘉義245", 
        "CYM":"良美", 
        "CYN1":"永康135", 
        "CYN2":"永康245",
        "CYK": "高雄教室",
        "CYD": "屏東教室"
    }
    
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
            classRoomChinese[classRoom],
            tmp[0],
            tmp[1],
            tmp[2],
            tmp[3],
            tmp[4],
        ])
    });

})
