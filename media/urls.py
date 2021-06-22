from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('',views.login),
    path('admin',admin.site.urls),
    path('login_check',views.login_check),
    path('queue',views.queue),
    path('dataview/<id>/',views.dataview),

    #============== Tssks =======
    path('vaidate_file',views.vaidate_file),
    path('processinput',views.processinput),
    path('entertaskdetailstodb',views.entertaskdetailstodb),
    path('loadtaskdata',views.loadtaskdata),
    path('ocrconverionengine',views.ocrconverionengine),

    #============== dataview ===========
    path('retivedatafromdb',views.retivedatafromdb),
    path('comparevalue',views.comparevalue),
    path('updatexlxs',views.updatexlxs),
    path('insertvaluetoexcel',views.insertvaluetoexcel),


    #test
    path('testingocrfunction',views.testingocrfunction),

    #============== User ============
    path('user_process_new_task',views.user_process_new_task),
    path('user_details',views.user_details),
    path('list_of_task',views.list_of_task),



    #============== Fuctionality ====
    path('Find_number_of_files',views.Find_number_of_files),


    #============== Testing ============
    path('ocrfunctionalitytest',views.ocrfunctionalitytest),


    #============= Training Model ==========
    path('TrainingEngine/<id>/',views.Training),
    path('LalbelData',views.LalbelData),
    
    path('PushLables',views.PushLables),
    path('FindListOfHeaders',views.FindListOfHeaders),
    path('FindSubList',views.FindSubList),
    path('PushValuesToCSV',views.PushValuesToCSV),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)