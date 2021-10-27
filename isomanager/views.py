from dal import autocomplete
from django.db.models import Q

from .models import OsEdition


class OSAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = OsEdition.objects.all()
        print(self.q)
        if self.q:
            qs = qs.filter(
                Q(os_edition_type__icontains=self.q) | Q(os_edition_name__icontains=self.q) |
                Q(os_edition_version=self.q) | Q(os_edition_language__icontains=self.q) |
                Q(os_edition_arch__icontains=self.q)
            )
        return qs
