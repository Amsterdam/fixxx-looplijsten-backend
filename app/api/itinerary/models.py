from django.db import models
from django.contrib.admin.utils import flatten
from django.core.validators import MinValueValidator, MaxValueValidator
from api.users.models import User
from api.cases.models import Case, Project, Stadium
from api.planner.algorithm.knapsack import ItineraryKnapsackSuggestions, ItineraryKnapsackList

class Itinerary(models.Model):
    """ Itinerary for visiting cases """

    created_at = models.DateField(auto_now_add=True)

    def get_center(self):
        '''
        Returns the center coordinates of the itinerary
        '''
        cases = self.get_cases()
        locations = [case.get_location() for case in cases]
        locations_lng = [location['lng'] for location in locations]
        locations_lat = [location['lat'] for location in locations]

        locations_lng = sum(locations_lng) / len(cases)
        locations_lat = sum(locations_lat) / len(cases)

        return {'lat': locations_lat, 'lng': locations_lng}

    def get_cases_for_date(date):
        '''
        returns a list of cases which are already in itineraries for a given date
        '''
        itineraries = Itinerary.objects.filter(created_at=date)
        itineraries = [itinerary.get_cases() for itinerary in itineraries]
        cases = flatten(itineraries)

        return cases

    def get_cases(self):
        '''
        Returns a list of cases for this itinerary
        '''
        cases = [item.case for item in self.items.all()]
        return cases

    def add_case(self, case_id, position):
        '''
        Adds a case to the itinerary
        '''
        case = Case.get(case_id=case_id)
        used_cases = Itinerary.get_cases_for_date(self.created_at)

        if case in used_cases:
            raise ValueError('This case is already used in an itinerary for this date')

        itinerary_item = ItineraryItem.objects.create(
            case=case,
            itinerary=self,
            position=position)

        return itinerary_item

    def get_suggestions(self):
        '''
        Returns a list of suggested cases which can be added to this itinerary
        '''
        # If no cases exists the suggestions algorithm won't work, this is a safe fallback
        if not self.get_cases():
            return self.get_cases_from_settings()

        # Initialise using this itinerary's settings
        generator = ItineraryKnapsackSuggestions(self.settings)

        # Exclude the cases which are already in itineraries
        cases = Itinerary.get_cases_for_date(self.created_at)
        generator.exclude(cases)

        # Generate suggestions based on this itineraries' center
        center = self.get_center()
        generated_list = generator.generate(center)

        return generated_list

    def get_cases_from_settings(self):
        '''
        Returns a list of cases based on the settings which can be added to this itinerary
        '''
        # Initialise using this itinerary's settings
        generator = ItineraryKnapsackList(self.settings)

        # Exclude cases which are already in itineraries
        cases = Itinerary.get_cases_for_date(self.created_at)
        generator.exclude(cases)

        # Generator the list
        generated_list = generator.generate()

        return generated_list

    def clear_team_members(self):
        '''
        Removes all team members from this itinerary
        '''
        team_members = self.team_members.all()

        for team_member in team_members:
            team_member.delete()

    def add_team_members(self, user_ids):
        '''
        Addes team members to this itinerary
        '''
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            ItineraryTeamMember.objects.create(user=user, itinerary=self)

    def __str__(self):
        '''
        A string representation of this itinerary
        '''
        team_members = self.team_members.all()
        team_members = [str(member) for member in team_members]
        string = ', '.join(team_members)

        return string

class ItinerarySettings(models.Model):
    """
    Settings for an itinerary
    """
    opening_date = models.DateField(blank=False,
                                    null=False)

    target_length = models.IntegerField(default=8,
                                        validators=[MinValueValidator(1), MaxValueValidator(20)])

    itinerary = models.OneToOneField(Itinerary,
                                     on_delete=models.CASCADE,
                                     null=False,
                                     unique=True,
                                     related_name='settings')

    projects = models.ManyToManyField(to=Project,
                                      blank=False,
                                      related_name='settings')

    primary_stadium = models.ForeignKey(to=Stadium,
                                        null=True,
                                        on_delete=models.CASCADE,
                                        related_name='settings_as_primary_stadium')

    secondary_stadia = models.ManyToManyField(to=Stadium,
                                              related_name='settings_as_secondary_stadia')

    exclude_stadia = models.ManyToManyField(to=Stadium,
                                            related_name='settings_as_exclude_stadia')

    start_case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.itinerary.__str__()


class ItineraryTeamMember(models.Model):
    """ Member of an Itinerary Team """

    class Meta:
        unique_together = ['user', 'itinerary']

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, null=False,
                             related_name='teams',
                             related_query_name="user")

    itinerary = models.ForeignKey(Itinerary,
                                  on_delete=models.CASCADE,
                                  null=False,
                                  related_name='team_members')

    def __str__(self):
        return self.user.full_name

class ItineraryItem(models.Model):
    """ Single Itinerary item """
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, null=False, related_name='items')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, null=True, blank=False, related_name='cases')
    position = models.FloatField(null=False, blank=False)
    checked = models.BooleanField(null=False, blank=False, default=False)

    class Meta:
        ordering = ['position']

    def __str__(self):
        if self.case:
            return self.case.__str__()
        else:
            return ''

    def set_position_to_last(self):
        '''
        Sets this item's position to the last in the ItineraryItem list
        '''
        itinerary_item_list = self.itinerary.items.all().order_by('position')
        itinerary_items = list(itinerary_item_list)

        if(len(itinerary_items) == 0):
            self.position = 1
        else:
            last_item = itinerary_items[-1]
            self.position = last_item.position + 1

    def check_items_same_position(self):
        '''
        Don't allow saving if another item in the list has the same position
        '''
        items_with_same_position = self.itinerary.items.all().filter(position=self.position)
        items_with_same_position = items_with_same_position.exclude(pk=self.pk)

        if items_with_same_position.exists():
            raise ValueError('An item with this position already exists')

    def check_items_same_case(self):
        '''
        Don't allow saving if the itinerary already contains the same case
        '''
        items_with_same_case = self.itinerary.items.all().filter(case=self.case)
        items_with_same_case = items_with_same_case.exclude(pk=self.pk)

        if items_with_same_case.exists():
            raise ValueError('The itinerary already contains this case')

    def save(self, *args, **kwargs):
        if self.position is None:
            # If no position is given, set the item to the last in list
            self.set_position_to_last()

        self.check_items_same_position()
        self.check_items_same_case()

        super().save(*args, **kwargs)

class Note(models.Model):
    """ A note for an Itinerary Item """
    itinerary_item = models.ForeignKey(ItineraryItem, on_delete=models.CASCADE,
                                       null=False, related_name='notes')
    text = models.TextField(null=False, blank=False, max_length=1024)
    author = models.ForeignKey(to=User, null=True, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        max_length = 20
        if len(self.text) > max_length:
            return '{}...'.format(self.text[:max_length])
        return self.text
