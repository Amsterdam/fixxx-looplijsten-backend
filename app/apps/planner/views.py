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


class SettingsPlannerViewSet(ViewSet, CreateAPIView):
    """
    Retrieves the planner settings which are used for generating lists
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PlannerSettingsSerializer

    def list(self, request):
        planner_settings, _ = Constance.objects.get_or_create(
            key=settings.CONSTANCE_PLANNER_SETTINGS_KEY
        )
        settings_data = planner_settings.value

        if settings_data:
            # Make sure the string from constance is converted to JSON
            settings_data = json.loads(settings_data)
        else:
            # Set the default value if nothing is set, and store it
            settings_data = settings.EXAMPLE_PLANNER_SETTINGS
            planner_settings.value = json.dumps(settings_data)
            planner_settings.save()

        return JsonResponse(settings_data)

    def create(self, request):
        data = request.data
        serializer = PlannerSettingsSerializer(data=data)
        is_valid = serializer.is_valid()

        if not is_valid:
            return JsonResponse(
                {
                    "message": "Could not validate posted data",
                    "errors": serializer.errors,
                },
                status=HttpResponseBadRequest.status_code,
            )

        planner_settings, _ = Constance.objects.get_or_create(
            key=settings.CONSTANCE_PLANNER_SETTINGS_KEY
        )
        planner_settings.value = json.dumps(data)
        planner_settings.save()

        return JsonResponse(data)


class PostalCodeRangePresetViewSet(ModelViewSet):
    """
    A view for listing PostalCodeRangeSets
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PostalCodeRangePresetSerializer
    queryset = PostalCodeRangeSet.objects.all()


class TeamSettingsViewSet(ModelViewSet):
    """
    A view for listing/adding/updating/removing a TeamSettings
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TeamSettingsSerializer
    queryset = TeamSettings.objects.all()


class DaySettingsViewSet(ModelViewSet):
    """
    A view for listing/adding/updating/removing a DaySettings
    """

    permission_classes = [IsAuthenticated]
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
        "cases.Project",
        "cases.Stadium",
        "cases.StadiumLabel",
        "--indent=4",
    )
    sys.stdout = sysout

    return response
