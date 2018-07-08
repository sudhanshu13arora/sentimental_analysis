from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


from .views import view_reviews,submit_review, signup, user_login, user_logout, view_self_comments, login_success, analysis, profile_view

urlpatterns = [
    url(r'^view/$',view_reviews, name="view_reviews"),
    url(r'^give/$',submit_review, name="submit_review"),
    url(r'^signup/$',signup, name='signup'),
    url(r'^login/$',user_login, name='login'),
    url(r'^logout/$',user_logout, name='logout'),
    url(r'^self/(?P<username>\w+)/$',view_self_comments, name='self'),
    url(r'login_success/$', login_success, name='login_success'),
    url(r'analysis/$', analysis, name='analysis'),
    url(r'^profile_view/(?P<username>\w+)/$',profile_view, name='profile_view')
]