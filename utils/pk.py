from datetime import datetime
from rest_framework import serializers
from rest_framework.response import Response


class PkSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


def check_date(from_date, to_date):
    try:
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
    except ValueError:
        return Response({'detail': 'from_date and to_date date format is wrong!'}, status=422)

    if from_date > to_date:
        return Response({'detail': 'from_date must be less than to_date!'}, status=422)
