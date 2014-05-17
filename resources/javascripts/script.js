$(function(){
	var form = $('.contact-form');
	var auto_agree=true;
	$("#send_sql").click(function() {
		if(!auto_agree){
			$(".confirm").show();
		}
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

//Timer
	if ($(".session_timer > a:nth-child(1)").length) {
		var Interval = setInterval(function(){
			var timer = parseInt($(".session_timer > a:nth-child(1)")[0].text.match(/\d+/));
			if (timer-1 > 0)	{
				$(".session_timer > a:nth-child(1)").html("Осталось "+(timer-1)+" min");
			} else {
				$(".session_timer > a:nth-child(1)").html("Время вышло");
				clearInterval(Interval);
			}
		}, 60000);
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
                if ($('.question_type').text() == 'SQL_query') {
					$(".messages").css("text-align","center");
					dataToTable(data,".messages",1);
				}
                else {
				    $(".messages").empty();
					$(".messages").css('text-align','left');
                    //$(".messages").append(data);
                    $(".messages").append("<pre>" + JSON.stringify(jQuery.parseJSON(data), "", 2) + "</pre>");
				}
			}
        );
	});

//Проверка у админа 
    $(".ajax-check-sql-admin").click(function(e) {
        var type_txt = null;
        if (typeof($("#id_type")[0]) === "undefined") {
            type_txt = $(".question_type")[0].innerHTML;
        } else {
            type_txt = $("#id_type :selected").text();
        }

		$.post(
            "/custom-admin/test_question/", //url
            {
				message: $("#id_answer")[0].value,
				type_txt: type_txt,
				csrfmiddlewaretoken: $("#question_form")[0][0].value
			}, function(data) {
				if (type_txt === "noSQL запрос" || type_txt === "noSQL_query") {
					$(".sql-check-table-admin").empty();
					$(".sql-check-table-admin").css("text-align","left");
					$(".sql-check-table-admin").append("<pre>" + JSON.stringify(jQuery.parseJSON(data), "", 2) + "</pre>");
				    //console.log($(".sql-check-table-admin"));
                } else {
					$(".sql-check-table-admin").css("text-align","center");
					dataToTable(data,".sql-check-table-admin",1);
				}
			}	
        );
		//console.log($("#id_type"))
		e.preventDefault();
	});
//Для пересчета показателя вопроса
	$(".ajax-recalc-que-admin").click(function() {
		$.post(
			"/custom-admin/question_action/?type=recalc",
			{
				url: $(this).baseURL,
				csrfmiddlewaretoken: $("#question_form")[0][0].value
			}, function(data) {
				$(".ajax-recalc-que-admin-success").empty();
				if (data) $(".ajax-recalc-que-admin-success").append("Показатели пересчитаны");
				else $(".ajax-recalc-que-admin-success").append(data);
			}
		);
	});
// Зачесть вопрос как правильный
	//Страница статистики юзера
    $(".ajax-make-que-right-admin").click(function(event) {
		$.get(
			$(this).attr("href"),
			function() {
				var get = $.parseJSON("{\""+this.url.split("?")[1].replace(/&/g,"\", \"").replace(/=/g,"\": \"")+"\"}");
				$("#RK"+get.rkid+"Att"+get.att+"Que"+get.queid).removeClass("error").addClass("success").empty().append(
					"<td colspan=\"3\"><h4 style=\"text-align:center\">Совпадение<small style=\"color:red\">(Исправлено)</small></h4></td>"
				);
				$("#RK"+get.rkid+"Att"+get.att+">h5").append(" +1");
			}
		);
		event.preventDefault();
	});
	//Страница статистики вопроса
	$(".make-right-question_stat-quest").click(function(e) {
		$.get(
			$(this).attr("href"),
			function() {
				var get = $.parseJSON("{\""+this.url.split("?")[1].replace(/&/g,"\", \"").replace(/=/g,"\": \"")+"\"}");
				var rowIndex= $("[data-target=#R"+get.rkid+"A"+get.att+"Q"+get.queid+"U"+get.uid+"]")[0].parentElement.rowIndex;
				$($("[data-target=#R"+get.rkid+"A"+get.att+"Q"+get.queid+"U"+get.uid+"]")[0].parentElement.parentElement.children[rowIndex]).css("background","#DFF0D8");
				var tds = $($("[data-target=#R"+get.rkid+"A"+get.att+"Q"+get.queid+"U"+get.uid+"]")[0].parentElement.children);
				$(tds[0]).css("background","#DFF0D8");
				$(tds[1]).css("background","#DFF0D8");
				$(tds[2]).css("background","#DFF0D8");
				$(tds[3]).css("display","none");
			}
		)
	});
//Статистика у админа
	$(document).ready(function() {
		$(".answer").each(function() {
			dataToTable(this.textContent,this,1);
		});
	});
	
//Навигация у админа в статистиске юзера
	$(".rk-headers > li:first").addClass("active");
	$(".rk-view:first").addClass("active");
    
	$(".rk-headers > li").click(function() {
		$(".active").removeClass("active");
 		$(this).addClass("active");
		$($(this).attr("name")).addClass("active");
	});
	
	$(".attempt-view").each(function() {
		$(this).css("display","none");
	});	
//Показываем/скрываем попытку юзера на странице статистики юзера
	$(".open-attempt").click(function(){
		//var rkid= this.id.split("RK")[1].split("Att")[0];
		if($("#"+this.id.split("_")[1]).css("display") != "none")	
			$("#"+this.id.split("_")[1]).css("display","none");
		else{
			$("#"+this.id.split("_")[1]).css("display","block");
			$("#"+this.id.split("_")[1] + "> table > tbody >tr.info").each(function(){
				$(this).css("display","none");
			});
			$("#"+this.id.split("_")[1] + "> table > tbody >tr.warning").each(function(){
                $(this).css("display","none");
            });
		}
	});
//Скрываем/показываем строки в таблице на странице статистики юзера
	$("tr.hided").click(function(e){
		console.log(this);
		if($("."+this.className.split(" ")[1]+".info").css("display") == "none")
			$("."+this.className.split(" ")[1]).css("display","row");
		else{
			$("."+this.className.split(" ")[1]+".info").css("display","none");
            $("."+this.className.split(" ")[1]+".warning").css("display","none");
		}
		e.preventDefault();
	});
//Скрываем/показываем строку на странице статистики вопроса
	//костыль, что при клики на "Засчитать" не выпадало
	var is_click_question_table_td3=false;
	$("table.question-table > tbody > tr").click( function() {
		if (is_click_question_table_td3 == true) {
			is_click_question_table_td3=false;
			return;
		}
		if(this.rowIndex % 2 == 1) 
    		if($(this.parentElement.children[this.rowIndex]).css("display") == "none")
    			$(this.parentElement.children[this.rowIndex]).css("display","row");
    		else
    			$(this.parentElement.children[this.rowIndex]).css("display","none");
    	else
    		$(this).css("display","none");
    });	
	$("table.question-table > tbody > tr > td:nth-child(4)").click( function(e) {	
		is_click_question_table_td3=true;
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
		data = jQuery.parseJSON(data);
		var result;	
    	if(data.query_error){
			if(clear) $(elem).empty;
            if(data.query_error != "empty_query") result = "query_error: \"" + data.query_error+"\"";
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
