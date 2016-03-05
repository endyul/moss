var moss_chart;
function fetchData() {
  var url = '/data';
  console.log('info request data');
  $.ajax({
    url: url,
    success: function(data) {
      var series = moss_chart.series[0];
      var shift = series.data.length > 59;
      data['point'][0] *= 1000;
      moss_chart.series[0].addPoint(data['point'],
                                    true,
                                    shift);
    },
    error: function() {
      display_connection_lost();
    },
    cache: false
  });
  return true;
}

function loadGraph() {
  /*
  Highcharts.setOptions({
    global: {
      useUTC: false
    }
  });
  */

  var options = {
    chart: {
      renderTo: 'container',
      type: 'spline',
      events: {
        load: function() {
          $.getJSON('history-data', function(data){
            for(var i = 0; i < data['points'].length; ++i) {
              data['points'][i][0] *= 1000;
            }
            moss_chart.series[0].setData(data['points']);
            moss_chart.yAxis[0].addPlotLine({
              value: data['fire_value'],
              color: 'red',
              width: 2,
              id: 'fire_value',
            });
          });
        }
      },
    },
    title: {
      text: 'moss @ data center'
    },
    xAxis: {
      type: 'datetime',
      dateTimeLabelFormats: {
        millisecond: '%H:%M:%S',
        minute: '%H:%M',
        hour: '%H:%M',
      },
      tickPixelInterval: 150
    },
    yAxis: {
      title: {
        text: 'Temperature (°C)'
      },
    },
    series: [{}],
  };

  moss_chart = new Highcharts.Chart(options);
}


$(document).ready(function() {
  loadGraph();
  setInterval(fetchData, 1000);
  //fetchData();
});

