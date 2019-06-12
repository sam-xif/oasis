from django.test import TestCase, RequestFactory
from graphene.test import Client
from django.contrib.auth.models import User
from .models import Project, Vote

from oasis_app.schema import schema

class VoteTest(TestCase):

    def login_test_user(test_case):
        test_case.user = User.objects.create_user(username='test', password='test')
        test_case.user.save()
        test_case.client.login(username='test', password='test')
        return test_case.user

    def setUp(self):
        test_user = self.login_test_user()
        oasis = Project.objects.create(name='Oasis',
                               summary='Northeastern Student-Led Kickstarter',
                               description='Oasis is a platform where student students have the opportunity to share, collaborate, and deploy real solutions that can further improve the Northeastern experience.',
                               creator=test_user,
                               lifecycle='PROTO')

        Vote.objects.create(type='U', project=oasis, creator=test_user)


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
        context_value = request_factory.get('/')
        context_value.user = User.objects.create(username='test1', password='test')
        client = Client(schema)

        result = client.execute(query, context_value=context_value)
        self.assertEqual(expected, result['data'])
