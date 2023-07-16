$(function(){
	$("#clear").click(function(event) {
		event.preventDefault();
		$("#url").val("");
		$("#results").empty();
		$("#qparams").empty();
		$("#comment").remove();
		$(this).blur();
	});
	$("#copy").click(function(event){
		let comment = encodeURIComponent($("#share-comment").val());
		let baseUrl = window.location.href.split('#')[0];
		baseUrl = baseUrl.split('&comment')[0];
		let shareUrl = baseUrl + "&comment=" + comment;
		console.log(comment);
		console.log(shareUrl);
		navigator.clipboard.writeText(shareUrl);
		$("#copy-status").fadeIn().delay( 5000 ).fadeOut( 400 )
	});
	$("#copy-button").click(function(event){
		let comment = encodeURIComponent($("#share-comment").val());
		let baseUrl = window.location.href.split('#')[0];
		baseUrl = baseUrl.split('&comment')[0];
		let shareUrl = baseUrl + "&comment=" + comment;
		let siteUrl = window.location.href.split('?')[0].replace("v3/", "");
		let buttonText = "[![Try it!](" + siteUrl + "static/img/try-trove-api-console.svg" + ")](" + shareUrl + ")";
		console.log(buttonText);
		navigator.clipboard.writeText(buttonText);
		$("#copy-status").fadeIn().delay( 5000 ).fadeOut( 400 )
	});
});