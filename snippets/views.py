from django.shortcuts import render, redirect, get_object_or_404
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
  snippet = get_object_or_404(Snippet, pk=snippet_id)

  return render(request, "snippets/snippet_detail.html", {"snippet": snippet})
