from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/notes/', include('notes.urls')),
    path('api/backend/',include('backend.urls')),
    path('api/listings/', include('listings.urls')),
    path('api/', include('users.urls')),
    path('api/bookmarks/', include('bookmarks.urls'))


]
