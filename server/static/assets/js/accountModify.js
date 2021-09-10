$(document).ready(()=>{
    var t = $('#example').DataTable({
        "orderClasses": false,
        "responsive": true,
        "createdRow": function( row, data, dataIndex ){
            $(row).addClass('table-warning');
            $(row).addClass('text-dark');
            $(row).addClass('font-weight-bold');
        }
    });
    $(".button_history").on("click", (event)=>{
        var counter = 1;
        t.clear()
        $(".dataTables_empty").addClass("table-warning text-dark font-weight-bold");
        $(".dataTables_empty").text("目前沒有紀錄");
        id = $(event.target).parent()[0].id;
        username = id.split("_")[0];

        action   = "getAccountModifyHistory";
        formData = new FormData();
        formData.append("username", username)
        $.ajax({
            'url': location.origin + "/managerPages/" + action,
            'method': 'POST',
            'processData': false,
            'contentType': false,
            'data': formData,
            'headers': {'X-CSRFToken': getCookie('csrftoken')},
            'success': (res) => {
                console.log(res)
                data = JSON.parse(res)
                for(i in data){
                    fields = data[i]['fields']
                    t.row.add( [
                        fields['modifier'],
                        fields['recordDate'],
                        fields['modifyFielddName'],
                        fields['originFieldData'],
                        fields['RevisedData'],

                    ]  ).draw( false  );
                }
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
