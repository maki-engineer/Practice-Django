from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import resolve
from snippets.models import Snippet
from snippets.views import top, snippet_new, snippet_edit, snippet_detail

UserModel = get_user_model()

class TopPageTest(TestCase):
  def test_top_page_returns_200_and_expected_title(self):
    response = self.client.get("/")
    self.assertContains(response, "Djangoスニペット", status_code=200)

  def test_top_page_uses_expected_template(self):
    response = self.client.get("/")
    self.assertTemplateUsed(response, "snippets/top.html")

class TopPageRenderSnippetsTest(TestCase):
  def setUp(self):
    self.user = UserModel.objects.create(
      username="test_user",
      email="test1@test.com",
      password="password"
    )
    self.snippet = Snippet.objects.create(
      title="title1",
      code="print('Hello, World.')",
      description="Hello, World.と出力するプログラムです。",
      created_by=self.user
    )

  def test_should_return_snippet_title(self):
    request      = RequestFactory().get("/")
    request.user = self.user
    response     = top(request)
    self.assertContains(response, self.snippet.title)

  def test_should_return_username(self):
    request      = RequestFactory().get("/")
    request.user = self.user
    response     = top(request)
    self.assertContains(response, self.user.username)

class CreateSnippetTest(TestCase):
  def setUp(self):
    self.user = UserModel.objects.create(
      username="test_user",
      email="test1@test.com",
      password="password"
    )
    self.client.force_login(self.user)

  def test_render_creation_form(self):
    response = self.client.get("/snippets/new/")
    self.assertContains(response, "スニペットの登録", status_code=200)

  def test_create_snippet(self):
    data = {'title': 'タイトル', 'code': 'コード', 'description': '解説'}
    self.client.post("/snippets/new/", data)

    snippet = Snippet.objects.get(title='タイトル')

    self.assertEqual('コード', snippet.code)
    self.assertEqual('解説', snippet.description)

class SnippetDetailTest(TestCase):
  def setUp(self):
    self.user = UserModel.objects.create(
      username="test_user",
      email="test1@test.com",
      password="password"
    )
    self.snippet = Snippet.objects.create(
      title="title1",
      code="print('Hello, World.')",
      description="Hello, World.と出力するプログラムです。",
      created_by=self.user
    )

  def test_should_use_expected_template(self):
    response = self.client.get("/snippets/%s/" % self.snippet.id)
    self.assertTemplateUsed(response, "snippets/snippet_detail.html")

  def test_top_page_returns_200_and_expected_heading(self):
    response = self.client.get("/snippets/%s/" % self.snippet.id)
    self.assertContains(response, self.snippet.title, status_code=200)

class EditSnippetTest(TestCase):
  def test_should_resolve_snippet_edit(self):
    found = resolve("/snippets/1/edit/")
    self.assertEqual(snippet_edit, found.func)
