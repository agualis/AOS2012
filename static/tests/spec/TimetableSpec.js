describe("Timetable", function() {
  var timetable;
  
  beforeEach(function() {
	timetable = new Timetable();
//    song = new Song();
  });

  it("test_add_talk_to_schedule_grid", function() {
	  
	var $talk=$('<div id="talk"></div>');  
	
	var $link=$('<a href="/talk/new/10/1/"></a>');  
	
	timetable.addTalk($link[0],$talk);
	
	var ajaxComplete=false
	$talk.ajaxComplete(function handler(event, XMLHttpRequest, ajaxOptions){
		ajaxComplete=true;
	});
	
	waitsFor(function(){
		return ajaxComplete;
	});
	runs(function () {
		expect($talk.find('form').length).toEqual(1);
	});
  });

});