


// $(document).ready(function() {
// $.ajaxSetup({ cache: false }); // This part addresses an IE bug. without it, IE will only load the first number and will never refresh
// var my_refresh = setInterval(function() {
// let csrftoken = '{{ csrf_token }}'
// var requestURL = "/returnPDF/" + document.getElementById("fileID").value;
// var dataJSON = {};
// // dataJSON["fileId"] = "iPhone";
// // dataJSON["Company"] = "Apple";
//
// $.ajax({
//         url: requestURL,
//         data: JSON.stringify(dataJSON),
//         headers:{'X-CSRFToken':csrftoken},
//         type: "POST",
//         dataType: "json",
//         contentType: "application/json;charset=utf-8",
//         success: function(returnData){
//             console.log(returnData);
//         },
//         error: function(xhr, ajaxOptions, thrownError){
//             console.log(xhr.status);
//             console.log(thrownError);
//         }
//     });
//
// }, 3000); // the "1000"
// });