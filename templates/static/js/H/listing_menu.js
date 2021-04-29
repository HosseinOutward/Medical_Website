var image_list = response.responseJSON.results;

for(i=0; i<image_list.length; i++) {
    var html = "<tr>";// real_id_imag

    html += '<td>'+'('+image_list[i].real_id_count_imag+')'
        +image_list[i].real_id_imag+'</td>';

    html += '<td><img class="user-avatar fa-square" src="'+image_list[i].thumbnail_imag+'" alt="User Avatar"></td>'

    if(image_list[i].label_data_imag != null){
        html += '<td> <span class="badge badge-success ml-2 mb-2 float-right">لیبل دار</span> </td>';
        html += '<td> <a href=/labeling/'+image_list[i].pk+' type="button"\n' +
            'class="btn btn-outline-primary float-right"\n' +
            'style="font-size: 12px"> تغییر </a> </td>';
    } else {
        html += '<td> <span class="badge badge-primary ml-2 mb-2 float-right">بدون لیبل</span> </td>';
        html += '<td> <a href=/labeling/'+image_list[i].pk+' type="button"\n' +
            'class="btn btn-outline-success float-right"\n' +
            'style="font-size: 12px"> شروع لیبل گذاری </a> </td>';
    }

    html += '<td> <a href="/edit_image/'+image_list[i].pk+'/" type="submit" class="btn btn-info ">\n'
        +'<span >تغییر اطلاعات ورودی</span></a></td>';

    html += '<td> <button type="button" class="btn btn-secondary" data-toggle="modal" data-target="#filterModal" onclick="getFilters('+ image_list[i].pk +')">' +
            '<span>نمایش لیبل‌ها</span></button></td>';
    html += '</tr>';

    $('#Image_List').find('tbody').append(html);
}

function getFilters(indx) {
    var apiURL='/_api/image/'+indx+'/'
    var response = $.ajax({
        url: apiURL,
        dataType: 'json',
        async: false,
        type: 'GET',
    });
    const names = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10",
                            "T11", "T12", "T13", "Max Aortic diameter dorsal" , "Max Aortic diameter ventral",
                            "carina", "Apex", "Dorsal border of CVC", "ventral CVC", "Cranial", "Heart", "CVC", "Aorta", "region 1", "region 2", "region 3"]
    var labels = JSON.parse(response.responseJSON.label_data_imag);
    var body = '';
    var data = {}
    for (var name of names)
        data[name] = [];
    for (var label of labels) {
        if (label.from_name) {
            for (var l of label.value[label.type]) {
                data[l].push(label.type);
            }
        }
    }
    for (const [name, type] of Object.entries(data)) {
        body += '<tr>';
        body += '<td>' + type + '</td>';
        body += '<td>' + name + '</td>';
        body += '</tr>';
    }
    $('#labelsList').find('tbody').html(body);
}