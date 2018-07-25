var url="https://raw.githubusercontent.com/awaisrauf/GE2018/master/prediction_code/results/graph_results/punjab.json";

var request = new XMLHttpRequest();
request.open("GET", url, false);
request.send(null)
var Data = JSON.parse(request.response);
   
   
   
   
// ########################################################
// Popularity History chart   

var PTI_line = Data["PTI Line"];
var PMLN_line = Data["PMLN Line"];
var PPP_line = Data["PPP Line"];


Highcharts.chart('container', {
    chart: {
        type: 'spline',
		marginTop: 5
    },
    title: {
        text: null
    },
    xAxis: {
        title: {
            text: 'Popularity Level in %'
        },
        type: 'datetime',
        labels: {
        formatter: function() {
       		 return Highcharts.dateFormat('%a %d %b', this.value);
      }
     
     }
     },
	  exporting: { enabled: false },  
    yAxis: {
        title: {
            text: 'Popularity in %'
        },
        labels: {
            formatter: function () {
                return this.value + '%';
            }
        }
    },
	
	
	
    tooltip: {
        crosshairs: true,
        shared: true
    },
    plotOptions: {
        spline: {
            marker: {
                radius: 4,
                lineColor: '#666666',
                lineWidth: 1
            }
        }
    },
    series: [{
        name: 'PTI',
        
        data: PTI_line,
        color: '#FF0000',
        pointStart: Date.UTC(2018, 6, 7),
		    pointInterval: 24 * 3600 * 1000 // one day

    }, {
        name: 'PMLN',
        data: PMLN_line,
        color: '#00FF00',
		    pointStart: Date.UTC(2018, 6, 7),
		    pointInterval: 24 * 3600 * 1000 // one day
    },

    
	
    {
        name: 'PPP',
        data: PPP_line,
		    pointStart: Date.UTC(2018, 6, 7),
		    pointInterval: 24 * 3600 * 1000 // one day
    }
    ]
});

//#################################################
// Daily Popularity 


var Punjab = Data["Punjab"];
;

Highcharts.chart('container1', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Popularity Levels of the day (10 July)'
    },
    xAxis: {
        categories: ['PTI', 'PMLN', 'PPP']
    },
    credits: {
        enabled: false
    },
	
	exporting: { enabled: false },
    series: [ {
        name: 'Punajb',
        data: Punjab
    }
    
	
	]
});