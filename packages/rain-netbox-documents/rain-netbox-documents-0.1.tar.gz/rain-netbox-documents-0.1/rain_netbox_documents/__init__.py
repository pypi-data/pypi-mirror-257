from extras.plugins import PluginConfig


class RainNetBoxDocumentsConfig(PluginConfig):
    name = 'rain_netbox_documents'
    verbose_name = ' Rain NetBox Documents'
    description = 'Simple document manager for rain NetBox'
    version = '0.1'
    base_url = 'rain-netbox-documents'


config = RainNetBoxDocumentsConfig


