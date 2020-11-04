from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from message.models import Message, Topic


class MessageTest(APITestCase):
    """Message tests
    """

    def setUp(self):
        """Setup test user
        """

        self.credentials = {'username': 'foo', 'password': 'SuperSecret1'}
        self.user = User.objects.create_user(**self.credentials)
        self.topic = Topic.objects.create(name="Ionic", creator=self.user)

    def test_get_message_list_unauthorized(self):
        """Unauthorized users should not be able to access messages
        """

        # Given that we are not logged in
        self.client.logout()

        # When the messages list is retrieved
        response = self.client.get(reverse('message-list'), format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_message_unauthorized(self):
        """Unauthorized users should not be able to access any message
        """

        # Given that we are not logged in
        self.client.logout()

        # When a message is retrieved
        message = Message.objects.create(content="Now supports VueJs", topic=self.topic, creator=self.user)
        response = self.client.get(reverse('topic-detail', kwargs={'pk': message.id}), format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_message_unauthorized(self):
        """Unauthorized users should not be able to create messages
        """

        # Given that we are not logged in
        self.client.logout()

        # When we attempt to create a message
        message = {'name': '', 'topic': self.topic.id, 'creator': self.user.id}
        response = self.client.post(reverse('message-list'), message, format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_message(self):
        """Authenticated users can post messages on topics
        """

        # Given that we are logged in
        self.client.login(**self.credentials)

        # When a message is created
        message = {'content': 'Angular 8 support added', 'topic': self.topic.id}
        response = self.client.post(reverse('message-list'), message, format='json')

        # Then we get a successful response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_message_from_topic(self):
        """Authenticated users can post messages on topics
        """

        # Given that we are logged in
        self.client.login(**self.credentials)

        # When a message is created
        message = {'content': 'Angular 9 support added'}
        response = self.client.post(reverse('topic-new-message', kwargs={'pk': self.topic.id}), message, format='json')

        # Then we get a successful response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_messages_for_topic(self):
        """Authenticated users can list the last 50 messages for a topic
        """

        # Given that we are logged in
        self.client.login(**self.credentials)

        # And there is a topic with messages
        for i in range(51):
            Message.objects.create(content=f'Test {i}', topic=self.topic, creator=self.user)

        # When we list messages for a topic
        response = self.client.get(reverse('topic-messages', kwargs={'pk': self.topic.id}), format='json')

        # Then we get a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # And 50 messages return
        response_data = response.json()
        self.assertEqual(response_data['count'], 51)
        self.assertEqual(len(response_data['results']), 50)
