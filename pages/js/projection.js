
Highcharts.chart('overallProjection', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    title: {
        text: 'Genearl Election 2018 Projection',
        align: 'center',
        verticalAlign: 'above',
        y: 40
    },
    tooltip: {
        pointFormat: ' <b>{point.y} Seats</b>'
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
        name: 'Nationl Assembly Seats Projection',
        innerSize: '50%',
        data: [
            ['PTI', 115],
            ['PMLN', 88],
            ['PPPP', 34],
            ['MMA', 6],
            ['IND', 11],
            ['Others',18],
            
        ]
    }]
});

