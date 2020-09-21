from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

admin.site.site_header = "TRAVMAKS ADMIN PANEL - A MAKS CUB3 PRODUCT"
admin.site.index_title = "TRAVMAKS - We make your travel easy!"

urlpatterns = [
    path('admin',admin.site.urls),
    path('',include('homeApp.urls'),name='homeapp'),
    path('accounts/',include('accounts.urls'),name='accounts'),
    path('qna/',include('qna.urls'),name='qnaPage'),
    path('travelagency/',include('travelagency.urls'),name='travelagency'),
    path('tour/',include('touring.urls'),name='tourFlow'),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
