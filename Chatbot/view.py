from django.shortcuts import render, HttpResponse

def paginaInicial(request):
    return render(request, "index.hmtl")