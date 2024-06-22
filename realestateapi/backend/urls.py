from django.urls import path,include
from . import views
from rest_framework import routers
#from users import views as userView
router = routers.DefaultRouter()
router.register(r'list',  views.ListingsView)
router.register(r'bookmarks',  views.BookMarksView)
router.register(r'inquiry',  views.InquiryView)
router.register(r'inquirymessage',  views.InquiryMessageView)
router.register(r'report',  views.ReportsView)
#router.register(r'user',  userView.UserView)
router.register(r'agent',  views.RealEstateAgentView)

urlpatterns =[
    path('', include(router.urls)),
]