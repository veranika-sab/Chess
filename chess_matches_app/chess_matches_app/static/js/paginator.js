$(document).ready(function(){
    $("#next, #previous").click(function(e){
        var url = $(this).attr('href');

        $.getJSON(url, function(data) {
            var tbl_body = "";
            $.each(data, function() {
                var tbl_row = "";
                var tournament_id;
                $.each(this, function(index , value) {
                    if (index==0) {
                        tournament_id = value;
                    }
                    if (index==1) {
                        tbl_row += "<td><a href='/tournaments/"+tournament_id+"'>"+value+"</a></td>";
                    }
                    else {
                        if (index==5) {
                            if (value==true) {
                                tbl_row += "<td> Завершен </td>";
                            }
                            else {
                                tbl_row += "<td> Не завершен </td>";
                            }
                        }
                        else {
                            tbl_row += "<td>"+value+"</td>";
                        }
                    }
                })
                tbl_body += "<tr class='success'>"+tbl_row+"</tr>";
            })
            $(".table tbody").html(tbl_body);
        });
        e.preventDefault();

        // change href for previous/next links and value of current page

        var current_page = $(".page-current").text();
        var page_next_href = $("#next").attr("href");
        var page_previous_href = $("#previous").attr("href");
        var page_amount = $(".page-amount").text();
        var page_regex = /page=([^&]+)/g;
        var clicked_link_id = $(this).attr('id');

        if (page_previous_href == "/tournaments/ajax/?page=0") { // make link previous enable if its not the first page
            $('#previous').attr("hidden", false);
            page_previous_href = $("#previous").attr("href");
        }

        if (page_next_href == "/tournaments/ajax/?page=None" || page_next_href == "/tournaments/ajax/?page=" + (+page_amount + 1) + "") { // make link next enable if its not the last page
            $('#next').attr("hidden", false);
            page_next_href = page_next_href.replace(page_regex, "page=" + (+page_amount + 1) + "");
            $("#next").attr("href", page_next_href);
        }

        var page_next_value = page_next_href.match("page=([^&]+)")[1];
        var page_previous_value = page_previous_href.match("page=([^&]+)")[1];

        if (clicked_link_id=='next') {
            $(".page-current").text(+current_page+1);
            page_next_value = +page_next_value + 1;
            page_previous_value = +page_previous_value + 1;
        }
        else {
            $(".page-current").text(+current_page-1);
            page_next_value = +page_next_value - 1;
            page_previous_value = +page_previous_value - 1;
        }

        page_next_href = url.replace(page_regex, "page=" + page_next_value + "");
        page_previous_href = url.replace(page_regex, "page=" + page_previous_value + "");

        $('#next').attr("href", page_next_href);
        $('#previous').attr("href", page_previous_href);

        if (page_previous_value == "0") {
            $('#previous').attr("hidden", true);
        }

        if (page_next_value > page_amount) {
            $('#next').attr("hidden", true);
        }
    });
});
