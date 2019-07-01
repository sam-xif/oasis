import snapshottest
from django.test import TestCase, RequestFactory
from graphene.test import Client, GraphQLError
from django.contrib.auth.models import User, AnonymousUser
from projects.models import Project, Vote, UserProfile

from oasis_app.schema import schema


class ProjectTest(snapshottest.TestCase, TestCase):
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
                               lifecycle='PROTOTYPE')

        Vote.objects.create(type='U', project=oasis, creator=test_user)

    """
    Snapshot tests for Project
    """

    def test_query(self):
        query = """
        { 
            projects {
                name
                summary
                description
                creator {
                    id
                }
                lifecycle
            }
        }"""

        client = Client(schema)
        self.assertMatchSnapshot(client.execute(query))

    def test_mutate(self):
        query = """
        mutation {
          createProject(
            description: "test"
            lifecycle: PROTOTYPE
            name: "test"
          ) {
            id
            name
          }
        } 
        """

        request_factory = RequestFactory()
        request_factory.user = self.user
        context_value = request_factory.get('/')
        context_value.user = self.user

        client = Client(schema)
        self.assertMatchSnapshot(client.execute(query, context_value=context_value))

