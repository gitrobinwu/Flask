// 高亮查询关键字
function highlight(text,words,tag){
	//默认的标签,如果没有指定，使用span
	tag = tag || 'span';
	for(var i=0; i<words.length; i++){
		var re=null;
		//定位到所有包含关键字的文本
		//高亮包含特殊字符的关键词
		if(words[i]=='C++' || words[i]=='c++'){
			re = new RegExp("(<[^>]*>)[^<>=]*("+ 'c\\+{2}' +")",'ig');
		}else {
			re = new RegExp("(<[^>]*>)[^<>=]*("+ words[i] +")",'ig');
		}
		console.log('re =================== '+re);

		if(re.test(text)){
			//查看所有匹配到的文本
			/*list = text.match(re);
			console.log(list);
			for(var j=0;j<list.length;j++){
				console.log(list[j]);
				prefix = list[j].match(re1)[0];
				console.log('prefix ======== '+prefix);
				console.log('term ====== '+list[j].replace(prefix,''));
			}*/
			text = text.replace(re,function(word){
				//匹配到词单元
				console.log('word =='+word);
				let re1= new RegExp("<[^<>]*>",'gi');
				//前缀部分
				let prefix = word.match(re1)[0];
				console.log('prefix ======== '+prefix);

				let term = word.replace(prefix,'');
				let re2 = null;
				if(words[i]=='C++' || words[i]=='c++'){
					re2 = new RegExp('c\\+{2}','gi'); 
				}else {
					re2 = new RegExp(words[i],'gi');
				}
			
				let terms = term.match(re2)
				console.log('terms ======= '+terms);
				//关键词文本部分
				tag_term = term.replace(re2,"<"+tag+' class="highlight">'+'$&'+'</'+tag+'>')
				if(prefix != '<small>'){
					return prefix+tag_term;
				}else {
					return prefix+term;
				}
			});
		}
	}
	return text;
}

