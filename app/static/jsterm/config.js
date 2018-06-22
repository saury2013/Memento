var CONFIG = CONFIG || {
	python_version: 'Python 3.6.2',
	gcc_version: '4.8.2',
	sys_platform: 'arch linux',
	username: 'allen',
	ipython: false
};


var ContactInformation = {
	email: {
		showStr: "邮件地址",
		type: "lnk",
		info: "这是我的个人邮箱",
		value: 'saury2011@sina.com'
	},
	github: {
		showStr: "Github",
		type: "lnk",
		info: "自己做的练习项目",
		value: 'http://github.com/saury2013'
	},
	blog: {
		showStr: "个人站点",
		type: "lnk",
		info: "自己写了一个写作平台，记录学习过程中的经验",
		value: 'http://threefish.xyz'
	},
	realname: {
		showStr: "真实姓名",
		type: "text",
		value: '三条鱼'
	}
};


var AboutMeStr = '***************************************************************************************<br>'+
          'hi,我是allen。现在居住地<span class="prettytext">深圳</span><br>'+
          '本人对未知得世界总是充满好奇，喜欢了解不同方面的知识。我一直梦想有过目不忘的本领，<br>' +
	      '但可惜现实很残酷，学过的很多知识转头就忘了。<br>'+
          '我相信很多人也是如此。那该如何呢？<br>'+
          '俗话说<span class="prettytext">好记性不如烂笔头</span>，确实如此。<br>' +
		  '既然不能过目不忘就写下来，时不时得回顾，做到<span class="prettytext">温故而知新</span>。<br>'+
          '这相当于一个私人版的wiki，把自己学到的知识加入进去，方便以后查找和温故。<br>'+
          '也可以记录自己在探索的路上所经历的艰难险阻。<br>'+
          '可以不断积累自己的技能，让自己越来越强大。<br>'+
          '这个是本人的<a href="http://github.com/saury2013" target="_blank">GitHub</a>上面看到我之前写的一些乱七八糟的项目。<br>'+
          '你可以通过邮件联系我 <a href="mailto:saury2011@sina.com">saury2011@sina.com</a><br>'+
          '最后你可以试着输入 <span class="prettytext">allen.__doc__</span> 看看这个module有哪些属性和方法以便您更好的了解和使用它<br>'+
          '你可以点击命令输出结果中的任何绿色文字连接。在输入命令的时候如果你想中途退出，请输入Ctrl+D或者Ctrl+C。<br>'+
          '你可以输入&uarr;或者&darr;查看之前输入的命令<br>'+
          '***************************************************************************************<br>'

var InitCommands = [
	"python",
	"import allen",
	"allen.__doc__",
	"exit()"
];

CONFIG.prompt = function(cwd, user) {
    if (CONFIG.ipython){
        return '>>> ';
    }
    else{
    	// CONFIG.ipython = false;
	    return '<span class="user">' + CONFIG.username + '</span><span style="color:#9e65ff;">-> ~ </span>';
	}
};