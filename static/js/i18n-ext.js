/**
 * cookie操作
 */
var getCookie = function(name, value, options) {
    if (typeof value != 'undefined') { // name and value given, set cookie
        options = options || {};
        if (value === null) {
            value = '';
            options.expires = -1;
        }
        var expires = '';
        if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
            var date;
            if (typeof options.expires == 'number') {
                date = new Date();
                date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
            } else {
                date = options.expires;
            }
            expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
        }
        var path = options.path ? '; path=' + options.path : '';
        var domain = options.domain ? '; domain=' + options.domain : '';
        var s = [cookie, expires, path, domain, secure].join('');
        var secure = options.secure ? '; secure' : '';
        var c = [name, '=', encodeURIComponent(value)].join('');
        var cookie = [c, expires, path, domain, secure].join('')
        document.cookie = cookie;
    } else { // only name given, get cookie
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
};

/**
 * 获取浏览器语言类型
 * @return {string} 浏览器国家语言
 */
var getNavLanguage = function(){
    if(navigator.appName == "Netscape"){
        var navLanguage = navigator.language;
        return navLanguage.substr(0,2);
    }
    return false;
}

/**
 * 设置语言类型
 */
var i18nLanguage = "zh-TW";

/*
设置一下网站支持的语言种类
 */
var webLanguage = ['zh-TW', 'en'];

/**
 * 执行页面i18n方法
 * @return
 */ 
var execI18n = function(){
    /*
    获取一下资源文件名
     */
    var optionEle = $("#i18n_pagename");
    if (optionEle.length < 1) {
        console.log("未找到页面名称元素，请在页面写入\n <meta id=\"i18n_pagename\" content=\"页面名(对应语言包的语言文件名)\">");
        return false;
    };
    var sourceName = optionEle.attr('content');
    sourceName = sourceName.split('-');
        /*
        首先获取用户浏览器设备之前选择过的语言类型
         */
        if (getCookie("userLanguage")) {
            i18nLanguage = getCookie("userLanguage");
        } else {
            // 获取浏览器语言
            var navLanguage = getNavLanguage();
            if (navLanguage) {
                // 判断是否在网站支持语言数组里
                var charSize = $.inArray(navLanguage, webLanguage);
                if (charSize > -1) {
                    i18nLanguage = navLanguage;
                    // 存到缓存中
                    getCookie("userLanguage",navLanguage);
                };
            } else{
                console.log("not navigator");
                return false;
            }
        }
        /* 需要引入 i18n 文件*/
        if ($.i18n == undefined) {
            console.log("请引入i18n js 文件")
            return false;
        };

        /*
        这里需要进行i18n的翻译
         */
        console.log(i18nLanguage);
        jQuery.i18n.properties({
            name : sourceName, //资源文件名称
            path : 'static/i18n_serv/' + i18nLanguage +'/', //资源文件路径
            mode : 'map', //用Map的方式使用资源文件中的值
            language : i18nLanguage,
            cache:  false,
            callback : function() {//加载成功后设置显示内容
                // usage:
                // i18nkey='xx',i18nattr is null: <ele>.html=val(xx);
                // i18nkey='xx1;xx2;xx3;xx4', i18nattr='text;html;val;a1':
                //      <ele>.text=val(xx1);<ele>.html=val(xx2);<ele>.val=val(xx3);<ele>.attr(xx4,val(xx4));
                var insertEle = $("[i18nkey]");
                console.log(".i18n 写入中...");
                var elec = insertEle.length;
                for(var i = 0; i < elec; i++) { // 这里的i是代表数组的下标
                    var ele = insertEle[i];
                    // 根据i18n元素的i18nkey获取内容
                    var i18nks = $(ele).attr('i18nkey').split(';');
                    var i18n_attr = $(ele).attr('i18nattr');
                    // default, change html
                    if(i18nks.length==1 && !i18n_attr){
                        var i18nw = i18nks[0];
                        if($.i18n.map.hasOwnProperty(i18nks[0])){
                            i18nw = $.i18n.prop(i18nks[0]);
                        }
                        else{
                            console.log("I18N ERROR: Key \""+i18nks[0]+"\" not exists!");
                        }
                        $(ele).html(i18nw);
                        continue;
                    }
                    var i18n_attrs = Array(0);
                    if(i18n_attr){
                        i18n_attrs = i18n_attr.split(';');
                    }
                    if(i18nks.length!=i18n_attrs.length){
                        console.log('error when analyzing i18n keys\n');
                        continue;
                    }

                    var kc = i18nks.length;
                    for(var j=0; j<kc; j++){
                        var i18nw = i18nks[j];
                        if($.i18n.map.hasOwnProperty(i18nks[j])){
                            i18nw = $.i18n.prop(i18nks[j]);
                        }
                        else{
                            console.log("I18N ERROR: Key \""+i18nks[j]+"\" not exists!");
                        }
                        switch(i18n_attrs[j]){
                            case 'text':
                                $(ele).text(i18nw);
                                break;
                            case 'html':
                                $(ele).html(i18nw);
                                break;
                            case 'val':
                                $(ele).val(i18nw);
                                break;
                            /*
                            case 'validationMessage':
                                ele.validationMessage = i18nw;
                                ele.setCustomValidity(i18nw);
                                break;
                            */
                            default:
                                $(ele).attr(i18n_attrs[j], i18nw);
                        }
                    }
                };
                console.log("写入完毕");
            }
        });
}

function changeLang(language){
    console.log(language);
        getCookie("userLanguage",language,{
            expires: 30,
            path:'/'
        });
        location.reload();
};
