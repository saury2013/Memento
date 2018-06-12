var CONFIG = CONFIG || {
	python_version: 'Python 3.6.2',
	gcc_version: '4.8.2',
	sys_platform: 'linux2',
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
          'hi,我的allen。现在居住地<i class="fa fa-map-marker">深圳</i><br>'+
          '目前是一名pythoner。之前一直用c做嵌入式的网络设备开发。后来因为换工作开始使用python来做web app。<br>'+
          '从此喜欢上了python的简捷,快速和<span class="prettytext">There is only one way to do it</span> 的编程思想。<br>'+
          '目前的技术栈是 python, C, tornado， flask, mongodb， redis， nodejs， golang, mysql, git, linux。网站部署常用的是supervisord+nginx+git<br>'+
          '这个是我的个人网站。当然你可以从<a href="http://github.com/jack-zh" target="_blank">GitHub</a>上面看到我之前写的一些乱七八糟的项目。<br>'+
          '你可以通过邮件联系我 <a href="mailto:zzh.coder@qq.com">zzh.coder#qq.com</a> 或者QQ: 715443050 或者<a target="_blank" href="'+ 'http://github.com/jack-zh' +'">微博</a><br>'+
          '最后你可以试着输入 <span class="prettytext">jack.__doc__</span> 看看这个module有哪些属性和方法以便您更好的了解和使用它<br>'+
          '你可以点击命令输出结果中的任何绿色文字连接。在输入命令的时候如果你想中途退出，请输入Ctrl+D或者Ctrl+C。<br>'+
          '你可以输入&uarr;或者&darr;查看之前输入的命令<br>'+
          '***************************************************************************************<br>'

var InitCommands = [
	"python",
	"import jack",
	"jack.__doc__",
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