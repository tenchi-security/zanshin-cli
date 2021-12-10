import unittest, json
from io import StringIO
from unittest.mock import patch

from zanshinsdk import Client
from zanshincli.main import OutputFormat, output_iterable, global_options

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        global_options['profile'] = 'default'

    def test_output_json(self):
        global_options['format'] = OutputFormat.JSON
        with patch('sys.stdout', new=StringIO()) as self.output:
            input = json.loads("""{"userId": "db33c4a0-cfb9-4f62-b014-9244ee49d", "name": "Zanshin", "email": "yo@tenchisecurity.com", "roles": ["ADMIN"], "identityProvider": "auth0", "lastIp": "4.3.2.1", "lastLogin": "2021-08-13T20:12:15.329Z", "loginsCount": 37, "picture": "meh.png", "createdAt": "2021-08-11T15:24:18.007Z", "updatedAt": "2021-08-11T15:24:18.007Z"}""")
            output_iterable([input])
            self.assertEqual("""{
    "userId": "db33c4a0-cfb9-4f62-b014-9244ee49d",
    "name": "Zanshin",
    "email": "yo@tenchisecurity.com",
    "roles": [
        "ADMIN"
    ],
    "identityProvider": "auth0",
    "lastIp": "4.3.2.1",
    "lastLogin": "2021-08-13T20:12:15.329Z",
    "loginsCount": 37,
    "picture": "meh.png",
    "createdAt": "2021-08-11T15:24:18.007Z",
    "updatedAt": "2021-08-11T15:24:18.007Z"
}""",  self.output.getvalue().strip())


    def test_output_table(self):
        global_options['format'] = OutputFormat.TABLE
        with patch('sys.stdout', new=StringIO()) as self.output:
            input = json.loads("""{"userId": "db33c4a0-cfb9-4f62-b014-9244ee49d", "name": "Zanshin", "email": "yo@tenchisecurity.com", "roles": ["ADMIN"], "identityProvider": "auth0", "lastIp": "4.3.2.1", "lastLogin": "2021-08-13T20:12:15.329Z", "loginsCount": 37, "picture": "meh.png", "createdAt": "2021-08-11T15:24:18.007Z", "updatedAt": "2021-08-11T15:24:18.007Z"}""")
            output_iterable([input])
            self.maxDiff = None
            self.assertEqual(
"""+--------------------------+-----------------------+------------------+---------+--------------------------+-------------+---------+---------+-------+--------------------------+-----------------------------------+
|        createdAt         |         email         | identityProvider |  lastIp |        lastLogin         | loginsCount |   name  | picture | roles |        updatedAt         |               userId              |
+--------------------------+-----------------------+------------------+---------+--------------------------+-------------+---------+---------+-------+--------------------------+-----------------------------------+
| 2021-08-11T15:24:18.007Z | yo@tenchisecurity.com |      auth0       | 4.3.2.1 | 2021-08-13T20:12:15.329Z |      37     | Zanshin | meh.png | ADMIN | 2021-08-11T15:24:18.007Z | db33c4a0-cfb9-4f62-b014-9244ee49d |
+--------------------------+-----------------------+------------------+---------+--------------------------+-------------+---------+---------+-------+--------------------------+-----------------------------------+""", 
self.output.getvalue().strip())
        
    def test_output_table(self):
        global_options['format'] = OutputFormat.CSV
        with patch('sys.stdout', new=StringIO()) as self.output:
            input = json.loads("""{"userId": "db33c4a0-cfb9-4f62-b014-9244ee49d", "name": "Zanshin", "email": "yo@tenchisecurity.com", "roles": ["ADMIN"], "identityProvider": "auth0", "lastIp": "4.3.2.1", "lastLogin": "2021-08-13T20:12:15.329Z", "loginsCount": 37, "picture": "meh.png", "createdAt": "2021-08-11T15:24:18.007Z", "updatedAt": "2021-08-11T15:24:18.007Z"}""")
            output_iterable([input])
            self.maxDiff = None
            self.assertEqual("createdAt,email,identityProvider,lastIp,lastLogin,loginsCount,name,picture,roles,updatedAt,userId\r\n2021-08-11T15:24:18.007Z,yo@tenchisecurity.com,auth0,4.3.2.1,2021-08-13T20:12:15.329Z,37,Zanshin,meh.png,ADMIN,2021-08-11T15:24:18.007Z,db33c4a0-cfb9-4f62-b014-9244ee49d", 
self.output.getvalue().strip())

if __name__ == '__main__':
    unittest.main()
