
import json
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos.error import GEOSException
from django.utils.translation import gettext_lazy as _

from rest_framework.serializers import ModelSerializer, Field
EMPTY_VALUES = (None, '', [], (), {})

from django.contrib.gis.geos import Point, Polygon 

class PolygonField(Field):
    """
    A field for handling GeoDjango PolyGone fields as a array format.
    Expected input format:
        {
            [
                [
                    51.778564453125,
                    35.59925232772949
                ],
                [
                    50.1470947265625,
                    34.80929324176267
                ],
                [
                    52.6080322265625,
                    34.492975402501536
                ],
                [
                    51.778564453125,
                    35.59925232772949
                ]
            ]
        }

    """
    type_name = 'PolygonField'
    type_label = 'polygon'

    default_error_messages = {
        'invalid': _('Enter a valid polygon.'),
    }

    def __init__(self, *args, **kwargs):
        super(PolygonField, self).__init__(*args, **kwargs)

    def to_internal_value(self, value):
        """
        Parse array data and return a polygon object
        """
        if value in EMPTY_VALUES and not self.required:
            return None

        try:
            new_value = []        
            for item in value:
                item = list(map(float, item))
                new_value.append(item)
        except ValueError:
            self.fail('invalid')
        
        try:
            return Polygon(new_value)
        except (GEOSException, ValueError, TypeError):
            self.fail('invalid')
        self.fail('invalid')


    def to_representation(self, value):
        """
        Transform POINT object to json.
        """
        if value is None:
            return value

        if isinstance(value, GEOSGeometry):
            value = {
                "type": "FeatureCollection",
                "features": [
                {
                    "type": "Feature",
                    "properties": {
                        
                    },
                    "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        value.boundary.array
                    ]
                    }
                }
                ]
            }

        return value
