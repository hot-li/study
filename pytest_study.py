"""
# http://www.51testing.com/html/74/n-4476374.html
#案例一：fixture的基本操作

import pytest
#指定为类夹具时，整个类运行执行一次这个夹具，且yield之前为setup操作，yield为teardown操作，teardown操作非必须
#pytest.fixture入参1：scope
#不指定scope时，默认为function级别，也就是用例级别，在调用时，每次都会执行fixture装饰的函数
'''
用例级别：scope = function
测试类级：scope = class
模块级别：scope = module
包级别： scope = package
会话级别：scope = session
执行顺序：packages>>session>>module>>class>>function
'''
##pytest.fixture入参1：autouse
#autouse=True:表示将fixture方法作用于控制fixture作用范围内的是否全部执行，比如下面函数即使在类方法中不传入具体的fixture也会全部执行fixture

@pytest.fixture(scope='class')
def login():
    print('登录操作')
    yield
    print('退出登录')

@pytest.fixture()
def log():
    print('需要日志')

class Test_login():
    def test_01(self,login,log):
        print('这里需要用到登录')

    def test_02(self):
        print('这里不需要用到登录')
        assert 1==1

    def test_03(self,log,login):
        print('这里也需要用到登录')
        assert 3==3

if __name__=='__main__':
    pytest.main(['vs'])



#案例二：fixture的相互调用:在fixture中传入另外个fixture的名字
import pytest

@pytest.fixture(scope='class')
def login():
    print('登录操作')
    yield
    print('退出登录')

@pytest.fixture()
def log(login):
    print('需要日志')

class Test_login():
    def test_01(self,log):
        print('这里需要用到登录')

if __name__=='__main__':
    pytest.main(['vs'])


#案例三：调用外部的自定义fixture
import pytest

class Test_login():
    def test_01(self,my_fixture):
        print('这里需要用到登录')

if __name__=='__main__':
    pytest.main(['vs'])


#案例四：标记单传参，参数化
#https://www.yht7.com/news/204465

import pytest
phone_list=['13612345678','15678909876','13787653653']

@pytest.mark.parametrize(argnames='phone_num',argvalues=phone_list)
def test_phone_number(phone_num): # 注意，这里的参数要和argnames参数名一致
    print('正在测试手机号{phone_num}')
if __name__=='__main__':
    pytest.main(['vs'])

#案例五：无跳过
import  pytest

@pytest.mark.skip
def test_reg():
    raise Exception('该功能暂未开发')
@pytest.mark.skip(reason='原因：该功能也没有开发完成')
#可以指定跳过的原因，非必须
def test_logout():
    raise Exception('该功能暂未开发完成')

def test_login():
    assert True

if __name__=='__main__':
    pytest.main(['vs'])

#案例六：有条件跳过

import  pytest
'''
使用方法：通过@pytest.mark.skipif(condition=跳过条件，reason=跳过原因)标记要跳过的测试用例。
参数condition：跳过的条件，值为True则跳过，值为False则继续执行，默认值为True
参数reason：必填，跳过的原因
'''
version=3
@pytest.mark.skipif(condition= version==3,reason='原因是ersion>3')
def test_reg():
    raise Exception('该功能暂未开发')

def test_login():
    assert True

if __name__=='__main__':
    pytest.main(['vs'])


#案例七：多参数传参+别名
import pytest

user_info = [
    ("张三", "18011111111"),
    ("李四", "18022222222"),
    ("王五", "18033333333")
]

@pytest.mark.parametrize(argnames="name,phonenum", argvalues=user_info,ids=['用户1','用户2','用户3'])
def test_read_info(name, phonenum):
    print(f"正在读取用户{name}，手机号{phonenum}")
    #会乱码，解决方法
    '''
    方法1. 在pytest.ini中加入disable_test_id_escaping_and_forfeit_all_rights_to_community_support=True
    方法2. 在conftest.py中加入
    # 收集每一个用例name和nodeid的中文显示，转化为utf-8形式
    def pytest_collection_modifyitems(items):
        for item in items:
            item.name = item.name.encode("utf-8").decode("unicode_escape")
            item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")
    '''

'''
#使用pytest-testreport生成报告
if __name__=='__main__':
    pytest.main(['sv','--report=musen.html',
                 '--title=演示A报告',
                 '--tester=测试员',
                 '--desc=报告描述信息',
                 '--template=2'])
'''

"""

#案例七-1：使用Allure生成报告
import pytest
import allure

@allure.story('登录功能')
class login():
    @allure.title('用例3')
    def test_03(self):
        print('测试用例3操作')
    @allure.title('用例4')
    def test_04(self):
        print('测试用例4操作')

if __name__ == "__main__":
    pytest.main(['-s', '-v', '--alluredir', './reports'])

"""
#案例七：失败重试
#失败重试
#pip install pytest-rerunfailures
#@pytest.mark.flaky(retun=1,reruns_delay=5) 重跑次数与重跑延迟时间
import pytest
import  requests
@pytest.mark.flaky(retun=1,reruns_delay=5)
def test():
    requests.get('http://234234234324.com')

if __name__=='__main__':
    pytest.main(['sv'])
"""
"""
#案例八：pip install pytest-ordering  控制用例的执行顺序（重点）
#@pytest.mark.run(order=4)的方式就不写代码了

#案例九：pip install pytest-xdist 多进程pytest-xdist
# https://www.cnblogs.com/guanqibuyu/p/16549822.html
# pytest test_add.py -n NUM    # NUM表示并发的进程数
'''
参数配置：
-n=* ：*代表进程数

解释：
①多cpu并行执行用例，直接加个-n参数即可，后面num参数就是并行数量，比如num设置为3
②-n auto ： 自动侦测系统里的CPU数目
③-n num ： 指定运行测试的处理器进程数
'''
#案例十：pip install pytest-parallel多线程pytest-parallel
'''
常用参数配置
① --workers=n ：多进程运行需要加此参数， n是进程数。默认为1
② --tests-per-worker=n ：多线程需要添加此参数，n是线程数
如果两个参数都配置了，就是进程并行；每个进程最多n个线程，总线程数：进程数*线程数

【注意】
①在windows上进程数永远为1。
②需要使用 if name == “main” :，在dos中运行会报错（即在命令行窗口运行测试用例会报错）

示例：
pytest test.py --workers 3 ：3个进程运行
pytest test.py --tests-per-worker 4：4个线程运行
pytest test.py --workers 2 --tests-per-worker 4 ：2个进程并行，且每个进程最多4个线程运行，即总共最多8个线程运行。
'''
import pytest
def test_03():
    print('测试用例3操作')
def test_04():
    print('测试用例4操作')

if __name__ == "__main__":
    pytest.main(["-s", "test_b.py", '--workers=2', '--tests-per-worker=4'])

'''
pytest-parallel与pytest-xdist对比说明
① pytest-parallel 比 pytst-xdist 相对好用，功能支持多。
② pytst-xdist 不支持多线程；
③pytest-parallel 支持python3.6及以上版本，所以如果想做多进程并发在linux或者mac上做，在Windows上不起作用（Workers=1），如果做多线程linux/mac/windows平台都支持，进程数为workers的值。
'''
"""
