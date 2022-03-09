from places.models import Country, CountryZone
from rest_framework.response import Response
from extra_scripts.EMS import existence_error
from icecream import ic
# get country code and/or date 4 : return contry_zone that zone.startDate <= date <= zone.endDate


def country_zone_checker(country_id=None, date=None, zone_type = 'import'):
    """return the CountryZone object based on the counrty_id , if the date is given set query in specific time else return the last obj"""
    if date:
        if zone_type== 'import': #TODO what to do with CountryZone 
            country_zone = CountryZone.objects.filter(
            country__id=country_id, start_date__lte=date, zone_type = 1).last()
            print('this is country zone \n\n ',country_zone)

        elif zone_type== 'export':
            country_zone = CountryZone.objects.filter(
            country__id=country_id, start_date__lte=date, zone_type = 2).last()
    else:

        if zone_type==  'import':
            country_zone = CountryZone.objects.filter(
            country__id=country_id,code__code__gte = 1, zone_type = 1 ).last()
        
        elif zone_type == 'export':
            ic(country_id)
            country_zone = CountryZone.objects.filter(
            country__id=country_id,code__code__gte = 1, zone_type = 2 ).last()
    ic(country_zone)
    return country_zone



def last_country_zone(country_id=None, zone_type = 'import'):
    """return zone field in country model based on export or import type """

    if zone_type == 'import':
        return Country.objects.get(id=country_id).zone
    else:
        return Country.objects.get(id=country_id).export_zone

