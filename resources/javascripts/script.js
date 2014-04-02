$(function(){
	var form = $('.contact-form');
	var auto_agree=true;
	$("#send_sql").click(function() {
		if(!auto_agree){
			$(".confirm").show();
		}
	});	
//Timer
	if ($(".session_timer > a:nth-child(1)").lengthc) {
		var Interval = setInterval(function(){
			var timer = parseInt($(".session_timer > a:nth-child(1)")[0].text.match(/\d+/));
			if (timer-1 > 0)	{
				$(".session_timer > a:nth-child(1)").html("Осталось "+(timer-1)+" min");
			} else {
				$(".session_timer > a:nth-child(1)").html("Время вышло");
				clearInterval(Interval);
			}
		}, 6000);
		$(".session_timer > a:nth-child(1)").html("Осталось "+parseInt($(".session_timer > a:nth-child(1)")[0].text.match(/\d+/))+" min");
	}

//выпадающее меню на профайл
	$("a.dropdown-toggle").click(function(e) {
		if($(".dropdown-menu").css('display') != 'block'){
      		$(".dropdown-menu").show();
			var click = true;
			$(document).bind('click.myEvent', function (e) {
          		if (!click && $(e.target).closest('.dropdown-menu').length == 0) {
            	$(".dropdown-menu").hide();
            	$(document).unbind('click.myEvent');
          	}
			click = false;
        });
		}
	});

//Проверка ответа на сервере и разбор в таблицу
	$("#ajax-check-sql").click(function() {
        var form = $('.contact-form');
		var get = parseGetParams();
        $.post(
            "/test_answer/?testid="+get.testid+"&queid="+get.queid, //url
            form.serialize(), function(data) {
                console.log(data);
				dataToTable(data,".messages",1);
			}
        );
	});
//Восстановление пароля
    $(".restore_link").click(function() {
		$(".login_form").css("display","none");
		$(".restore_form").css("display","block");
	});
	
	$(".login_link").click(function() {
    	$(".login_form").css("display","block");
    	$(".restore_form").css("display","none");
    });

//Статистика у админа
	$(".users").ready(function(){
		$(".answer").each(function() {
			dataToTable(this.textContent,this,1);
		});
	});
});

function parseGetParams() { 
   var $_GET = {}; 
   var __GET = window.location.search.substring(1).split("&"); 
   for(var i=0; i<__GET.length; i++) { 
      var getVar = __GET[i].split("="); 
      $_GET[getVar[0]] = typeof(getVar[1])=="undefined" ? "" : getVar[1]; 
   } 
   return $_GET; 
}

function dataToTable(data, elem, clear) {      //success method
    if (!elem) return;
	try {
		data=data.replace(/: "/g,": '").replace(/"}/g,"'}").replace(/r '/,"r \\\'").replace(/' at/,"\\\' at"); // TO DELETE
		data = jQuery.parseJSON(data.replace(/ u\'/g, " \'").replace(/: (?=[0-9])/g,": '").replace(/L,/g,"',").replace(/'/g,"\"").replace(/None/g,"\"None\""));
		var result;	
    	if(data.sql_query_error){
			if(clear) $(elem).empty;
    		result = "sql_query_error: \"" + data.sql_query_error+"\"";
		} else if(data[0]) {
       		result = "<table class=\"table\" back>\n<thead>\n<tr>\n";
        	for(var k in data[0]){
        		result+="<th>"+k+"</th>\n";
   			}
        	result+="</tr></thead>\n<tbody style=\"background-color:transparent\">\n";
	   	 	for(var k in data){
    			result+="<tr>";
        		for(var j in data[k]){
        			result+="<th>"+data[k][j]+"</th>";
       	 		}
        		result+="</tr>\n";
    		}
   			result +="</tbody>\n</table>";
   		}
		if(clear) $(elem).empty();
    	if(!result) $(elem).append("<h4>Empty set</h4>");
		$(elem).append(result);
    } catch(err) {
		console.log(err,data);
		if(clear) $(elem).empty();
		$(elem).append("<h4>"+data+"<h4>");

	}
}
