from django.apps import AppConfig


class IsomanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'isomanager'

    def ready(self):
        remote_catalog = self.get_model('RemoteCatalog')

        if remote_catalog.objects.count() < 1:
            payload = {
                "catalog_name":"default",
                "json_catalog":None,
                "version":"1.0",
                "auto_update":True,
                "priority":"1",
                "remote_url":"http://raph.info/dim.json"
            }
            remote_catalog.objects.create(**payload)
