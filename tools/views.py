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
        if 'user' in self.kwargs:
            if 'selection' in self.kwargs:
                return Tools.objects.filter(available=self.kwargs['selection'].upper(), watcher__gte=1)

        if 'selection' in self.kwargs:
            ndx = self.kwargs['selection']
            if ndx == 'days' or ndx == 'hours' or ndx == 'weeks':
                return Tools.objects.filter(available=self.kwargs['selection'].upper())
            if ndx == 'powered':
                return Tools.objects.filter(powered=True)
            if ndx == 'unpowered':
                return Tools.objects.filter(powered=False)
            if ndx == 'recent':
                return Tools.objects.all().order_by('-id')[:3]
            if ndx == 'popular':
                return Tools.objects.filter(watchers__gte=1)
        return Tools.objects.all()


class CreateView(UserPassesTestMixin, generic.CreateView):
    model = Tools
    template_name = 'tools/tools_new.html'
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
