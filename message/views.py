from datetime import datetime
from django.db.models import Max, QuerySet, Value
from django.db.models.functions import Coalesce
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from message import models, serializers


class MessageViewSet(viewsets.ModelViewSet):
    """Message REST view
    """

    queryset: QuerySet = models.Message.objects.filter(active=True)
    serializer_class = serializers.MessageSerializer


class TopicViewSet(viewsets.ModelViewSet):
    """Topic REST view
    """

    queryset: QuerySet = models.Topic.objects.filter(active=True).annotate(
        most_recent=Coalesce(Max('message__created'), Value(datetime.utcfromtimestamp(0)))
    ).order_by('-most_recent')
    serializer_class = serializers.TopicSerializer

    @action(detail=True, methods=['GET'], serializer_class=serializers.MessageSerializer)
    def messages(self, *_args, **_kwargs) -> Response:
        """Return messages for the specified topic
        """

        topic: models.Topic = self.get_object()
        messages: QuerySet = topic.message_set.all()

        page = self.paginate_queryset(messages)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], serializer_class=serializers.MessageSerializer)
    def new_message(self, request: Request, *_args, **_kwargs) -> Response:
        """Create new message for topic
        """

        topic: models.Topic = self.get_object()
        serializer = self.get_serializer(data={**request.data, 'topic': topic.id})

        if serializer.is_valid():
            models.Message.objects.create(**request.data, topic=topic, creator=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
