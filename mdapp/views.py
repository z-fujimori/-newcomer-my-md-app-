from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from mdapp.models import Mdfile
from django.urls import reverse, reverse_lazy
from .forms import CreateMdfileForm
from . import converter


def index(request):
    return render(request, 'mdapp/index.html')

class List(ListView):
    model = Mdfile
    template_name = "mdapp/index.html"

class Detail(DeleteView):
    model = Mdfile
    template_name = "mdapp/detail.html"

class CreateFile(CreateView):
    model = Mdfile
    form_class = CreateMdfileForm
    template_name = "mdapp/create.html"
    # success_url = reverse_lazy('mdapp:index')
    def form_valid(self, form):
        self.object = form.save(commit=False)  # 明示的にobjectを更新
        isinstance = form.instance
        isinstance.html_text = converter.markdown_to_html(isinstance.base_text)
        self.object.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('mdapp:ditail', kwargs={'pk': self.object.id})

class UpdateFile(UpdateView):
    model = Mdfile
    form_class = CreateMdfileForm
    template_name = "mdapp/create.html"
    success_url = reverse_lazy('mdapp:index')
    def form_valid(self, form):
        self.object = form.save()  # 明示的にobjectを更新
        isinstance = form.instance
        isinstance.html_text = converter.markdown_to_html(isinstance.base_text)
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('mdapp:ditail', kwargs={'pk': self.object.id})

