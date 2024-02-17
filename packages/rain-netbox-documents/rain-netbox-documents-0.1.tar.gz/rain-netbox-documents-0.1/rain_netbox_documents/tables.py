import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import SiteDocument

class SiteDocumentTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    document_type = ChoiceFieldColumn()
    site = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = SiteDocument
        fields = ('pk', 'id', 'name', 'external_url', 'document_type', 'site', 'comments', 'actions')
        default_columns = ('name', 'document_type', 'site')