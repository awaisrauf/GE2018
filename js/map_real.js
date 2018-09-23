
var url="https://raw.githubusercontent.com/awaisrauf/GE2018/master/election_prediction/results/result_real.json";

var request = new XMLHttpRequest();
request.open("GET", url, false);
request.send(null)
var Data = JSON.parse(request.response);
//console.log(Data["NA-1"])
//console.log(Data)




function drawChart() {
    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Latitude');
    data.addColumn('number', 'Longitude');
    data.addColumn('string', 'Party');
    data.addColumn('number', 'Party Number');
    

     var text = "";
		var i;
		for (i = 1; i < 272; i++) {
   	   text = "NA-" + i;
       conData = Data[text];
       data.addRows([[conData[1],conData[0],conData[2],conData[3]]]);
    }
    
    var options = {
                region: 'PK',
                colorAxis: {
                colors: ['#FF0000', '#008000', '#000000', '#fff', '#FFFF00','#FFA500','#800080'],
                values: [5, 6, 7, 8,9,10,11]
                },
                tooltip: { textStyle: { fontName: '"Verdana"', fontSize: 14 } },
                keepAspectRatio: true,
                height: 600,
                width: 1000,
                legend: false,
            }
    
    var chart = new google.visualization.GeoChart(document.querySelector('#chart_div'));
    chart.draw(data, options);
}
google.load('visualization', '1', {packages:['geochart'], callback: drawChart});