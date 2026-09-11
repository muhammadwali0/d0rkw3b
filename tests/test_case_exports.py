import csv
import io
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET

from d0rkw3b import investigate
from d0rkw3b.cases.exports import export_data, graph, timeline
from d0rkw3b.cases.store import CaseStore


class ExportTests(unittest.TestCase):
    def test_graphs_and_timeline_preserve_provenance(self):
        with tempfile.TemporaryDirectory() as root:
            with CaseStore(root, writable=True) as store:
                store.new('test')
                store.save('test', investigate('alice@example.com'))
                store.note('test', 'A < B & C')
                case = store.show('test')
                for format, namespace in [('graphml', 'http://graphml.graphdrawing.org/xmlns'), ('gexf', 'http://www.gexf.net/1.2draft')]:
                    encoded = graph(case, format)
                    tree = ET.fromstring(encoded)
                    self.assertEqual(len(tree.findall('.//{' + namespace + '}node')), 2)
                    self.assertEqual(len(tree.findall('.//{' + namespace + '}edge')), 1)
                    self.assertIn('email syntax parsing', encoded)
                    self.assertIn('uses_domain', encoded)
                events = timeline(case)
                self.assertTrue(any(e['time_kind'] == 'created_at' for e in events))
                self.assertTrue(any(e['time_kind'] == 'observed_at' for e in events))
                self.assertTrue(any(e['time_kind'] == 'collected_at' for e in events))
                self.assertEqual(json.loads(export_data(case)), case)
                lines = export_data(case, 'jsonl').splitlines()
                self.assertTrue(all(json.loads(line) for line in lines))
                rows = list(csv.DictReader(io.StringIO(export_data(case, 'csv'))))
                self.assertTrue(all(json.loads(row['record_json']) for row in rows))
                self.assertIn('provenance', export_data(case, 'markdown'))
