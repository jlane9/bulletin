from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from message.models import Message, Topic


class TopicTest(APITestCase):
    """Message topic tests
    """

    def setUp(self):
        """Setup test user
        """

        self.credentials = {'username': 'foo', 'password': 'SuperSecret1'}
        self.user = User.objects.create_user(**self.credentials)

    def test_get_topic_list_unauthorized(self):
        """Unauthorized users should not be able to access topics
        """

        # Given that we are not logged in
        self.client.logout()

        # When the topics list is retrieved
        response = self.client.get(reverse('topic-list'), format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_topic_unauthorized(self):
        """Unauthorized users should not be able to access any topic
        """

        # Given that we are not logged in
        self.client.logout()

        # When a topic is retrieved
        topic = Topic.objects.create(name="Ionic", creator=self.user)
        response = self.client.get(reverse('topic-detail', kwargs={'pk': topic.id}), format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_topic_unauthorized(self):
        """Unauthorized users should not be able to create topics
        """

        # Given that we are not logged in
        self.client.logout()

        # When we attempt to create a topic
        topic = {'name': "React", 'creator': self.user.id}
        response = self.client.post(reverse('topic-list'), topic, format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_topic(self):
        """Any authenticated user can create a new topic
        """

        # Given that we are logged in
        self.client.login(**self.credentials)

        # When a topic is created
        topic = {'name': 'React'}
        response = self.client.post(reverse('topic-list'), topic, format='json')

        # Then we get a successful response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_topic_by_most_recent(self):
        """Authenticated users can list topics by most recently active
        """

        # Given that we are logged in
        self.client.login(**self.credentials)

        # And there are topics with messages
        topic1 = Topic.objects.create(name="Ionic", creator=self.user)
        topic2 = Topic.objects.create(name="React", creator=self.user)
        topic3 = Topic.objects.create(name="VueJs", creator=self.user)

        Message.objects.create(content=f'Test 1', topic=topic2, creator=self.user)
        Message.objects.create(content=f'Test 2', topic=topic3, creator=self.user)
        Message.objects.create(content=f'Test 3', topic=topic1, creator=self.user)

        # When we retrieve topics
        response = self.client.get(reverse('topic-list'), format='json')

        # Then we get a successful response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # And they should be in order of most recently commented
        messages = [message['name'] for message in response.json()['results']]
        self.assertEqual(messages, ['Ionic', 'VueJs', 'React'])
