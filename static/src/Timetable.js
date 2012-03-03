function Timetable() {
}
Timetable.prototype.addTalk = function(elem, div) {
  
	var $div=$(div);
		
	var url=elem.href;
//	var settings={
//			success: function	success(data, textStatus, jqXHR){
//				$div.html(data);
//			},
//			error: function error(jqXHR, textStatus, errorThrown){ console.error(this.name+": "+jqXHR); },
//			dataType: "html"
//	};
	
//	$.ajax( url, settings );
	
	$div.load(url);
	
};