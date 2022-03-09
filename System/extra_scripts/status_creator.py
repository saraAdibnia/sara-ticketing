
from order.models.part_model import Part
from rest_framework.exceptions import ValidationError
from order.models import Waybill, Packaging
from status.models import *
from order.models import Status
from order.serializers import StatusSerializer, WaybillSerializer
from .EMS import validation_error
from order.serializers import ExportWaybillSerializerRegister1
from external_transit.serializers import ExternalTransitSerializerRegister1

# do not use
from external_transit.models import ExternalTransit


def status_creator(waybill=None, kind=None, text=None, show_to_customer=True, part=None, many=False, arr=None):

    if many == False:
        status_serialized = StatusSerializer(
            data={
                'waybill': waybill,
                'kind': kind,
                'part': part,
                'text': text,
                'show_to_customer': show_to_customer
            }
        )
        if not status_serialized.is_valid():
            return False
        status_serialized.save()

        return True
    else:
        status_serialized = StatusSerializer(
            data=arr,
            many=True
        )
        if not status_serialized.is_valid():
            return False
        status_serialized.save()

        return True


def waybill_status_creator(status_number=None, waybill_obj=None, request=None, pack_obj=None, location=None):

    try:
        w_status_main = WStatusMain.objects.filter(
            number=status_number).first()

        created = WStatusMain_Waybill.objects.create(
            w_status_main=w_status_main, waybill=waybill_obj, pack=pack_obj, created_by=request.user)
        created.save()

        w_updated = WaybillSerializer(
            waybill_obj,
            data={
                "last_w_status_main_id": w_status_main.id,
                "location": location
            },
            partial=True
        )
        if not w_updated.is_valid():
            return validation_error(w_updated)
        w_updated.save()
        return True
    except IndexError:
        return ValidationError("waybill or user is not defiend")


def export_waybill_status_creator(status_number=None, export_waybill_obj=None, request=None, pack_obj=None, location=None):

    try:
        w_status_main = WStatusMain.objects.filter(
            number=status_number).first()

        created = WStatusMain_ExportWaybill.objects.create(
            w_status_main=w_status_main, export_waybill=export_waybill_obj, pack=pack_obj, created_by=request.user)
        created.save()

        w_updated = ExportWaybillSerializerRegister1(
            export_waybill_obj,
            data={
                "last_w_status_main_id": w_status_main.id,
                "location": location
            },
            partial=True
        )
        if not w_updated.is_valid():
            return validation_error(w_updated)
        w_updated.save()
        return True
    except IndexError:
        return ValidationError("waybill or user is not defiend")


def part_status_creator(status_number=None, part_id=None, request=None, tran_man_path_detail_id=None, location=None):

    try:
        p_status_main = PStatusMain.objects.filter(
            number=status_number).first()
        part = Part.objects.filter(
            id=part_id).first()
        if tran_man_path_detail_id is not None:
            p = PStatusMain_Part.objects.create(
                p_status_main=p_status_main, part=part, created_by=request.user, tran_man_path_detail_id=tran_man_path_detail_id, location=location)
        else:
            p = PStatusMain_Part.objects.create(
                p_status_main=p_status_main, part=part, created_by=request.user, location=location)
        p.save()
        return True
    except IndexError:
        return ValidationError("part or user is not defiend")


def pack_status_creator(status_number=None, pack_obj=None, waybill_obj=None, request=None):

    try:
        pack_status_main = PackStatusMain.objects.filter(
            number=status_number
        ).first()

        p = PackStatusMain_Pack.objects.create(
            pack_status_main=pack_status_main, pack=pack_obj, waybill=waybill_obj, created_by=request.user)
        p.save()
        return True
    except IndexError:
        return ValidationError("pack or user or waybill is not defiend")


def external_transit_status_creator(status_number=None, external_transit_obj=None, request=None, pack_obj=None, location=None):

    try:
        w_status_main = WStatusMain.objects.filter(
            number=status_number).first()

        created = WStatusMain_ExternalTransit.objects.create(
            w_status_main=w_status_main, external_transit=external_transit_obj, pack=pack_obj, created_by=request.user)
        created.save()
        
        w_updated = ExternalTransitSerializerRegister1(
            external_transit_obj,
            data={
                "last_w_status_main_id": w_status_main.id,
                "location": location
            },
            
            partial=True
        )
        if not w_updated.is_valid():
            return validation_error(w_updated)
        w_updated.save()
        return True
    except IndexError:
        return ValidationError("waybill or user is not defiend")
