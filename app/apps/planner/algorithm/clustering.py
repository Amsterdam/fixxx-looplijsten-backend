import logging

from apps.planner.algorithm.base import ItineraryGenerateAlgorithm
from apps.planner.utils import get_case_coordinates
from sklearn.cluster import OPTICS

LOGGER = logging.getLogger(__name__)


class ItineraryGenerateCluster(ItineraryGenerateAlgorithm):
    """Generates an itinerary using a clustering algorithm"""

    MIN_SAMPLE_SIZE = 3

    def optics_clustering(self, cluster_size, cases):
        if cluster_size < self.MIN_SAMPLE_SIZE:
            return [], cases

        coordinates = get_case_coordinates(cases)
        clusters = OPTICS(min_samples=3, min_cluster_size=cluster_size).fit(coordinates)

        clustering_labels = clusters.labels_
        n_lists = max(clustering_labels) + 1

        groups = [[] for i in range(0, n_lists)]
        unplanned_cases = []

        for i in range(0, len(cases)):
            group = clustering_labels[i]
            case = cases[i]
            if group == -1:
                unplanned_cases.append(case)
            else:
                groups[group].append(case)

        return groups, unplanned_cases

    def generate(self):
        cases = self.__get_eligible_cases__()

        LOGGER.info("Generating list with {} eligible cases".format(len(cases)))

        # The cluster size cannot be larger then the number of unplanned cases
        cluster_size = min(self.target_length, len(cases))

        # Do a clustering using this subset
        clusters, rest = self.optics_clustering(cluster_size, cases)

        # Select the best list and append it to the itinerary
        if not clusters:
            LOGGER.warning("Could not generate clusters")
            return []

        return clusters[0]
