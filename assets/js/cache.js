function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
MathJax.Hub.Queue(function () {
		if(cacheObjects.objs.length)
			dumpCache();
	}
);
cacheObjects = {objs:[]};
function dumpCache(){
	if(!cacheObjects.useragent){
		var layoutEngine = "";
		var engines = ["WebKit","Firefox","Trident","Presto"];
		for(var i = 0;i<engines.length;i++){
			if(navigator.userAgent.indexOf(engines[i])>-1)
			layoutEngine = engines[i];
		}
		cacheObjects.useragent = layoutEngine;
	}
	var csrf = getCookie('csrftoken');
	var data = {'data':JSON.stringify(cacheObjects),'csrfmiddlewaretoken':csrf};
	$.post('/mathjax_cache',data,function(resp){
		
		//handle response
	});
	cacheObjects.objs = [];
}
MathJax.Hub.Register.MessageHook("New Math",function (message) {
	var script = $(MathJax.Hub.getJaxFor(message[1]).SourceElement());
	if(script.attr("type") == "math/mml"){//can't cache
		return;
	}
	var type = "";
	var raw = script.html();
	
	if(raw.trim().length == 0)
		return;//don't cache empty equations
	var parsed = script.prev().clone();
	var html = parsed.wrap("<div>").parent().html();
	if (html.substring(0,"<div".length).toLowerCase()=="<div"){
		type = "block";
	}
	if (html.substring(0,"<span".length).toLowerCase()=="<span"){
		type = "inline";
	}
	
	var csrf_token = getCookie('csrftoken');
	var data = {
		'e':raw,
		'p':html,
		't':type
	}
	cacheObjects.objs.push(data);
	if(cacheObjects.objs.length>10)
		dumpCache();
});