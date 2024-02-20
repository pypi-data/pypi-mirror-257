import pathlib
import os
import pytest
from zeblok.deploy import DeployModel
from zeblok.utils.errors import InvalidCredentialsError, AuthenticationError, ServerError, ModelDeploymentError, \
    InvalidModelFolder, FileUploadError
import requests

AUTHENTICATION_MESSAGE = 'User not authenticated. Please check your token or api_access_key or api_access_secret'
TEMP_ERROR_TEXT = 'error_text'
SECRET_KEY = 'some_secret_key'
USERNAME = 'temp_username'
MODEL_FOLDER_PATH = 'temp_model_folder_path'


@pytest.fixture
def deploy_model_data():
    return DeployModel(
        base_url='temp_base_url', token='Bearer temp-token', bucket_name='temp_bucket_name', username='temp_username',
        storage_url='temp_storage_url'
    )


class MockServerErrorResponse:
    def __init__(self, url, headers, data):
        self.status_code = 500
        self.text = TEMP_ERROR_TEXT


class MockAuthenticationErrorResponse:
    def __init__(self, url, headers, data):
        self.status_code = 401
        self.text = ''


class UploadModelUtils:
    @staticmethod
    def mock_exists(self):
        return True

    @staticmethod
    def mock_is_dir(self):
        return True

    @staticmethod
    def mock_os_access(path, mode=os.W_OK):
        return True

    @staticmethod
    def mock_os_remove(path):
        return

    @staticmethod
    def mock_prepare_model_zip(self, model_folder_path: pathlib.Path):
        return model_folder_path.parent.joinpath(f'{model_folder_path.name.lower()}.zip')

    @staticmethod
    def mock_validate_folder_format(self, model_folder_path):
        return

    @staticmethod
    def mock_upload_file(self, file_name, username, secret_key):
        return 'temp_presigned_get_url'

    @staticmethod
    def mock_register_image_name(self, image_name):
        return


class TestGetNamespaces:
    def test_random_error(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockServerErrorResponse)
        with pytest.raises(expected_exception=ServerError, match=TEMP_ERROR_TEXT):
            deploy_model_data.get_namespaces()

    def test_invalid_token(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockAuthenticationErrorResponse)
        with pytest.raises(expected_exception=AuthenticationError, match=AUTHENTICATION_MESSAGE):
            deploy_model_data.get_namespaces()

    def test_success(self, deploy_model_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 200

            @staticmethod
            def json():
                return {'success': True, 'data': [
                    {'_id': 'id_1', 'name': 'namespace1'},
                    {'_id': 'id_2', 'name': 'namespace2'}
                ]}

        monkeypatch.setattr(requests, 'get', MockResponse)
        assert deploy_model_data.get_namespaces() == [{'_id': 'id_1', 'name': 'namespace1'},
                                                      {'_id': 'id_2', 'name': 'namespace2'}]


class TestGetDatacenters:
    def test_random_error(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockServerErrorResponse)
        with pytest.raises(expected_exception=ServerError, match=TEMP_ERROR_TEXT):
            deploy_model_data.get_datacenters()

    def test_invalid_token(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockAuthenticationErrorResponse)
        with pytest.raises(expected_exception=AuthenticationError, match=AUTHENTICATION_MESSAGE):
            deploy_model_data.get_datacenters()

    def test_success(self, deploy_model_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 200

            @staticmethod
            def json():
                return {'message': 'success', "success": True, 'data': [
                    {"_id": "id_1", "logoUrl": "", "name": "datacenter_1",
                     "chartJson": {"namespacePodLevel": "", "clusterLevel": "", "nodeLevel": ""}},
                    {"_id": "id_2", "logoUrl": "", "name": "datacenter_2",
                     "chartJson": {"namespacePodLevel": "", "clusterLevel": "", "nodeLevel": ""}},
                ]}

        monkeypatch.setattr(requests, 'get', MockResponse)
        assert deploy_model_data.get_datacenters() == [{'_id': 'id_1', 'name': 'datacenter_1'},
                                                       {'_id': 'id_2', 'name': 'datacenter_2'}]


class TestGetImageNames:
    def test_random_error(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockServerErrorResponse)
        with pytest.raises(expected_exception=ServerError, match=TEMP_ERROR_TEXT):
            deploy_model_data.get_model_pipelines()

    def test_invalid_token(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(requests, 'get', MockAuthenticationErrorResponse)
        with pytest.raises(expected_exception=AuthenticationError, match=AUTHENTICATION_MESSAGE):
            deploy_model_data.get_model_pipelines()

    def test_success(self, deploy_model_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 200

            @staticmethod
            def json():
                return {'success': True, 'data': [
                    {'_id': 'id_1', 'imageName': 'image_name_1', 'createdAt': '', 'organisationId': ''},
                    {'_id': 'id_2', 'imageName': 'image_name_2', 'createdAt': '', 'organisationId': ''}
                ]}

        monkeypatch.setattr(requests, 'get', MockResponse)
        assert deploy_model_data.get_model_pipelines() == [{'_id': 'id_1', 'imageName': 'image_name_1'},
                                                           {'_id': 'id_2', 'imageName': 'image_name_2'}]


class TestDeployModelInit:
    def test_empty_base_url(self):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='base_url cannot empty'):
            DeployModel(base_url='', token='Bearer temp-token')

    def test_int_base_url(self):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='base_url can only be of type String'):
            DeployModel(base_url=1, token='Bearer temp-token')

    def test_empty_token(self, deploy_model_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='token cannot empty'):
            DeployModel(base_url='temp_base_url', token='')

    def test_int_token(self):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='token can only be of type String'):
            DeployModel(base_url='temp_base_url', token=1)

    def test_without_bearer_token(self):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='Please pass a valid Bearer token'):
            DeployModel(base_url='temp_base_url', token='temp_token')


class TestModelDeployment:
    @staticmethod
    def mock_get_model_pipelines(self):
        return [{'_id': 1, 'imageName': 'image_name_1'}, {'_id': 2, 'imageName': 'image_name_2'}]

    def test_empty_deployment_name(self, deploy_model_data):
        with pytest.raises(expected_exception=ValueError, match='ai_api_type cannot empty'):
            deploy_model_data.deploy_model(deployment_name='', namespace_id='', platform_id='', model_pipeline='')

    def test_int_deployment_name(self, deploy_model_data):
        with pytest.raises(expected_exception=ValueError, match='ai_api_type can only be of type String'):
            deploy_model_data.deploy_model(deployment_name=1, namespace_id='', platform_id='', model_pipeline='')

    def test_empty_namespace_id(self, deploy_model_data):
        with pytest.raises(expected_exception=ValueError, match='namespace_id cannot empty'):
            deploy_model_data.deploy_model(deployment_name='deployment_name_1', namespace_id='', platform_id='',
                                           model_pipeline='')

    def test_int_namespace_id(self, deploy_model_data):
        with pytest.raises(expected_exception=ValueError, match='namespace_id can only be of type String'):
            deploy_model_data.deploy_model(
                deployment_name='deployment_name_1', namespace_id=1, platform_id='', model_pipeline=''
            )

    def test_empty_platform_id(self, deploy_model_data):
        with pytest.raises(expected_exception=ValueError, match='platform_id cannot empty'):
            deploy_model_data.deploy_model(
                deployment_name='deployment_name_1', namespace_id='namespace_id_2', platform_id='', model_pipeline=''
            )

    def test_int_platform_id(self, deploy_model_data):
        with pytest.raises(expected_exception=ValueError, match='platform_id can only be of type String'):
            deploy_model_data.deploy_model(
                deployment_name='deployment_name_1', namespace_id='namespace_id_1', platform_id=1, model_pipeline=''
            )

    def test_empty_image_name(self, deploy_model_data):
        with pytest.raises(expected_exception=ValueError, match='image_name cannot empty'):
            deploy_model_data.deploy_model(
                deployment_name='deployment_name_1', namespace_id='namespace_id_1', platform_id='platform_id_1',
                model_pipeline=''
            )

    def test_int_image_name(self, deploy_model_data):
        with pytest.raises(expected_exception=ValueError, match='image_name can only be of type String'):
            deploy_model_data.deploy_model(
                deployment_name='deployment_name_1', namespace_id='namespace_id_1', platform_id='platform_id_1',
                model_pipeline=1
            )

    def test_nonexistent_image_name(self, deploy_model_data, monkeypatch):
        def mock_get_model_pipelines(param_1):
            return [{'_id': 2, 'imageName': 'image_name_2'}, {'_id': 3, 'imageName': 'image_name_3'}]

        monkeypatch.setattr(DeployModel, 'get_model_pipelines', mock_get_model_pipelines)
        with pytest.raises(expected_exception=ValueError, match='Image Name: image_name_1 not found in the database'):
            deploy_model_data.deploy_model(
                deployment_name='deployment_name_1', namespace_id='namespace_id_1', platform_id='platform_id_1',
                model_pipeline='image_name_1'
            )

    def test_invalid_token(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(DeployModel, 'get_model_pipelines', self.mock_get_model_pipelines)
        monkeypatch.setattr(requests, 'post', MockAuthenticationErrorResponse)

        with pytest.raises(expected_exception=AuthenticationError, match=AUTHENTICATION_MESSAGE):
            deploy_model_data.deploy_model(
                deployment_name='deployment_name_1', namespace_id='namespace_id_1', platform_id='platform_id_1',
                model_pipeline='image_name_1'
            )

    def test_random_error(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(DeployModel, 'get_model_pipelines', self.mock_get_model_pipelines)
        monkeypatch.setattr(requests, 'post', MockServerErrorResponse)

        with pytest.raises(expected_exception=ServerError, match=TEMP_ERROR_TEXT):
            deploy_model_data.deploy_model(
                deployment_name='deployment_name_1', namespace_id='namespace_id_1', platform_id='platform_id_1',
                model_pipeline='image_name_1'
            )

    def test_deployment_error(self, deploy_model_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 201

            @staticmethod
            def json():
                return {
                    "success": False,
                    "message": "Not able to deploy the model",
                    "deployment": {
                        "deploymentName": "deployment_name_1", "imageName": "image_name_1", "kioskId": None, "__v": 0,
                        "endPoint": "someendpoint.com", "platform": "platform_id_1", "deploymentStatus": "deploying",
                        "addedBy": "", "organisationId": "", "namespaceId": "namespace_id_1", "users": [],
                        "nodePreference": "NO PREFERENCE", "_id": "temp_id", "createdAt": "", "updatedAt": ""
                    }
                }

        monkeypatch.setattr(DeployModel, 'get_model_pipelines', self.mock_get_model_pipelines)
        monkeypatch.setattr(requests, 'post', MockResponse)
        with pytest.raises(expected_exception=ModelDeploymentError, match='Not able to deploy the model'):
            deploy_model_data.deploy_model(
                deployment_name='deployment_name_1', namespace_id='namespace_id_1', platform_id='platform_id_1',
                model_pipeline='image_name_1'
            )

    def test_success(self, deploy_model_data, monkeypatch, capsys):
        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 201

            @staticmethod
            def json():
                return {
                    "success": True,
                    "message": "Deployment Created",
                    "deployment": {
                        "deploymentName": "deployment_name_1", "imageName": "image_name_1", "kioskId": None, "__v": 0,
                        "endPoint": "someendpoint.com", "platform": "platform_id_1", "deploymentStatus": "deploying",
                        "addedBy": "", "organisationId": "", "namespaceId": "namespace_id_1", "users": [],
                        "nodePreference": "NO PREFERENCE", "_id": "temp_id", "createdAt": "", "updatedAt": ""
                    }
                }

        monkeypatch.setattr(DeployModel, 'get_model_pipelines', self.mock_get_model_pipelines)
        monkeypatch.setattr(requests, 'post', MockResponse)

        assert deploy_model_data.deploy_model(
            deployment_name='deployment_name_1', namespace_id='namespace_id_1', platform_id='platform_id_1',
            model_pipeline='image_name_1'
        ) == True

        captured = capsys.readouterr()
        assert captured.out == "\nDeployment Created: someendpoint.com\n"


class TestValidateFolderFormat(UploadModelUtils):
    def test_empty_model_folder_path(self, deploy_model_data):
        with pytest.raises(expected_exception=ValueError, match='Model folder path is empty'):
            deploy_model_data.upload_model(
                model_folder_path='', username='temp_username', storage_secret_key='some_secret_key'
            )

    def test_does_not_exist(self, deploy_model_data, monkeypatch):
        def mock_exists(temp):
            return False

        temp_model_folder_path = r'temp_model_folder_path'
        monkeypatch.setattr(pathlib.Path, 'exists', mock_exists)
        with pytest.raises(
                expected_exception=FileNotFoundError,
                match=f"{pathlib.Path(temp_model_folder_path)} does not exist"
        ):
            deploy_model_data.upload_model(
                model_folder_path=temp_model_folder_path, username='temp_username', storage_secret_key='some_secret_key'
            )

    def test_not_a_directory(self, deploy_model_data, monkeypatch):
        def mock_is_dir(temp):
            return False

        temp_model_folder_path = r'temp_model_folder_path'
        monkeypatch.setattr(pathlib.Path, 'exists', self.mock_exists)
        monkeypatch.setattr(pathlib.Path, 'is_dir', mock_is_dir)
        with pytest.raises(
                expected_exception=NotADirectoryError,
                match=f"{pathlib.Path(temp_model_folder_path)} is not a folder"
        ):
            deploy_model_data.upload_model(
                model_folder_path=temp_model_folder_path, username='temp_username', storage_secret_key='some_secret_key'
            )

    def test_no_write_access(self, deploy_model_data, monkeypatch):
        def mock_os_access(path, mode=os.W_OK):
            return False

        temp_model_folder_path = r'temp_model_folder_path'
        monkeypatch.setattr(pathlib.Path, 'exists', self.mock_exists)
        monkeypatch.setattr(pathlib.Path, 'is_dir', self.mock_is_dir)
        monkeypatch.setattr(os, 'access', mock_os_access)

        with pytest.raises(
                expected_exception=PermissionError,
                match=f"Folder doesn't have write permission: {temp_model_folder_path}"
        ):
            deploy_model_data.upload_model(
                model_folder_path=temp_model_folder_path, username='temp_username', storage_secret_key='some_secret_key'
            )

    def test_invalid_bentoml_format(self, deploy_model_data, monkeypatch):
        temp_model_folder_path = r'temp_model_folder_path'

        monkeypatch.setattr(pathlib.Path, 'exists', self.mock_exists)
        monkeypatch.setattr(pathlib.Path, 'is_dir', self.mock_is_dir)
        monkeypatch.setattr(os, 'access', self.mock_os_access)

        with pytest.raises(
                expected_exception=InvalidModelFolder,
                match=f"Invalid BentoML folder format: {temp_model_folder_path}"
        ):
            deploy_model_data.upload_model(
                model_folder_path=temp_model_folder_path, username='temp_username', storage_secret_key='some_secret_key'
            )

    def test_success_bentoml_format(self, deploy_model_data, monkeypatch, tmp_path):
        temp_model_folder_path = 'temp_model_folder_path'
        temp_dir = tmp_path / temp_model_folder_path
        temp_dir.mkdir()
        p = temp_dir / "Dockerfile"
        p.write_text("temp_content")

        monkeypatch.setattr(pathlib.Path, 'exists', self.mock_exists)
        monkeypatch.setattr(pathlib.Path, 'is_dir', self.mock_is_dir)
        monkeypatch.setattr(os, 'access', self.mock_os_access)
        monkeypatch.setattr(os, 'remove', self.mock_os_remove)
        monkeypatch.setattr(DeployModel, '_DeployModel__prepare_model_zip', self.mock_prepare_model_zip)

        with pytest.raises(expected_exception=ValueError, match="Secret key must not be empty"):
            deploy_model_data.upload_model(
                model_folder_path=temp_dir.as_posix(), username='temp_username', storage_secret_key=''
            )


class TestZipCreation(UploadModelUtils):
    def test_success_model_zip(self, deploy_model_data, monkeypatch, tmp_path):
        temp_dir = tmp_path / MODEL_FOLDER_PATH
        temp_dir.mkdir()
        p = temp_dir / "Dockerfile"
        p.write_text("temp_content")

        monkeypatch.setattr(pathlib.Path, 'is_dir', self.mock_is_dir)
        monkeypatch.setattr(os, 'access', self.mock_os_access)
        monkeypatch.setattr(os, 'remove', self.mock_os_remove)

        assert deploy_model_data._DeployModel__prepare_model_zip(temp_dir) == tmp_path.joinpath(
            MODEL_FOLDER_PATH + '.zip')


class TestUploadModel:
    def test_empty_username(self, deploy_model_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='username cannot empty'):
            deploy_model_data.upload_model(
                model_folder_path='temp_model_folder_path', username='', storage_secret_key='some_secret_key'
            )

    def test_int_username(self, deploy_model_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match='username can only be of type String'):
            deploy_model_data.upload_model(
                model_folder_path='temp_model_folder_path', username=1, storage_secret_key='some_secret_key'
            )


class TestRegisterImageName(UploadModelUtils):

    def test_invalid_token(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(DeployModel, '_DeployModel__validate_folder_format', self.mock_validate_folder_format)
        monkeypatch.setattr(DeployModel, '_DeployModel__prepare_model_zip', self.mock_prepare_model_zip)
        monkeypatch.setattr(DeployModel, '_DeployModel__upload_file', self.mock_upload_file)

        monkeypatch.setattr(requests, 'post', MockAuthenticationErrorResponse)
        with pytest.raises(expected_exception=AuthenticationError, match=AUTHENTICATION_MESSAGE):
            deploy_model_data.upload_model(
                model_folder_path=MODEL_FOLDER_PATH, username=USERNAME, storage_secret_key=SECRET_KEY
            )

    def test_random_error(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(DeployModel, '_DeployModel__validate_folder_format', self.mock_validate_folder_format)
        monkeypatch.setattr(DeployModel, '_DeployModel__prepare_model_zip', self.mock_prepare_model_zip)
        monkeypatch.setattr(DeployModel, '_DeployModel__upload_file', self.mock_upload_file)

        monkeypatch.setattr(requests, 'post', MockServerErrorResponse)

        with pytest.raises(expected_exception=ServerError, match=TEMP_ERROR_TEXT):
            deploy_model_data.upload_model(
                model_folder_path=MODEL_FOLDER_PATH, username=USERNAME, storage_secret_key=SECRET_KEY
            )

    def test_register_error(self, deploy_model_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 201

            @staticmethod
            def json():
                return {
                    "success": False,
                    "message": "Not able to register the image name",
                    "aiModel": {
                        "imageName": "", "addedBy": "", "organisationId": "", "_id": "", "createdAt": "",
                        "updatedAt": ""
                    }
                }

        monkeypatch.setattr(DeployModel, '_DeployModel__validate_folder_format', self.mock_validate_folder_format)
        monkeypatch.setattr(DeployModel, '_DeployModel__prepare_model_zip', self.mock_prepare_model_zip)
        monkeypatch.setattr(DeployModel, '_DeployModel__upload_file', self.mock_upload_file)
        monkeypatch.setattr(requests, 'post', MockResponse)

        with pytest.raises(expected_exception=FileUploadError, match='Not able to register the image name'):
            deploy_model_data.upload_model(
                model_folder_path=MODEL_FOLDER_PATH, username=USERNAME, storage_secret_key=SECRET_KEY
            )

    def test_success(self, deploy_model_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 201
                self.text = TEMP_ERROR_TEXT

            @staticmethod
            def json():
                return {
                    "success": True,
                    "message": "Ai-Model Created",
                    "aiModel": {
                        "imageName": "", "addedBy": "", "organisationId": "", "_id": "", "createdAt": "",
                        "updatedAt": ""
                    }
                }

        monkeypatch.setattr(DeployModel, '_DeployModel__validate_folder_format', self.mock_validate_folder_format)
        monkeypatch.setattr(DeployModel, '_DeployModel__prepare_model_zip', self.mock_prepare_model_zip)
        monkeypatch.setattr(DeployModel, '_DeployModel__upload_file', self.mock_upload_file)
        monkeypatch.setattr(requests, 'post', MockResponse)

        with pytest.raises(expected_exception=ServerError, match=TEMP_ERROR_TEXT):
            deploy_model_data.upload_model(
                model_folder_path=MODEL_FOLDER_PATH, username=USERNAME, storage_secret_key=SECRET_KEY
            )


class TestCrossCloudServiceCall(TestRegisterImageName):
    def test_invalid_token(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(DeployModel, '_DeployModel__register_image_name', self.mock_register_image_name)
        super().test_invalid_token(deploy_model_data=deploy_model_data, monkeypatch=monkeypatch)

    def test_random_error(self, deploy_model_data, monkeypatch):
        monkeypatch.setattr(DeployModel, '_DeployModel__register_image_name', self.mock_register_image_name)
        super().test_random_error(deploy_model_data=deploy_model_data, monkeypatch=monkeypatch)

    def test_cross_cloud_service_error(self, deploy_model_data, monkeypatch):
        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 200

            @staticmethod
            def json():
                return {
                    "success": False,
                    "job": "unable to call cross cloud service",
                    "aiModel": {
                        "imageName": "", "addedBy": "", "organisationId": "", "_id": "", "createdAt": "",
                        "updatedAt": ""
                    }
                }

        monkeypatch.setattr(DeployModel, '_DeployModel__validate_folder_format', self.mock_validate_folder_format)
        monkeypatch.setattr(DeployModel, '_DeployModel__prepare_model_zip', self.mock_prepare_model_zip)
        monkeypatch.setattr(DeployModel, '_DeployModel__upload_file', self.mock_upload_file)
        monkeypatch.setattr(DeployModel, '_DeployModel__register_image_name', self.mock_register_image_name)
        monkeypatch.setattr(requests, 'post', MockResponse)

        with pytest.raises(expected_exception=FileUploadError, match='unable to call cross cloud service'):
            deploy_model_data.upload_model(
                model_folder_path=MODEL_FOLDER_PATH, username=USERNAME, storage_secret_key=SECRET_KEY
            )

    def test_success_upload_model(self, deploy_model_data, monkeypatch, capsys, tmp_path):
        class MockResponse:
            def __init__(self, url, headers, data):
                self.status_code = 200

            @staticmethod
            def json():
                return {
                    "success": True,
                    "job": "job submitted",
                    "aiModel": {
                        "imageName": "", "addedBy": "", "organisationId": "", "_id": "", "createdAt": "",
                        "updatedAt": ""
                    }
                }

        monkeypatch.setattr(DeployModel, '_DeployModel__validate_folder_format', self.mock_validate_folder_format)
        monkeypatch.setattr(DeployModel, '_DeployModel__prepare_model_zip', self.mock_prepare_model_zip)
        monkeypatch.setattr(DeployModel, '_DeployModel__upload_file', self.mock_upload_file)
        monkeypatch.setattr(DeployModel, '_DeployModel__register_image_name', self.mock_register_image_name)
        monkeypatch.setattr(requests, 'post', MockResponse)

        temp_dir = tmp_path / "Resnet" / MODEL_FOLDER_PATH

        assert deploy_model_data.upload_model(
            model_folder_path=temp_dir.as_posix(), username=USERNAME, storage_secret_key=SECRET_KEY
        ) == f"zeblok/{temp_dir.parent.name.lower()}:{MODEL_FOLDER_PATH}"

        captured = capsys.readouterr()
        assert captured.out == f'\nSuccessfully uploaded the Model folder | Filename: {MODEL_FOLDER_PATH}.zip, Image Name: zeblok/{temp_dir.parent.name.lower()}:{MODEL_FOLDER_PATH}\n'


def test_upload_file(deploy_model_data, monkeypatch):
    import minio
    temp_url = 'temp_url'

    def mock_os_remove(path):
        return

    class MockResponse:
        def __init__(self, endpoint='', access_key=USERNAME, secret_key=SECRET_KEY, secure=False):
            self.secret_key = secret_key

        def fput_object(self, bucket_name, object_name, file_path, content_type, progress, part_size):
            return

        def presigned_get_object(self, bucket_name, object_name, expires):
            return temp_url

    monkeypatch.setattr(os, 'remove', mock_os_remove)
    monkeypatch.setattr(minio, 'Minio', MockResponse)
    assert deploy_model_data._DeployModel__upload_file(file_name=pathlib.Path(MODEL_FOLDER_PATH), username=USERNAME,
                                                       secret_key=SECRET_KEY) == temp_url
