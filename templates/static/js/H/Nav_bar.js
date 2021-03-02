function make_html(link, sym)
    {return '<li class="page-item"><a class="page-link" href="'+link+'">'+sym+'</a></li>'}

function make_link(page_num){
    if(page_num<1){page_num=1}
    if(page_num>page_count){page_num=page_count}
    var url = currentURL
    url.searchParams.set("page", page_num)
    return url
}

var html=""

html += '<li class="page-item"> <a class="page-link" href="'+make_link(current_page-1)+'" aria-label="Previous">'+
            '<span aria-hidden="true">&laquo;</span> <span class="sr-only">Previous</span>'+
        '</a> </li>'

html += make_html(make_link(1), 1)

if(current_page>=4 && page_count>=7) {html += make_html("#", "…")}
if(current_page>=3 && page_count>=7) {html += make_html(make_link(current_page-1), current_page-1)}

if(current_page!=1){html += make_html(make_link(current_page), current_page)}

if(current_page<=page_count-1 && page_count>=7) {html += make_html(make_link(current_page+1), current_page+1)}
if(current_page<=page_count-1 && page_count>=7) {html += make_html("#", "…")}

if(current_page!=page_count){html += make_html(make_link(page_count), page_count)}

html += '<li class="page-item"> <a class="page-link" href="'+make_link(current_page+1)+'" aria-label="Next">'+
            '<span aria-hidden="true">&raquo;</span> <span class="sr-only">Next</span>'+
        '</a> </li>'

$('#pagination-nav').append(html);