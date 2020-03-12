from datetime import datetime
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

from utils.safety_lock import safety_lock
import utils.queries as q
import utils.queries_brk_api as brk_api
import utils.queries_bag_api as bag_api

from api.itinerary.serializers import CaseSerializer
from api.itinerary.models import Itinerary

class CaseViewSet(ViewSet):
    """
    A Viewset for showing a single Case in detail
    """

    permission_classes = [IsAuthenticated]

    @safety_lock
    def retrieve(self, request, pk):
        case_id = pk
        related_case_ids = q.get_related_case_ids(case_id)

        wng_id = related_case_ids.get('wng_id', None)
        adres_id = related_case_ids.get('adres_id', None)

        if not wng_id or not adres_id:
            return HttpResponseNotFound('Case not found')

        # Get the bag_data first in order to retrieve the 'verblijfsobjectidentificatie' id
        bag_data = bag_api.get_bag_data(wng_id)
        bag_id = bag_data.get('verblijfsobjectidentificatie')

        data = {
            'bwv_hotline_bevinding': q.get_bwv_hotline_bevinding(wng_id),
            'bwv_hotline_melding': q.get_bwv_hotline_melding(wng_id),
            'bwv_personen': q.get_bwv_personen(adres_id),
            'import_adres': q.get_import_adres(wng_id),
            'import_stadia': q.get_import_stadia(case_id),
            'bwv_tmp': q.get_bwv_tmp(case_id, adres_id),
            'statements': q.get_statements(case_id),
            'vakantie_verhuur': q.get_rental_information(wng_id),
            'bag_data': bag_data,
            'brk_data': brk_api.get_brk_data(bag_id),
            'related_cases': q.get_related_cases(adres_id)
        }

        return JsonResponse(data)


class CaseSearchViewSet(ViewSet, ListAPIView):
    """
    A temporary search ViewSet for listing cases
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CaseSerializer

    @safety_lock
    def list(self, request):
        postal_code = request.GET.get('postalCode', None)
        street_number = request.GET.get('streetNumber', None)
        suffix = request.GET.get('suffix', None)

        if postal_code is None:
            return HttpResponseBadRequest('Missing postal code is required')
        elif not street_number:
            return HttpResponseBadRequest('Missing steet number is required')
        else:
            items = q.get_search_results(postal_code, street_number, suffix)

            # Enrich the search result data with teams whose itinerary contains this item
            # TODO: Quickly implemented for demo/prototyping. Revisit and improve this later.
            items_mapped = {}
            for item in items:
                item['teams'] = []
                items_mapped[item.get('case_id')] = item

            itineraries = Itinerary.objects.filter(created_at=datetime.now()).all()
            for itinerary in itineraries:
                case_ids = [case.case_id for case in itinerary.get_cases()]
                for case_id in case_ids:
                    item = items_mapped.get(case_id, None)
                    if item:
                        item['teams'].append(itinerary.__str__())

            return JsonResponse({'cases': items})
