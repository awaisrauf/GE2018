
Highcharts.chart('overallProjection', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false,
		marginTop: 5

    },
    tooltip: {
        pointFormat: ' <b>{point.y} Seats</b>'
    },
    title:{
        text: null,
    style: {
        display: 'none'
    }
    },
    
    plotOptions: {
        pie: {
        colors: [
     '#D32929', 
     '#0DBD15', 
     '#060606', 
     '#FDFDFD',
     '#24CBE5', 
     '#FF9655', 
     '#FFF263', 
     '#6AF9C4'
   ],
        allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.y}',
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%']
        }
    },
    exporting: { enabled: false },
    series: [{
        type: 'pie',
        name: 'Projection',
        innerSize: '50%',
        data: [
            ['PTI', 17],
            ['PMLN', 1],
            ['PPPP', 28],
            ['MQM', 2],
            ['IND', 7],
			['PSP',2]
            ['Others',11],
            
        ]
    }]
});

