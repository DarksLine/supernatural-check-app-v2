from django.shortcuts import render, redirect
from random import randint
from django.views.generic import View


# Класс страницы приветствия и инициализации сессии
class IndexView(View):

    def get(self, request):
        request.session["success"] = { 'num1': 0, 'num2': 0, 'num3': 0 }
        request.session["iter"] = 1
        request.session["proc_succ"] = { 'num1': 0, 'num2': 0, 'num3': 0 }
        request.session["guess"] = []
        return render(request, 'index.html')


# Класс страницы начала и повтора тестирования, а также генерации "предсказаний"
class InitialView(View):

    def get(self, request):
        res = {'num1': None,'num2': None,'num3': None}
        for element in res:
            res[element] = randint(10,99)

        request.session["res"] = res
        return render(request, 'initial.html')


# Класс-миксин для подсчета процента достоверности предсказаний
class ProcentMixin:

    @classmethod
    def procent(cls, request, predict, mind):
        success = request.session["success"]
        for element in predict:
            if predict.get(element) == mind:
                success[element] = success[element] + 1
        
        procent = { 'num1': 0, 'num2': 0, 'num3': 0 }
        for element in procent:
            procent[element] =  int((success.get(element) / request.session["iter"]) * 100)
        request.session["success"] = success
        return procent


# Класс страницы тестирования с методом пост
class TestingView(ProcentMixin, View):

    def get(self, request):
        return render(request, 'testing.html', request.session["res"])

    def post(self,request):
        request.session["number_in_head"] = int(request.POST['answer'])
        request.session["proc_succ"] = ProcentMixin.procent(request, request.session["res"], request.session["number_in_head"])
        request.session["iter"] += 1
        return redirect('/result')


# Класс страницы результата
class ResultView(View):
    
    def get(self, request):
        predict = request.session["res"]
        predict['answer'] = request.session["number_in_head"]

        guess = request.session["guess"]
        guess.insert(0, predict)

        request.session["guess"] = guess
        proc_succ = request.session["proc_succ"]
        return render(request, 'result.html', {'dict_res': guess, 'procent_success': proc_succ})