$(document).ready(function(){
    var player_one_result = $("#id_player_one_result")
    var player_two_result = $("#id_player_two_result")

    player_one_result.change(function(){
        MatchResultChange(player_one_result, player_two_result)
    });
    player_two_result.change(function(){
        MatchResultChange(player_two_result, player_one_result)
    });
});

function MatchResultChange(changedPlayerResult, toChangePlayerResult){
    var toChangePlayerValue;

    switch (changedPlayerResult.val()){
        case "-1.0":  toChangePlayerValue = "-1.0"; break;
        case "0.0":   toChangePlayerValue = "1.0";  break;
        case "0.5":   toChangePlayerValue = "0.5";  break;
        case "1.0":   toChangePlayerValue = "0.0";  break;
    }
    toChangePlayerResult.val(toChangePlayerValue);
}