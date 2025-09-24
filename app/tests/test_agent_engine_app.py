import unittest
from unittest.mock import MagicMock, patch
from google.api_core.exceptions import AlreadyExists, NotFound
from google.cloud.iam_admin_v1.types import ServiceAccount
from google.iam.v1.policy_pb2 import Binding

# Assuming _create_service_account is in app.agent_engine_app
from app.agent_engine_app import _create_service_account, _grant_service_account_roles, deploy_agent
from app.agent.root_agent.agent import root_agent
from google.adk.artifacts import GcsArtifactService

class TestServiceAccountCreation(unittest.TestCase):

    @patch('app.agent_engine_app.IAMClient')
    def test_create_service_account_success(self, MockIAMClient):
        mock_client_instance = MockIAMClient.return_value
        mock_client_instance.create_service_account.return_value = ServiceAccount(email='test-sa@test-project.iam.gserviceaccount.com')

        project_id = 'test-project'
        service_account_id = 'test-sa'
        
        email = _create_service_account(project_id, service_account_id)
        
        MockIAMClient.assert_called_once()
        mock_client_instance.create_service_account.assert_called_once_with(
            name=f"projects/{project_id}",
            service_account_id=service_account_id,
            service_account=ServiceAccount(display_name=service_account_id),
        )
        self.assertEqual(email, 'test-sa@test-project.iam.gserviceaccount.com')

    @patch('app.agent_engine_app.IAMClient')
    def test_create_service_account_already_exists(self, MockIAMClient):
        mock_client_instance = MockIAMClient.return_value
        mock_client_instance.create_service_account.side_effect = AlreadyExists('Service account already exists')
        mock_client_instance.get_service_account.return_value = ServiceAccount(email='existing-sa@test-project.iam.gserviceaccount.com')

        project_id = 'test-project'
        service_account_id = 'existing-sa'
        
        email = _create_service_account(project_id, service_account_id)
        
        MockIAMClient.assert_called_once()
        mock_client_instance.create_service_account.assert_called_once() # This will be called and raise AlreadyExists
        mock_client_instance.get_service_account.assert_called_once_with(
            name=f"projects/{project_id}/serviceAccounts/{service_account_id}@{project_id}.iam.gserviceaccount.com"
        )
        self.assertEqual(email, 'existing-sa@test-project.iam.gserviceaccount.com')

    @patch('app.agent_engine_app.IAMClient')
    def test_create_service_account_other_exception(self, MockIAMClient):
        mock_client_instance = MockIAMClient.return_value
        mock_client_instance.create_service_account.side_effect = Exception('Some other error')

        project_id = 'test-project'
        service_account_id = 'error-sa'
        
        with self.assertRaises(Exception) as cm:
            _create_service_account(project_id, service_account_id)
        
        self.assertIn('Some other error', str(cm.exception))

class TestServiceAccountRoleGranting(unittest.TestCase):

    @patch('app.agent_engine_app.IAMClient')
    def test_grant_service_account_roles_success(self, MockIAMClient):
        mock_client_instance = MockIAMClient.return_value
        mock_policy = MagicMock()
        mock_client_instance.get_iam_policy.return_value = mock_policy

        project_id = 'test-project'
        service_account_email = 'test-sa@test-project.iam.gserviceaccount.com'
        roles = ['roles/vertexai.user', 'roles/logging.logWriter']
        
        _grant_service_account_roles(project_id, service_account_email, roles)
        
        MockIAMClient.assert_called_once()
        mock_client_instance.get_iam_policy.assert_called_once_with(
            resource=f"projects/{project_id}/serviceAccounts/{service_account_email}"
        )
        self.assertEqual(len(mock_policy.bindings.add.call_args_list), 2)
        mock_policy.bindings.add.assert_any_call(Binding(role='roles/vertexai.user', members=[f"serviceAccount:{service_account_email}"]))
        mock_policy.bindings.add.assert_any_call(Binding(role='roles/logging.logWriter', members=[f"serviceAccount:{service_account_email}"]))
        mock_client_instance.set_iam_policy.assert_called_once_with(
            resource=f"projects/{project_id}/serviceAccounts/{service_account_email}",
            policy=mock_policy
        )

    @patch('app.agent_engine_app.IAMClient')
    def test_grant_service_account_roles_not_found(self, MockIAMClient):
        mock_client_instance = MockIAMClient.return_value
        mock_client_instance.get_iam_policy.side_effect = NotFound('Service account not found')

        project_id = 'test-project'
        service_account_email = 'non-existent-sa@test-project.iam.gserviceaccount.com'
        roles = ['roles/vertexai.user']
        
        # Expect no exception, but a print statement
        with patch('app.agent_engine_app.logging.info') as mock_logging_info:
            _grant_service_account_roles(project_id, service_account_email, roles)
            mock_logging_info.assert_called_once_with(f"Service account {service_account_email} not found. Cannot grant roles.")
        
        MockIAMClient.assert_called_once()
        mock_client_instance.get_iam_policy.assert_called_once_with(
            resource=f"projects/{project_id}/serviceAccounts/{service_account_email}"
        )
        mock_client_instance.set_iam_policy.assert_not_called()

from app.agent_engine_app import deploy_agent
from app.agent.root_agent.agent import root_agent
from google.adk.artifacts import GcsArtifactService

class TestAgentDeploymentIntegration(unittest.TestCase):

    @patch('app.agent_engine_app.get_deployment_config')
    @patch('app.agent_engine_app._create_service_account')
    @patch('app.agent_engine_app._grant_service_account_roles')
    @patch('app.agent_engine_app.create_bucket_if_not_exists')
    @patch('app.agent_engine_app.vertexai.init')
    @patch('app.agent_engine_app.agent_engines')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('pathlib.Path.mkdir')
    @patch('json.dump')
    def test_deploy_agent_with_new_service_account(self, mock_json_dump, mock_mkdir, mock_open, mock_agent_engines, mock_vertexai_init, mock_create_bucket, mock_grant_roles, mock_create_sa, mock_get_config):
        # Mock deployment config
        mock_config = MagicMock()
        mock_config.project = 'test-project'
        mock_config.location = 'us-central1'
        mock_config.staging_bucket = 'test-bucket'
        mock_config.requirements_file = 'requirements.txt'
        mock_get_config.return_value = mock_config

        # Mock service account creation
        mock_create_sa.return_value = 'new-sa@test-project.iam.gserviceaccount.com'

        # Mock agent_engines.create
        mock_remote_agent = MagicMock()
        mock_remote_agent.resource_name = 'projects/test/locations/test/reasoningEngines/123'
        mock_agent_engines.create.return_value = mock_remote_agent

        # Mock open for requirements.txt
        mock_open.return_value.__enter__.return_value.read.return_value = 'package1\npackage2'

        # Call deploy_agent
        deployed_agent = deploy_agent(
            agent=root_agent,
            agent_name='test-agent',
            agent_description='A test agent',
            extra_packages=['./app/agent'],
            agent_id=None # This will trigger new SA creation
        )

        # Assertions
        mock_get_config.assert_called_once()
        mock_create_sa.assert_called_once_with('test-project', 'test-project-ai-agent-account')
        mock_grant_roles.assert_called_once_with(
            'test-project',
            'new-sa@test-project.iam.gserviceaccount.com',
            ['roles/vertexai.user', 'roles/logging.logWriter', 'roles/storage.objectViewer']
        )
        mock_create_bucket.assert_called_once()
        mock_vertexai_init.assert_called_once()
        mock_agent_engines.create.assert_called_once()
        self.assertEqual(deployed_agent, mock_remote_agent)
        
        # Verify agent_config passed to create
        args, kwargs = mock_agent_engines.create.call_args
        self.assertIn('service_account', kwargs)
        self.assertEqual(kwargs['service_account'], 'new-sa@test-project.iam.gserviceaccount.com')

    @patch('app.agent_engine_app.get_deployment_config')
    @patch('app.agent_engine_app._create_service_account')
    @patch('app.agent_engine_app._grant_service_account_roles')
    @patch('app.agent_engine_app.create_bucket_if_not_exists')
    @patch('app.agent_engine_app.vertexai.init')
    @patch('app.agent_engine_app.agent_engines')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('pathlib.Path.mkdir')
    @patch('json.dump')
    def test_deploy_agent_with_existing_service_account(self, mock_json_dump, mock_mkdir, mock_open, mock_agent_engines, mock_vertexai_init, mock_create_bucket, mock_grant_roles, mock_create_sa, mock_get_config):
        # Mock deployment config
        mock_config = MagicMock()
        mock_config.project = 'test-project'
        mock_config.location = 'us-central1'
        mock_config.staging_bucket = 'test-bucket'
        mock_config.requirements_file = 'requirements.txt'
        mock_get_config.return_value = mock_config

        # Mock service account creation (should not be called if SA is specified)
        mock_create_sa.return_value = 'specified-sa@test-project.iam.gserviceaccount.com'

        # Mock agent_engines.get().update()
        mock_remote_agent = MagicMock()
        mock_remote_agent.resource_name = 'projects/test/locations/test/reasoningEngines/123'
        mock_agent_engines.get.return_value.update.return_value = mock_remote_agent

        # Mock open for requirements.txt
        mock_open.return_value.__enter__.return_value.read.return_value = 'package1\npackage2'

        # Call deploy_agent with a specified agent_id (which implies an existing SA)
        deployed_agent = deploy_agent(
            agent=root_agent,
            agent_name='test-agent',
            agent_description='A test agent',
            extra_packages=['./app/agent'],
            agent_id='projects/test/locations/test/reasoningEngines/existing-agent-id'
        )

        # Assertions
        mock_get_config.assert_called_once()
        mock_create_sa.assert_called_once_with('test-project', 'test-project-ai-agent-account') # Still called to get the email for the default SA
        mock_grant_roles.assert_called_once_with(
            'test-project',
            'specified-sa@test-project.iam.gserviceaccount.com',
            ['roles/vertexai.user', 'roles/logging.logWriter', 'roles/storage.objectViewer']
        )
        mock_create_bucket.assert_called_once()
        mock_vertexai_init.assert_called_once()
        mock_agent_engines.get.assert_called_once_with('projects/test/locations/test/reasoningEngines/existing-agent-id')
        mock_agent_engines.get.return_value.update.assert_called_once()
        self.assertEqual(deployed_agent, mock_remote_agent)
        
        # Verify agent_config passed to update
        args, kwargs = mock_agent_engines.get.return_value.update.call_args
        self.assertIn('service_account', kwargs)
        self.assertEqual(kwargs['service_account'], 'specified-sa@test-project.iam.gserviceaccount.com')

class TestAgentPermissionsE2E(unittest.TestCase):
    # This is a placeholder for an end-to-end test.
    # Actual execution would require a deployed agent and real GCP resources.

    def test_agent_can_access_gcs_with_storage_object_viewer_role(self):
        # Steps:
        # 1. Deploy an agent with a service account that has 'Storage Object Viewer' role.
        # 2. Ensure a GCS bucket exists with some test data.
        # 3. Interact with the deployed agent to make it attempt to read from the GCS bucket.
        # 4. Assert that the agent successfully reads the data.
        # This test cannot be fully automated in a unit/integration test suite without a live deployment.
        self.skipTest("End-to-end test requires live deployment and GCP resources.")
