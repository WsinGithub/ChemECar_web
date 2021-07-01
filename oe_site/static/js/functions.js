function set_chart() {
    chart.setOption(option);
}

function load_data() {
    // console.log(record_on)
    myajax = $.ajax({
        // The URL for the request
        url: "get_data",
        // Whether this is a POST or GET request
        type: "GET",
        // The type of data we expect back
        dataType: "json",
        async: false,
        success: function (jsondata) {
            server_info = eval(jsondata);
        },
        error: function () {
        }
    });
    // console.log(server_info)

    record_on=server_info.record_on;
    if (record_on) {
        // var t = [];
        // var d = [];
        ymin=server_info.data[0][1];
        ymax=server_info.data[0][1];
        for (let data of server_info.data) {
            // t.push(data[0])
            // d.push(data[1])
            if(data[1]>ymax){
                ymax=data[1];
            }
            if(data[1]<ymin){
                ymin=data[1];
            }
        }
        option.yAxis.min=ymin;
        option.yAxis.max=ymax;
        // option.xAxis.data = t;
        // option.series[0].data = d;
        option.xAxis.min=server_info.data[0][0];
        option.xAxis.max=server_info.data[server_info.data.length-1][0];
        option.series[0].data=server_info.data;
        set_chart();
    }

    if (is_owner === false && record_on === true){
        $("#spector").fadeIn(400);
    }else{
        $("#spector").hide();
    }
    // console.log(is_owner);
    // console.log(record_on);
}
