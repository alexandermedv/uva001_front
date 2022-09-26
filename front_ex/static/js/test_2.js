$(document).ready(function() {
    $('#download-report-button').click(function(e) {
        e.preventDefault();
        alert("cors!");
    });
});    
// $(document).ready(function() {
//     $('#download-report-button').click(function(e) {
//         e.preventDefault();
//         const url = 'http://msc199-sdb04.domain.local:9002/api/reports/report_test';
//         $.get(url)
//         .done(function get_async_status(data){
//             // alert(jQuery.param(data));
//             const uuid = data.task_id;
//             const url_ask = 'http://msc199-sdb04.domain.local:9002/api/reports/report_test?task_id='+uuid;
//             $.get(url_ask)
//             .done(function(data){
//                 const state = data.state;
//                 if (state == 'SUCCESS'){
//                     $('#download-report-button').text('Скачать фаил (xlsx)');
//                     clearTimeout(get_async_status);

//                     const download_href = 'http://msc199-sdb04.domain.local:9002/api/uploads/test.xlsx';
//                     // $.get(download_href);
//                     const a = document.createElement('a');
//                     document.body.appendChild(a);
//                     a.style='display: none';
//                     // a.href=asyncData.location;
//                     a.href = 'http://msc199-sdb04.domain.local:9002/api/uploads/test.xlsx'
//                     // a.download=asyncData.filename;
//                     a.click();
//                 }
//                 else {
//                     $('#download-report-button').text('Загрузка...');
//                     // 0,5 миллисекунд
//                     setTimeout(function() { get_async_status(data) }, 1000);
//                 }
//                 // alert(`task_id=${task_id}, state=${state}, kwargs=${kwargs}`);
//             });
//         });            
//     });        
// });
alert('test');