$(function(){
	$("#clear").click(function(event) {
		event.preventDefault();
		$("#url").val("");
		$("#results").empty();
		$("#comment").remove();
		$(this).blur();
	});
	$("#copy").click(function(event){
		let comment = encodeURIComponent($("#share-comment").val());
		let baseUrl = window.location.href.split('#')[0];
		let shareUrl = baseUrl + "&comment=" + comment;
		console.log(comment);
		console.log(shareUrl);
		navigator.clipboard.writeText(shareUrl);
		$("#copy-status").fadeIn().delay( 5000 ).fadeOut( 400 )
	});
});