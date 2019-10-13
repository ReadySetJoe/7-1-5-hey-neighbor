from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Tools


def is_superuser_check(user):
    return user.is_superuser


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'tools/index.html'

    def get_queryset(self):
        if 'selection' in self.kwargs:
            return Tools.objects.filter(available=self.kwargs['selection'].upper())
        return Tools.objects.all()


class CreateView(UserPassesTestMixin, generic.CreateView):
    model = Tools
    template_name = 'tools/create.html'
    fields = '__all__'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('tools:index')


@user_passes_test(is_superuser_check)
def delete_view(request, pk):
    tool = get_object_or_404(Tools, pk=pk)
    tool.delete()
    return HttpResponseRedirect(reverse_lazy('tools:index'))


def increment_watchers(request, pk):
    tool = get_object_or_404(Tools, pk=pk)
    tool.watchers += 1
    tool.save()
    return HttpResponseRedirect(reverse('tools:index'))
