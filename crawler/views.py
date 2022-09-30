from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Count, Aggregate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView


from .forms import SiteConfCreateForm, ConfigValuesCreateForm
from .invoke_backend import InvokeBackend
from .models import SiteConf, ConfigValues, Job, Task


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteConfCreateView(CreateView):
    model = SiteConf
    form_class = SiteConfCreateForm
    template_name = 'crawler/siteconf/create.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteConfDetailView(DetailView):
    model = SiteConf
    context_object_name = 'site_conf'
    template_name = 'crawler/siteconf/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteConfListView(ListView):
    model = SiteConf
    template_name = 'crawler/siteconf/list.html'
    context_object_name = 'site_confs'
    paginate_by = 25
    queryset = SiteConf.objects.all().order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # jobs_dict = dict()
        # for sc in context["site_confs"]:
        #     jobs_dict[sc.pk] = sc.jobs.all().order_by('-created_at')[:5]
        # print(jobs_dict)
        #print(Job.objects.values('site_conf').filter(site_conf__in=context["site_confs"]).group_by('site_conf'))


        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteConfEditView(UpdateView):
    model = SiteConf
    form_class = SiteConfCreateForm
    template_name = 'crawler/siteconf/edit.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class JobListView(ListView):
    model = Job
    template_name = 'crawler/job/list.html'
    context_object_name = 'jobs'
    paginate_by = 100
    queryset = Job.objects.all().order_by('-created_at')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TaskListView(ListView):
    model = Task
    template_name = 'crawler/task/list.html'
    context_object_name = 'tasks'
    paginate_by = 25
    queryset = Task.objects.all().order_by('-created_at')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigValuesCreateView(CreateView):
    model = ConfigValues
    form_class = ConfigValuesCreateForm
    template_name = 'crawler/config_values/create.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigValuesDetailView(DetailView):
    model = ConfigValues
    context_object_name = "config_value"
    template_name = 'crawler/config_values/detail.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigValuesListView(ListView):
    model = ConfigValues
    template_name = 'crawler/config_values/list.html'
    context_object_name = 'config_values'
    paginate_by = 100
    queryset = ConfigValues.objects.all().order_by('-created_at')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ConfigValuesEditView(UpdateView):
    model = ConfigValues
    form_class = ConfigValuesCreateForm
    template_name = 'crawler/config_values/edit.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class JobDetailView(DetailView):
    model = Job
    context_object_name = 'job'
    template_name = 'crawler/job/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# @login_required(login_url='/login/')
def scrape(request, pk):
    site_conf: SiteConf = get_object_or_404(SiteConf, pk=pk)

    if not site_conf.enabled:
        return JsonResponse({'status': 'ERROR', 'message': 'SiteConf crawling is disabled'})

    if site_conf.is_locked:
        return JsonResponse({'status': 'ERROR', 'message': 'SiteConf already in sync, can\'t place parallel requests'})

    ib = InvokeBackend(site_conf)

    flag = request.GET.get("redirect_to_job")
    if flag and flag.lower() == 'yes':
        return redirect(f'/job/{ib.job.id}')

    return JsonResponse({"status": "OK", "message": f"Crawling Started, job_id: {ib.job.id}"})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class Home(ListView):
    model = Job
    template_name = 'crawler/home.html'
    context_object_name = 'jobs'
    paginate_by = 100
    queryset = Job.objects.all().order_by('-created_at')