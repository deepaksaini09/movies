from rest_framework import serializers


class CastMovieActors(serializers.Serializer):
    id = serializers.IntegerField()
    characterName = serializers.CharField(max_length=100)
    realName = serializers.CharField(max_length=100)
    peopleProfileLink = serializers.CharField(max_length=500)
    takingPartInEpisode = serializers.CharField(max_length=100)
    created_at = serializers.DateTimeField()
    archived_at = serializers.DateTimeField()
    imageOfCastPerson = serializers.CharField(max_length=500)
