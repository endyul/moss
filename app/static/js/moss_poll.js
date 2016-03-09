var moss_chart;
var interval_fetch;

var fetchRealtimeData = function() {
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

function drawFireLine() {
  $.getJSON('settings/fire-value', function(data){
    var fire_value = data['fire_value'];
    if(fire_value)
      moss_chart.yAxis[0].addPlotLine({
        value: fire_value,
        color: 'red',
        width: 2,
        id: 'fire_value',
      });
  });
}

function loadGraph(load_function) {
  Highcharts.setOptions({
    global: {
      useUTC: false
    }
  });

  var options = {
    chart: {
       renderTo: 'container',
       type: 'spline',
       events: {
         load: load_function
       }
    },
    title: {
      text: 'Moss @ SCIR'
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
      max: 40
    },
    series: [{name:'data center'}],
    tooltip:{
      valueSuffix: '°C'
    }
  };
  moss_chart = new Highcharts.Chart(options);
}


$(document).ready(function() {
  loadGraph(function(){
    fetchData('data/recent');
    interval_fetch = setInterval(fetchRealtimeData, 1000);
    drawFireLine();
  });
});

var fetchData = function(url) {
  $.getJSON(url, function(data){
    for(var i = 0; i < data['points'].length; ++i) {
      data['points'][i][0] *= 1000;
    }
    moss_chart.series[0].setData(data['points']);
  });
}

$('#realtime-tab').click(function (e) {
  console.log('toggle realtime view');
  e.preventDefault();
  loadGraph(function(){
    fetchData('data/recent');
    interval_fetch = setInterval(fetchRealtimeData, 1000);
    drawFireLine();
  });
});

$("#day-tab").click(function (e) {
  console.log('toggle day view');
  e.preventDefault();
  loadGraph(function(){
    clearInterval(interval_fetch);
    fetchData('data/day');
    drawFireLine();
  });
});

$('#week-tab').click(function (e) {
  console.log('toggle week view');
  e.preventDefault();
  loadGraph(function(){
    clearInterval(interval_fetch);
    fetchData('data/week');
    drawFireLine();
  });
});

$('#month-tab').click(function (e) {
  console.log('toggle month view');
  e.preventDefault();
  loadGraph(function(){
    clearInterval(interval_fetch);
    fetchData('data/month');
    drawFireLine();
  });
});

$('#year-tab').click(function (e) {
  console.log('toggle year view');
  e.preventDefault();
  loadGraph(function(){
    clearInterval(interval_fetch);
    fetchData('data/year');
    drawFireLine();
  });
});
