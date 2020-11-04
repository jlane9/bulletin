from rest_framework import serializers
from message.models import Message, Topic
from bulletin.serializers import UserSerializer


class TopicSerializer(serializers.ModelSerializer):
    """Topic REST serializer
    """

    creator = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        """Topic REST serializer metadata
        """

        model = Topic
        fields = ('id', 'name', 'creator', 'created', 'updated')

    def save(self, **kwargs):
        """Add creator to topic
        """

        kwargs['creator'] = self.fields['creator'].get_default()
        return super().save(**kwargs)

    def to_representation(self, instance: Topic) -> dict:
        """Return a JSON representation of a topic

        :param Topic instance: Topic instance
        :return: JSON representation of topic instance
        :rtype: dict
        """

        self.fields['creator'] = UserSerializer(read_only=True)
        return super(TopicSerializer, self).to_representation(instance)


class MessageSerializer(serializers.ModelSerializer):
    """Message REST serializer
    """

    creator = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        """Message REST serializer metadata
        """

        model = Message
        fields = ('id', 'content', 'topic', 'creator', 'created', 'updated')

    def save(self, **kwargs):
        """Add creator to message
        """

        kwargs['creator'] = self.fields['creator'].get_default()
        return super().save(**kwargs)

    def to_representation(self, instance: Message) -> dict:
        """Return a JSON representation of a message

        :param Message instance: Message instance
        :return: JSON representation of message instance
        :rtype: dict
        """

        self.fields['topic'] = TopicSerializer(read_only=True)
        self.fields['creator'] = UserSerializer(read_only=True)
        return super(MessageSerializer, self).to_representation(instance)
