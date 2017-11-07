/*文档就绪事件*/
$(document).ready(function(){
	var editorContent = CKEDITOR.replace('ckhtml',{
		//设置编辑器样式kama moono
		skin: 'kama',
		//设置工具栏的位置，可选bottom
		toolbarLocation: 'top',
		//工具栏是否可以被收缩
		toolbarCanCollapse: true,
		//设置默认语言
		language: 'zh-cn',
		defaultLanguage: 'zh-cn',
		allowedContent: true,
		//移除元素路径
		removePlugins:  'elementspath',
		//是否可拖拽
		resize_enabled: true, 
		//设置字体栏可选择的字体
		font_names: 'Arial;Times New Roman;Verdana;YaHei Consolas Hybird;Courier New;宋体;黑体;微软雅黑',
		//设置默认字体
		font_defaultLabel: '宋体',
		//设置字体大小栏可显示的大小
		fontSize_sizes: '10/10px;12/12px;14/14px;16/16px;18/18px;20/20px;24/24px;28/28px',
		//设置默认的字体大小
		fontSize_defaultLabel: '14px',
		//设置按回车键时插入什么标签，有CKEDITOR.ENTER_BR、CKEDITOR.ENTER_DIV、CKEDITOR.ENTER_P
		//推荐是P，不推荐BR，config.shiftEnterMode默认是BR
		enterMode: CKEDITOR.ENTER_BR,// 配置Enter是换行
		shiftEnterMode: CKEDITOR.ENTER_P, // 配置Shift + Enter是换段落
		//是否要将编辑器中的内容作为一个完整的HTML页面输出，即自动添加<html>，<head>和<body>标记，默认为false
		//config.fullPage =true
		//设置缩进风格，默认是px
		indentUnit: 'em',
		//设置缩进的步长，默认是40
		indentOffset: 2,
		//设置编辑器启动时的编辑模式， "wysiwyg"或者"source"，默认是wysiwyg
		//startupMode: 'source',
		//设置每个Tab键的空格数，默认为0，即不是插入空格，而是在各功能间切换
		tabSpaces: 4,
		//设置文件上传路由路径
		filebrowserUploadUrl: '/ckupload/', 
		//extraPlugins: 'preview,colorbutton,font,find,save',//预览
		//设置搜索高亮
		find_highlight: {
			element : 'span',
			styles : { 'background-color' : '#ff0', 'color' : '#00f' }
		},
		//设置我的工具栏
		toolbar: 'mytoolbar',
		toolbar_mytoolbar: [
		['Source','Preview','Print','-','Save','NewPage'],
		['Cut','Copy','Paste','PasteText','PasteFromWord','-','SelectAll', 'RemoveFormat'],
		['Undo','Redo','-','Find','Replace'],
		'/',
		['NumberedList','BulletedList','-','Outdent','Indent','Blockquote','-','CreateDiv','ShowBlocks'],
		['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
		['Link','Unlink','Anchor'],
		['Image','Flash','Table','-','Smiley','SpecialChar','-','HorizontalRule','PageBreak'],
		['Maximize','Iframe'],
		'/',
		['Styles','Format','Font','FontSize'],
		['TextColor','BGColor'],
		['Bold','Italic','Underline','Strike','-','Subscript','Superscript']
		],
		//是否强制复制来的内容去除格式 plugins/pastetext/plugin.js
		forcePasteAsPlainText: false,
	});
});


