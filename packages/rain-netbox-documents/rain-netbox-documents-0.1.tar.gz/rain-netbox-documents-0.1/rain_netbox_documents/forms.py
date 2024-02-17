from dcim.models import Site
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from .models import SiteDocument

class SiteDocumentForm(NetBoxModelForm):
    site = DynamicModelChoiceField(
        queryset=Site.objects.all()
    )
    comments = CommentField()
    class Meta:
        model = SiteDocument
        fields = ('name', 'document', 'external_url', 'document_type', 'site', 'comments', 'tags')
