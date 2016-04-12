$(document).ready(function(){
	// Load the Visualization API and the piechart package.
	google.charts.load('current', {'packages':['corechart', 'bar']});
	// Set a callback to run when the Google Visualization API is loaded.
	google.charts.setOnLoadCallback(drawChart);
});

function tagDistribution(element_id) {
	var json = $.ajax({
		url: "parsers/tagDist.php",
		dataType: "json",
		async: false
	}).responseText;
	var options = {
		legend: { position: 'none' },
		title: 'Tag distribution',
		chartArea: {width: '80%'},
		colors: ['#b0120a', '#ffab91'],
		histogram: {
			bucketSize: 1
		},
		hAxis: {
			title: 'Number of tags',
			minValue: 0,
			showTextEvery: 1
		},
		vAxis: {
			title: 'Number of clips'
		}
	};
	var data = new google.visualization.DataTable();
	data.addColumn('string', 'Clip title');
	data.addColumn('number', 'Clip Tags');
	data.addRows(JSON.parse(json));
	var chart = new google.visualization.Histogram(document.getElementById(element_id));
	chart.draw(data, options);
};

function lengthDistribution(element_id) {
	var json = $.ajax({
		url: "parsers/length.php",
		dataType: "json",
		async: false
	}).responseText;
	var options = {
		legend: { position: 'none' },
		title: 'Length distribution',
		chartArea: {width: '80%'},
		colors: ['#b0120a', '#ffab91'],
		hAxis: {
			title: 'Length',
			minValue: 0,
			maxValue: 600,
			textPosition: 'out',
			showTextEvery: 3
		},
		vAxis: {
			title: 'Number of clips'
		}
	};
	var data = new google.visualization.DataTable();
	data.addColumn('string', 'Clip title');
	data.addColumn('number', 'Length');
	data.addRows(JSON.parse(json));
	
	var chart = new google.visualization.Histogram(document.getElementById(element_id));
	

	chart.draw(data, options);
};

function mostUsed(element_id) {
	var json = $.ajax({
		url: "parsers/mostUsed.php",
		dataType: "json",
		async: false
	}).responseText;
	var options = {
		title: 'Tag usage',
		chartArea: {width: '80%'},
		legend: { position: 'none' },
		height: 500,
		hAxis: {
			title: 'Horizontal'
		},
		vAxis: {
			title: 'Vertical'
		}
	};
	var data = new google.visualization.DataTable();
	data.addColumn('string', 'Tag');
	data.addColumn('number', 'Count');
	data.addRows(JSON.parse(json));
	
	var chart = new google.visualization.ColumnChart(document.getElementById(element_id));
	

	chart.draw(data, options);
};


function drawChart() {
	tagDistribution('tag-dist');
	lengthDistribution('length-dist');
	mostUsed('most-used');
}