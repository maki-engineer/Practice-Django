from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from snippets.models import Snippet
from snippets.forms import SnippetForm
from rest_framework import viewsets, filters
from .serializer import SnippetSerializer

def top(request):
  snippets = Snippet.objects.all()

  return render(request, "snippets/top.html", {"snippets": snippets})

@login_required
def snippet_new(request):
  if request.method == 'POST':
    form = SnippetForm(request.POST)
    if form.is_valid():
      snippet            = form.save(commit=False)
      snippet.created_by = request.user
      snippet.save()
      return redirect(snippet_detail, snippet_id=snippet.pk)
  else:
    form = SnippetForm()
    return render(request, "snippets/snippet_new.html", {"form": form})

@login_required
def snippet_edit(request, snippet_id):
  snippet = get_object_or_404(Snippet, pk=snippet_id)
  if snippet.created_by_id != request.user.id:
    return HttpResponseForbidden("このスニペットの編集は許可されていません！")

  if request.method == 'POST':
    form = SnippetForm(request.POST, instance=snippet)
    if form.is_valid():
      form.save()
      return redirect('snippet_detail', snippet_id=snippet_id)
  else:
    form = SnippetForm(instance=snippet)
    return render(request, "snippets/snippet_edit.html", {"form": form})

def snippet_detail(request, snippet_id):
  snippet = get_object_or_404(Snippet, pk=snippet_id)

  return render(request, "snippets/snippet_detail.html", {"snippet": snippet})

class SnippetViewSet(viewsets.ModelViewSet):
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
