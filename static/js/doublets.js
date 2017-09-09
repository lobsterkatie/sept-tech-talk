"use strict";

$(document).ready(function () {

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


});

