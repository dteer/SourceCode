from werkzeug.routing import Rule, Map

# 路由绑定
url_map = Map([
    Rule('/', endpoint='index', methods=['GET']),
    Rule('/about', endpoint='about', methods=['GET']),
])
# 添加路由
url_map.add(Rule('/hello', endpoint='hello', methods=['GET']))
# 实例化url对象
urls = url_map.bind('127.0.0.1:5000')
# 路由匹配
endpoint = urls.match(path_info="/")
print("1.", url_map)
print("2.", endpoint)