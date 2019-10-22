from django.shortcuts import render

# Create your views here.
import time, datetime

def show_time(request):

    t = datetime.datetime.now()
    # 这里的参数可以是其他的类型吗 list 对象
    return render(request, 'showtime.html', {"time": t})


class Animal():
    def __init__(self, name, age):
        self.name = name
        self.age =age



def query(request):

    # 这个先传个list到template
    list = ['村长', '书记', '老板']
    d = {'name': 'tom', "age": 12, "hobby": "蓝球"}
    animal = Animal('dog1', 13)
    test = "hell o wor ld !"

    t = datetime.datetime.now()
    a = "<a href="">click</a>"
    return render(request, 'index.html', locals())