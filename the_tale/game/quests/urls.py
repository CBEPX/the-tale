# coding: utf-8

from dext.views.dispatcher import resource_patterns
from .views import QuestsResource

urlpatterns = resource_patterns(QuestsResource)
