from django.shortcuts import render
import logging
# Create your views here.
def NutriliteSearchPage(request,selectTag):
    return render(request, 'nutritionSearchPage.html', {
        'data': "Hello Django ",
    })
