import pytest
from zeblok.auth import APIAuth
from zeblok.utils.errors import InvalidCredentialsError
from zeblok.utils.error_message import INVALID_API_ACCESS_KEY_TYPE, EMPTY_API_ACCESS_KEY, \
    INVALID_API_ACCESS_SECRET_TYPE, EMPTY_API_ACCESS_SECRET


@pytest.fixture()
def valid_api_auth_data():
    return {
        'api_access_key': 'temp_api_access_key',
        'api_access_secret': 'temp_api_access_secret',
        'app_url': 'app.intel.zeblok.com'
    }


class TestAPIAuthInstanceCreationAPIAccessKey:
    def test_invalid_int_api_access_key(self, valid_api_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_API_ACCESS_KEY_TYPE):
            valid_api_auth_data.pop('api_access_key')
            APIAuth(api_access_key=1, **valid_api_auth_data)

    def test_invalid_float_api_access_key(self, valid_api_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_API_ACCESS_KEY_TYPE):
            valid_api_auth_data.pop('api_access_key')
            APIAuth(api_access_key=1.2, **valid_api_auth_data)

    def test_invalid_list_api_access_key(self, valid_api_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_API_ACCESS_KEY_TYPE):
            valid_api_auth_data.pop('api_access_key')
            APIAuth(api_access_key=[1], **valid_api_auth_data)

    def test_invalid_empty_username(self, valid_api_auth_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match=EMPTY_API_ACCESS_KEY):
            valid_api_auth_data.pop('api_access_key')
            APIAuth(api_access_key='', **valid_api_auth_data)


class TestAPIAuthInstanceCreationAPIAccessSecret:
    def test_invalid_int_api_access_secret(self, valid_api_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_API_ACCESS_SECRET_TYPE):
            valid_api_auth_data.pop('api_access_secret')
            APIAuth(api_access_secret=1, **valid_api_auth_data)

    def test_invalid_float_api_access_secret(self, valid_api_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_API_ACCESS_SECRET_TYPE):
            valid_api_auth_data.pop('api_access_secret')
            APIAuth(api_access_secret=1.2, **valid_api_auth_data)

    def test_invalid_list_api_access_secret(self, valid_api_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_API_ACCESS_SECRET_TYPE):
            valid_api_auth_data.pop('api_access_secret')
            APIAuth(api_access_secret=[1], **valid_api_auth_data)

    def test_invalid_empty_api_access_secret(self, valid_api_auth_data):
        with pytest.raises(expected_exception=InvalidCredentialsError, match=EMPTY_API_ACCESS_SECRET):
            valid_api_auth_data.pop('api_access_secret')
            APIAuth(api_access_secret='', **valid_api_auth_data)


class TestAPIAuthMemberFunctions:
    def test_app_url(self, valid_api_auth_data):
        assert APIAuth(**valid_api_auth_data).app_url == valid_api_auth_data['app_url']

    def test_api_access_key(self, valid_api_auth_data):
        assert APIAuth(**valid_api_auth_data).api_access_key == valid_api_auth_data['api_access_key']

    def test_api_access_secret(self, valid_api_auth_data):
        assert APIAuth(**valid_api_auth_data).api_access_secret == valid_api_auth_data['api_access_secret']

    def test_get_api_creds(self, valid_api_auth_data):
        assert APIAuth(**valid_api_auth_data).get_api_creds() == (
            valid_api_auth_data['api_access_key'], valid_api_auth_data['api_access_secret'])


@pytest.mark.skip(reason="Implement it when url validation logic is fixed")
class TestAPIAuthInstanceCreationAppUrl:
    def test_empty_app_url(self, valid_api_auth_data):
        with pytest.raises(expected_exception=TypeError, match=INVALID_API_ACCESS_KEY_TYPE):
            valid_api_auth_data.pop('app_url')
            APIAuth(app_url='', **valid_api_auth_data)
