from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name = "signup"),
    path('signin', views.signin, name = "signin"),
	path('logout/', views.logout, name="logout"),
 
    path("",views.home,name = "home"),
    path("aboutus",views.aboutus,name = "aboutus"),
    path("base",views.base,name = "base"),
    path("contactus",views.contactus,name = "contactus"),
    path("contactpost/",views.contactpost,name = "contactpost"),
    path("contactlist/",views.contactlist,name = "contactlist"),
    path("viewcontact/<int:id>/",views.viewcontact,name = "viewcontact"),
    path('deletecontact/<int:id>/', views.deletecontact, name = "deletecontact"),
    path("dashboard/",views.dashboard,name = "dashboard"),
    path("services/",views.services,name = "services"),
    
    
    path("house/",views.house,name = "house"),
    path("houseoneroom/",views.houseoneroom,name = "houseoneroom"),
    path("housetworoom/",views.housetworoom,name = "housetworoom"),
    
    path("faq/",views.faq,name = "faq"),
    path("pricing/",views.pricing,name = "pricing"),
    path("privancy/",views.privancy,name = "privancy"),
    
    path("roompost/",views.roompost,name = "roompost"),
    path("mypayment/",views.mypayment,name = "mypayment"),
    path("allpayment/",views.allpayment,name = "allpayment"),
    
    path("manual_control/",views.manual_control,name = "manual_control"),
    path("mytesting/",views.mytesting,name = "mytesting"),

    
    
    path('viewroom/<str:pk>/', views.viewroom.as_view(), name = "viewroom"),
    path('payment/<int:product_id>/', views.PaymentView.as_view(), name='payment'),  # Update this line
    path('pesapal/transaction/completed/', views.payment_completed, name='payment_completed'),
    
    
    #mqtt
    path('<device_id>/<command>/', views.control_esp8266, name='control_esp8266'),

]