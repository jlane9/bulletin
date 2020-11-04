from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTest(APITestCase):
    """Authentication tests
    """

    def test_unique_user(self):
        """Users must have a unique username
        """

        User.objects.create_user(username='bar', password='SecretPassword1')

        # Given we have a username that already exists
        payload = {'username': 'bar', 'password': 'NewUserPass1'}

        # When we signup for an account using that username and password
        response = self.client.post(reverse('user-list'), payload, format='json')

        # Then the new user fails to create
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username="bar").count(), 1)

        # And the error message is that the username already exists
        self.assertEqual(response.json()['username'], ['A user with that username already exists.'])

    def test_signup_user(self):
        """Users can sign up with username & password
        """

        # Given we have a username and password
        payload = {'username': 'foo', 'password': 'SuperSecret1'}

        # When we signup for an account using that username and password
        response = self.client.post(reverse('user-list'), payload, format='json')

        # Then the user is successfully created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(username="foo").count(), 1)

    def test_login_user(self):
        """Users can login with username & password
        """

        # Given we have created a user
        credentials = {'username': 'foo', 'password': 'SuperSecret1'}
        User.objects.create_user(**credentials)

        # When we login to that user using the username and password
        response = self.client.post(reverse('jwt-auth'), credentials, format='json')

        # Then the user should receive a successful login
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.json()['token'])

    def test_unauthorized_user_list(self):
        """Users cannot retrieve user list unless they are logged in
        """

        # Given that we are not logged in
        self.client.logout()

        # When the users list is retrieved
        response = self.client.get(reverse('user-list'), format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_detailed(self):
        """Users cannot retrieve user list unless they are logged in
        """

        # Given that we are not logged in
        self.client.logout()

        # When the user is retrieved
        user = User.objects.create_user({'username': 'foo', 'password': 'SuperSecret1'})
        response = self.client.get(reverse('user-detail', kwargs={"pk": user.id}), format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_delete(self):
        """Users cannot retrieve user list unless they are logged in
        """

        # Given that we are not logged in
        self.client.logout()

        # When the user is deleted
        user = User.objects.create_user({'username': 'foo', 'password': 'SuperSecret1'})
        response = self.client.delete(reverse('user-detail', kwargs={"pk": user.id}), format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_update(self):
        """Users cannot retrieve user list unless they are logged in
        """

        # Given that we are not logged in
        self.client.logout()

        # When the user is updated
        credentials = {'username': 'foo', 'password': 'SuperSecret1'}
        user = User.objects.create_user(**credentials)
        credentials['password'] = 'ChangeMe123'
        response = self.client.put(reverse('user-detail', kwargs={"pk": user.id}), credentials, format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_patch(self):
        """Users cannot retrieve user list unless they are logged in
        """

        # Given that we are not logged in
        self.client.logout()

        # When the user is patched
        user = User.objects.create_user({'username': 'foo', 'password': 'SuperSecret1'})
        response = self.client.put(reverse('user-detail', kwargs={"pk": user.id}), {'is_staff': False}, format='json')

        # Then we get an unsuccessful response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_edit_only_self(self):
        """Users can alter their own account
        """

        # Given we have two users
        credentials = {'username': 'foo', 'password': 'SuperSecret1'}
        User.objects.create_user(**credentials)
        user2 = User.objects.create_user({'username': 'bar', 'password': 'VerySecret1'})

        # When we try to update a user from a different user
        self.client.login(**credentials)
        response = self.client.patch(reverse('user-detail', kwargs={"pk": user2.id}), {'is_staff': True}, format='json')

        # Then the user should be forbidden from doing so
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], 'You do not have permission to perform this action.')
