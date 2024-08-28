from django.urls import path, re_path

from . import views

app_name = 'crawler'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('siteconf/', views.SiteConfListView.as_view(), name='siteconf-list'),
    path('siteconf/new', views.SiteConfCreateView.as_view(), name='siteconf-create'),
    path('siteconf/new/json', views.SiteConfByJSONView.as_view(), name='siteconf-create-json'),
    path('siteconf/<pk>', views.SiteConfDetailView.as_view(), name='siteconf-detail'),
    path('siteconf/<pk>/edit', views.SiteConfEditView.as_view(), name='siteconf-edit'),
    path('siteconf/<pk>/delete', views.SiteConfDeleteView.as_view(), name='siteconf-delete'),
    path('siteconf/<pk>/duplicate', views.duplicate_site_conf, name='siteconf-duplicate'),
    path('siteconf/<siteconf_pk>/jobs', views.JobsListViewBySiteConf.as_view(), name='siteconf-jobs'),
    path('siteconf/<siteconf_pk>/tasks', views.TaskListViewBySiteConf.as_view(), name='siteconf-tasks'),

    path('config-value/', views.ConfigValuesListView.as_view(), name='config-value-list'),
    path('config-value/new', views.ConfigValuesCreateView.as_view(), name='config-value-create'),
    path('config-value/<pk>', views.ConfigValuesDetailView.as_view(), name='config-value-detail'),
    path('config-value/<pk>/edit', views.ConfigValuesEditView.as_view(), name='config-value-edit'),
    path('config-value/<pk>/delete', views.ConfigValuesDeleteView.as_view(), name='config-value-delete'),

    path('job/', views.JobListView.as_view(), name='job-list'),
    path('job/<pk>', views.JobDetailView.as_view(), name='job-detail'),

    path('task/', views.TaskListView.as_view(), name='task-list'),
    path('task/<pk>/toggle-bookmark', views.toggle_bookmark, name='task-bookmark'),
    path('task/<pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('bookmarks', views.BookmarkTaskListViewBySiteConf.as_view(), name='bookmarks'),
    path('search', views.TaskSearchView.as_view(), name='task-search'),

    path('task/random', views.get_random_task, name='get-random-task'),

    path('scrape/<pk>', views.scrape, name='scrape'),

    path('category/new', views.CategoryCreateView.as_view(), name='category-create'),
    path('category/<pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('category/<pk>/edit/', views.CategoryEditView.as_view(), name='category-edit'),
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('category/<int:pk>/tasks/', views.TasksByCategory.as_view(), name='category-tasks'),

    path('data/dump/', views.data_dump, name='data-dump'),
    path('data/bulk-create/', views.DataBulkCreate.as_view(), name='data-bulk-create'),

    ### NF
    path('siteconf-ns/', views.SiteConfListView_NS.as_view(), name='siteconf-ns-list'),
    path('job-ns/', views.JobListView_NS.as_view(), name='job-ns-list'),
    path('task-ns/', views.TaskListView_NS.as_view(), name='task-ns-list'),
    path('stats/', views.jobs_by_date_and_status, name='stats'),

]

# urlpatterns = [
#     path('create-game/', views.CreateGame.as_view(), name='create-game'),
#     path('join-game/', views.JoinGame.as_view(), name='join-game'),
#     path('play-game/<str:uid>', views.play_game, name='play-game'),
#     path('get-board/<str:uid>', views.get_board, name='get-board'),
#     path('mark-cell/<str:uid>', views.MarkCell.as_view(), name='mark_cell'),
#     path('clean-up', views.clean_up, name='clean-up'),
#     path('thanks/', views.thanks, name='thanks'),
# ]