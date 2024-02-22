from django.views.generic.list import ListView
from django.conf import settings

from .models import DjangoActionLogEntry


class Log(ListView):
    model = DjangoActionLogEntry
    paginate_by = 100

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
            if app_labels := getattr(
                settings, "LOG_LIST_NOSTAFF_EXCLUDE_APP_LABELS", None
            ):
                queryset = queryset.exclude(content_type__app_label__in=app_labels)
        elif app_labels := getattr(settings, "LOG_LIST_EXCLUDE_APP_LABELS", None):
            queryset = queryset.exclude(content_type__app_label__in=app_labels)
        return queryset
