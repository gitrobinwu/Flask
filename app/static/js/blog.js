/*文档就绪事件*/
$(document).ready(function(){
	//console.log('11111111111111');
	//console.log('**********'+$('.post-body').outerHeight()+'*************');
	$('li.listBox').each(function(index,domEle){
		//console.log('############'+$(domEle).outerHeight()+'################');
		//设置超出隐藏的高度，如果小于454内容全部显示，否则隐藏超出内容
		if($(domEle).outerHeight()<454){
			console.log('22222222222222');
			console.log($(domEle).children('div.listBoxCenter').html());
			//$(domEle).children('div.listBoxCenter').css('height',);
		}else {
			$(domEle).children('div.listBoxCenter').css("height","250px");
		}
	});
});


