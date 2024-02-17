from netbox.views.generic import ObjectChangeLogView
from django.urls import path
from . import models, views

urlpatterns = (
    path('site-documents/', views.SiteDocumentListView.as_view(), name='sitedocument_list'),
    path('site-documents/add/', views.SiteDocumentEditView.as_view(), name='sitedocument_add'),
    path('site-documents/<int:pk>/', views.SiteDocumentView.as_view(), name='sitedocument'),
    path('site-documents/<int:pk>/edit/', views.SiteDocumentEditView.as_view(), name='sitedocument_edit'),
    path('site-documents/<int:pk>/delete/', views.SiteDocumentDeleteView.as_view(), name='sitedocument_delete'),

    path('site-documents/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='sitedocument_changelog', kwargs={
        'model': models.SiteDocument
    }),
)