#python_api_test  
适用于http以及https接口测试。
可接受接口返回值未json字符。
需要注意的是发送参数使用加密规则，如无需加密，使用则需移除相关参数。
采用python-requests+pytest+yaml+allure实现对数据读取，接口发送请求值校验，测试报告输出。

##所需安装第三方包：  
1. pyyaml  
安装方式: pip install pyyaml  
http://pyyaml.org/
2. pytest  
安装方式: pip install pytest  
http://pytest.org/  
3. requests  
安装方式: pip install requests  
http://python-requests.org/  
4. pytest-allure-adaptor  
安装方式: pip install pytest-allure-adaptor  
https://github.com/allure-framework/allure-python  
5. pytest-timeout  
安装方式: pip install pytest-timeout  
https://bitbucket.org/pytest-dev/pytest-timeout/  
6. pytest-ordering  
安装方式: pip install pytest-ordering  
https://github.com/ftobia/pytest-ordering  
7. allure-command-line  
mac安装方式: brew install allure  
win安装方式:  
1)下载allure-command-line的安装包  
https://github.com/allure-framework/allure-core/releases/latest  
2)解压缩至allure-commandline目录  
3)*将该目录添加至环境变量  
4)使用bin目录下的allure.bat或allure执行    

##工程目录：  
python_api_test  
│  base_test.py  
│  README.md  
│  runner.py  
│  utils.py  
│  
├─configs  
│  │  config.yaml  
│  │  temp.yaml  
│  │  
│  └─user  
│          login.yaml  
│  
├─report  
│  │  
│  └─html  
├─tests  
│  │  login_test.py  

base_test.py    基础测试类，可添加测试用例setup, teardown方法与其他可继承的测试用例属性  
README.md   介绍文件  
runner.py        执行入口  
test_temp.py   测试文件，可忽略  
utils.py            工具组件类，包含测试用例中使用的一些方法  
configs            配置文件区域，包含测试工程配置文件与接口数据配置文件，接口数据类配置文件按照原接口地址放置  
report              测试报告生成目录，包含allure测试报告与allure-html测试报告  
tests                 测试用例目录，放置测试用例目录  

##要点：    
1. openssl需更新至最新版本  
2. 注意pytest包相关的兼容版本  
3. 接口请求包含unicode字符串时需注意处理  

##命令行运行：  
python3 -m pytest xxxx --alluredir yyyy  
xxxx: pytest的执行目录或者执行文件  
yyyy: allure测试报告的输出目录  

##生成报告：  
allure generate xxxx -o yyyy  
xxxx: allure测试报告的输出目录  
yyyy: allure-html测试报告的输出目录  