document.addEventListener("DOMContentLoaded", function() {
  var jqXHR_Data = $.ajax({
					type: "POST",
					url: "http://localhost:5000/getTableNames",
					async: false,
					crossDomain: true,
    				contentType: 'application/json;charset=UTF-8',
    				success: function(data){
    					// alert(data);
    					// console.log(data);
    					// console.log(data);
    					var jsData = JSON.parse(data);
    					// alert(jsData);
    					console.log(jsData);
    					populateDatasetList(jsData['result']);
    				}
				});
});

function goToAbout(){
	window.location="http://localhost/ogd/about.html";
}

function goToHelp(){
	window.location="http://localhost/ogd/help.html";
}

// window.onload = function() {
  
// };

function loadDataset() {
	var name = document.getElementById("dataset_name").value;

	var dataString = name;

	if (name == '') {
		alert("Please Fill Dataset Name");
	} else {
	/*
			AJAX code to submit form.
			$.ajax({
				type: "GET",
				url: "getDataset.php",
				data: dataString,
				success: function(data) {
					alert(data);
					var jsData = JSON.parse(data);
					// generateTable(jsData);
					generateTableNew(jsData);
					var jqXHR_Data = $.ajax({
						type: "POST",
						url: "http://localhost:5000/loadTable",
						async: false,
						data: JSON.stringify({input:data}, null, '\t'),
	    				contentType: 'application/json;charset=UTF-8',
	    				success: function(data){
	    					alert(data);
	    					console.log(data);
	    				}
					});
				}
			});
	*/
		document.getElementById("loadTest").disabled = 'disabled';
		document.getElementById("loadTest").disabled = '';

		var jsObject = {"input":dataString};

		var jqXHR_Data = $.ajax({
					type: "POST",
					url: "http://localhost:5000/loadTable",
					async: false,
					data: JSON.stringify(jsObject, null, '\t'),
					crossDomain: true,
    				contentType: 'application/json;charset=UTF-8',
    				success: function(data){
    					// alert(data);
    					// console.log(data);
    					// console.log(data);
    					real_order_data = data;	
    					var jsData = JSON.parse(data);
    					// alert(jsData);
						generateTableNew(jsData,real_order_data);
    				}
				});

	}

	return false;
}

var raw_data_glob;
var data_col_select_glob;
var data_inp_param_glob;
var data_col_names_glob;
var data_email_glob;

function getParseData(raw_data){

	var data = [];

	for(var i=0;i<raw_data.length;i++){
		
		var temp = [];

		for(item in raw_data[i]){
			temp.push(raw_data[i][item]);
		}

		data.push(temp);
	}

	return data;
}

function getParseDataColumns(raw_data){

	var data = [];

	if(raw_data.length==0){
		return data;
	}

	for(item in raw_data[0]){
		var temp = {};	
		temp.title = item;

		data.push(temp);
	}

	return data;
}

function generateTable(data){

	var columnDefinition = new Object();
	columnDefinition.columns = parseData(data);
	columnDefinition.fitColumns = true;

	$("#display_table").tabulator(columnDefinition);
	$("#display_table").tabulator("setData",data);							
}

function generateTableNew(raw_data,real_order_data){

	document.getElementById("table-content-separator").className = "visible";	

	document.getElementById("contain-table").innerHTML = '<div style="background-color: #FFFFFF;border-color: #000000;padding: 20px;border-radius: 13px;box-shadow: 0px 0px 15px #888888;"><table id="example" class="display" ></table></div>';

	data_col_names_glob = getParseDataColumns(raw_data);

	var table = $('#example').DataTable({
        data: getParseData(raw_data),
        columns: data_col_names_glob,
        "scrollX": true
    });

	generateForm(raw_data);
	// console.log(raw_data);
	// parseGData(real_order_data);
	jsonGlob = real_order_data;
	gload();
	// $.getScript('visual.js', function() { parseData(real_order_data); });
}

function parseData(data){
	var columns = new Array();

	var keys = Object.keys(data[0]);

	for (var i in keys) {
		var temp = new Object();
		temp.title = keys[i];
		temp.field = keys[i];
		// temp.headerSort = false;
		columns.push(temp);
	}

	return columns;
}

function generateForm(raw_data){
	raw_data_glob = raw_data;
	if(raw_data.length==0){
		return data;
	}

	document.getElementById("ml-content-separator").className = "visible";

	document.getElementById("contain-selection").innerHTML = '<div id="div_column-selection" style="background-color: #FFFFFF;border-color: #000000;padding: 20px;border-radius: 13px;box-shadow: 0px 0px 15px #888888;"><div id="column-selection" class="container-fluid"></div></div>'

	var index = 0;

	var row_dom = "";

	for(item in raw_data[0]){		
		var col_name = item;
		row_dom += '<div id="row_'+index+'" class="form-group row"><div class="col-lg-3"><strong>'+col_name+'</strong></div><div class="col-lg-9"><label class="radio-inline"><input type="radio" name="optradio_'+index+'"> Input</label><label class="radio-inline"><input type="radio" name="optradio_'+index+'" > Output</label><label class="radio-inline"><input type="radio" name="optradio_'+index+'" checked="checked"> None</label></div></div>';
		index++;
	}

	// this.disabled=true;this.value='Submitting...';
	var submit_button_dom = '<div id="row_'+index+'" class="form-group row"><input id = "generateForm" onclick="scrapeColSelection()" type="button" value="Continue Selection"></div>';
	row_dom = '<form id="column-selection-form">'+row_dom+submit_button_dom+'</form>';

	document.getElementById("column-selection").innerHTML = row_dom;
}

function scrapeColSelection(){
	document.getElementById("generateForm").disabled = 'disabled';
	document.getElementById("generateForm").disabled = '';
	
	var ele = document.getElementById("column-selection-form").elements;

	ele = Object.values(ele);

	var ip_col = [];
	var op_col = [];

	console.log(ele);

	for(var i=0;i<ele.length-1;i=i+3){
		
		if(ele[i].checked){
			ip_col.push(i/3);
		}
		else if(ele[i+1].checked){
			op_col.push(i/3);
		}
	}	
	console.log(ip_col);
	console.log(op_col);

	// var jqXHR_Data = $.ajax({
	// 				type: "POST",
	// 				url: "http://localhost:5000/runAnalytics",
	// 				async: false,
	// 				data: JSON.stringify({input:[ip_col,op_col]}, null, '\t'),
 //    				contentType: 'application/json;charset=UTF-8'
	// 			});		

	// alert(jqXHR_Data.responseText);

	generateInputForm(ip_col,op_col);

	data_col_select_glob = [ip_col,op_col];	
}

function generateInputForm(ip_col,op_col){
	if(raw_data_glob.length==0){
		return data;
	}
	document.getElementById("contain-parameter").innerHTML = '<div id = "ip-selection" class="container-fluid" style="background-color: #FFFFFF;border-color: #000000;padding: 20px;border-radius: 13px;box-shadow: 0px 0px 15px #888888;"><form><div class="row" style="text-align: center;"><div class="col-lg-3"><!-- <p><strong>Year</strong></p> --></div><div class="col-lg-3"><strong>Start</strong></div><div class="col-lg-3"><strong>Number of Values</strong></div><div class="col-lg-3"><strong>Increment</strong></div></div></form></div>'


	var row_dom = "";

	var all_col = Object.keys(raw_data_glob[0]);

	for(var i=0;i<ip_col.length;i++){
		var col_name = all_col[ip_col[i]];
		row_dom += '<div class="row"><div class="col-lg-3"><p><strong>'+col_name+'</strong></p></div><div class="col-lg-3"><label><input id = "txt_s_'+ip_col[i]+'" type="text" name="ip_text" style="border:2px solid #000000"></label></div><div class="col-lg-3"><label><input id = "txt_n_'+ip_col[i]+'" type="text" name="ip_text" style="border:2px solid #000000"></label></div><div class="col-lg-3"><label><input id = "txt_i_'+ip_col[i]+'" type="text" name="ip_text" style="border:2px solid #000000"></label></div></div>';
	}

	// this.disabled=true;this.value='Submitting...';
	var submit_button_dom = '<div class="form-group row"><input id = "generateInputForm" onclick="scrapeInpParameters()" type="button" value="Predict"></div>';
	row_dom = '<form id="input-selection-form">'+row_dom+submit_button_dom+'</form>';

	document.getElementById("ip-selection").innerHTML += row_dom;
}

function scrapeInpParameters(){
	// document.getElementById("generateInputForm").disabled = 'disabled';
	// document.getElementById("generateInputForm").disabled = '';

	var s_ele = Object.values($('input[id^="txt_s_"]'));
	var n_ele = Object.values($('input[id^="txt_n_"]'));
	var i_ele = Object.values($('input[id^="txt_i_"]'));

	var sar = [];
	var nar = [];
	var iar = [];
	var indices = [];
	var inp_param =[];

	for(var i=0;i<s_ele.length-2;i++){
		var index = parseInt((s_ele[i].id).substring(6));
		// sar.push(s_ele[i].value);
		// nar.push(n_ele[i].value);
		// iar.push(i_ele[i].value);
		// indices.push(index);
		var temp = [index,s_ele[i].value,n_ele[i].value,i_ele[i].value];
		inp_param.push(temp);
	}

	data_inp_param_glob = inp_param;

	console.log(inp_param);

	var jqXHR_Data = $.ajax({
					type: "POST",
					url: "http://localhost:5000/runMLComponent",
					async: false,
					data: JSON.stringify({input:[data_col_select_glob[0],data_col_select_glob[1],data_inp_param_glob]}, null, '\t'),
    				contentType: 'application/json;charset=UTF-8',
					success: function(data) {
						var img_url = "/ogd/visual.jpg";
						console.log(img_url);
						// document.getElementById('yourimage').src = "url/of/image.jpg?random="+new Date().getTime();
						document.getElementById("visualizationImage").src = img_url+'?random='+new Date().getTime();
						// alert("image should have loaded");
						// $('#visualization').html('<img class="img-responsive"  src="'+img_url+'"/>');
						console.log(data.result);
						populateResult(data.result);
						// alert(data.result);
					}
				});		
}

function populateDatasetList(search_options){
	var ele = document.getElementById("search_options");
	// alert("yes");

	// var search_options = ["birthrate_statewise_1971-2012_per1000","registered_motor_vehicles_in_thousands","railwayfinancialresults_incrores","fdi_equity_in_flows_in_million_usd","annual_survey_of_datasets","riceproduction_statewise_inthousandtonnes"];

	for(var i=0;i<search_options.length;i++){
		var search_item = '<option value="'+search_options[i]+'">';
		ele.innerHTML += search_item;
	}
}

function populateResult(result){
	var i=0;
	var j=0;

	row_data = [];

	for(i=0;i<result.length;i++){
		row_ar = [];
    	for (j=0;j<result[i].length;j++){
    		if(result[i][j] == ','){

    		}
    		else {
    			row_ar.push(result[i][j]);
    		}
    	}
    	row_data.push(row_ar);
	} 

	col_data = [];

	for(i=0;i<data_col_select_glob[0].length;i++){
		var temp = data_col_select_glob[0][i];
		col_data.push(data_col_names_glob[temp]);
	}

	for(i=0;i<data_col_select_glob[1].length;i++){
		var temp = data_col_select_glob[1][i];
		col_data.push(data_col_names_glob[temp]);
	}

	console.log("************");
	console.log(data_col_select_glob);
	console.log(data_col_names_glob);
	console.log(row_data);
	console.log(col_data);

	generateResultTable(row_data,col_data);
}

function generateResultTable(row_data,col_data){
	document.getElementById("contain-result-table").innerHTML = '<div style="background-color: #FFFFFF;border-color: #000000;padding: 20px;border-radius: 13px;box-shadow: 0px 0px 15px #888888;"><table id="resultDataTable" class="display" style="min-width: 100%;"></table></div>';

	console.log(row_data);
	console.log(col_data);

	var table = $('#resultDataTable').DataTable({
        data: row_data,
        columns: col_data
        // "scrollX": true
    });
	console.log("complete data");
    console.log(table.rows().data().toArray());

    var i=0;
    var j=0;
    arobj = [];
    for(i=0;i<row_data.length;i++){
    	temp = {};
    	for(j=0;j<col_data.length;j++){
    		arobj[col_data[j]] = row_data[i][j];
    	}
    }
    console.log(arobj);
}

// this is almost the end [Snehil Ameta] [User Data save and load]

function getUserId(){
	console.log(localStorage.getItem("email"));
	return localStorage.getItem("email");
}

//saves userData into sql database
//TODO: implement http://localhost:5000/saveUserData
//		input: json object which has all user data from current session
//		output: none
function saveUserData()
{
	var userId = getUserId();
	var datasetName = document.getElementById("dataset_name").value;
	var ioSelection = data_col_select_glob;
	var inputParam = data_inp_param_glob;
	var colNames = data_col_names_glob;

	var user_data = [userId, datasetName, ioSelection, inputParam, colNames];
	var jsObject = {"input":user_data,"id":userId};

	console.log("User Data Object");
	console.log(jsObject);

	var jqXHR_Data = $.ajax({
						type: "POST",
						url: "http://localhost:5000/saveUserData",
						async: false,
						data: JSON.stringify(jsObject, null, '\t'),
						crossDomain: true,
						contentType: 'application/json;charset=UTF-8',
						success: function(data){
						}
	});

	alert("User Data Saved");
}

//opens a new window with user history
function loadUserData(){

	var userId = getUserId();

	data_email_glob = userId;

	// var f = document.createElement("form");
	// f.setAttribute('method',"post");
	// f.setAttribute('action',"history.html");

	// var textfield = document.createElement("input");
	// textfield.type = "text";
	// textfield.name = "user_data";
	// textfield.value = userId;

	window.open('/ogd/history.html','User History');
	// f.submit();

	// generateUserHistoryView();
}

// this is the end [Sakshum and Jatin] [Visualization]

function gload(){
	document.getElementById("visual-content-separator").className = "visible";
	document.getElementById("visual-content").className = "visible";
	google.charts.load('current', {'packages':['corechart', 'controls']});
	google.charts.setOnLoadCallback(decideGraphs);
	// alert("gload called");
	// alert(jsonGlob);

	document.getElementById("corrContainer").className = "visible";

	document.getElementById("mlContainer").className="visible";

	generateCorrInputForm(data_col_names_glob);
}

var chart;
var dashboard;
var donutRangeSlider;
var data2;
var rangeSliderColumnNumber = 0;
var data2ForHistogram;
var noOfRecords;

function parseGData()
{
    // var jsonObj = JSON.parse('[{ "year": "2014","value1": 1, "value2": 10.5},{ "year": "2015","value1": 2, "value2": 20.5},{ "year": "2016","value1": 3, "value2": 1.5}]');

    // var jsonObj = JSON.parse('[{ "year": 2014,"value1": 1, "value2": 10.5},{ "year": 2015,"value1": 2, "value2": 20.5},{ "year": 2016,"value1": 3, "value2": 1.5}]');

    var jsonObj = JSON.parse(jsonGlob);

    console.log(jsonObj);
    
    for(var i=0;i<jsonObj.length;i++){
        delete jsonObj[i].Entry;
    }

    noOfRecords = jsonObj.length;

    // console.log(noOfRecords);

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
	parseGData();
	// dataToStringType();
	var htmlToInsert='';
	if(typeof data2[1][0]=='number')
	{
		document.getElementById("parent2").innerHTML = htmlToInsert;
		console.log(data2[0][rangeSliderColumnNumber])
		drawChart(data2[0][rangeSliderColumnNumber]);
	}
	else if(typeof data2[1][0]=='string')
	{
		drawHistoAndPie('PieChart',1);
		document.getElementById("parent1").innerHTML = htmlToInsert;
	}
}

function dataToStringType() // This function makes data to string type and lets you plot histograms and pie data
{
	for (var i = 1; i <= noOfRecords; i++) {
		data2[i][0] = String(data2[i][0]);
	};
}

function drawChart(filterColumnLabel) {

	if (filterColumnLabel === undefined) {
		filterColumnLabel = data2[0][rangeSliderColumnNumber];
	}

	var data = new google.visualization.arrayToDataTable(data2);

	dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

	donutRangeSlider = new google.visualization.ControlWrapper({
		'controlType': 'NumberRangeFilter',
		'containerId': 'rangeSlider_div',
		'options': {
		'filterColumnLabel': filterColumnLabel
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
				'maxZoomIn': 20.0
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
	chart.setChartType(chartType);
	donutRangeSlider.setOption('filterColumnLabel',data2[0][rangeSliderColumnNumber]);
	dashboard.draw(google.visualization.arrayToDataTable(data2));
	changeMenu(chartType);
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

//this is really the end [Simarjeet] [User Login and Stuff]
function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	localStorage.setItem("image", profile.getImageUrl());
	localStorage.setItem("email", profile.getEmail());
	localStorage.setItem("name", profile.getName());
	
	window.location="http://localhost/ogd/index.html";
}

function signOut() {
	alert("You have signed out sucessfully");
	window.location="http://localhost/ogd/login.html";
}

function topbarSave() {
	//add method
	alert("Save here");
}

function topbarLoad() {
	//add method
	alert("Load here");
	
}

function topbarExtra() {
	//add method
	alert("Extra here");
}

function onLoadHome() {
	$("#pic").attr('src',localStorage.getItem("image"));
	$("#email").text(localStorage.getItem("email"));
	
	updateDatabase(localStorage.getItem("name"), localStorage.getItem("email"));
}

function updateDatabase(name, email) {
	var posting = $.post("test.php", {
		name: name,	
		email: email
	});
	
	posting.done(function(data){
		// alert(data);
	});
	
	posting.fail(function(data){
		// alert("DB query failed");
	});
}

//plase stop and end this [Snehil Ameta] [Correlation]

function generateCorrInputForm(colNames){
	document.getElementById("corr-contain-selection").innerHTML = '<div style="background-color: #FFFFFF;border-color: #000000;padding: 20px;border-radius: 13px;box-shadow: 0px 0px 15px #888888;"><div id="corr-column-selection" class="container-fluid"></div></div>'

	var index = 0;

	var row_dom = "";

	for(var i=0;i<colNames.length;i++){		
		var col_name = colNames[i]["title"];
		row_dom += '<div class="checkbox"><label><input type="checkbox" value="" id="row_'+i+'"><em>'+col_name+'</em></label></div>';
	}

	// this.disabled=true;this.value='Submitting...';
	var submit_button_dom = '<div id="corr_row_'+index+'" class="form-group row"><input id = "generateCorrForm" onclick="scrapeCorrColSelection()" type="button" value="Continue Selection"></div>';
	row_dom = '<form id="corr-column-selection-form">'+row_dom+submit_button_dom+'</form>';

	document.getElementById("corr-column-selection").innerHTML = row_dom;
}

function scrapeCorrColSelection(){
	// document.getElementById("generateForm").disabled = 'disabled';
	// document.getElementById("generateForm").disabled = '';
	
	var ele = document.getElementById("corr-column-selection-form").elements;

	ele = Object.values(ele);

	var ip_col = [1];
	var op_col = [];

	console.log(ele);

	for(var i=2;i<ele.length;i=i+1){
		if(ele[i].checked){
			op_col.push(i);
		}
		else {
		}
	}	
	console.log(ip_col);
	console.log(op_col);

	var jqXHR_Data = $.ajax({
					type: "POST",
					url: "http://localhost:5000/runCorrComponent",
					async: false,
					data: JSON.stringify({"input":[ip_col,op_col]}, null, '\t'),
    				contentType: 'application/json;charset=UTF-8',
					success: function(data) {
						var img_url = "/ogd/corr.png";
						console.log(img_url);
						// document.getElementById('yourimage').src = "url/of/image.jpg?random="+new Date().getTime();
						document.getElementById("corrVisualizationImage").src = img_url+'?random='+new Date().getTime();
						// alert("image should have loaded");
						// $('#visualization').html('<img class="img-responsive"  src="'+img_url+'"/>');
						// console.log(data.result);
						// populateResult(data.result);
						// alert(data.result);
					}
				});
}


