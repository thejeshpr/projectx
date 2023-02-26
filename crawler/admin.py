from django.contrib import admin

from .models import SiteConf, Job, Task, ExtraTaskData, ConfigValues, Category


@admin.register(SiteConf)
class SiteConfAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'base_url',
        'created_at',
        'enabled',
        'extra_data_json',
        'icon',
        'is_locked',
        'name',
        'scraper_name',
        'updated_at',
    )
    list_filter = ('created_at', 'enabled', 'is_locked', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'error', 'site_conf', 'status')
    list_filter = ('created_at', 'site_conf')
    date_hierarchy = 'created_at'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'data',
        'is_bookmarked',
        'job',
        'name',
        'site_conf',
        'unique_key',
        'updated_at',
        'url',
    )
    list_filter = ('created_at', 'is_bookmarked', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(ExtraTaskData)
class ExtraTaskDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'task', 'data', 'updated_at')
    list_filter = ('created_at', 'task', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(ConfigValues)
class ConfigValuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'key', 'val', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)