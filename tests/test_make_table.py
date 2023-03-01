import unittest
import textwrap
import jtbl.cli


class MyTests(unittest.TestCase):

    def setUp(self):
        self.SUCCESS, self.ERROR = True, False
        self.columns = 80

    def test_simple_key_value(self):
        stdin = [{"key": "value"}]
        expected = textwrap.dedent('''\
        key
        -----
        value''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns), (self.SUCCESS, expected))

    def test_multi_key_value(self):
        stdin = [{"key1": "value1", "key2": "value1"}, {"key1": "value2", "key2": "value2"}]
        expected = textwrap.dedent('''\
        key1    key2
        ------  ------
        value1  value1
        value2  value2''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns), (self.SUCCESS, expected))

    def test_null_string(self):
        stdin = [None]
        self.assertRaises(AttributeError, jtbl.cli.make_table, data=stdin, columns=self.columns)

    def test_array_input(self):
        stdin = ["value1", "value2", "value3"]
        self.assertRaises(AttributeError, jtbl.cli.make_table, data=stdin, columns=self.columns)

    def test_deep_nest(self):
        stdin = [{"this":{"is":{"a":{"deeply":{"nested":{"structure":"value1","item2":"value2"}}}}}}]
        expected = textwrap.dedent('''\
        this
        ---------------------------------------------------------------------------------
        {'is': {'a': {'deeply': {'nested': {'structure': 'value1', 'item2': 'value2'}}}}}''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=100), (self.SUCCESS, expected))

    def test_jc_dig(self):
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
        ╒══════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╤════════╕
        │ id   │ opco   │ stat   │ flag   │   quer │   answ │   auth │   addi │ ques   │ answ   │   quer │   serv │ when   │   rcvd │
        │      │ de     │ us     │ s      │   y_nu │   er_n │   orit │   tion │ tion   │ er     │   y_ti │     er │        │        │
        │      │        │        │        │      m │     um │   y_nu │   al_n │        │        │     me │        │        │        │
        │      │        │        │        │        │        │      m │     um │        │        │        │        │        │        │
        ╞══════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╪════════╡
        │ 5565 │ QUER   │ NOER   │ ['qr   │      1 │      5 │      0 │      1 │ {'na   │ [{'n   │     44 │   2600 │ Wed    │    143 │
        │ 8    │ Y      │ ROR    │ ', '   │        │        │        │        │ me':   │ ame'   │        │        │ Mar    │        │
        │      │        │        │ rd',   │        │        │        │        │  'ww   │ : 'w   │        │        │ 18 1   │        │
        │      │        │        │  'ra   │        │        │        │        │ w.cn   │ ww.c   │        │        │ 2:20   │        │
        │      │        │        │ ']     │        │        │        │        │ n.co   │ nn.c   │        │        │ :59    │        │
        │      │        │        │        │        │        │        │        │ m.',   │ om.'   │        │        │ PDT    │        │
        │      │        │        │        │        │        │        │        │  'cl   │ , 'c   │        │        │ 2020   │        │
        │      │        │        │        │        │        │        │        │ ass'   │ lass   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ : 'I   │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ N',    │ IN',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ 'typ   │  'ty   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ e':    │ pe':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │ 'A'}   │  'CN   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ AME'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 't   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ tl':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  147   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 'd   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ata'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : 't   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ urne   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ r-tl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ s.ma   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ p.fa   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ stly   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .net   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .'},   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  {'n   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ame'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : 't   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ urne   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ r-tl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ s.ma   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ p.fa   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ stly   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .net   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .',    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'cla   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ss':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'IN   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ', '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ type   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ A',    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'ttl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': 5   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 'd   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ata'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : '1   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 51.1   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 01.1   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .67'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ }, {   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'nam   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ e':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'tur   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ner-   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ tls.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ map.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ fast   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ly.n   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ et.'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 'c   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ lass   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ IN',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'ty   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ pe':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'A'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , 't   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ tl':   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  5,    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'dat   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ a':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ '151   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .101   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ .65.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 67'}   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , {'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ name   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ turn   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ er-t   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ls.m   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ap.f   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ astl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ y.ne   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ t.',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'cl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ass'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : 'I   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ N',    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'typ   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ e':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'A',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'tt   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ l':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 5, '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ data   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 151.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 101.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 129.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 67'}   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ , {'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ name   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ turn   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ er-t   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ls.m   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ap.f   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ astl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ y.ne   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ t.',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'cl   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ass'   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ : 'I   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ N',    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'typ   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ e':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 'A',   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │  'tt   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ l':    │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 5, '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ data   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ': '   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 151.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 101.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 193.   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ 67'}   │        │        │        │        │
        │      │        │        │        │        │        │        │        │        │ ]      │        │        │        │        │
        ╘══════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╧════════╛''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=80), (self.SUCCESS, expected))

    def test_jc_dig_150cols(self):
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
        ╒═══════╤══════════╤══════════╤═════════╤══════════╤══════════╤══════════╤══════════╤══════════╤══════════╤══════════╤══════════╤════════╤════════╕
        │    id │ opcode   │ status   │ flags   │   query_ │   answer │   author │   additi │ questi   │ answer   │   query_ │   server │ when   │   rcvd │
        │       │          │          │         │      num │     _num │   ity_nu │   onal_n │ on       │          │     time │          │        │        │
        │       │          │          │         │          │          │        m │       um │          │          │          │          │        │        │
        ╞═══════╪══════════╪══════════╪═════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪══════════╪════════╪════════╡
        │ 55658 │ QUERY    │ NOERRO   │ ['qr',  │        1 │        5 │        0 │        1 │ {'name   │ [{'nam   │       44 │     2600 │ Wed Ma │    143 │
        │       │          │ R        │  'rd',  │          │          │          │          │ ': 'ww   │ e': 'w   │          │          │ r 18 1 │        │
        │       │          │          │  'ra']  │          │          │          │          │ w.cnn.   │ ww.cnn   │          │          │ 2:20:5 │        │
        │       │          │          │         │          │          │          │          │ com.',   │ .com.'   │          │          │ 9 PDT  │        │
        │       │          │          │         │          │          │          │          │  'clas   │ , 'cla   │          │          │ 2020   │        │
        │       │          │          │         │          │          │          │          │ s': 'I   │ ss': '   │          │          │        │        │
        │       │          │          │         │          │          │          │          │ N', 't   │ IN', '   │          │          │        │        │
        │       │          │          │         │          │          │          │          │ ype':    │ type':   │          │          │        │        │
        │       │          │          │         │          │          │          │          │ 'A'}     │  'CNAM   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ E', 't   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ tl': 1   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 47, 'd   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ata':    │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 'turne   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ r-tls.   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ map.fa   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ stly.n   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ et.'},   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │  {'nam   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ e': 't   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ urner-   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ tls.ma   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ p.fast   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ly.net   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ .', 'c   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ lass':   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │  'IN',   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │  'type   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ': 'A'   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ , 'ttl   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ': 5,    │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 'data'   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ : '151   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ .101.1   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ .67'},   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │  {'nam   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ e': 't   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ urner-   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ tls.ma   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ p.fast   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ly.net   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ .', 'c   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ lass':   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │  'IN',   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │  'type   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ': 'A'   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ , 'ttl   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ': 5,    │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 'data'   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ : '151   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ .101.6   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 5.67'}   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ , {'na   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ me': '   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ turner   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ -tls.m   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ap.fas   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ tly.ne   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ t.', '   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ class'   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ : 'IN'   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ , 'typ   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ e': 'A   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ', 'tt   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ l': 5,   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │  'data   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ': '15   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 1.101.   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 129.67   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ '}, {'   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ name':   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │  'turn   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ er-tls   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ .map.f   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ astly.   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ net.',   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │  'clas   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ s': 'I   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ N', 't   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ype':    │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 'A', '   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ttl':    │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 5, 'da   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ ta': '   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 151.10   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 1.193.   │          │          │        │        │
        │       │          │          │         │          │          │          │          │          │ 67'}]    │          │          │        │        │
        ╘═══════╧══════════╧══════════╧═════════╧══════════╧══════════╧══════════╧══════════╧══════════╧══════════╧══════════╧══════════╧════════╧════════╛''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=150), (self.SUCCESS, expected))

    def test_jc_dig_150cols_t(self):
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
           id  opcode    status    flags       query_nu    answer_n    authorit    addition  question    answer      query_ti    server  when       rcvd
        -----  --------  --------  --------  ----------  ----------  ----------  ----------  ----------  --------  ----------  --------  -------  ------
        55658  QUERY     NOERROR   ['qr', '           1           5           0           1  {'name':    [{'name'          44      2600  Wed Mar     143''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, truncate=True, columns=150), (self.SUCCESS, expected))

    def test_jc_dig_nowrap(self):
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
           id  opcode    status    flags                 query_num    answer_num    authority_num    additional_num  question                                              answer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       query_time    server  when                            rcvd
        -----  --------  --------  ------------------  -----------  ------------  ---------------  ----------------  ----------------------------------------------------  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  ------------  --------  ----------------------------  ------
        55658  QUERY     NOERROR   ['qr', 'rd', 'ra']            1             5                0                 1  {'name': 'www.cnn.com.', 'class': 'IN', 'type': 'A'}  [{'name': 'www.cnn.com.', 'class': 'IN', 'type': 'CNAME', 'ttl': 147, 'data': 'turner-tls.map.fastly.net.'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.1.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.65.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.129.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.193.67'}]            44      2600  Wed Mar 18 12:20:59 PDT 2020     143''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, nowrap=True, columns=150), (self.SUCCESS, expected))

    def test_jc_dig_nowrap_t_cols_80(self):
        """test that nowrap overrides both truncate and columns"""
        stdin = [{"id": 55658, "opcode": "QUERY", "status": "NOERROR", "flags": ["qr", "rd", "ra"], "query_num": 1, "answer_num": 5, "authority_num": 0, "additional_num": 1, "question": {"name": "www.cnn.com.", "class": "IN", "type": "A"}, "answer": [{"name": "www.cnn.com.", "class": "IN", "type": "CNAME", "ttl": 147, "data": "turner-tls.map.fastly.net."}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.1.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.65.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.129.67"}, {"name": "turner-tls.map.fastly.net.", "class": "IN", "type": "A", "ttl": 5, "data": "151.101.193.67"}], "query_time": 44, "server": "2600", "when": "Wed Mar 18 12:20:59 PDT 2020", "rcvd": 143}]
        expected = textwrap.dedent('''\
           id  opcode    status    flags                 query_num    answer_num    authority_num    additional_num  question                                              answer                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       query_time    server  when                            rcvd
        -----  --------  --------  ------------------  -----------  ------------  ---------------  ----------------  ----------------------------------------------------  -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  ------------  --------  ----------------------------  ------
        55658  QUERY     NOERROR   ['qr', 'rd', 'ra']            1             5                0                 1  {'name': 'www.cnn.com.', 'class': 'IN', 'type': 'A'}  [{'name': 'www.cnn.com.', 'class': 'IN', 'type': 'CNAME', 'ttl': 147, 'data': 'turner-tls.map.fastly.net.'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.1.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.65.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.129.67'}, {'name': 'turner-tls.map.fastly.net.', 'class': 'IN', 'type': 'A', 'ttl': 5, 'data': '151.101.193.67'}]            44      2600  Wed Mar 18 12:20:59 PDT 2020     143''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, nowrap=True, columns=80, truncate=True), (self.SUCCESS, expected))

    def test_jc_dig_answer(self):
        stdin = [{"name":"www.cnn.com.","class":"IN","type":"CNAME","ttl":147,"data":"turner-tls.map.fastly.net."},{"name":"turner-tls.map.fastly.net.","class":"IN","type":"A","ttl":5,"data":"151.101.1.67"},{"name":"turner-tls.map.fastly.net.","class":"IN","type":"A","ttl":5,"data":"151.101.65.67"},{"name":"turner-tls.map.fastly.net.","class":"IN","type":"A","ttl":5,"data":"151.101.129.67"},{"name":"turner-tls.map.fastly.net.","class":"IN","type":"A","ttl":5,"data":"151.101.193.67"}]
        expected = textwrap.dedent('''\
        name                        class    type      ttl  data
        --------------------------  -------  ------  -----  --------------------------
        www.cnn.com.                IN       CNAME     147  turner-tls.map.fastly.net.
        turner-tls.map.fastly.net.  IN       A           5  151.101.1.67
        turner-tls.map.fastly.net.  IN       A           5  151.101.65.67
        turner-tls.map.fastly.net.  IN       A           5  151.101.129.67
        turner-tls.map.fastly.net.  IN       A           5  151.101.193.67''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=80), (self.SUCCESS, expected))

    def test_float_format(self):
        stdin = [{"a": 1000000, "b": 1000000.1}]
        expected = '      a          b\n-------  ---------\n1000000  1000000.1'

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=80), (self.SUCCESS, expected))

    def test_json_lines(self):
        """test JSON Lines data"""
        stdin = [
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
        expected = textwrap.dedent('''\
        name     type    ipv4_addr      ipv4_mask
        -------  ------  -------------  -------------
        lo0              127.0.0.1      255.0.0.0
        gif0
        stf0
        XHC0
        XHC20
        VHC128
        XHC1
        en5
        ap1
        en0              192.168.1.221  255.255.255.0
        p2p0
        awdl0
        en1
        en2
        en3
        en4
        bridge0
        utun0
        utun1
        utun2
        utun3
        utun4
        vmnet1           192.168.101.1  255.255.255.0
        vmnet8           192.168.71.1   255.255.255.0''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns), (self.SUCCESS, expected))

    def test_markdown(self):
        """test markdown output"""
        stdin = [
            {
                "column1": "data",
                "column2": 123,
                "column3": True,
                "column4": None
            },
            {
                "column1": "This is a long string that should not be truncated by the markdown table format. Lines should not be wrapped for markdown.",
                "column2": 123,
                "column3": True,
                "column4": None
            }
        ]

        expected = textwrap.dedent('''\
        | column1                                                                                                                    |   column2 | column3   | column4   |
        |----------------------------------------------------------------------------------------------------------------------------|-----------|-----------|-----------|
        | data                                                                                                                       |       123 | True      |           |
        | This is a long string that should not be truncated by the markdown table format. Lines should not be wrapped for markdown. |       123 | True      |           |''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns, nowrap=True, table_format='github'), (self.SUCCESS, expected))


    def test_add_remove_fields(self):
        """test with added and missing fields"""
        stdin = [{"foo this is a very long long key":"this is a very very long string yes it is"},{"foo this is a very long long key":"medium length string","bar this is another very long string":"now is the time for all good men to come to the aide of their party"},{"baz is yet another long key name":"hello there how are you doing today? I am fine, thank you.","bar this is another very long string":"short string"}]
        expected = textwrap.dedent('''\
        ╒════════════════════════════════╤════════════════════════════════╤════════════════════════════════╕
        │ foo this is a very long long   │ bar this is another very lon   │ baz is yet another long key    │
        │  key                           │ g string                       │ name                           │
        ╞════════════════════════════════╪════════════════════════════════╪════════════════════════════════╡
        │ this is a very very long str   │                                │                                │
        │ ing yes it is                  │                                │                                │
        ├────────────────────────────────┼────────────────────────────────┼────────────────────────────────┤
        │ medium length string           │ now is the time for all good   │                                │
        │                                │  men to come to the aide of    │                                │
        │                                │ their party                    │                                │
        ├────────────────────────────────┼────────────────────────────────┼────────────────────────────────┤
        │                                │ short string                   │ hello there how are you doin   │
        │                                │                                │ g today? I am fine, thank yo   │
        │                                │                                │ u.                             │
        ╘════════════════════════════════╧════════════════════════════════╧════════════════════════════════╛''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=100), (self.SUCCESS, expected))


    def test_csv(self):
        """test csv output"""
        stdin = [{"LatD":"41","LatM":"5","LatS":"59","NS":"N","LonD":"80","LonM":"39","LonS":"0","EW":"W","City":"Youngstown","State":"OH"},{"LatD":"42","LatM":"52","LatS":"48","NS":"N","LonD":"97","LonM":"23","LonS":"23","EW":"W","City":"Yankton","State":"SD"},{"LatD":"46","LatM":"35","LatS":"59","NS":"N","LonD":"120","LonM":"30","LonS":"36","EW":"W","City":"Yakima","State":"WA"},{"LatD":"42","LatM":"16","LatS":"12","NS":"N","LonD":"71","LonM":"48","LonS":"0","EW":"W","City":"Worcester","State":"MA"},{"LatD":"43","LatM":"37","LatS":"48","NS":"N","LonD":"89","LonM":"46","LonS":"11","EW":"W","City":"Wisconsin Dells","State":"WI"},{"LatD":"36","LatM":"5","LatS":"59","NS":"N","LonD":"80","LonM":"15","LonS":"0","EW":"W","City":"Winston-Salem","State":"NC"},{"LatD":"49","LatM":"52","LatS":"48","NS":"N","LonD":"97","LonM":"9","LonS":"0","EW":"W","City":"Winnipeg","State":"MB"},{"LatD":"39","LatM":"11","LatS":"23","NS":"N","LonD":"78","LonM":"9","LonS":"36","EW":"W","City":"Winchester","State":"VA"},{"LatD":"34","LatM":"14","LatS":"24","NS":"N","LonD":"77","LonM":"55","LonS":"11","EW":"W","City":"Wilmington","State":"NC"}]
        expected = textwrap.dedent('''\
        LatD,LatM,LatS,NS,LonD,LonM,LonS,EW,City,State\r
        41,5,59,N,80,39,0,W,Youngstown,OH\r
        42,52,48,N,97,23,23,W,Yankton,SD\r
        46,35,59,N,120,30,36,W,Yakima,WA\r
        42,16,12,N,71,48,0,W,Worcester,MA\r
        43,37,48,N,89,46,11,W,Wisconsin Dells,WI\r
        36,5,59,N,80,15,0,W,Winston-Salem,NC\r
        49,52,48,N,97,9,0,W,Winnipeg,MB\r
        39,11,23,N,78,9,36,W,Winchester,VA\r
        34,14,24,N,77,55,11,W,Wilmington,NC\r
        ''')

        self.assertEqual(jtbl.cli.make_csv_table(data=stdin), (self.SUCCESS, expected))


    def test_html(self):
        """test html output"""
        stdin = [{"LatD":"41","LatM":"5","LatS":"59","NS":"N","LonD":"80","LonM":"39","LonS":"0","EW":"W","City":"Youngstown","State":"OH"},{"LatD":"42","LatM":"52","LatS":"48","NS":"N","LonD":"97","LonM":"23","LonS":"23","EW":"W","City":"Yankton","State":"SD"},{"LatD":"46","LatM":"35","LatS":"59","NS":"N","LonD":"120","LonM":"30","LonS":"36","EW":"W","City":"Yakima","State":"WA"},{"LatD":"42","LatM":"16","LatS":"12","NS":"N","LonD":"71","LonM":"48","LonS":"0","EW":"W","City":"Worcester","State":"MA"},{"LatD":"43","LatM":"37","LatS":"48","NS":"N","LonD":"89","LonM":"46","LonS":"11","EW":"W","City":"Wisconsin Dells","State":"WI"},{"LatD":"36","LatM":"5","LatS":"59","NS":"N","LonD":"80","LonM":"15","LonS":"0","EW":"W","City":"Winston-Salem","State":"NC"},{"LatD":"49","LatM":"52","LatS":"48","NS":"N","LonD":"97","LonM":"9","LonS":"0","EW":"W","City":"Winnipeg","State":"MB"},{"LatD":"39","LatM":"11","LatS":"23","NS":"N","LonD":"78","LonM":"9","LonS":"36","EW":"W","City":"Winchester","State":"VA"},{"LatD":"34","LatM":"14","LatS":"24","NS":"N","LonD":"77","LonM":"55","LonS":"11","EW":"W","City":"Wilmington","State":"NC"}]

        expected = textwrap.dedent('''\
        <table>
        <thead>
        <tr><th style="text-align: right;">  LatD</th><th style="text-align: right;">  LatM</th><th style="text-align: right;">  LatS</th><th>NS  </th><th style="text-align: right;">  LonD</th><th style="text-align: right;">  LonM</th><th style="text-align: right;">  LonS</th><th>EW  </th><th>City           </th><th>State  </th></tr>
        </thead>
        <tbody>
        <tr><td style="text-align: right;">    41</td><td style="text-align: right;">     5</td><td style="text-align: right;">    59</td><td>N   </td><td style="text-align: right;">    80</td><td style="text-align: right;">    39</td><td style="text-align: right;">     0</td><td>W   </td><td>Youngstown     </td><td>OH     </td></tr>
        <tr><td style="text-align: right;">    42</td><td style="text-align: right;">    52</td><td style="text-align: right;">    48</td><td>N   </td><td style="text-align: right;">    97</td><td style="text-align: right;">    23</td><td style="text-align: right;">    23</td><td>W   </td><td>Yankton        </td><td>SD     </td></tr>
        <tr><td style="text-align: right;">    46</td><td style="text-align: right;">    35</td><td style="text-align: right;">    59</td><td>N   </td><td style="text-align: right;">   120</td><td style="text-align: right;">    30</td><td style="text-align: right;">    36</td><td>W   </td><td>Yakima         </td><td>WA     </td></tr>
        <tr><td style="text-align: right;">    42</td><td style="text-align: right;">    16</td><td style="text-align: right;">    12</td><td>N   </td><td style="text-align: right;">    71</td><td style="text-align: right;">    48</td><td style="text-align: right;">     0</td><td>W   </td><td>Worcester      </td><td>MA     </td></tr>
        <tr><td style="text-align: right;">    43</td><td style="text-align: right;">    37</td><td style="text-align: right;">    48</td><td>N   </td><td style="text-align: right;">    89</td><td style="text-align: right;">    46</td><td style="text-align: right;">    11</td><td>W   </td><td>Wisconsin Dells</td><td>WI     </td></tr>
        <tr><td style="text-align: right;">    36</td><td style="text-align: right;">     5</td><td style="text-align: right;">    59</td><td>N   </td><td style="text-align: right;">    80</td><td style="text-align: right;">    15</td><td style="text-align: right;">     0</td><td>W   </td><td>Winston-Salem  </td><td>NC     </td></tr>
        <tr><td style="text-align: right;">    49</td><td style="text-align: right;">    52</td><td style="text-align: right;">    48</td><td>N   </td><td style="text-align: right;">    97</td><td style="text-align: right;">     9</td><td style="text-align: right;">     0</td><td>W   </td><td>Winnipeg       </td><td>MB     </td></tr>
        <tr><td style="text-align: right;">    39</td><td style="text-align: right;">    11</td><td style="text-align: right;">    23</td><td>N   </td><td style="text-align: right;">    78</td><td style="text-align: right;">     9</td><td style="text-align: right;">    36</td><td>W   </td><td>Winchester     </td><td>VA     </td></tr>
        <tr><td style="text-align: right;">    34</td><td style="text-align: right;">    14</td><td style="text-align: right;">    24</td><td>N   </td><td style="text-align: right;">    77</td><td style="text-align: right;">    55</td><td style="text-align: right;">    11</td><td>W   </td><td>Wilmington     </td><td>NC     </td></tr>
        </tbody>
        </table>''')

        self.assertEqual(jtbl.cli.make_table(data=stdin, columns=self.columns, nowrap=True, table_format='html'), (self.SUCCESS, expected))


    def test_rotate(self):
        """test html output"""
        stdin = [{"LatD":"41","LatM":"5","LatS":"59","NS":"N","LonD":"80","LonM":"39","LonS":"0","EW":"W","City":"Youngstown","State":"OH"},{"LatD":"42","LatM":"52","LatS":"48","NS":"N","LonD":"97","LonM":"23","LonS":"23","EW":"W","City":"Yankton","State":"SD"},{"LatD":"46","LatM":"35","LatS":"59","NS":"N","LonD":"120","LonM":"30","LonS":"36","EW":"W","City":"Yakima","State":"WA"},{"LatD":"42","LatM":"16","LatS":"12","NS":"N","LonD":"71","LonM":"48","LonS":"0","EW":"W","City":"Worcester","State":"MA"},{"LatD":"43","LatM":"37","LatS":"48","NS":"N","LonD":"89","LonM":"46","LonS":"11","EW":"W","City":"Wisconsin Dells","State":"WI"},{"LatD":"36","LatM":"5","LatS":"59","NS":"N","LonD":"80","LonM":"15","LonS":"0","EW":"W","City":"Winston-Salem","State":"NC"},{"LatD":"49","LatM":"52","LatS":"48","NS":"N","LonD":"97","LonM":"9","LonS":"0","EW":"W","City":"Winnipeg","State":"MB"},{"LatD":"39","LatM":"11","LatS":"23","NS":"N","LonD":"78","LonM":"9","LonS":"36","EW":"W","City":"Winchester","State":"VA"},{"LatD":"34","LatM":"14","LatS":"24","NS":"N","LonD":"77","LonM":"55","LonS":"11","EW":"W","City":"Wilmington","State":"NC"}]

        expected = textwrap.dedent('''\
        item: 0
        ────────────────────────────────────────────────────────────────────────────────
        LatD   41
        LatM   5
        LatS   59
        NS     N
        LonD   80
        LonM   39
        LonS   0
        EW     W
        City   Youngstown
        State  OH

        item: 1
        ────────────────────────────────────────────────────────────────────────────────
        LatD   42
        LatM   52
        LatS   48
        NS     N
        LonD   97
        LonM   23
        LonS   23
        EW     W
        City   Yankton
        State  SD

        item: 2
        ────────────────────────────────────────────────────────────────────────────────
        LatD   46
        LatM   35
        LatS   59
        NS     N
        LonD   120
        LonM   30
        LonS   36
        EW     W
        City   Yakima
        State  WA

        item: 3
        ────────────────────────────────────────────────────────────────────────────────
        LatD   42
        LatM   16
        LatS   12
        NS     N
        LonD   71
        LonM   48
        LonS   0
        EW     W
        City   Worcester
        State  MA

        item: 4
        ────────────────────────────────────────────────────────────────────────────────
        LatD   43
        LatM   37
        LatS   48
        NS     N
        LonD   89
        LonM   46
        LonS   11
        EW     W
        City   Wisconsin Dells
        State  WI

        item: 5
        ────────────────────────────────────────────────────────────────────────────────
        LatD   36
        LatM   5
        LatS   59
        NS     N
        LonD   80
        LonM   15
        LonS   0
        EW     W
        City   Winston-Salem
        State  NC

        item: 6
        ────────────────────────────────────────────────────────────────────────────────
        LatD   49
        LatM   52
        LatS   48
        NS     N
        LonD   97
        LonM   9
        LonS   0
        EW     W
        City   Winnipeg
        State  MB

        item: 7
        ────────────────────────────────────────────────────────────────────────────────
        LatD   39
        LatM   11
        LatS   23
        NS     N
        LonD   78
        LonM   9
        LonS   36
        EW     W
        City   Winchester
        State  VA

        item: 8
        ────────────────────────────────────────────────────────────────────────────────
        LatD   34
        LatM   14
        LatS   24
        NS     N
        LonD   77
        LonM   55
        LonS   11
        EW     W
        City   Wilmington
        State  NC
        ''')

        self.assertEqual(jtbl.cli.make_rotate_table(data=stdin, columns=self.columns, nowrap=True, rotate=True), (self.SUCCESS, expected))


    def test_rotate_single_item(self):
        """test html output"""
        stdin = [{"LatD":"41","LatM":"5","LatS":"59","NS":"N","LonD":"80","LonM":"39","LonS":"0","EW":"W","City":"Youngstown","State":"OH"}]

        expected = textwrap.dedent('''\
        LatD   41
        LatM   5
        LatS   59
        NS     N
        LonD   80
        LonM   39
        LonS   0
        EW     W
        City   Youngstown
        State  OH
        ''')

        self.assertEqual(jtbl.cli.make_rotate_table(data=stdin, columns=self.columns, nowrap=True, rotate=True), (self.SUCCESS, expected))


if __name__ == '__main__':
    unittest.main()
