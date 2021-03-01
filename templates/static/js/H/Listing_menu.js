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
    html += '</tr>';

    $('#Image_List').find('tbody').append(html);
}