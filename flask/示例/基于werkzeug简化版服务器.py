from werkzeug.wrappers import Response, Request
from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule


class Jlask(object):
    # 初始化url_map和存储endpoint对应视图函数
    # 这里是一个小坑，不能再__init__中初始化，这样会使得在类被调用的时候，执行了初始化的代码，导致原先创建的路由都丢失
    url_map = Map([])
    endpoint_dict = {}

    def dispatch_request(self, request):
        # 获取请求的路由
        url = request.path
        urls = self.url_map.bind('127.0.0.1:5000')
        # 匹配得到endpoint
        endpoint = urls.match(path_info=url)[0]
        # 获取到视图函数处理得结果
        view_func = self.endpoint_dict[endpoint]
        result = view_func(request)
        return Response(result)

    def wsgi_app(self, environ, start_response):
        # 启动
        # 实例化request，存入environ，这里的request就是werkzeug中对于environ的处理，可以通过request来获取各种请求信息
        request = Request(environ)
        print(request.args)
        # 调用dispatch_request解析url，得到对应的视图函数处理的结果
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        # 调用到wsgi_app，来执行url对应视图函数
        return self.wsgi_app(environ, start_response)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        # 获取请求方法
        methods = options.pop('methods', None)
        # 如果没有定义endpoint，就用试图函数的名字
        if endpoint is None:
            endpoint = view_func.__name__
            # 生成rule
            # rule： 定义的路由
            self.url_map.add(Rule(rule, endpoint=endpoint, methods=methods))
            # 存储endpoint对应的视图函数
            self.endpoint_dict[endpoint] = view_func
            # print(self.endpoint_dict)
            # print(self.url_map)


app = Jlask()


def Hello(request):
    return "Hello World"


app.add_url_rule(rule='/', view_func=Hello, methods=['GET'])

if __name__ == '__main__':
    run_simple('127.0.0.1', 5000, app)

