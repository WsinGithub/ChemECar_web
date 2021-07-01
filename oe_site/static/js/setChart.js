var chart = echarts.init(document.getElementById('chart'));

option = {
    grid:{
        left:'5%',
        right:'5%',
        top:'5%',
        bottom:'8%',
    },
    xAxis: {
        type:'value',
        minInterval:1,
    },
    yAxis: {
        type: 'value',
    },
    series: [
        {
            type: 'line',
            symbolSize: 4,
            symbol: 'circle',
            smooth: true,
            // $$$ chart update duration
            animationDurationUpdate:100,
            animationEasingUpdate: 'quinticOut',
        },
    ],

};
