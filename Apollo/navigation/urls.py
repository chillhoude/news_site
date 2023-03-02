from django.urls import path,include
from . import views
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('tags/',filter_tag,name='tag'),
    path('news',news,name='news'),
    path('news/filter/',filter_date,name='filter'),
    path('public',Public.as_view(),name='public'),
    path('news/filter/<int:pk>',Show_post.as_view(),name='filter_post'),
    path('blog',BlogView.as_view(),name='blog'),
    path('interview',Interview.as_view(),name='interview'),
    path('<int:pk>/',Show_post.as_view(),name='show_post'),
    path('<int:pk>/like/', AddLike.as_view(), name='like'),
    path('<int:pk>/dislike/', AddDislike.as_view(), name='dislike'),
    path('<int:pk>/commentlike/', AddLikeComment.as_view(), name='likecomment'),
    path('create_post/',create_post,name='create_post'),
    path('userview/<int:pk>',UserDetailView.as_view(),name='user')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)