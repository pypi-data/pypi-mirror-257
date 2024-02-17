from netbox.models import NetBoxModel
from django.db import models
from django.urls import reverse
from utilities.choices import ChoiceSet
from .utils import file_upload

class SiteDocTypeChoices(ChoiceSet):
    key = 'DocTypeChoices.site'

    CHOICES = [
        ('diagram', 'Network Diagram', 'green'),
        ('floorplan', 'Floor Plan', 'purple'),
        ('purchaseorder', 'Purchase Order', 'orange'),
        ('quote', 'Quote', 'indigo'),
        ('wirelessmodel', 'Wireless Model (Ekahau)', 'yellow'),
        ('other', 'Other', 'gray'),
    ]


class SiteDocument(NetBoxModel):
    name = models.CharField(
        max_length=1000,
        blank=True,
        help_text='(Optional) Specify a name to display for this document. If no name is specified, the filename or url will be used.'
    )

    document = models.FileField(
        upload_to=file_upload,
        blank=True
    )

    external_url = models.URLField(
        blank=True,
        max_length=255
    )

    document_type = models.CharField(
        max_length=30,
        choices=SiteDocTypeChoices
    )

    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.CASCADE,
        related_name='documents'
    )

    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('-created', 'name')
        verbose_name_plural = "Site Documents"
        verbose_name = "Site Document"

    def __str__(self):
        return self.name

    def get_document_type_color(self):
        return SiteDocTypeChoices.colors.get(self.document_type)

    @property
    def filename(self):
        if self.external_url:
            return self.external_url

        return str(self.document.name)
        # if self.document:
        #     filename = self.document.name.rsplit('/', 1)[-1]
        #     return filename.split('_', 1)[1]
    
    # def get_document_type_display()

    def get_absolute_url(self):
        return reverse('plugins:rain_netbox_documents:sitedocument', args=[self.pk])
