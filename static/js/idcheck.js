function change15To18(card)
{
	if(card.length == '15')
	{
		var arrInt = new Array(7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2); 
		var arrCh = new Array('1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'); 
		var cardTemp = 0, i;   
		card = card.substr(0, 6) + '19' + card.substr(6, card.length - 6);
		for(i = 0; i < 17; i ++) 
		{ 
			cardTemp += card.substr(i, 1) * arrInt[i]; 
		} 
		card += arrCh[cardTemp % 11]; 
		return card;
	}
	return card;
};
function checkID(idnum)
{
    var city={11:"北京",12:"天津",13:"河北",14:"山西",15:"内蒙古",21:"辽宁",22:"吉林",23:"黑龙江 ",31:"上海",32:"江苏",33:"浙江",34:"安徽",35:"福建",36:"江西",37:"山东",41:"河南",42:"湖北 ",43:"湖南",44:"广东",45:"广西",46:"海南",50:"重庆",51:"四川",52:"贵州",53:"云南",54:"西藏 ",61:"陕西",62:"甘肃",63:"青海",64:"宁夏",65:"新疆",71:"台湾",81:"香港",82:"澳门",91:"国外 "};
    var pass = true;
    var msg = "验证成功";
    //验证身份证格式（6个地区编码，8位出生日期，3位顺序号，1位校验位）
    if(!idnum || !/^\d{6}(18|19|20|21)?\d{2}(0[1-9]|1[012])(0[1-9]|[12]\d|3[01])\d{3}(\d|[xX])?$/.test(idnum)){
        pass=false;
        msg = "身份证号格式错误";
    }else if(!city[idnum.substr(0,2)]){
        pass=false;
        msg = "身份证号地址编码错误";
    }else{
        //18位身份证需要验证最后一位校验位
        var idnum2 = idnum;
        if(idnum.length == 15){
            idnum2 = change15To18(idnum);
        }
        if(idnum2.length == 18){
            idnum2 = idnum2.split('');
            //∑(ai×Wi)(mod 11)
            //加权因子
            var factor = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2 ];
            //校验位
            var parity = [ 1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2 ];
            var sum = 0;
            var ai = 0;
            var wi = 0;
            for (var i = 0; i < 17; i++)
            {
                ai = idnum2[i];
                wi = factor[i];
                sum += ai * wi;
            }
            if(parity[sum % 11] != idnum2[17].toUpperCase()){
                pass=false;
                msg = "身份证号校验位错误";
            }
        }
        else{
            pass=false;
            msg = "身份证号位数错误";
        }
    }
    return {res:pass,msg:msg} ;
};