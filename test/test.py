import hashlib
import requests
import unittest


class APITester(unittest.TestCase):
    ep = 'http://localhost:5000/api'

    def get_md5(self, orgstr):
        _m2 = hashlib.md5()
        _m2.update(orgstr.encode("utf-8", "ignore"))
        return _m2.hexdigest()
    
    def change2admin(self):
        self.test_a00_logout()
        self.g['un'] = 'admin'
        self.g['pw'] = 'haha'
        self.test_100_getSecret()
        self.test_203_login()

    def change2staff(self):
        self.test_a00_logout()
        self.g['un'] = 't1s1'
        self.g['pw'] = 'hhhaaa'
        self.test_100_getSecret()
        self.test_203_login()

    def change2parent1(self):
        self.test_a00_logout()
        self.g['un'] = 't21dda'
        self.g['pw'] = 'hhhahahaha'
        self.test_100_getSecret()
        self.test_203_login()

    def change2parent2(self):
        self.test_a00_logout()
        self.g['un'] = 't21dfweavrfega'
        self.g['pw'] = 'hhhaaa'
        self.test_100_getSecret()
        self.test_203_login()

    def setUp(self):
        self.g = globals()
        self.g['un'] = 'admin'
        self.g['pw'] = 'haha'

    def test_100_getSecret(self):
        print("Test getSecret")
        res = requests.get(self.ep+'/getSecret')
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
        self.g['sk'] = resj['data'][0]['secret_key']
        self.g['secret_login'] = resj['data'][0]['secret']
        print(res.text)

    def _test_200_login(self):
        '''
        Test login if passwd is wrong
        '''
        print("Test login, passwd is wrong")
        pwmd5 = self.get_md5(self.get_md5('hhh')+self.g['secret_login'])
        params = {'username': self.g['un'],
                  'passwd_md5': pwmd5, 'secret_key': self.g['sk']}
        res = requests.post(self.ep+"/login", data=params)
        resj = res.json()
        self.assertEqual(resj['code'], 23, "error:\n"+res.text)
        print(res.text)

    def _test_201_login(self):
        '''
        Test login if username is wrong
        '''
        print("Test login, username is wrong")
        pwmd5 = self.get_md5(self.get_md5(self.g['pw'])+self.g['secret_login'])
        params = {'username': 'nhfuweifan',
                  'passwd_md5': pwmd5, 'secret_key': self.g['sk']}
        res = requests.post(self.ep+"/login", data=params)
        resj = res.json()
        self.assertEqual(resj['code'], 51, "error:\n"+res.text)
        print(res.text)

    def _test_202_login(self):
        '''
        Test login if sevret key is wrong
        '''
        print("Test login, sevret key is wrong")
        pwmd5 = self.get_md5(self.get_md5(self.g['pw'])+self.g['secret_login'])
        params = {
            'username': self.g['un'], 'passwd_md5': pwmd5, 'secret_key': self.g['sk']+'a'}
        res = requests.post(self.ep+"/login", data=params)
        resj = res.json()
        self.assertEqual(resj['code'], 51, "error:\n"+res.text)
        print(res.text)

    def test_203_login(self):
        '''
        Test login
        '''
        print("Test login")
        pwmd5 = self.get_md5(self.get_md5(self.g['pw'])+self.g['secret_login'])
        params = {'username': self.g['un'],
                  'passwd_md5': pwmd5, 'secret_key': self.g['sk']}
        res = requests.post(self.ep+"/login", data=params)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
        print(res.text)
        self.g['secret'] = resj['data'][0]['secret']
        self.g['token'] = resj['data'][0]['token']

    def _test_300_checkUsername(self):
        print("Test checkUsername")
        res = requests.get(self.ep+"/checkUsername",
                           params={'username': 'admin'})
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
        print("exists:\n"+res.text)
        res = requests.get(self.ep+"/checkUsername",
                           params={'username': 'admin111'})
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
        print("not exists:\n"+res.text)

    def _test_307_users_parents(self):
        print("Test users/parents")
        page = 0
        limit = 10
        sk = self.g['sk']
        keys = 'page,limit,secret_key'
        signpre = 'page={0}&limit={1}&secret_key={2}'.format(
            str(page),
            str(limit),
            str(sk))
        sign = self.get_md5(signpre+self.g['secret'])
        params = {
            'page':page,
            'limit':limit,
            'secret_key':sk,
            'keys':keys,
            'sign':sign
        }
        res = requests.get(self.ep+"/users/parents",
                           params=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)

    def _test_307_users_parents2(self):
        print("Test users/parents")
        page = 0
        limit = 10
        sk = self.g['sk']
        keys = 'page,limit,simple,secret_key'
        signpre = 'page={0}&limit={1}&simple=1&secret_key={2}'.format(
            str(page),
            str(limit),
            str(sk))
        sign = self.get_md5(signpre+self.g['secret'])
        params = {
            'page':page,
            'limit':limit,
            'simple':1,
            'secret_key':sk,
            'keys':keys,
            'sign':sign
        }
        res = requests.get(self.ep+"/users/parents",
                           params=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
        
    def _test_308_users_parents(self):
        print("Test users/parents, sign error")
        page = 0
        limit = 10
        sk = self.g['sk']
        keys = 'page,limit,secret_key'
        signpre = 'page={0}&limit={1}&secret_key={2}'.format(
            str(page),
            str(limit),
            str(sk))
        sign = self.get_md5(signpre+self.g['secret'])
        params = {
            'page':page,
            'limit':limit,
            'secret_key':sk,
            'keys':keys,
            'sign':sign+"a"
        }
        res = requests.get(self.ep+"/users/parents",
                           params=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 24, "error:\n"+res.text)
        
    def _test_303_users_parents(self):
        print("Test users/parents, no authority")
        # change user
        self.change2parent1()

        page = 0
        limit = 10
        sk = self.g['sk']
        keys = 'page,limit,secret_key'
        signpre = 'page={0}&limit={1}&secret_key={2}'.format(
            str(page),
            str(limit),
            str(sk))
        sign = self.get_md5(signpre+self.g['secret'])
        params = {
            'page':page,
            'limit':limit,
            'secret_key':sk,
            'keys':keys,
            'sign':sign
        }
        res = requests.get(self.ep+"/users/parents",
                           params=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 30, "error:\n"+res.text)

        # change user
        self.change2admin()
    
    def _test_304_users_staffs(self):
        print("Test users/staffs")
        page = 0
        limit = 10
        sk = self.g['sk']
        keys = 'page,limit,secret_key'
        signpre = 'page={0}&limit={1}&secret_key={2}'.format(
            str(page),
            str(limit),
            str(sk))
        sign = self.get_md5(signpre+self.g['secret'])
        params = {
            'page':page,
            'limit':limit,
            'secret_key':sk,
            'keys':keys,
            'sign':sign
        }
        res = requests.get(self.ep+"/users/staffs",
                           params=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
    
    def _test_305_users_parent(self):
        print("Test users/parent")
        id = 2
        sk = self.g['sk']
        keys = 'id,secret_key'
        signpre = 'id={0}&secret_key={1}'.format(
            str(id),
            str(sk))
        sign = self.get_md5(signpre+self.g['secret'])
        params = {
            'id':id,
            'secret_key':sk,
            'keys':keys,
            'sign':sign
        }
        res = requests.get(self.ep+"/users/parent",
                           params=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)

    def _test_306_users_staff(self):
        print("Test users/staff")
        id = 1
        sk = self.g['sk']
        keys = 'id,secret_key'
        signpre = 'id={0}&secret_key={1}'.format(
            str(id),
            str(sk))
        sign = self.get_md5(signpre+self.g['secret'])
        params = {
            'id':id,
            'secret_key':sk,
            'keys':keys,
            'sign':sign
        }
        res = requests.get(self.ep+"/users/staff",
                           params=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)

    def _test_300_users_parent_post(self):
        print("test add parent")
        params = {
            "username":'t21dda',
            "name":'tty',
            "name_chs":'h哈哈',
            "relations":'ffewfcewd',
            "edu":'xx',
            "occupation":'safds',
            "tel":'fcwervrwdw',
            "email":'afatpig@foxmail.com',
            "reason":'gvervgrevresaVR二十',
            "passwd_md5":self.get_md5('hhhaaa'),
            "secret_key":self.g['sk'],
            "keys":'username,name,name_chs,relations,edu,occupation,tel,email,reason,passwd_md5,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.post(self.ep+"/users/parent",
                           data=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)

    def _test_301_users_staff_post(self):
        print("test add staff")
        params = {
            "username":'t1s1',
            "name":'tty',
            "name_chs":'h哈哈',
            "gender":'f',
            "group_id":0,
            "email":'vrevsravweftr',
            "passwd_md5":self.get_md5('hhhaaa'),
            "secret_key":self.g['sk'],
            "keys":'username,name,name_chs,gender,group_id,email,passwd_md5,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.post(self.ep+"/users/staff",
                           data=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)

    def _test_309_users_staff_put(self):
        print("test update staff")
        params = {
            'id':15,
            "username":'t1s1',
            "gender":'m',
            "group_id":1,
            "secret_key":self.g['sk'],
            "keys":'id,username,gender,group_id,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.put(self.ep+"/users/staff",
                           data=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
    
    def _test_310_users_parent_put(self):
        print("test update parent")
        params = {
            'id':12,
            "child_ids":'1,5',
            "secret_key":self.g['sk'],
            "keys":'id,child_ids,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.put(self.ep+"/users/parent",
                           data=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
    

    def test_320_get_cids(self):
        print("test get cids")
        self.change2parent1()
        params = {
            "secret_key":self.g['sk'],
            "keys":'secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.get(self.ep+"/users/parent/cids",
                           params=params)
        print(res.text)
        self.change2admin()

    def _test_311_users_staff_delete(self):
        print("test delete staff")
        params = {
            'id':15,
            "secret_key":self.g['sk'],
            "keys":'id,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.delete(self.ep+"/users/staff",
                           data=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
    
    def _test_312_users_parent_delete(self):
        print("test delete parent")
        params = {
            'id':12,
            "secret_key":self.g['sk'],
            "keys":'id,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.delete(self.ep+"/users/parent",
                           data=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)

    

    def _test_400_children_info_post(self):
        print("test add children info")
        params = {
            'name': 'Xiaohong',
            'name_chs': 'Dahong',
            'alias':'hahah',
            'gender': 'Female',
            'religion': 'A1',
            'birth_cert_no':'BIRTHCERTNUM1',
            'born_day': '2019-10-03',
            'place_birth':'LIGHT',
            'address':'Beijing, Light, Haha, Are you kidding?',
            'date_in': '2020-01-3',
            'tel':'+86-123456789',
            'email':'abc@def.com',
            'caregiver': 't21dda',
            'lang': 'en',
            'group_id':'100',
            "secret_key":self.g['sk'],
            "keys":'name,name_chs,alias,gender,religion,birth_cert_no,born_day,place_birth,address,date_in,tel,email,caregiver,lang,group_id,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.post(self.ep+"/children/info",
                           data=params)
        print(res.text)
        resj = res.json()
        # self.assertEqual(resj['code'], 0, "error:\n"+res.text)

    def _test_402_children_info_put(self):
        print("test update children info")
        # post parent 
        '''
        params = {
            "username":'t21dfweavrfega',
            "name":'tty',
            "name_chs":'h哈哈',
            "relations":'ffewfcewd',
            "edu":'xx',
            "occupation":'safds',
            "tel":'fcwervrwdw',
            "email":'vrevsravweftr',
            "reason":'gvervgrevresaVR二十',
            "passwd_md5":self.get_md5('hhhaaa'),
            "secret_key":self.g['sk'],
            "keys":'username,name,name_chs,relations,edu,occupation,tel,email,reason,passwd_md5,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.post(self.ep+"/users/parent",
                           data=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
        '''
        # put child
        params = {
            'alias':'hah',
            'gender': 'female',
            "email":'a.a.a',
            "secret_key":self.g['sk'],
            "keys":'alias,gender,email,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.put(self.ep+"/children/info",
                           data=params)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)


    def _test_403_children_infos(self):
        print("test children infos")
        params = {
            'page':0,
            'limit':10,
            "secret_key":self.g['sk'],
            "keys":'page,limit,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.get(self.ep+"/children/infos",
                           params=params)
        print(res.headers)
        print(res.text)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
    
    def _test_404_children_info(self):
        print("test children info")
        print('parent1')
        self.change2parent1()
        params = {
            'id':4850697613102216244,
            "secret_key":self.g['sk'],
            "keys":'id,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.get(self.ep+"/children/info",
                           params=params)
        #print(res.headers)
        print(res.text)
        #resj = res.json()
        #self.assertEqual(resj['code'], 0, "error:\n"+res.text)
        print('parent2')
        self.change2parent2()
        params = {
            'id':4850697613102216244,
            "secret_key":self.g['sk'],
            "keys":'id,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.get(self.ep+"/children/info",
                           params=params)
        #print(res.headers)
        print(res.text)
        print('staff')
        self.change2staff()
        params = {
            'alias':'hah',
            "secret_key":self.g['sk'],
            "keys":'alias,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.get(self.ep+"/children/info",
                           params=params)
        #print(res.headers)
        print(res.text)
        print('admin')
        self.change2admin()
        params = {
            'id':4850697613102216244,
            "secret_key":self.g['sk'],
            "keys":'id,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        # print(pss)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.get(self.ep+"/children/info",
                           params=params)
        #print(res.headers)
        print(res.text)
        print(res.headers)
    
    def _chkstatus(self, sid, tp):
        scp = {
            'id':sid,
            'secret_key':self.g['sk'],
            'keys':'id,secret_key',
        }
        _s = self.build_sign_str(scp['keys'], scp)
        scp['sign'] = self.get_md5(_s + self.g['secret'])
        res = requests.get(self.ep+"/status/"+tp,
                           params=scp)
        return res

    def _test_405_children_status(self):
        #ts = ['temp','skin','meal','nap','diaper','health','perform']
        params = {
            'alias':'hah'
        }

        # temp
        print("insert temperature------------")
        _p = params.copy()
        _p['temperature'] = 36.6
        _p['secret_key'] = self.g['sk']
        _p['keys'] = 'alias,temperature,secret_key'
        _s = self.build_sign_str(_p['keys'], _p)
        _p['sign'] = self.get_md5(_s + self.g['secret'])
        res = requests.post(self.ep+"/status/temperature",
                           data=_p)
        print(res.text)
        res2 = self._chkstatus(1, 'temperature')
        print(res2.text)

        # skin
        print("insert skin------------")
        _p = params.copy()
        _p['condition_id'] = 0
        _p['remark']='表现良好'
        _p['secret_key'] = self.g['sk']
        _p['keys'] = 'alias,condition_id,remark,secret_key'
        _s = self.build_sign_str(_p['keys'], _p)
        _p['sign'] = self.get_md5(_s + self.g['secret'])
        res = requests.post(self.ep+"/status/skin",
                           data=_p)
        print(res.text)
        res2 = self._chkstatus(1, 'skin')
        print(res2.text)

        # meal
        print("insert meal------------")
        _p = params.copy()
        _p['mealtype'] = 0
        _p['qty']=3
        _p['secret_key'] = self.g['sk']
        _p['keys'] = 'alias,mealtype,qty,secret_key'
        _s = self.build_sign_str(_p['keys'], _p)
        _p['sign'] = self.get_md5(_s + self.g['secret'])
        res = requests.post(self.ep+"/status/meal",
                           data=_p)
        print(res.text)
        res2 = self._chkstatus(3, 'meal')
        print(res2.text)

        # nap
        print("nap------------")
        _p = params.copy()
        _p['napquality'] = 0
        _p['remark']=3
        _p['secret_key'] = self.g['sk']
        _p['keys'] = 'alias,napquality,remark,secret_key'
        _s = self.build_sign_str(_p['keys'], _p)
        _p['sign'] = self.get_md5(_s + self.g['secret'])
        res = requests.post(self.ep+"/status/nap",
                           data=_p)
        print(res.text)
        res2 = self._chkstatus(1, 'nap')
        print(res2.text)

        # diaper
        print("nap------------")
        _p = params.copy()
        _p['diaper_id'] = 0
        _p['secret_key'] = self.g['sk']
        _p['keys'] = 'alias,diaper_id,secret_key'
        _s = self.build_sign_str(_p['keys'], _p)
        _p['sign'] = self.get_md5(_s + self.g['secret'])
        res = requests.post(self.ep+"/status/diaper",
                           data=_p)
        print(res.text)
        res2 = self._chkstatus(1, 'diaper')
        print(res2.text)

        # health
        print("health------------")
        _p = params.copy()
        _p['health_status_id'] = 0
        _p['secret_key'] = self.g['sk']
        _p['keys'] = 'alias,health_status_id,secret_key'
        _s = self.build_sign_str(_p['keys'], _p)
        _p['sign'] = self.get_md5(_s + self.g['secret'])
        res = requests.post(self.ep+"/status/health",
                           data=_p)
        print(res.text)
        res2 = self._chkstatus(1, 'health')
        print(res2.text)

        # perform
        print("perform------------")
        _p = params.copy()
        _p['perform_id'] = 0
        _p['secret_key'] = self.g['sk']
        _p['keys'] = 'alias,perform_id,secret_key'
        _s = self.build_sign_str(_p['keys'], _p)
        _p['sign'] = self.get_md5(_s + self.g['secret'])
        res = requests.post(self.ep+"/status/perform",
                           data=_p)
        print(res.text)
        res2 = self._chkstatus(1, 'perform')
        print(res2.text)
        

    def _test_412_children_statuses(self):
        ts = ['temp','skin','meal','nap','diaper','health','perform']
        for _t in ts:
            print('get ' + _t)
            params = {
                'type':_t,
                'page':0,
                'limit':10,
                "secret_key":self.g['sk'],
                "keys":'type,page,limit,secret_key',
                "sign":''
            }
            pss = self.build_sign_str(params['keys'], params)
            params['sign'] = self.get_md5(pss + self.g['secret'])
            res = requests.get(self.ep+"/children/statuses",
                            params=params)
            print(res.text)
        for _t in ts:
            print('get ' + _t)
            params = {
                'type':_t,
                "secret_key":self.g['sk'],
                "keys":'type,secret_key',
                "sign":''
            }
            pss = self.build_sign_str(params['keys'], params)
            params['sign'] = self.get_md5(pss + self.g['secret'])
            res = requests.get(self.ep+"/children/statuses",
                            params=params)
            print(res.text)
    def _test_411_children_status_get(self):
        print('get status by alias')
        params = {
            'alias':'hah',
            'startt':'2020-1-5',
            'endt':'2020-01-10',
            "secret_key":self.g['sk'],
            "keys":'endt,startt,alias,secret_key',
            "sign":''
        }
        pss = self.build_sign_str(params['keys'], params)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res = requests.get(self.ep+"/children/status",
                        params=params)
        print(res.text)
    
    def _test_500_changepw(self):
        print('send vcode')
        params = {
            'username':'t21dda',
            "email":'afatpig@foxmail.com'
        }
        res = requests.get(self.ep+"/passwd/sendVCode",
                        params=params)
        print(res.text)

        print('change pw\nplease input the verification code: \n')
        params = {
            'username':'t21dda',
            "passwd_md5":self.get_md5('hhhahahaha')
        }
        vcode = input()
        params['vcode']=vcode
        res = requests.put(self.ep+"/passwd",
                        data=params)
        print(res.text)
        self.change2parent1()
        self.change2admin()
    
    def _test_600_file_post(self):
        fs = ['Documents/API说明.pdf','Documents/API说明.docx','Documents/APP.jpg','Documents/下拉列表.txt','Documents/开发流程.png','Documents/开发流程.xmind','Documents/原型/Mobil工作流.png','Documents/设计简版.docx']
        for fn in fs:
            header={"ct":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"}
            files = {'file':open(fn,'rb')}
            params = {
                'alias':'hah',
                'secret_key':self.g['sk'],
                'keys':'alias,secret_key'
            }
            pss = self.build_sign_str(params['keys'], params)
            params['sign'] = self.get_md5(pss + self.g['secret'])
            res=requests.post(self.ep+"/file",params,files=files,headers=header)
            print(res.text)
    
    def _test_601_files(self):
        params = {
            'page':'0',
            'limit':10,
            'alias':'hah',
            'secret_key':self.g['sk'],
            'keys':'page,limit,alias,secret_key'
        }
        pss = self.build_sign_str(params['keys'], params)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res=requests.get(self.ep+"/files",params)
        print(res.text)

    def _test_602_file_get(self):
        params = {
            'id':13,
            'secret_key':self.g['sk'],
            'keys':'id,secret_key'
        }
        pss = self.build_sign_str(params['keys'], params)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res=requests.get(self.ep+"/file",params)
        print(len(res.text))

    def _test_603_file_delete(self):
        params = {
            'id':13,
            'secret_key':self.g['sk'],
            'keys':'id,secret_key'
        }
        pss = self.build_sign_str(params['keys'], params)
        params['sign'] = self.get_md5(pss + self.g['secret'])
        res=requests.delete(self.ep+"/file",data=params)
        print(res.text)

    def build_sign_str(self, keys, params):
        _ks = keys.split(',')
        _vs = [_k + "=" + str(params[_k]) for _k in _ks]
        return '&'.join(_vs)
            

    def test_a00_logout(self):
        print("Test logout")
        sign = self.get_md5("secret_key="+self.g['sk']+self.g['secret'])
        params = {
            'secret_key': self.g['sk'],
            'keys': 'secret_key',
            'sign': sign
        }
        res = requests.post(self.ep+"/logout", data=params)
        resj = res.json()
        self.assertEqual(resj['code'], 0, "error:\n"+res.text)
        print(res.text)


if __name__ == "__main__":
    unittest.main()
