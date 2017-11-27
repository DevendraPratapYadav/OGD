google.charts.load('current', {'packages':['corechart', 'controls']});
      google.charts.setOnLoadCallback(decideGraphs);

      var chart;
      var dashboard;
      var donutRangeSlider;
      var data2;

      
      function parseData(jsonObj)
      {
        // var jsonObj = JSON.parse('[{ "year": "2014","value1": 1, "value2": 10.5},{ "year": "2015","value1": 2, "value2": 20.5},{ "year": "2016","value1": 3, "value2": 1.5}]');
        // var jsonObj = JSON.parse('[{ "year": 2014.12,"value1": 1, "value2": 10.5},{ "year": 2015.67,"value1": 2, "value2": 20.5},{ "year": 2016.23,"value1": 3, "value2": 1.5}]');

        console.log("this the real shit = ");
        console.log(jsonObj);
        var jsonObj = JSON.parse(jsonObj);
        // console.log(jsonObj);

        var noOfRecords = jsonObj.length;
        console.log(noOfRecords);

        data2 = new Array();

        var labels = Object.keys(jsonObj[0]);

        data2.push(labels);

        for (var i = 0; i < noOfRecords; i++) {
          var newRow = Object.values(jsonObj[i]);
          data2.push(newRow);
        };

      }

      function decideGraphs()
      {
        parseData();
        var htmlToInsert='';
        if(typeof data2[1][0]=='number')
        {
          document.getElementById("parent2").innerHTML = htmlToInsert;
          drawChart();
        }
        else if(typeof data2[1][0]=='string')
        {
          drawHistoAndPie('PieChart',1);
          document.getElementById("parent1").innerHTML = htmlToInsert;
        }
      }

      function drawChart() {


        var data = new google.visualization.arrayToDataTable(data2);

        dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

        donutRangeSlider = new google.visualization.ControlWrapper({
          'controlType': 'NumberRangeFilter',
          'containerId': 'rangeSlider_div',
          'options': {
            'filterColumnLabel': 'Year'
          }
        });


        chart = new google.visualization.ChartWrapper({
          'chartType': 'ColumnChart',
          'containerId': 'chart_div',
          'options': {
            'width': 800,
            'height': 500,
            'legend': 'right',
          'explorer': { 
            'actions': ['dragToZoom', 'rightClickToReset'],
            'axis': 'horizontal',
            'keepInBounds': true,
            'maxZoomIn': 4.0
          }
          }
        });

        dashboard.bind(donutRangeSlider, chart);

        changeMenu(chart.getChartType());

        dashboard.draw(data);

        // console.log(appropriateDataForHistogram(2,data2));
        // console.log(chart.getOption('axes'));
        

      }

      function appropriateDataForHistogram(colNumber,data)
      {
        var convertedData = new Array();
        labelsRow = new Array();
        labelsRow.push(data[0][0]);
        labelsRow.push(data[0][colNumber]);
        convertedData.push(labelsRow);
        for (var i = 1; i < data.length; i++) {
          var newRecord = new Array();
          newRecord.push(data[i][0]);
          newRecord.push(data[i][colNumber])
          convertedData.push(newRecord);
        };
        return convertedData;

      }

      function changeChartType(chartType)
      {
        if(chartType=='Histogram')
        {
          var newDataForHistogram = appropriateDataForHistogram(2,data2);
          chart.setChartType(chartType);
          donutRangeSlider.setOption('filterColumnLabel','values');
          dashboard.draw(google.visualization.arrayToDataTable(newDataForHistogram))

        }
        else if(chartType=='PieChart')
        {
          var newDataForHistogram = appropriateDataForHistogram(2,data2);
          chart.setChartType(chartType);
          donutRangeSlider.setOption('filterColumnLabel','values');
          dashboard.draw(google.visualization.arrayToDataTable(newDataForHistogram))

        }
        else
        {
          chart.setChartType(chartType);
          donutRangeSlider.setOption('filterColumnLabel','Year');
          dashboard.draw(google.visualization.arrayToDataTable(data2));
          changeMenu(chartType);
        }
      }

      function changeMenu(chartType)
      {
        if (chartType=='ColumnChart')
        {var htmlToInsert = '<button class="btn1" onclick="changeStack();">Toggle stack</button>';
        document.getElementById("availableProperties").innerHTML = htmlToInsert;
        }
        else
        {
          var htmlToInsert = '';
        document.getElementById("availableProperties").innerHTML = htmlToInsert;
        }
      }

      function changeStack()
      {

          if (chart.getOption('isStacked')==null || chart.getOption('isStacked')==false)
          {
            chart.setOption('isStacked', true);
          }
          else
          {
            chart.setOption('isStacked', false);
          }

          chart.draw();
      }

      function drawHistoAndPie(chartType,colNumber)
      {
        

        var histoData = appropriateDataForHistogram(colNumber,data2);
        console.log(histoData);
        console.log(histoData[0]);
        var data = new google.visualization.arrayToDataTable(histoData);
        var chart2;
        if (chartType=='Histogram')
        {
          chart2 = new google.visualization.Histogram(document.getElementById('chart_div_2'));
        }
        else if(chartType=='PieChart')
        {
          chart2 = new google.visualization.PieChart(document.getElementById('chart_div_2'));
        }
        console.log(histoData[0][1]);
        var options =  {
            'title': histoData[0][1],
            'width': 800,
            'height': 500,
            'legend': 'right'
          };

        chart2.draw(data,options);
      }
