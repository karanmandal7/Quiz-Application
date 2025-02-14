
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from .models import *
import random
from django.shortcuts import render,redirect
# Create your views here.

def home(request):
    context={'categories': Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/quiz/?category={request.GET.get('category')}")
    return render(request,'home.html',context)
def quiz(request):
    context={'category':request.GET.get('category')}
    return render(request,'quiz.html',context)
def get_quiz(request):
    try:
        question_objs=Question.objects.all()
        if request.GET.get('category'):
            question_objs=question_objs.filter(category__category_name__icontains=request.GET.get('category'))
        question_objs=list(question_objs)  
        data=[]
        random.shuffle(question_objs)
        for question_obj in question_objs:
           
            data.append({
                "uid": question_obj.uid,
                "category": question_obj.category.category_name,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answers": question_obj.get_answers()
            })
        payload={'status': True,'data':data}
        return JsonResponse(payload)
    except Exception as e:
        print(e)
    return HttpResponse("OOPS!! Something went wrong")


def result(request):
    # correct_answers = 0
    # responses = Response.objects.filter(user=request.user)
    # for response in responses:
    #     if response.answer == response.question.correct_answer:
    #         correct_answers += 1
    return render(request, 'result.html')