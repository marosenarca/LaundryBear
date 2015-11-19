$(".done-button").on("click", function(){
    var status = 3;
    $.post(done-url,{status:status})
});