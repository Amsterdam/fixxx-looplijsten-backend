import datetime
import json
import sys

from apps.planner.models import DaySettings, PostalCodeRangeSet, TeamSettings
from apps.planner.serializers import (
    DaySettingsSerializer,
    PlannerSettingsSerializer,
    PostalCodeRangePresetSerializer,
    TeamSettingsSerializer,
)
from constance.backends.database.models import Constance
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.management import call_command
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet


class PostalCodeRangePresetViewSet(ModelViewSet):
    """
    A view for listing PostalCodeRangeSets
    """

    serializer_class = PostalCodeRangePresetSerializer
    queryset = PostalCodeRangeSet.objects.all()


class TeamSettingsViewSet(ModelViewSet):
    """
    A view for listing/adding/updating/removing a TeamSettings
    """

    serializer_class = TeamSettingsSerializer
    queryset = TeamSettings.objects.all()


class DaySettingsViewSet(ModelViewSet):
    """
    A view for listing/adding/updating/removing a DaySettings
    """

    serializer_class = DaySettingsSerializer
    queryset = DaySettings.objects.all()


@user_passes_test(lambda u: u.is_superuser)
def dumpdata(request):
    sysout = sys.stdout
    fname = "%s-%s.json" % ("top-planner", datetime.datetime.now().strftime("%Y-%m-%d"))
    response = HttpResponse(content_type="application/json")
    response["Content-Disposition"] = "attachment; filename=%s" % fname

    sys.stdout = response
    call_command(
        "dumpdata",
        "planner",
        "visits.Situation",
        "visits.Observation",
        "visits.SuggestNextVisit",
        "cases.Project",
        "cases.Stadium",
        "cases.StadiumLabel",
        "--indent=4",
    )
    sys.stdout = sysout

    return response
