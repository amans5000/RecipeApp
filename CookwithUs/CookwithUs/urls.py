from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', loginPage, name='loginPage'),
    path('logout/', logoutPage, name='logoutPage'),
    path('register/', registerPage, name='registerPage'),
    path('addrecipe/', addRecipe, name='addRecipe'),
    path('delete_recipe/<id>/', deleteRecipe, name='delete_recipe'),
    path('update_recipe/<int:id>/', updateRecipe, name='update_recipe'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns() 
