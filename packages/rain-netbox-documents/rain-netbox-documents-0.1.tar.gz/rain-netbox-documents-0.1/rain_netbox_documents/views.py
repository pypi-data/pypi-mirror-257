from netbox.views import generic
from . import forms, models, tables

class SiteDocumentView(generic.ObjectView):
    queryset = models.SiteDocument.objects.all()

class SiteDocumentListView(generic.ObjectListView):
    queryset = models.SiteDocument.objects.all()
    table = tables.SiteDocumentTable

class SiteDocumentEditView(generic.ObjectEditView):
    queryset = models.SiteDocument.objects.all()
    form = forms.SiteDocumentForm

class SiteDocumentDeleteView(generic.ObjectDeleteView):
    queryset = models.SiteDocument.objects.all()