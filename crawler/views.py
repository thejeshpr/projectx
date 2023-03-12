import json
import uuid

from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Count, Aggregate
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView, DeleteView

from .forms import SiteConfCreateForm, ConfigValuesCreateForm, SiteConfFormByJSON, BulkCreateForm
from .invoke_backend import InvokeBackend
from .models import SiteConf, ConfigValues, Job, Task, Category


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
        json_data = dict(
            name=context['site_conf'].name,
            base_url=context['site_conf'].base_url,
            enabled=context['site_conf'].enabled,
            is_locked=context['site_conf'].is_locked,
            icon=context['site_conf'].icon,
            scraper_name=context['site_conf'].scraper_name
        )

        if context["site_conf"].extra_data_json and context["site_conf"].extra_data_json != "{}":
            json_data["extra_data_json"] = context["site_conf"].extra_data_json.replace('"', '\"')
        else:
            json_data["extra_data_json"] = "{}"

        context["json_data"] = json.dumps(json_data, indent=4)
        return context


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteConfListView(ListView):
    model = SiteConf
    template_name = 'crawler/siteconf/list_v2.html'
    context_object_name = 'site_confs'
    paginate_by = 50
    queryset = SiteConf.objects.all().order_by('-created_at')

    # CODE for fetching last job status of each site conf
    # from django.db.models import Max, Subquery, OuterRef
    #
    # siteconfs_with_last_job_status = SiteConf.objects.annotate(
    #     last_job_status=Subquery(
    #         Job.objects.filter(
    #             site_conf_id=OuterRef('pk')
    #         ).order_by('-created_at').values('status')[:1]
    #     )
    # )
    # for siteconf in siteconfs_with_last_job_status:
    #     print(siteconf.name, siteconf.last_job_status)

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
class SiteConfDeleteView(DeleteView):
    model = SiteConf
    template_name = 'crawler/generic/delete.html'
    success_url = reverse_lazy("crawler:home")


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
    success_url = reverse_lazy('crawler:config-value-list')


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
class ConfigValuesDeleteView(DeleteView):
    model = ConfigValues
    success_url = reverse_lazy('crawler:config-value-list')
    template_name = 'crawler/generic/delete.html'


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


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SiteConfByJSONView(FormView):
    template_name = 'crawler/siteconf/create_by_json.html'
    form_class = SiteConfFormByJSON
    success_url = None

    def form_valid(self, form):
        # form.create_site_conf()
        json_data = json.loads(form.cleaned_data.get("json_data"))
        sc_obj = SiteConf.objects.create(
            name=json_data.get("name"),
            scraper_name=json_data.get("scraper_name"),
            icon=json_data.get("icon"),
            base_url=json_data.get("base_url"),
            extra_data_json=json_data.get("extra_data_json"),
            enabled=json_data.get("enabled"),
            is_locked=json_data.get("is_locked")
        )
        self.success_url = reverse_lazy('crawler:siteconf-detail', kwargs=dict(pk=sc_obj.pk))
        return super().form_valid(form)


def duplicate_site_conf(request, pk):
    # sc: SiteConf = get_object_or_404(SiteConf, pk=pk)
    original_obj = get_object_or_404(SiteConf, pk=pk)
    obj_dict = model_to_dict(original_obj)
    # obj_dict.category = original_obj.category
    obj_dict.pop('id')  # remove the ID field to avoid duplication
    obj_dict.pop('category')
    new_obj = SiteConf(**obj_dict, category=original_obj.category)

    new_uuid = uuid.uuid4()

    # Get the last 4 characters of the UUID's hex string
    short_uuid = new_uuid.hex[-4:]

    new_obj.name = f"{new_obj.name} - Copy({short_uuid})"
    new_obj.save()
    return redirect(reverse_lazy('crawler:siteconf-edit', kwargs=dict(pk=new_obj.pk)))


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class JobsListViewBySiteConf(ListView):
    model = Job
    context_object_name = 'jobs'
    paginate_by = 20
    template_name = 'crawler/job/list_by_siteconf.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['site_conf'] = SiteConf.objects.get(pk=self.kwargs.get('siteconf_pk'))
        return context

    def get_queryset(self):
        return Job.objects.filter(site_conf__pk=self.kwargs.get('siteconf_pk')).order_by('-created_at', '-pk')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TaskListViewBySiteConf(ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 25
    # template_name = 'crawler/task/list_by_siteconf.html'
    template_name = 'crawler/task/list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['site_conf'] = SiteConf.objects.get(pk=self.kwargs.get('siteconf_pk'))
        context['extra_info'] = context['site_conf']
        return context

    def get_queryset(self):
        return Task.objects.filter(site_conf__pk=self.kwargs.get('siteconf_pk')).order_by('-created_at', '-pk')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class BookmarkTaskListViewBySiteConf(ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 25
    # template_name = 'crawler/task/list_by_siteconf.html'
    template_name = 'crawler/task/list.html'

    def get_queryset(self):
        return Task.objects.filter(is_bookmarked=True).order_by('-created_at', '-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the category object to the context
        context['extra_info'] = 'Bookmarks'
        return context


@login_required(login_url='/login/')
def toggle_bookmark(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_bookmarked = not task.is_bookmarked
    task.save()
    action = "marked" if task.is_bookmarked else "unmarked"
    return JsonResponse({"status": "ok", "action": action})

    # task = Task.objects.filter(pk=pk).first()
    # if task:
    #     task.is_bookmarked = not task.is_bookmarked
    #     task.save()
    #     action = "marked" if task.is_bookmarked else "unmarked"
    #     return JsonResponse({"status": "ok", "action": action})
    # else:
    #     return JsonResponse({"status": "error", "desc": "task not found"})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'crawler/category/create.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryEditView(UpdateView):
    model = Category
    fields = ['name']
    context_object_name = "category"
    template_name = 'crawler/category/edit.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'crawler/category/list.html'
    context_object_name = 'categories'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('crawler:category-list')
    template_name = 'crawler/generic/delete.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'crawler/category/detail.html'
    context_object_name = 'category'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TasksByCategory(ListView):
    model = Task
    context_object_name = 'tasks'
    paginate_by = 25
    template_name = 'crawler/task/list.html'

    def get_queryset(self):
        # Get the category pk from the url
        category_pk = self.kwargs.get('pk')

        # Get the category object
        category = Category.objects.get(pk=category_pk)

        # Get all tasks linked to siteConf objects that are linked to the category
        tasks = Task.objects.filter(site_conf__category=category).order_by('-created_at')
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the category object to the context
        context['extra_info'] = Category.objects.get(pk=self.kwargs.get('pk'))
        return context


@login_required(login_url='/login/')
def data_dump(request):
    categories = list(Category.objects.values('name'))
    config_values = list(ConfigValues.objects.values('key', 'val'))

    site_confs = list(SiteConf.objects.values(
        'name',
        'scraper_name',
        'icon',
        'base_url',
        'extra_data_json',
        'enabled',
        'category__name'
    ))
    # site_confs = SiteConf.objects.all()
    # site_confs_data = list()
    # for site_conf in site_confs:
    #     dict_data = model_to_dict(site_conf)
    #     if dict_data['category']:
    #         dict_data['category'] = Category.objects.get(pk=dict_data['category']).name
    #     site_confs_data.append(dict_data)
    return JsonResponse({
        "categories": categories,
        "config_values": config_values,
        "site_confs": site_confs
    })


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DataBulkCreate(FormView):
    template_name = 'crawler/generic/data_bulk_create.html'
    form_class = BulkCreateForm
    success_url = reverse_lazy('crawler:siteconf-list')

    def form_valid(self, form):
        data = json.loads(form.cleaned_data.get("data"))
        objs = list()

        # create categories
        for entry in data['categories']:
            print("createing: ", entry.get('name') + " TEST")
            Category.objects.get_or_create(name=entry.get('name') + " TEST")

        # create config-values
        for entry in data['config_values']:
            print("createing: ", entry.get('key') + " TEST")
            ConfigValues.objects.get_or_create(
                key=entry.get('key') + " TEST",
                val=entry.get('val'),
            )

        # create site_confs
        for entry in data['site_confs']:
            print("createing: ", entry.get('name') + " TEST")
            if entry.get('category'):
                cat = Category.objects.get(name=entry.get('category'))
            else:
                cat = None

            objs.append(SiteConf(
                name=entry.get("name") + "TEST",
                scraper_name=entry.get("scraper_name"),
                icon=entry.get("icon"),
                base_url=entry.get("base_url"),
                extra_data_json=entry.get("extra_data_json"),
                enabled=entry.get("enabled"),
                is_locked=False,
                category=cat
            ))
        SiteConf.objects.bulk_create(objs)
        return super().form_valid(form)
