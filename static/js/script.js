$(function(){
	$("#clear").click(function(event) {
		event.preventDefault();
		$("#url").val("");
		$("#results").empty();
		$(this).blur();
	});
});