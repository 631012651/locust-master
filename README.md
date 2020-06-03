                                                 **Locust教程**
一、安装
$ pip3 install locust
一旦安装了Locust，在您的外壳中应该有一个locust命令。（如果您不使用virtualenv，则应确保python脚本目录位于路径中）。
要查看可用选项，请运行：
$ locust --help

快速开始
在Locust中，您可以使用Python代码定义用户行为。然后，您可以使用该locust命令和（可选）其Web界面在收集请求统计信息时生成并模拟大量用户。
locustfile.py示例
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

让我们分解一下
import random
from locust import HttpUser, task, between
locust文件只是普通的Python模块，它可以从其他文件或包中导入代码。
class QuickstartUser(HttpUser):
在这里，我们为要模拟的用户定义一个类。它继承自?HttpUser该client属性，从而为每个用户提供一个属性，该属性是的一个实例HttpSession，可用于向要加载测试的目标系统发出HTTP请求。当测试开始时，locust将为它模拟的每个用户创建一个此类的实例，并且这些用户中的每个将开始在自己的绿色gevent线程中运行。
wait_time = between(5, 9)
我们的类定义了一个wait_time函数，该函数将使模拟用户在每个任务执行后等待5到9秒。有关更多信息，请参见wait_time属性。
@task
def index_page(self):
    self.client.get("/hello")
    self.client.get("/world")

@task(3)
def view_item(self):
    ...
我们还通过用修饰两个方法来声明了两个任务@task，其中一个具有较高的权重（3）。当这种类型的用户运行时，它会选择一个hello或一个（view_item有三倍的选择机会）?view_item调用该方法，然后统一选择一个介于5到9之间的持续时间，并在该持续时间内休眠。等待时间过后，它将选择一个新任务并继续重复执行。
@task(3)
def view_item(self):
    item_id = random.randint(1, 10000)
    self.client.get(f"/item?id={item_id}", name="/item")
在此view_item任务中，我们通过使用查询参数加载动态URL，该参数是从1到10000之间随机选择的数字。为了不在Locust的统计信息中获得10k个单独的条目-由于统计信息是按URL分组的，因此我们使用名称参数将所有这些请求分组到一个名为的条目下"/item"。
请注意，只有用修饰的方法@task会被调用，因此您可以按自己喜欢的方式定义自己的内部帮助器方法。
def on_start(self):
此外，我们还声明了on_start方法。每个模拟用户启动时都会调用具有该名称的方法。有关更多信息，请参见on_start和on_stop方法。
locust开始
将上面的代码放在当前目录中名为locustfile.py的文件中，然后运行：
$ locust
如果您的locust文件位于其他位置，则可以使用?-f
$ locust -f locust_files/my_locust_file.py
注意
要查看所有可用选项，请输入：或检查配置locust?--help

Locust的网络界面
使用上述命令行之一启动Locust后，应该打开浏览器并将其指向http://127.0.0.1:8089。然后，您应该会收到类似以下内容的问候：
 
填写表格并尝试！（但请注意，如果您不更改locust文件以匹配目标系统，则大多数情况下会收到错误响应）
 ? 

编写Locust文件
locustfile是普通的python文件。唯一的要求是它声明至少一个类-我们称它为从该类继承的用户类User。
User class
一个用户类别代表一个用户（或者，如果有的话，一群locust）。locust将为每个正在模拟的用户生成（孵化）User类的一个实例。User类通常应定义一些属性。
wait_time attribute
除了task属性，还应该声明一个?wait_time方法。它用于确定模拟用户在执行任务之间等待多长时间。Locust带有一些内置函数，这些函数返回一些常用的wait_time方法。
最常见的是between。它用于使模拟用户在每次执行任务后等待介于最小值和最大值之间的随机时间。其他内置的等待时间函数是constant和?constant_pacing。
使用以下locustfile，每个用户将在任务之间等待5到15秒：
from locust import User, task, between

class MyUser(User):
    @task
    def my_task(self):
        print("executing my_task")

    wait_time = between(5, 15)

wait_time方法应该返回秒数（或几分之一秒），并且也可以在TaskSet类上声明，在这种情况下，它将仅用于该TaskSet。
也可以直接在User或TaskSet类上声明自己的wait_time方法。下面的User类将开始休眠一秒钟，然后休眠一，二，三，依此类推。
class MyUser(User):
    last_wait_time = 0

    def wait_time(self):
        self.last_wait_time += 1
        return self.last_wait_time

    ...

weight attribute
如果文件中存在多个用户类，并且在命令行上未指定任何用户类，则Locust将产生相等数量的每个用户类。您还可以通过将它们作为命令行参数传递，来指定要从同一locustfile中使用哪些用户类：
$ locust -f locust_file.py WebUser MobileUser
如果您希望模拟更多特定类型的用户，则可以在这些类上设置一个weight属性。举例来说，网络用户的可能性是移动用户的三倍：
class WebUser(User):
    weight = 3
    ...

class MobileUser(User):
    weight = 1
    ...

host attribute
host属性是要加载的主机的URL前缀（即“?http://google.com?”）。通常，这是在locust--host启动时在Locust的Web UI或命令行中使用该?选项指定的。
如果在用户类中声明了主机属性，则--host?在命令行或Web请求中未指定任何主机属性时将使用该属性。
tasks attribute
User类可以使用@task装饰器在其下声明为方法的任务，但是也可以使用task属性指定任务，这将在下面更详细地描述。

Tasks
启动负载测试后，将为每个模拟用户创建一个User类的实例，并且它们将在其自己的绿色线程中运行。这些用户运行时，他们选择执行的任务，休眠一会儿，然后选择一个新任务，依此类推。
这些任务是普通的python可调用对象，并且-如果我们正在对拍卖网站进行负载测试-则它们可以执行诸如“加载起始页”，“搜索某些产品”，“竞标”等工作。
Declaring tasks
声明用户类（或TaskSet）使用task装饰器的任务的典型方法?。
这是一个例子：
from locust import User, task, constant

class MyUser(User):
    wait_time = constant(1)

    @task
    def my_task(self):
        print("User instance (%r) executing my_task" % self)
@task采用可选的weight参数，该参数可用于指定任务的执行率。在以下示例中，task2被选择为task1的机会是两倍：
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
使用@task装饰器声明任务是一种便利，通常是执行任务的最佳方法。但是，也可以通过设置tasks属性来定义User或TaskSet的任务?（使用@task装饰器实际上只是填充task属性）。
在任务属性为任务的列表，或<task：int>的字典，其中，任务或者是一个可调用python或使用taskset类（低于更多）。如果任务是普通的python函数，则它们会收到一个参数，即正在执行任务的User实例。
这是声明为普通python函数的User任务的示例：
from locust import User, constant

def my_task(l):
    pass

class MyUser(User):
    tasks = [my_task]
    wait_time = constant(1)
如果将task属性指定为列表，则每次执行任务时，都会从task属性中随机选择它。但是，如果任务是字典，则将可调用项作为键，将整数作为值，则将随机选择要执行的任务，但将整数作为比率。因此，任务看起来像这样：
{my_task: 3, another_task: 1}
my_task的执行可能性是another_task的?3倍。
在内部，上面的dict实际上将扩展为如下所示的列表（并且tasks属性已更新）：
[my_task, my_task, my_task, another_task]
然后使用Python的random.choice()从列表中选择任务。
Tagging tasks
通过使用标记<locust.tag>装饰器标记任务，您可以使用--tags和--exclude-tags参数对测试期间执行的任务保持谨慎。考虑以下示例：
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
如果您使用来启动此测试，则在测试期间将仅执行task1和task2。如果您以开头，则只会执行task2和task3。--tags?tag1--tags?tag2?tag3
--exclude-tags行为将完全相反。所以，如果你开始测试?，只有TASK1，TASK2和task4将被执行。排除总是胜于包含，因此，如果任务具有包含的标签和包含的标签，则该任务将不会执行。--exclude-tags?tag3
TaskSet class
由于实际的网站通常以分层的方式构建，包括多个子部分，因此locust具有TaskSet类。locust任务不仅可以是Python可调用的，还可以是TaskSet类。TaskSet是locust任务的集合，将像直接在User类上声明的任务一样执行，使用户在两次任务执行之间处于休眠状态。这是一个带有TaskSet的locustfile的简短示例：
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
也可以使用@task装饰器直接在User / TaskSet类下内联TaskSet：
class MyUser(User):
    @task(1)
    class MyTaskSet(TaskSet):
        ...
TaskSet类的任务可以是其他TaskSet类，从而可以将它们嵌套任何数量的级别。这使我们能够定义一种行为，以更现实的方式模拟用户。
例如，我们可以使用以下结构定义TaskSet：
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
当运行中的用户线程选择TaskSet类执行时，将创建该类的实例，然后执行将进入该TaskSet。然后发生的是，将拾取并执行TaskSet的任务之一，然后线程将休眠一段时间，该持续时间由User的wait_time函数指定（除非wait_time已直接在TaskSet类上声明函数，在这种情况下，它将使用该函数），然后从TaskSet的任务中选择一个新任务，然后再次等待，依此类推。
 
中断任务集
有关TaskSet的重要一件事是它们永远不会停止执行其任务，而将执行交给他们自己的父User / TaskSet。这必须由开发人员通过调用TaskSet.interrupt()方法来完成。
interrupt（self，reschedule = True?）
中断TaskSet并将执行控制移交给父TaskSet。
如果reschedule为True（默认），则父用户将立即重新安排并执行新任务。
在下面的示例中，如果我们没有调用stop任务self.interrupt()，那么模拟用户一旦进入论坛任务集中就永远不会停止运行该任务：
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
使用中断功能，我们可以与任务权重一起定义模拟用户离开论坛的可能性。
TaskSet和User类中的任务之间的差异
与直接驻留在User下的任务相比，驻留在TaskSet下的任务的不同之处在于，它们在执行时传递的参数（self对于使用@task装饰器声明为方法的任务）是对TaskSet实例的引用，而不是User实例。可以从TaskSet实例中通过访问User实例?TaskSet.user。TaskSet还包含一个便捷?client属性，该属性引用User实例上的client属性。
SequentialTask??Set类
SequentialTaskSet是TaskSet，但其任务将按照声明的顺序执行。SequentialTask??Set类上的任务的权重将被忽略。可以将SequentialTask??Sets嵌套在TaskSet中，反之亦然。
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
在上面的示例中，任务以声明的顺序执行：
1.	first_task
2.	function_task
3.	second_task
4.	third_task
然后它将重新开始first_task。
on_start和on_stop方法
用户和TaskSet类可以声明一个on_start方法和/或?on_stop方法。用户on_start在开始运行时将调用它的方法，而on_stop在停止运行时将调用它的?方法?。对于TaskSet，该?on_start方法在模拟用户开始执行该TaskSet?on_stop时被调用，并在模拟用户停止执行该TaskSet时interrupt()被调用（被调用时或杀死该用户时）。
test_start和test_stop事件
如果需要在负载测试的开始或结束时运行一些代码，则应使用?test_start和test_stop?事件。您可以在locustfile的模块级别为这些事件设置侦听器：
from locust import events

@events.test_start.add_listener
def on_test_start(**kwargs):
    print("A new test is starting")

@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print("A new test is ending")
在运行Locust分布式系统时，test_start和test_stop事件将仅在主节点中触发
发出HTTP请求
到目前为止，我们仅介绍了User的任务计划部分。为了实际负载测试系统，我们需要发出HTTP请求。为了帮助我们做到这一点，HttpLocust?该类存在。使用此类时，每个实例都会获得一个client属性，该?属性将是HttpSession可以用于发出HTTP请求的一个实例?。
Class HttpUser(*args,?**kwargs) 
表示要被孵化并攻击要进行负载测试的系统的HTTP“用户”。
该用户的行为由其任务定义。可以使用on方法直接在类上声明任务，也可以通过设置来声明任务。@task?decoratortasks?attribute
此类在实例化时创建一个客户端属性，该属性是一个HTTP客户端，支持在请求之间保持用户会话。
client= None
	在Locust实例化后创建的HttpSession实例。客户端支持cookie，因此保持HTTP请求之间的会话。
从HttpUser类继承时，我们可以使用其client属性对服务器发出HTTP请求。这是一个蝗虫文件的示例，可用于对具有两个URL的站点进行负载测试。/和/ about /：
from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(5, 15)

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def about(self):
        self.client.get("/about/")
使用上面的User类，每个模拟用户将在请求之间等待5到15秒，并且/将被请求的请求是/ about /的两倍。
使用HTTP客户端
HttpUser的每个实例HttpSession?在client属性中都有一个实例。在HttpSession类实际上是一个子类?requests.Session，可以用来做HTTP请求，将使用报告给用户的统计，get，?post，put，?delete，head，?patch和options?方法。HttpSession实例将在请求之间保留cookie，以便可用于登录网站并在请求之间保持会话。也可以从User实例的TaskSet实例中引用client属性，以便轻松地从您的任务中检索客户端并发出HTTP请求。
这是一个简单的示例，它向/ about路径发出GET请求（在这种情况下，我们假设self?是TaskSetor或HttpUser?class?的实例：
response = self.client.get("/about")
print("Response status code:", response.status_code)
print("Response content:", response.text)
这是发出POST请求的示例：
response = self.client.post("/login", {"username":"testuser", "password":"secret"})
安全模式
HTTP客户端配置为以safe_mode运行。这是因为由于连接错误，超时或类似原因而失败的任何请求都不会引发异常，而是返回一个空的虚拟Response对象。该请求将在用户统计信息中报告为失败。返回的虚拟Response的content属性将设置为None，其status_code将为0。
手动控制请求是成功还是失败
默认情况下，除非HTTP响应代码为OK（<400），否则请求将被标记为失败的请求。大多数情况下，此默认值是您想要的。但是，有时（例如，当测试您希望返回404的URL端点时，或者测试设计错误的系统，即使发生错误，该系统也可能返回200 OK），需要手动控制蝗虫是否应将请求视为成功或失败。失败。
通过使用catch_response参数和with语句，即使响应代码正确，也可以将请求标记为失败?：
with self.client.get("/", catch_response=True) as response:
    if response.content != b"Success":
        response.failure("Got wrong response")
就像可以将具有OK响应代码的请求标记为失败一样，也可以将catch_response?参数与with语句一起使用，以使导致HTTP错误代码的请求在统计信息中仍被报告为成功：
with self.client.get("/does_not_exist/", catch_response=True) as response:
    if response.status_code == 404:
        response.success()
使用动态参数将对请求的分组
网站上的URL包含某种动态参数的页面是很常见的。通常，在用户的统计信息中将这些URL分组在一起是很有意义的。这可以通过将name参数传递给HttpSession's?不同的请求方法来完成。
例：
# Statistics for these requests will be grouped under: /blog/?id=[id]
for i in range(10):
    self.client.get("/blog?id=%i" % i, name="/blog?id=[id]")

如何构建测试代码
重要的是要记住，locustfile.py只是由Locust导入的普通Python模块。从该模块中，您可以像在任何Python程序中一样正常地导入其他python代码。当前的工作目录会自动添加到python的目录中sys.path，因此可以使用python?import语句导入工作目录中的所有python文件/模块/软件包。
对于小型测试，将所有测试代码保存在一个中locustfile.py应该可以正常工作，但是对于大型测试套件，您可能需要将代码拆分为多个文件和目录。
当然，构建测试源代码的方式完全取决于您，但是我们建议您遵循Python最佳实践。这是一个虚构的Locust项目的示例文件结构：
·	项目根目录
o	common/
§	__init__.py
§	auth.py
§	config.py
o	locustfile.py
o	requirements.txt?（外部Python依赖项通常保存在requirements.txt中）
具有多个不同locustfiles的项目也可以将它们保存在单独的子目录中：
·	项目根目录
o	common/
§	__init__.py
§	auth.py
§	config.py
o	locustfiles/
§	api.py
§	website.py
o	requirements.txt
使用上述任何项目结构，您的locustfile都可以使用以下方法导入公共库：
import common.auth

在没有Web UI的情况下运行locust
您可以在没有Web UI的情况下运行locust-例如，如果您希望以某种自动化流程（例如CI服务器）运行locust，请将该--headless标志与-u和一起使用-r：
$ locust -f locust_files/my_locust_file.py --headless -u 1000 -r 100
-u指定要产生的用户数，并-r指定填充率（每秒要产生的用户数）。
设置测试时间限制
如果要指定测试的运行时间，可以使用--run-time或进行操作-t：
$ locust -f --headless -u 1000 -r 100 --run-time 1h30m

允许任务在关闭时完成迭代
默认情况下，locust将立即停止您的任务。如果您想让任务完成迭代，则可以使用。--stop-timeout?<seconds>
$ locust -f --headless -u 1000 -r 100 --run-time 1h30m --stop-timeout 99

在没有Web UI的情况下运行Locust分布式
如果要在没有Web UI的情况下运行Locust分布式，则应--expect-workers在启动主节点时指定该选项，以指定预期要连接的辅助节点的数量。然后它将等待直到许多工作节点已连接，然后才能开始测试。
控制locust进程的退出代码
在CI环境中运行Locust时，您可能希望控制Locust进程的退出代码。您可以通过设置实例的来在测试脚本?process_exit_code中执行此操作?Environment。
下面的示例将在满足以下任一条件时将退出代码设置为非零：
·	超过1％的请求失败
·	平均响应时间超过200毫秒
·	响应时间的第95个百分位数大于800毫秒
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
（此代码可以放入locustfile.py或locustfile中导入的任何其他文件中）
添加网络路由
Locust使用Flask来提供Web UI，因此很容易将Web端点添加到Web UI。通过监听init事件，我们可以检索对Flask应用程序实例的引用，并使用该引用来设置新的路由：
from locust import events

@events.init.add_listener
def on_locust_init(web_ui, **kw):
    @web_ui.app.route("/added_page")
    def my_added_page():
        return "Another page"
现在，您应该能够启动蝗虫并浏览到http://127.0.0.1:8089/added_pa??ge
下一个??以前



FAQ
locust启动后打不开WebUI监控页面
解决方案
增加–web-host参数
locust -f load_test.py --web-host="127.0.0.1"


