from django.urls import path, re_path

from . import views

app_name = 'crawler'

urlpatterns = [
    path('', views.SiteConfListView.as_view(), name='home'),
    path('siteconf/', views.SiteConfListView.as_view(), name='siteconf-list'),
    path('siteconf/new', views.SiteConfCreateView.as_view(), name='siteconf-create'),
    path('siteconf/<pk>', views.SiteConfDetailView.as_view(), name='siteconf-detail'),

    path('config-value/new', views.ConfigValuesCreateView.as_view(), name='config-value-create'),
    path('config-value/<pk>', views.ConfigValuesDetailView.as_view(), name='config-value-detail'),

    path('job/', views.JobListView.as_view(), name='job-list'),
    path('job/<pk>', views.JobDetailView.as_view(), name='job-detail'),

    path('task/', views.TaskListView.as_view(), name='task-list'),

    path('scrape/<pk>', views.scrape, name='scrape'),
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