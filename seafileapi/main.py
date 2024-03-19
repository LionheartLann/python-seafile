import json
import requests
import os

from seafileapi.exceptions import ClientHttpError
from seafileapi.utils import urljoin


def parse_headers(token):
    return {
        'Authorization': 'Token ' + token,
        'Content-Type': 'application/json',
    }

def parse_response(response):
    if response.status_code >= 400:
        raise ConnectionError(response.status_code, response.text)
    else:
        try:
            data = json.loads(response.text)
            return data
        except:
            pass


class Repo(object):


    def __init__(self, token, server_url):

        self.server_url = server_url
        self.token = token
        self.repo_id = None
        self.timeout = 30
        self.headers = None

        self._by_api_token = True


    def auth(self, by_api_token=True):
        if not by_api_token:
            self._by_api_token = False
        self.headers = parse_headers(self.token)

    def _repo_info_url(self):
        if self._by_api_token:
            return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/via-repo-token/repo-info/')

        return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/repos/%s/' % self.repo_id)

    def _repo_dir_url(self):
        if self._by_api_token:
            return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/via-repo-token/dir/')

        return "%s/%s" % (self.server_url.rstrip('/'), 'api/v2.1/repos/%s/dir/' % self.repo_id)


    def get_repo_details(self):
        url = self._repo_info_url()
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        repo = parse_response(response)
        return {
            'repo_id': repo.get('repo_id'),
            'repo_name': repo.get('repo_name'),
            'size': repo.get('size'),
            'file_count': repo.get('file_count'),
            'last_modified': repo.get('last_modified'),
        }

    def list_dir(self, dir_path='/'):
        url = self._repo_dir_url()
        params = {
            'p': dir_path,
            'path': dir_path
        }
        response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
        resp = parse_response(response)
        return resp['dirent_list']


    def create_dir(self):
        pass

    def rename_dir(self):
        pass


    def delete_dir(self):
        pass


    def get_file(self):
        pass


    def create_file(self):
        pass



    def rename_file(self):
        pass


    def delete_file(self):
        pass



class SeafileAPI(object):

    def __init__(self, login_name, password, server_url):
        self.login_name = login_name
        self.username = None
        self.password = password
        self.server_url = server_url.strip().strip('/')
        self.token = None
        self.timeout = 30

        self.headers = None

    def auth(self):
        data = {
            'username': self.login_name,
            'password': self.password,
        }
        url = "%s/%s" % (self.server_url.rstrip('/'), 'api2/auth-token/')
        res = requests.post(url, data=data)
        if res.status_code != 200:
            raise ClientHttpError(res.status_code, res.content)
        token = res.json()['token']
        assert len(token) == 40, 'The length of seahub api auth token should be 40'
        self.token = token
        self.headers = parse_headers(token)

    def _repo_obj(self, repo_id):
        repo = Repo(self.token, self.server_url)
        repo.repo_id = repo_id
        repo.auth(by_api_token=False)

        return repo

    def list_repos(self):
        url = urljoin(self.server_url, 'api2/repos')
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        return parse_response(response)

    def get_repo(self, repo_id):
        url = urljoin(self.server_url, 'api2/repos/%s' % repo_id)
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        data = parse_response(response)
        repo_id = data.get('id')
        return self._repo_obj(repo_id)

    def create_repo(self, repo_name):
        pass

    def delete_repo(self, repo_id):
        pass