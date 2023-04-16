from django.shortcuts import render
from django.http import HttpResponse
from snippets.models import Snippet

def top(request):
  snippets = Snippet.objects.all()

  return render(request, "snippets/top.html", {"snippets": snippets})

def snippet_new(request):
  return HttpResponse("スニペットの登録")

def snippet_edit(request, snippet_id):
  return HttpResponse("スニペットの編集")

def snippet_detail(request, snippet_id):
  return HttpResponse("スニペットの詳細閲覧")
