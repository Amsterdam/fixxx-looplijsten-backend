from rest_framework import serializers
from api.planner.const import PROJECTS, STAGES

class ListSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    number_of_lists = serializers.IntegerField(required=True)
    length_of_lists = serializers.IntegerField(required=True)
    primary_stadium = serializers.ChoiceField(required=False, choices=STAGES)
    secondary_stadia = serializers.MultipleChoiceField(required=False, choices=STAGES)
    exclude_stadia = serializers.MultipleChoiceField(required=False, choices=STAGES)

    def validate_mutual_exclusivity(self, stadia_a, stadia_b, message):
        for stadium in stadia_a:
            if stadium in stadia_b:
                raise serializers.ValidationError(message)

    def validate_does_not_contain(self, stadium, stadia, message):
        if stadium in stadia:
            raise serializers.ValidationError(message)

    def validate(self, data):
        secondary_stadia = data.get('secondary_stadia', [])
        exclude_stadia = data.get('exclude_stadia', [])
        error_message = "exclude_stadia and secondary_stadia should be mutually exclusive"
        self.validate_mutual_exclusivity(secondary_stadia, exclude_stadia, error_message)

        primary_stadium = data.get('primary_stadium', None)
        if primary_stadium:
            error_message = "The primary_stadium cannot be in exclude_stadia "
            self.validate_does_not_contain(primary_stadium, exclude_stadia, error_message)

        return data


class WeekListSerializer(serializers.Serializer):
    opening_date = serializers.DateField(required=True)
    opening_reasons = serializers.MultipleChoiceField(required=True, choices=PROJECTS)
    lists = ListSerializer(required=True, many=True)
