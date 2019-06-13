from django.test import TestCase, RequestFactory
from graphene.test import Client, GraphQLError
from django.contrib.auth.models import User, AnonymousUser
from .models import Project, Vote

from oasis_app.schema import schema

class VoteTest(TestCase):

    def login_test_user(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.user.save()
        self.client.login(username='test', password='test')
        return self.user

    def setUp(self):
        test_user = self.login_test_user()
        oasis = Project.objects.create(name='Oasis',
                               summary='Northeastern Student-Led Kickstarter',
                               description='Oasis is a platform where student students have the opportunity to share, collaborate, and deploy real solutions that can further improve the Northeastern experience.',
                               creator=test_user,
                               lifecycle='PROTO')

        Vote.objects.create(type='U', project=oasis, creator=test_user)

    """ Tests that querying the list of votes works correctly """
    def test_get_votes(self):
        query = """
        query {
          votes {
            id
            type
          }
        }
        """
        expected = {
            "votes": [
                {
                    "id": "1",
                    "type": "U"
                 }
            ]
        }
        client = Client(schema)
        result = client.execute(query)
        self.assertEqual(expected, result['data'])

    """ Tests that a user can create a vote """
    def test_create_vote(self):
        query = """
        mutation {
          createVote(
            projectId:1
            voteType: U) {
            id
            type
          }
        }
        """
        expected = {
            "createVote": {
                "id": 2,
                "type": "Up"
            }
        }
        request_factory = RequestFactory()
        request_factory.user = self.user
        context_value = request_factory.get('/')
        context_value.user = self.user
        client = Client(schema, context_value=context_value)

        result = client.execute(query)
        self.assertEqual(expected, result['data'])

    """ Tests that an unauthenticated user will not be allowed to create a vote"""
    def test_unauthenticated_user_create_vote(self):
        query = """
        mutation {
          createVote(
            projectId:1
            voteType: U) {
            id
            type
          }
        }
        """
        expected = {
            "createVote": {
                "id": 2,
                "type": "Up"
            }
        }
        request_factory = RequestFactory()
        request_factory.user = AnonymousUser()
        context_value = request_factory.get('/')
        context_value.user = AnonymousUser()
        client = Client(schema)
        try:
            result = client.execute(query, context_value=context_value)
        except GraphQLError:
            self.assertEqual('User must be logged in to vote', GraphQLError.message)
