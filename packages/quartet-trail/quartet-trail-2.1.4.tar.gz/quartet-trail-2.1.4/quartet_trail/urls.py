# -*- coding: utf-8 -*-
from django.apps import apps
from django.urls import re_path
from . import models
from . import views

urlpatterns = []


def register_models(app_list, exclude_models):
    """
    Registers all models for given app name.
    Ties the model to quartet_trail rather than
    the original app for table creation. No db/model
    changes are done on the original app.
    """
    for app_name in app_list:
        app = apps.get_app_config(app_name)
        for model in list(app.models.values()):
            if models.get_model_fullname(model) not in exclude_models:
                api_endpoint = re_path(
                    "^quartet-trail/" + model.__qualname__ + "/?",
                    views.QuartetTrailViewSet.as_view({"get": "list"}),
                )
                urlpatterns.append(api_endpoint)


register_models(models.tracked_app_list, models.exclude_models)
