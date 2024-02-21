# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import re_path, include

from quartet_masterdata.urls import urlpatterns as quartet_masterdata_urls

app_name = "quartet_masterdata"

urlpatterns = [
    re_path(r"^", include(quartet_masterdata_urls)),
]
