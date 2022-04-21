1. 安裝說明：
    環境：python3.7，請使用pip install -r requirements.txt安裝依賴項；
    需要使用MySQL數據庫。

2. 配置說明：
    文件config.conf是配置文件，請依照格式將配置設定好，使程序正常運行。最主要的幾個設置是：
        database相關設置，用於連接數據庫；
        web相關設置，用於配置服務器；
        mail相關設置，用於配置電子郵箱以發送郵件驗證碼。
    admin.txt裡配置了管理員賬號，系統初始化時會自動載入賬號，可以自行編寫但必須依照完全相同的格式。管理員賬號可以這樣設置，但其他角色的賬號必須通過網頁或API註冊。

3. 運行說明：
    在安裝好依賴，啟動MySQL，配置好相關參數以後，可以直接在根目錄下運行python main.py，也可以點擊runserver.bat啟動服務器。

4. 文件說明：
    data/:      初始化數據，包括下拉列表等等。
    Documents/: 文檔
    files/:     用戶上傳的文件
    logs/:      網站運行的log
    static/:    圖片、css、js、字體、國際化文件等等，包括自行編寫的和使用的第三方前端庫文件
    templates/: 前端HTML模板文件
    admin.txt:  用於初始化admin用戶賬號
    build.sql:  數據庫建庫代碼（不用手動建庫，程序第一次運行會自動建庫）
    config.conf:配置文件
    main.py:    主入口
    preenv.py:  構建初始化環境，主要是建立數據庫結構
    test.py:    部分API測試
    test.rest:  部分API測試
    api_xxx.py: API實現代碼
    pg_xxx.py:  頁面響應代碼

具体做了：
$git clone https://github.com/afatpig/BabyInfo.git
$cd BabyInfo
$sudo yum install -y mysql-server （安裝MySQL Server）
$sudo yum install -y mysql-devel (安装MySQL头文件，因为安装mysqlclient 报错是缺少mysql.h)
$sudo python -m pip install -r requirements.txt （安装依赖）
$sudo service mysqld start （启动MySQL）
$sudo mysqladmin -u root password 'cnujireau3289h' (修改MySQL密码)
$nano config.conf (编辑修改程序的数据库配置)
$python -m venv venv
$. venv/bin/activate
$python -m pip install --upgrade pip (更新pip)
$python main.py (运行)