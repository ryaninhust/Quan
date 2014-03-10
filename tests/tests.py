import sys
sys.path.append('/home/vagrant/personal/new_simi')

from core.tests import AppTestCase
from core.tests import requests

import json

DOMAIN = 'http://vagrant.intra.douban.com:8000'


class TestLogin(AppTestCase):
    test_url = DOMAIN + '/login/'

    def test_post(self):
        json_content = {'cell_phone': 13667148901, 'password': 'hello user'}
        response = requests.post(self.test_url, data=json.dumps(json_content))
        self.assertEqual(response.status_code, 200)


class TestUsers(AppTestCase):
    test_url = DOMAIN + '/user/'

    def test_post(self):
        json_content = {'cell_phone': 13667148902, 'password': 'hello user'}
        response = requests.post(self.test_url, data=json.dumps(json_content))
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json().keys())
        self.assertIn('url', response.json().keys())

    def test_get(self):
        response = requests.get(self.test_url)
        self.assertEqual(response.status_code, 200)


class TestUser(AppTestCase):
    test_url = DOMAIN + '/user/1/'

    def test_get(self):
        response = requests.get(self.test_url)
        self.assertEqual(200, response.status_code)
        user_dict = response.json()
        self.assertEqual(user_dict['cell_phone'], '13667148900')

    def test_put(self):
        json_content = {'name': 'yuanbowen', 'email': 'yuanbowen@douban.com'}
        response = requests.put(self.test_url, data=json.dumps(json_content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'yuanbowen')
        self.assertEqual(response.json()['email'], 'yuanbowen@douban.com')


class TestCirlces(AppTestCase):
    test_url = DOMAIN + '/circle/'

    def test_post(self):
        headers = {'Authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff7a'}
        json_content = {'name': 'fucking girl', 'description': 'fucking girl'}
        response = requests.post(self.test_url, data=json.dumps(json_content),
                                 headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'fucking girl')


class TestCircle(AppTestCase):
    test_url = DOMAIN + '/circle/1/'

    def test_get(self):
        headers = {'Authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff7a'}
        response = requests.get(self.test_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        headers = {'Authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff71'}
        response = requests.get(self.test_url, headers=headers)
        self.assertEqual(response.status_code, 403)

    def test_put(self):
        headers = {'Authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff7a'}
        json_content = {'name': 'fuck man', 'description': 'fuck boy'}
        response = requests.put(
            self.test_url, headers=headers, data=json.dumps(json_content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'fuck man')
        self.assertEqual(response.json()['description'], 'fuck boy')


class TestCircleStatus(AppTestCase):
    test_url = DOMAIN + '/circle/1/status/'

    def test_get(self):
        headers = {'Authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff7a'}
        response = requests.get(self.test_url, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        headers = {'Authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff7a'}
        json_content = {'content': 'this is the first fuck'}
        response = requests.post(self.test_url, headers=headers,
                                 data=json.dumps(json_content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['content'], 'this is the first fuck')


class TestCircleMember(AppTestCase):
    test_url = DOMAIN + '/circle/1/member/'

    def test_get(self):
        headers = {'Authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff7a'}
        response = requests.get(self.test_url, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        headers = {'authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff7a'}
        json_content = {'member_id': 2}
        response = requests.post(self.test_url, headers=headers,
                                 data=json.dumps(json_content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['member_id'], 2)
        self.assertEqual(response.json()['status'], 1)


class TestCircleMemberDetail(AppTestCase):
    test_url = DOMAIN + '/circle/1/member/2/'

    def test_get(self):
        headers = {'authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff7a'}
        response = requests.get(self.test_url, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        headers = {'authorization': '930b5250fb9e23c32e8b9357d8334aa3e373ff7a'}
        json_content = {'status': 2}
        response = requests.put(self.test_url, headers=headers,
                                data=json.dumps(json_content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 2)


class TestStatusDiscussionList(AppTestCase):
    test_url = DOMAIN + '/status/1/discussion/'

    def test_get(self):
        response = requests.get(self.test_url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        json_content = {'user_id': 1, 'content': 'hehe'}
        response = requests.post(self.test_url, data=json.dumps(json_content))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['content'], 'hehe')
