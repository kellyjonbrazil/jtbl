import unittest
import textwrap
import jtbl.cli


class MyTests(unittest.TestCase):

    def setUp(self):
        self.SUCCESS, self.ERROR = True, False
        self.columns = 80

    def test_no_piped_data(self):
        stdin = None
        expected = textwrap.dedent('''\
        jtbl:   Missing piped data
        ''')

        self.assertEqual(jtbl.cli.get_json(stdin, columns=self.columns), (self.ERROR, expected))

    def test_null_data(self):
        stdin = ''
        expected = textwrap.dedent('''\
        jtbl:   Missing piped data
        ''')

        self.assertEqual(jtbl.cli.get_json(stdin, columns=self.columns), (self.ERROR, expected))

    def test_hello_string(self):
        stdin = 'hello'
        expected = textwrap.dedent('''\
        jtbl:  Exception - Expecting value: line 1 column 1 (char 0)
               Cannot parse line 1 (Not JSON or JSON Lines data):
               hello
        ''')

        self.assertEqual(jtbl.cli.get_json(stdin, columns=self.columns), (self.ERROR, expected))

    def test_array_input(self):
        stdin = '["value1", "value2", "value3"]'
        expected = ["value1", "value2", "value3"]

        self.assertEqual(jtbl.cli.get_json(stdin, columns=self.columns), (self.SUCCESS, expected))

    def test_deep_nest(self):
        stdin = '{"this":{"is":{"a":{"deeply":{"nested":{"structure":"value1","item2":"value2"}}}}}}'
        expected = [{"this":{"is":{"a":{"deeply":{"nested":{"structure":"value1","item2":"value2"}}}}}}]

        self.assertEqual(jtbl.cli.get_json(stdin, columns=self.columns), (self.SUCCESS, expected))

    def test_jc_dig(self):
        stdin = '[{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]'
        expected = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        self.assertEqual(jtbl.cli.get_json(stdin, columns=self.columns), (self.SUCCESS, expected))

    def test_json_lines(self):
        """test JSON Lines data"""
        stdin = textwrap.dedent('''\
        {"name":"lo0","type":null,"ipv4_addr":"127.0.0.1","ipv4_mask":"255.0.0.0"}
        {"name":"gif0","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"stf0","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"XHC0","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"XHC20","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"VHC128","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"XHC1","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"en5","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"ap1","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"en0","type":null,"ipv4_addr":"192.168.1.221","ipv4_mask":"255.255.255.0"}
        {"name":"p2p0","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"awdl0","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"en1","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"en2","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"en3","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"en4","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"bridge0","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"utun0","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"utun1","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"utun2","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"utun3","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"utun4","type":null,"ipv4_addr":null,"ipv4_mask":null}
        {"name":"vmnet1","type":null,"ipv4_addr":"192.168.101.1","ipv4_mask":"255.255.255.0"}
        {"name":"vmnet8","type":null,"ipv4_addr":"192.168.71.1","ipv4_mask":"255.255.255.0"}''')
        expected = [
            {"name":"lo0","type":None,"ipv4_addr":"127.0.0.1","ipv4_mask":"255.0.0.0"},
            {"name":"gif0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"stf0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"XHC0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"XHC20","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"VHC128","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"XHC1","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en5","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"ap1","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en0","type":None,"ipv4_addr":"192.168.1.221","ipv4_mask":"255.255.255.0"},
            {"name":"p2p0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"awdl0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en1","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en2","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en3","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"en4","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"bridge0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun0","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun1","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun2","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun3","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"utun4","type":None,"ipv4_addr":None,"ipv4_mask":None},
            {"name":"vmnet1","type":None,"ipv4_addr":"192.168.101.1","ipv4_mask":"255.255.255.0"},
            {"name":"vmnet8","type":None,"ipv4_addr":"192.168.71.1","ipv4_mask":"255.255.255.0"}
        ]

        self.assertEqual(jtbl.cli.get_json(stdin, columns=self.columns), (self.SUCCESS, expected))


if __name__ == '__main__':
    unittest.main()
