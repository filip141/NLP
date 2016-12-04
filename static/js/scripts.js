
function find_words(keywords, textAreaContent){
    console.log(keywords);
    var splitted = textAreaContent.split(" ");
    for(var i = 0; i < keywords.length; i++){
        var randomColour = '#'+(Math.random()*0xFFFFFF<<0).toString(16);
        var lookupArray = keywords[i];
        for(var word_idx in splitted){
            var word = splitted[word_idx];
            var idx = lookupArray.indexOf(word)
            if(idx > -1){
                splitted[word_idx] = '<span style="color: ' + randomColour
                         + '"><b>' + word + '</b></span>';
            }
        }
    }
    var newText = splitted.join(" ");
    var topics = keywords[0][0] + ", " + keywords[0][1] + ", " + keywords[0][2];
    $("#locked_id").empty();
    $("#est_topic").empty();
    $("<p>" + newText + "</p>").appendTo("#locked_id");
    $("<p>" + "Estimated Topic: " + topics + "</p>").appendTo("#est_topic");
}

function topic_words(topic_w){
    var newTable = ""
    console.log(topic_w);
    for(var topic_idx in topic_w){
        var sel_topic = topic_w[topic_idx];
        newTable = newTable + "<tr>";
        for(var word_idx = 0; word_idx < 12; word_idx++){
            var sel_word = sel_topic[word_idx];
            newTable = newTable + '<td>';
            newTable = newTable + sel_word;
            newTable = newTable + '</td>';
        }
        newTable = newTable + "</tr>";
    }
    $("#topic_words").empty();
    console.log(newTable)
    $(newTable).appendTo("#topic_words");
}

$(document).ready(function(){
    $(".locked_table").hide();
    $("#purelda").click(function(){
        var textAreaContent = $("#unlocked_textarea").val();
        var data = {
            'text': textAreaContent,
        }
        $.ajax({
                url: '/purelda',
                method: 'POST',
                dataType: "json",
                data: JSON.stringify(data, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(data) {
                    var keywords = data.keywords;
                    var topic = data.topic_words;
                    find_words(keywords, textAreaContent);
                    topic_words(topic);
                },
                 error: function(error) {
                    console.log(error);
                }
        });
    });


    $("#gensimlda").click(function(){
        var textAreaContent = $("#unlocked_textarea").val();
        var data = {
            'text': textAreaContent,
        }
        $.ajax({
                url: '/gensimlda',
                method: 'POST',
                dataType: "json",
                data: JSON.stringify(data, null, '\t'),
                contentType: 'application/json;charset=UTF-8',
                success: function(data) {
                    var keywords = data.keywords;
                    var topic = data.topic_words;
                    find_words(keywords, textAreaContent);
                    topic_words(topic);
                },
                 error: function(error) {
                    console.log(error);
                }
        });
    });

    $('#modesel li a').click(function(){
        var choosen = $(this).text();
        if(choosen == "Keywords"){
            $(".locked_table").hide();
            $(".locked_box").show();
        }
        else{
            $(".locked_box").hide();
            $(".locked_table").show();
        }
    });

});