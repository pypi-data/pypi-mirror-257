import unittest
import os

from acdh_obj2xml_pyutils import ObjectToXml


TABLE_ID = "1474"
BR_TOKEN = os.environ.get('BASEROW_TOKEN')


class TestObjectToXml(unittest.TestCase):
    """Tests for `acdh_baserow_utils` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_object_to_tei(self):
        input = [{"id": "test1", "filename": "test1"}]
        obj_cl = ObjectToXml(br_input=input)
        tei = [x for x in obj_cl.make_xml(save=False)]
        self.assertTrue("test1" in str(tei[0]))

    def test_002_object_to_tei(self):
        input = [{"id": "test1", "filename": "test1"}]
        obj_cl = ObjectToXml(br_input=input)
        tei = obj_cl.make_xml_single(save=False)
        self.assertTrue("test1" in str(tei))
