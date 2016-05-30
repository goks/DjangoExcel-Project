from django.conf.urls import url

from Excelinp import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^download/(.*)', views.download, name="download"),
    url(r'^download_attachment/(.*)/(.*)', views.download_as_attachment,
        name="download_attachment"),
    url(r'^exchange/(.*)', views.exchange, name="exchange"),
    url(r'^parse/(.*)', views.parse, name="parse"),
    url(r'^import/', views.import_data, name="import"),
    url(r'^import_sheet/', views.import_sheet, name="import_sheet"),
    url(r'^export/(.*)', views.export_data, name="export"),
    url(r'^home/',  views.upload, name='uplink'),
    url(r'^products/(?P<pk>\w+)/$', views.itemDescription, name='itemDescription'),
    url(r'^search/', views.search,name='search'),
]