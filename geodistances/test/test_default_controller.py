# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from geodistances.models.locations import Locations  # noqa: E501
from geodistances.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_calculate_distance(self):
        """Test case for calculate_distance

        calculateDistance
        """
        locations = {
  "address_1" : "address_1",
  "address_2" : "address_2"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/distance',
            method='POST',
            headers=headers,
            data=json.dumps(locations),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
