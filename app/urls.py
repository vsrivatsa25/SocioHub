from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from main.views import IndexPageView, ChangeLanguageView, post_image, profile_picture, post_interest, SearchPage, Liked, Follow, FriendList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexPageView.as_view(), name='index'),
    path('post/', post_image, name='newpost'),
    path('liked/', Liked.as_view(), name='liked'),
    path('friends/', FriendList.as_view(), name='friends'),
    path('follow/<userid', Follow.as_view(), name='follow'),
    path('profilepicture/', profile_picture, name='profilepic'),
    path('interests/', post_interest, name='interests'),
    path('search/<s', SearchPage.as_view(), name='search'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('language/', ChangeLanguageView.as_view(), name='change_language'),

    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATICFILES_URL, document_root=settings.STATICFILES_DIR)
