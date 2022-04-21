/**
 * 计算sign
 * 根据keys组合字符串，然后签名，并把签名结果存入params里
 * @param {dict} params
 * @param {Array} keys
 */
function sign(params, keys){
    var sstr = buildSignStr(params, keys);
    var secret = localStorage.getItem("sc");
    var signstr = hex_md5(sstr+secret);
    params['sign'] = signstr;
    return params;
}

/**
 * 计算用于签名的字符串
 * keys in params is required
 * @param {dict} params 
 */
function buildSignStr(params){
    var sstr = '';
    keys = params.keys.split(',');
    var kc = keys.length;
    for(var ki=0; ki<kc; ki++){
        if(ki>0){
            sstr += '&';
        }
        sstr += keys[ki] + '=' + params[keys[ki]];
    }
    return sstr;
}

verifiesdef = {
    required_i18n: function (value, item) { //value：表单的值、item：表单的DOM对象
        if(value==null || value=='')return $.i18n.prop('reqval');
    }
}
