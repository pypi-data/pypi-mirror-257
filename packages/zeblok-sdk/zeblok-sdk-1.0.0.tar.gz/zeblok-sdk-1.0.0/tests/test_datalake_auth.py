import pytest
import minio
from zeblok.auth import DatalakeAuth
from zeblok.utils.error_message import INVALID_DATALAKE_USERNAME_TYPE, EMPTY_DATALAKE_USERNAME, \
    INVALID_DATALAKE_SECRET_KEY_TYPE, EMPTY_DATALAKE_SECRET_KEY, INVALID_BUCKET_NAME_TYPE, EMPTY_BUCKET_NAME
from zeblok.utils.errors import InvalidCredentialsError, InvalidBucketName


@pytest.fixture()
def valid_datalake_auth_data():
    return {
        'datalake_username': 'temp_datalake_username',
        'datalake_secret_key': 'temp_datalake_secret_key',
        'datalake_url': 'datalake.intel.zeblok.com:9000',
        'bucket_name': 'temp-bucket'
    }


class TestDatalakeAuthInstanceCreationDatalakeUsername:
    def test_invalid_int_datalake_username(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_DATALAKE_USERNAME_TYPE):
            valid_datalake_auth_data.pop('datalake_username')
            DatalakeAuth(datalake_username=1, **valid_datalake_auth_data)

    def test_invalid_float_datalake_username(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_DATALAKE_USERNAME_TYPE):
            valid_datalake_auth_data.pop('datalake_username')
            DatalakeAuth(datalake_username=1.2, **valid_datalake_auth_data)

    def test_invalid_list_datalake_username(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_DATALAKE_USERNAME_TYPE):
            valid_datalake_auth_data.pop('datalake_username')
            DatalakeAuth(datalake_username=[1], **valid_datalake_auth_data)

    def test_invalid_empty_username(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match=EMPTY_DATALAKE_USERNAME):
            valid_datalake_auth_data.pop('datalake_username')
            DatalakeAuth(datalake_username='', **valid_datalake_auth_data)


class TestDatalakeAuthInstanceCreationDatalakeSecretKey:
    def test_invalid_int_datalake_secret_key(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_DATALAKE_SECRET_KEY_TYPE):
            valid_datalake_auth_data.pop('datalake_secret_key')
            DatalakeAuth(datalake_secret_key=1, **valid_datalake_auth_data)

    def test_invalid_float_datalake_secret_key(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_DATALAKE_SECRET_KEY_TYPE):
            valid_datalake_auth_data.pop('datalake_secret_key')
            DatalakeAuth(datalake_secret_key=1.2, **valid_datalake_auth_data)

    def test_invalid_list_datalake_secret_key(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_DATALAKE_SECRET_KEY_TYPE):
            valid_datalake_auth_data.pop('datalake_secret_key')
            DatalakeAuth(datalake_secret_key=[1], **valid_datalake_auth_data)

    def test_invalid_empty_datalake_secret_key(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match=EMPTY_DATALAKE_SECRET_KEY):
            valid_datalake_auth_data.pop('datalake_secret_key')
            DatalakeAuth(datalake_secret_key='', **valid_datalake_auth_data)


class TestDatalakeAuthInstanceCreationDatalakeBucket:
    def test_invalid_int_bucket_name(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_BUCKET_NAME_TYPE):
            valid_datalake_auth_data.pop('bucket_name')
            DatalakeAuth(bucket_name=1, **valid_datalake_auth_data)

    def test_invalid_float_bucket_name(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_BUCKET_NAME_TYPE):
            valid_datalake_auth_data.pop('bucket_name')
            DatalakeAuth(bucket_name=1.2, **valid_datalake_auth_data)

    def test_invalid_list_bucket_name(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_BUCKET_NAME_TYPE):
            valid_datalake_auth_data.pop('bucket_name')
            DatalakeAuth(bucket_name=[1], **valid_datalake_auth_data)

    def test_invalid_empty_bucket_name(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=InvalidBucketName, match=EMPTY_BUCKET_NAME):
            valid_datalake_auth_data.pop('bucket_name')
            DatalakeAuth(bucket_name='', **valid_datalake_auth_data)


class TestAPIAuthMemberFunctions:
    @staticmethod
    def mock_bucket_exists(self, bucket_name):
        return True

    def test_datalake_url(self, valid_datalake_auth_data, monkeypatch):
        monkeypatch.setattr(minio.api.Minio, 'bucket_exists', self.mock_bucket_exists)
        assert DatalakeAuth(**valid_datalake_auth_data).datalake_url == valid_datalake_auth_data['datalake_url']

    def test_datalake_username(self, valid_datalake_auth_data, monkeypatch):
        monkeypatch.setattr(minio.api.Minio, 'bucket_exists', self.mock_bucket_exists)
        assert DatalakeAuth(**valid_datalake_auth_data).datalake_username == valid_datalake_auth_data[
            'datalake_username']

    def test_datalake_secret_key(self, valid_datalake_auth_data, monkeypatch):
        monkeypatch.setattr(minio.api.Minio, 'bucket_exists', self.mock_bucket_exists)
        assert DatalakeAuth(**valid_datalake_auth_data).datalake_secret_key == valid_datalake_auth_data[
            'datalake_secret_key']


@pytest.mark.skip(reason="Implement it when url validation logic is fixed")
class TestDatalakeAuthInstanceCreationDatalakeUrl:
    def test_empty_app_url(self, valid_datalake_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_API_ACCESS_KEY_TYPE):
            valid_datalake_auth_data.pop('datalake_url')
            DatalakeAuth(datalake_url='', **valid_datalake_auth_data)
