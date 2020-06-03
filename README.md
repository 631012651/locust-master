                                                 **Locust�̳�**
һ����װ
$ pip3 install locust
һ����װ��Locust�������������Ӧ����һ��locust������������ʹ��virtualenv����Ӧȷ��python�ű�Ŀ¼λ��·���У���
Ҫ�鿴����ѡ������У�
$ locust --help

���ٿ�ʼ
��Locust�У�������ʹ��Python���붨���û���Ϊ��Ȼ��������ʹ�ø�locust����ͣ���ѡ����Web�������ռ�����ͳ����Ϣʱ���ɲ�ģ������û���
locustfile.pyʾ��
import random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def index_page(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(3)
    def view_item(self):
        item_id = random.randint(1, 10000)
        self.client.get(f"/item?id={item_id}", name="/item")

    def on_start(self):
        self.client.post("/login", {"username":"foo", "password":"bar"})

�����Ƿֽ�һ��
import random
from locust import HttpUser, task, between
locust�ļ�ֻ����ͨ��Pythonģ�飬�����Դ������ļ�����е�����롣
class QuickstartUser(HttpUser):
���������ΪҪģ����û�����һ���ࡣ���̳���?HttpUser��client���ԣ��Ӷ�Ϊÿ���û��ṩһ�����ԣ��������ǵ�һ��ʵ��HttpSession����������Ҫ���ز��Ե�Ŀ��ϵͳ����HTTP���󡣵����Կ�ʼʱ��locust��Ϊ��ģ���ÿ���û�����һ�������ʵ����������Щ�û��е�ÿ������ʼ���Լ�����ɫgevent�߳������С�
wait_time = between(5, 9)
���ǵ��ඨ����һ��wait_time�������ú�����ʹģ���û���ÿ������ִ�к�ȴ�5��9�롣�йظ�����Ϣ����μ�wait_time���ԡ�
@task
def index_page(self):
    self.client.get("/hello")
    self.client.get("/world")

@task(3)
def view_item(self):
    ...
���ǻ�ͨ��������������������������������@task������һ�����нϸߵ�Ȩ�أ�3�������������͵��û�����ʱ������ѡ��һ��hello��һ����view_item��������ѡ����ᣩ?view_item���ø÷�����Ȼ��ͳһѡ��һ������5��9֮��ĳ���ʱ�䣬���ڸó���ʱ�������ߡ��ȴ�ʱ���������ѡ��һ�������񲢼����ظ�ִ�С�
@task(3)
def view_item(self):
    item_id = random.randint(1, 10000)
    self.client.get(f"/item?id={item_id}", name="/item")
�ڴ�view_item�����У�����ͨ��ʹ�ò�ѯ�������ض�̬URL���ò����Ǵ�1��10000֮�����ѡ������֡�Ϊ�˲���Locust��ͳ����Ϣ�л��10k����������Ŀ-����ͳ����Ϣ�ǰ�URL����ģ��������ʹ�����Ʋ�����������Щ������鵽һ����Ϊ����Ŀ��"/item"��
��ע�⣬ֻ�������εķ���@task�ᱻ���ã���������԰��Լ�ϲ���ķ�ʽ�����Լ����ڲ�������������
def on_start(self):
���⣬���ǻ�������on_start������ÿ��ģ���û�����ʱ������þ��и����Ƶķ������йظ�����Ϣ����μ�on_start��on_stop������
locust��ʼ
������Ĵ�����ڵ�ǰĿ¼����Ϊlocustfile.py���ļ��У�Ȼ�����У�
$ locust
�������locust�ļ�λ������λ�ã������ʹ��?-f
$ locust -f locust_files/my_locust_file.py
ע��
Ҫ�鿴���п���ѡ������룺��������locust?--help

Locust���������
ʹ������������֮һ����Locust��Ӧ�ô������������ָ��http://127.0.0.1:8089��Ȼ����Ӧ�û��յ������������ݵ��ʺ�
 
��д��񲢳��ԣ�������ע�⣬�����������locust�ļ���ƥ��Ŀ��ϵͳ������������»��յ�������Ӧ��
 ? 

��дLocust�ļ�
locustfile����ͨ��python�ļ���Ψһ��Ҫ��������������һ����-���ǳ���Ϊ�Ӹ���̳е��û���User��
User class
һ���û�������һ���û������ߣ�����еĻ���һȺlocust����locust��Ϊÿ������ģ����û����ɣ�������User���һ��ʵ����User��ͨ��Ӧ����һЩ���ԡ�
wait_time attribute
����task���ԣ���Ӧ������һ��?wait_time������������ȷ��ģ���û���ִ������֮��ȴ��೤ʱ�䡣Locust����һЩ���ú�������Щ��������һЩ���õ�wait_time������
�������between��������ʹģ���û���ÿ��ִ�������ȴ�������Сֵ�����ֵ֮������ʱ�䡣�������õĵȴ�ʱ�亯����constant��?constant_pacing��
ʹ������locustfile��ÿ���û���������֮��ȴ�5��15�룺
from locust import User, task, between

class MyUser(User):
    @task
    def my_task(self):
        print("executing my_task")

    wait_time = between(5, 15)

wait_time����Ӧ�÷����������򼸷�֮һ�룩������Ҳ������TaskSet��������������������£����������ڸ�TaskSet��
Ҳ����ֱ����User��TaskSet���������Լ���wait_time�����������User�ཫ��ʼ����һ���ӣ�Ȼ������һ�����������������ơ�
class MyUser(User):
    last_wait_time = 0

    def wait_time(self):
        self.last_wait_time += 1
        return self.last_wait_time

    ...

weight attribute
����ļ��д��ڶ���û��࣬��������������δָ���κ��û��࣬��Locust���������������ÿ���û��ࡣ��������ͨ����������Ϊ�����в������ݣ���ָ��Ҫ��ͬһlocustfile��ʹ����Щ�û��ࣺ
$ locust -f locust_file.py WebUser MobileUser
�����ϣ��ģ������ض����͵��û������������Щ��������һ��weight���ԡ�������˵�������û��Ŀ��������ƶ��û���������
class WebUser(User):
    weight = 3
    ...

class MobileUser(User):
    weight = 1
    ...

host attribute
host������Ҫ���ص�������URLǰ׺������?http://google.com?������ͨ����������locust--host����ʱ��Locust��Web UI����������ʹ�ø�?ѡ��ָ���ġ�
������û������������������ԣ���--host?�������л�Web������δָ���κ���������ʱ��ʹ�ø����ԡ�
tasks attribute
User�����ʹ��@taskװ��������������Ϊ���������񣬵���Ҳ����ʹ��task����ָ�������⽫���������ϸ��������

Tasks
�������ز��Ժ󣬽�Ϊÿ��ģ���û�����һ��User���ʵ�����������ǽ������Լ�����ɫ�߳������С���Щ�û�����ʱ������ѡ��ִ�е���������һ�����Ȼ��ѡ��һ���������������ơ�
��Щ��������ͨ��python�ɵ��ö��󣬲���-����������ڶ�������վ���и��ز���-�����ǿ���ִ�����硰������ʼҳ����������ĳЩ��Ʒ���������ꡱ�ȹ�����
Declaring tasks
�����û��ࣨ��TaskSet��ʹ��taskװ����������ĵ��ͷ���?��
����һ�����ӣ�
from locust import User, task, constant

class MyUser(User):
    wait_time = constant(1)

    @task
    def my_task(self):
        print("User instance (%r) executing my_task" % self)
@task���ÿ�ѡ��weight�������ò���������ָ�������ִ���ʡ�������ʾ���У�task2��ѡ��Ϊtask1�Ļ�����������
from locust import User, task, between

class MyUser(User):
    wait_time = between(5, 15)

    @task(3)
    def task1(self):
        pass

    @task(6)
    def task2(self):
        pass

tasks attribute
ʹ��@taskװ��������������һ�ֱ�����ͨ����ִ���������ѷ��������ǣ�Ҳ����ͨ������tasks����������User��TaskSet������?��ʹ��@taskװ����ʵ����ֻ�����task���ԣ���
����������Ϊ������б���<task��int>���ֵ䣬���У����������һ���ɵ���python��ʹ��taskset�ࣨ���ڸ��ࣩ�������������ͨ��python�����������ǻ��յ�һ��������������ִ�������Userʵ����
��������Ϊ��ͨpython������User�����ʾ����
from locust import User, constant

def my_task(l):
    pass

class MyUser(User):
    tasks = [my_task]
    wait_time = constant(1)
�����task����ָ��Ϊ�б���ÿ��ִ������ʱ�������task���������ѡ���������ǣ�����������ֵ䣬�򽫿ɵ�������Ϊ������������Ϊֵ�������ѡ��Ҫִ�е����񣬵���������Ϊ���ʡ���ˣ�����������������
{my_task: 3, another_task: 1}
my_task��ִ�п�������another_task��?3����
���ڲ��������dictʵ���Ͻ���չΪ������ʾ���б�����tasks�����Ѹ��£���
[my_task, my_task, my_task, another_task]
Ȼ��ʹ��Python��random.choice()���б���ѡ������
Tagging tasks
ͨ��ʹ�ñ��<locust.tag>װ�����������������ʹ��--tags��--exclude-tags�����Բ����ڼ�ִ�е����񱣳ֽ�������������ʾ����
from locust import User, constant, task, tag

class MyUser(User):
    wait_time = constant(1)

    @tag('tag1')
    @task
    def task1(self):
        pass

    @tag('tag1', 'tag2')
    @task
    def task2(self):
        pass

    @tag('tag3')
    @task
    def task3(self):
        pass

    @task
    def task4(self):
        pass
�����ʹ���������˲��ԣ����ڲ����ڼ佫��ִ��task1��task2��������Կ�ͷ����ֻ��ִ��task2��task3��--tags?tag1--tags?tag2?tag3
--exclude-tags��Ϊ����ȫ�෴�����ԣ�����㿪ʼ����?��ֻ��TASK1��TASK2��task4����ִ�С��ų�����ʤ�ڰ�������ˣ����������а����ı�ǩ�Ͱ����ı�ǩ��������񽫲���ִ�С�--exclude-tags?tag3
TaskSet class
����ʵ�ʵ���վͨ���Էֲ�ķ�ʽ��������������Ӳ��֣����locust����TaskSet�ࡣlocust���񲻽�������Python�ɵ��õģ���������TaskSet�ࡣTaskSet��locust����ļ��ϣ�����ֱ����User��������������һ��ִ�У�ʹ�û�����������ִ��֮�䴦������״̬������һ������TaskSet��locustfile�ļ��ʾ����
from locust import User, TaskSet, between

class ForumSection(TaskSet):
    @task(10)
    def view_thread(self):
        pass

    @task(1)
    def create_thread(self):
        pass

    @task(1)
    def stop(self):
        self.interrupt()

class LoggedInUser(User):
    wait_time = between(5, 120)
    tasks = {ForumSection:2}

    @task
    def index_page(self):
        pass
Ҳ����ʹ��@taskװ����ֱ����User / TaskSet��������TaskSet��
class MyUser(User):
    @task(1)
    class MyTaskSet(TaskSet):
        ...
TaskSet����������������TaskSet�࣬�Ӷ����Խ�����Ƕ���κ������ļ�����ʹ�����ܹ�����һ����Ϊ���Ը���ʵ�ķ�ʽģ���û���
���磬���ǿ���ʹ�����½ṹ����TaskSet��
- Main user behaviour
  - Index page
  - Forum page
    - Read thread
      - Reply
    - New thread
    - View next page
  - Browse categories
    - Watch movie
    - Filter movies
  - About page
�������е��û��߳�ѡ��TaskSet��ִ��ʱ�������������ʵ����Ȼ��ִ�н������TaskSet��Ȼ�������ǣ���ʰȡ��ִ��TaskSet������֮һ��Ȼ���߳̽�����һ��ʱ�䣬�ó���ʱ����User��wait_time����ָ��������wait_time��ֱ����TaskSet������������������������£�����ʹ�øú�������Ȼ���TaskSet��������ѡ��һ��������Ȼ���ٴεȴ����������ơ�
 
�ж�����
�й�TaskSet����Ҫһ������������Զ����ִֹͣ�������񣬶���ִ�н��������Լ��ĸ�User / TaskSet��������ɿ�����Աͨ������TaskSet.interrupt()��������ɡ�
interrupt��self��reschedule = True?��
�ж�TaskSet����ִ�п����ƽ�����TaskSet��
���rescheduleΪTrue��Ĭ�ϣ������û����������°��Ų�ִ��������
�������ʾ���У��������û�е���stop����self.interrupt()����ôģ���û�һ��������̳�����о���Զ����ֹͣ���и�����
class RegisteredUser(User):
    @task
    class Forum(TaskSet):
        @task(5)
        def view_thread(self):
            pass

        @task(1)
        def stop(self):
            self.interrupt()

    @task
    def frontpage(self):
        pass
ʹ���жϹ��ܣ����ǿ���������Ȩ��һ����ģ���û��뿪��̳�Ŀ����ԡ�
TaskSet��User���е�����֮��Ĳ���
��ֱ��פ����User�µ�������ȣ�פ����TaskSet�µ�����Ĳ�֮ͬ�����ڣ�������ִ��ʱ���ݵĲ�����self����ʹ��@taskװ��������Ϊ�����������Ƕ�TaskSetʵ�������ã�������Userʵ�������Դ�TaskSetʵ����ͨ������Userʵ��?TaskSet.user��TaskSet������һ�����?client���ԣ�����������Userʵ���ϵ�client���ԡ�
SequentialTask??Set��
SequentialTaskSet��TaskSet���������񽫰���������˳��ִ�С�SequentialTask??Set���ϵ������Ȩ�ؽ������ԡ����Խ�SequentialTask??SetsǶ����TaskSet�У���֮��Ȼ��
def function_task(taskset):
    pass

class SequenceOfTasks(SequentialTaskSet):
    @task
    def first_task(self):
        pass

    tasks = [functon_task]

    @task
    def second_task(self):
        pass

    @task
    def third_task(self):
        pass
�������ʾ���У�������������˳��ִ�У�
1.	first_task
2.	function_task
3.	second_task
4.	third_task
Ȼ���������¿�ʼfirst_task��
on_start��on_stop����
�û���TaskSet���������һ��on_start������/��?on_stop�������û�on_start�ڿ�ʼ����ʱ���������ķ�������on_stop��ֹͣ����ʱ����������?����?������TaskSet����?on_start������ģ���û���ʼִ�и�TaskSet?on_stopʱ�����ã�����ģ���û�ִֹͣ�и�TaskSetʱinterrupt()�����ã�������ʱ��ɱ�����û�ʱ����
test_start��test_stop�¼�
�����Ҫ�ڸ��ز��ԵĿ�ʼ�����ʱ����һЩ���룬��Ӧʹ��?test_start��test_stop?�¼�����������locustfile��ģ�鼶��Ϊ��Щ�¼�������������
from locust import events

@events.test_start.add_listener
def on_test_start(**kwargs):
    print("A new test is starting")

@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print("A new test is ending")
������Locust�ֲ�ʽϵͳʱ��test_start��test_stop�¼����������ڵ��д���
����HTTP����
��ĿǰΪֹ�����ǽ�������User������ƻ����֡�Ϊ��ʵ�ʸ��ز���ϵͳ��������Ҫ����HTTP����Ϊ�˰�������������һ�㣬HttpLocust?������ڡ�ʹ�ô���ʱ��ÿ��ʵ��������һ��client���ԣ���?���Խ���HttpSession�������ڷ���HTTP�����һ��ʵ��?��
Class HttpUser(*args,?**kwargs) 
��ʾҪ������������Ҫ���и��ز��Ե�ϵͳ��HTTP���û�����
���û�����Ϊ���������塣����ʹ��on����ֱ����������������Ҳ����ͨ����������������@task?decoratortasks?attribute
������ʵ����ʱ����һ���ͻ������ԣ���������һ��HTTP�ͻ��ˣ�֧��������֮�䱣���û��Ự��
client= None
	��Locustʵ�����󴴽���HttpSessionʵ�����ͻ���֧��cookie����˱���HTTP����֮��ĻỰ��
��HttpUser��̳�ʱ�����ǿ���ʹ����client���ԶԷ���������HTTP��������һ���ȳ��ļ���ʾ���������ڶԾ�������URL��վ����и��ز��ԡ�/��/ about /��
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(5, 15)

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def about(self):
        self.client.get("/about/")
ʹ�������User�࣬ÿ��ģ���û���������֮��ȴ�5��15�룬����/���������������/ about /��������
ʹ��HTTP�ͻ���
HttpUser��ÿ��ʵ��HttpSession?��client�����ж���һ��ʵ������HttpSession��ʵ������һ������?requests.Session������������HTTP���󣬽�ʹ�ñ�����û���ͳ�ƣ�get��?post��put��?delete��head��?patch��options?������HttpSessionʵ����������֮�䱣��cookie���Ա�����ڵ�¼��վ��������֮�䱣�ֻỰ��Ҳ���Դ�Userʵ����TaskSetʵ��������client���ԣ��Ա����ɵش����������м����ͻ��˲�����HTTP����
����һ���򵥵�ʾ��������/ about·������GET��������������£����Ǽ���self?��TaskSetor��HttpUser?class?��ʵ����
response = self.client.get("/about")
print("Response status code:", response.status_code)
print("Response content:", response.text)
���Ƿ���POST�����ʾ����
response = self.client.post("/login", {"username":"testuser", "password":"secret"})
��ȫģʽ
HTTP�ͻ�������Ϊ��safe_mode���С�������Ϊ�������Ӵ��󣬳�ʱ������ԭ���ʧ�ܵ��κ����󶼲��������쳣�����Ƿ���һ���յ�����Response���󡣸��������û�ͳ����Ϣ�б���Ϊʧ�ܡ����ص�����Response��content���Խ�����ΪNone����status_code��Ϊ0��
�ֶ����������ǳɹ�����ʧ��
Ĭ������£�����HTTP��Ӧ����ΪOK��<400�����������󽫱����Ϊʧ�ܵ����󡣴��������£���Ĭ��ֵ������Ҫ�ġ����ǣ���ʱ�����磬��������ϣ������404��URL�˵�ʱ�����߲�����ƴ����ϵͳ����ʹ�������󣬸�ϵͳҲ���ܷ���200 OK������Ҫ�ֶ����ƻȳ��Ƿ�Ӧ��������Ϊ�ɹ���ʧ�ܡ�ʧ�ܡ�
ͨ��ʹ��catch_response������with��䣬��ʹ��Ӧ������ȷ��Ҳ���Խ�������Ϊʧ��?��
with self.client.get("/", catch_response=True) as response:
    if response.content != b"Success":
        response.failure("Got wrong response")
������Խ�����OK��Ӧ�����������Ϊʧ��һ����Ҳ���Խ�catch_response?������with���һ��ʹ�ã���ʹ����HTTP��������������ͳ����Ϣ���Ա�����Ϊ�ɹ���
with self.client.get("/does_not_exist/", catch_response=True) as response:
    if response.status_code == 404:
        response.success()
ʹ�ö�̬������������ķ���
��վ�ϵ�URL����ĳ�ֶ�̬������ҳ���Ǻܳ����ġ�ͨ�������û���ͳ����Ϣ�н���ЩURL������һ���Ǻ�������ġ������ͨ����name�������ݸ�HttpSession's?��ͬ�����󷽷�����ɡ�
����
# Statistics for these requests will be grouped under: /blog/?id=[id]
for i in range(10):
    self.client.get("/blog?id=%i" % i, name="/blog?id=[id]")

��ι������Դ���
��Ҫ����Ҫ��ס��locustfile.pyֻ����Locust�������ͨPythonģ�顣�Ӹ�ģ���У������������κ�Python������һ�������ص�������python���롣��ǰ�Ĺ���Ŀ¼���Զ���ӵ�python��Ŀ¼��sys.path����˿���ʹ��python?import��䵼�빤��Ŀ¼�е�����python�ļ�/ģ��/�������
����С�Ͳ��ԣ������в��Դ��뱣����һ����locustfile.pyӦ�ÿ����������������Ƕ��ڴ��Ͳ����׼�����������Ҫ��������Ϊ����ļ���Ŀ¼��
��Ȼ����������Դ����ķ�ʽ��ȫȡ���������������ǽ�������ѭPython���ʵ��������һ���鹹��Locust��Ŀ��ʾ���ļ��ṹ��
��	��Ŀ��Ŀ¼
o	common/
��	__init__.py
��	auth.py
��	config.py
o	locustfile.py
o	requirements.txt?���ⲿPython������ͨ��������requirements.txt�У�
���ж����ͬlocustfiles����ĿҲ���Խ����Ǳ����ڵ�������Ŀ¼�У�
��	��Ŀ��Ŀ¼
o	common/
��	__init__.py
��	auth.py
��	config.py
o	locustfiles/
��	api.py
��	website.py
o	requirements.txt
ʹ�������κ���Ŀ�ṹ������locustfile������ʹ�����·������빫���⣺
import common.auth

��û��Web UI�����������locust
��������û��Web UI�����������locust-���磬�����ϣ����ĳ���Զ������̣�����CI������������locust���뽫��--headless��־��-u��һ��ʹ��-r��
$ locust -f locust_files/my_locust_file.py --headless -u 1000 -r 100
-uָ��Ҫ�������û�������-rָ������ʣ�ÿ��Ҫ�������û�������
���ò���ʱ������
���Ҫָ�����Ե�����ʱ�䣬����ʹ��--run-time����в���-t��
$ locust -f --headless -u 1000 -r 100 --run-time 1h30m

���������ڹر�ʱ��ɵ���
Ĭ������£�locust������ֹͣ�����������������������ɵ����������ʹ�á�--stop-timeout?<seconds>
$ locust -f --headless -u 1000 -r 100 --run-time 1h30m --stop-timeout 99

��û��Web UI�����������Locust�ֲ�ʽ
���Ҫ��û��Web UI�����������Locust�ֲ�ʽ����Ӧ--expect-workers���������ڵ�ʱָ����ѡ���ָ��Ԥ��Ҫ���ӵĸ����ڵ��������Ȼ�������ȴ�ֱ����๤���ڵ������ӣ�Ȼ����ܿ�ʼ���ԡ�
����locust���̵��˳�����
��CI����������Locustʱ��������ϣ������Locust���̵��˳����롣������ͨ������ʵ�������ڲ��Խű�?process_exit_code��ִ�д˲���?Environment��
�����ʾ����������������һ����ʱ���˳���������Ϊ���㣺
��	����1��������ʧ��
��	ƽ����Ӧʱ�䳬��200����
��	��Ӧʱ��ĵ�95���ٷ�λ������800����
import logging
from locust import events

@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 800:
        logging.error("Test failed due to 95th percentil response time > 800 ms")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0
���˴�����Է���locustfile.py��locustfile�е�����κ������ļ��У�
�������·��
Locustʹ��Flask���ṩWeb UI����˺����׽�Web�˵���ӵ�Web UI��ͨ������init�¼������ǿ��Լ�����FlaskӦ�ó���ʵ�������ã���ʹ�ø������������µ�·�ɣ�
from locust import events

@events.init.add_listener
def on_locust_init(web_ui, **kw):
    @web_ui.app.route("/added_page")
    def my_added_page():
        return "Another page"
���ڣ���Ӧ���ܹ������ȳ沢�����http://127.0.0.1:8089/added_pa??ge
��һ��??��ǰ



FAQ
locust������򲻿�WebUI���ҳ��
�������
���ӨCweb-host����
locust -f load_test.py --web-host="127.0.0.1"


