"use strict";

$(document).ready(function () {

    //do a search and add the results to the DOM
    $("#input-form").submit(function (evt) {
        evt.preventDefault();
        const formData = {"start_word": $("#start-word").val(),
                          "end_word": $("#end-word").val()};
        $.post("/do-search.json", formData, function (results) {
            //put the results in the right places
            $("#dfs-med-path-len").html(results.DFS.med_path_length);
            $("#bfs-med-path-len").html(results.BFS.med_path_length);
            $("#dfs-med-time").html(results.DFS.med_search_time);
            $("#bfs-med-time").html(results.BFS.med_search_time);
            $("#dfs-med-efficiency").html(results.DFS.med_efficiency);
            $("#bfs-med-efficiency").html(results.BFS.med_efficiency);
            $("#dfs-sample-path").html(results.DFS.sample_path.join(" -> "));
            $("#bfs-sample-path").html(results.BFS.sample_path.join(" -> "));
        });
    });


    /////////////////////////////////////////////////////////////////////////
    // ChartJS stuff

    //reset the max-word-length dropdown (so it matches the default, specified
    //below)
    $("#max-word-length").val("5");

    //set some global options for all charts
    const dfsColor = "blue";
    const bfsColor = "red";
    Chart.defaults.global.elements.line.fill = false;
    Chart.defaults.global.animation.duration = 750;

    //the chart, chart data, and options are declared globally so they can be
    //changed by various functions
    let resultsChart;
    let dataBySubject;
    let currentSubject = "pathLength";
    let currentMaxWordLength = 5;

    let chartData = {
        "labels": undefined, //will get set by AJAX call to get data
        "datasets": [
            {"label": "BFS",
             "data": undefined, //will get set by AJAX call to get data
             "borderColor": bfsColor,
             "pointBackgroundColor": bfsColor,
            },
            {"label": "DFS",
             "data": undefined, //will get set by AJAX call to get data
             "borderColor": dfsColor,
             "pointBackgroundColor": dfsColor,
            }
        ]
    };

    let chartOptions = {
        "scales": {
            "yAxes": [{
                "ticks": {
                    "beginAtZero": true
                },
                "scaleLabel": {
                    "display": true,
                    "labelString": "num words in path",
                    "fontSize": 20,
                }
            }],
            "xAxes": [{
                "scaleLabel": {
                    "display": true,
                    "labelString": "word length",
                    "fontSize": 20,
                }
            }]
        },
        "elements": {
            "line": {
                "cubicInterpolationMode": "monotone"
            }
        }
    };


    //get the correct data for the chart from global dataBySubject data store
    function getData(subject, maxWordLength) {

        //make a deep copy of the data for the given subject so we can mess
        //with it without affecting the original
        let data = JSON.parse(JSON.stringify(dataBySubject[subject]));

        //slice the data for each search type so it only goes up through the
        //desired word length
        for (let searchType of ["BFS", "DFS"]) {
            data[searchType] = data[searchType].slice(0, maxWordLength - 1);
        }

        //return the results
        return data;
    }


    //create or update the chart
    function makeChart() {
        //get the data for the chart and put it in the appropriate places
        //in the chartData and chartOptions objects
        const data = getData(currentSubject, currentMaxWordLength);
        chartData.datasets[0].data = data.BFS;
        chartData.datasets[1].data = data.DFS;
        chartOptions.scales.yAxes[0].scaleLabel.labelString = data.yAxisLabel;

        if (resultsChart) {
            resultsChart.destroy();
        }

        //create (or recreate) the chart
        const chartContext = $("#results-graph")[0].getContext('2d');
        const chartConfig = {"type": "line",
                             "data": chartData,
                             "options": chartOptions};
        resultsChart = new Chart(chartContext, chartConfig);
    }


    //make an AJAX request on pageload to get chart data from the database
    $.get("/chart-data.json", function (results) {

        //get x-axis labels
        chartData.labels = results.wordLengths;

        //put the  data into the global dataBySubject object for later
        //reference
        dataBySubject = results;

        //make the chart
        makeChart();
    });


    //change the max word length of the chart
    $("#max-word-length").change(function (evt) {
        currentMaxWordLength = $(this).val();
        makeChart();
    });


    //change the subject of the chart
    $(".swap-chart").click(function (evt) {
        currentSubject = $(this).data("subject");
        makeChart();
    });

});

