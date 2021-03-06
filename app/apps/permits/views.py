import json
import logging

from apps.permits.api_queries_decos_join import DecosJoinRequest
from apps.permits.forms import SearchForm
from apps.permits.serializers import DecosPermitSerializer, PermitCheckmarkSerializer
from constance.backends.database.models import Constance
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

bag_id = OpenApiParameter(
    name="bag_id",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description="Verblijfsobjectidentificatie",
)


class PermitViewSet(ViewSet):
    @extend_schema(
        parameters=[bag_id],
        description="Get permit checkmarks based on bag id",
        responses={200: PermitCheckmarkSerializer()},
    )
    @action(detail=False, url_name="permit checkmarks", url_path="checkmarks")
    def get_permit_checkmarks(self, request):
        bag_id = request.GET.get("bag_id")
        response = DecosJoinRequest().get_checkmarks_by_bag_id(bag_id)

        serializer = PermitCheckmarkSerializer(data=response)

        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.initial_data)

    @extend_schema(
        parameters=[bag_id],
        description="Get permit details based on bag id",
        responses={200: DecosPermitSerializer(many=True)},
    )
    @action(detail=False, url_name="permit details", url_path="details")
    def get_permit_details(self, request):
        bag_id = request.GET.get("bag_id")
        response = DecosJoinRequest().get_permits_by_bag_id(bag_id)

        serializer = DecosPermitSerializer(data=response, many=True)

        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.initial_data)

    @extend_schema(description="test connection with decos")
    @action(detail=False, url_name="test decos connection", url_path="test-connect")
    def get_test_decos_connect(self, request):
        import requests

        response = requests.get(
            "https://decosdvl.acc.amsterdam.nl/decosweb/aspx/api/v1/"
        )

        if response.ok:
            return Response(response)
        return False


class DecosAPISearch(UserPassesTestMixin, FormView):
    form_class = SearchForm
    template_name = "decos_search.html"
    success_url = "/admin/decos-api-search/"

    def get_context_data(self, **kwargs):
        kwargs["base_url"] = settings.DECOS_JOIN_API
        return super().get_context_data(**kwargs)

    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            if form.cleaned_data.get("search_url"):
                response = DecosJoinRequest().get(form.cleaned_data.get("search_url"))
            elif form.cleaned_data.get("bag_id"):
                response = DecosJoinRequest().get_decos_object_with_bag_id(
                    form.cleaned_data.get("bag_id")
                )
            else:
                response = DecosJoinRequest().get("")

        context = self.get_context_data(**kwargs)
        context["form"] = form
        context["decos_data"] = response

        return self.render_to_response(context)
