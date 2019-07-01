from django.test import TestCase, RequestFactory
from graphene.test import Client, GraphQLError
from django.contrib.auth.models import User, AnonymousUser
from projects.models import Project, Vote, UserProfile

from oasis_app.schema import schema

class VoteTest(TestCase):

    def login_test_user(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.user.save()
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.user_profile.save()
        self.client.login(username='test', password='test')
        return self.user_profile

    def setUp(self):
        test_user = self.login_test_user()
        oasis = Project.objects.create(name='Oasis',
                               summary='Northeastern Student-Led Kickstarter',
                               description='Oasis is a platform where student students have the opportunity to share, collaborate, and deploy real solutions that can further improve the Northeastern experience.',
                               creator=test_user,
                               lifecycle='PROTO')

        Vote.objects.create(type='U', project=oasis, creator=test_user)

    def test_get_votes(self):
        """ Tests that querying the list of votes works correctly """
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


    def test_create_vote(self):
        """ Tests that a user can create a vote """
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


    def test_unauthenticated_user_create_vote(self):
        """ Tests that an unauthenticated user will not be allowed to create a vote"""
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

    def test_unidentified_project_create_vote(self):
        """ Tests that an error will be thrown when the project specified in the create vote is not found """
        query = """
        mutation {
          createVote(
            projectId:2
            voteType: D) {
            id
            type
          }
        }
        """
        expected = {
            "createVote": {
                "id": 2,
                "type": "Down"
            }
        }
        request_factory = RequestFactory()
        request_factory.user = self.user
        context_value = request_factory.get('/')
        context_value.user = self.user
        client = Client(schema)
        try:
            result = client.execute(query, context_value=context_value)
        except GraphQLError:
            self.assertEqual('Could not find the specified project.', GraphQLError.message)



