
from order.serializers.fake_serializers import GroupFakeDetailSerializer
from order.models import FakeName, FakeFamilyName
from order.models.fake_names import FakePhoneNumber
import random
from extra_scripts.EMS import validation_error
from rest_framework.response import Response




def fakeGroupNameFamily(group_id):

    fakename_obj = FakeName.objects.all()

    fakefamilyname_obj = FakeFamilyName.objects.all()

    fakephone_obj = FakePhoneNumber.objects.all()

    name_item = random.randrange(0, len(fakename_obj))
    familyname_item = random.randrange(0, len(fakefamilyname_obj))
    phone_item = random.randrange(0, len(fakephone_obj))

    final_fake_name = fakename_obj[name_item]

    final_fake_familyname = fakefamilyname_obj[familyname_item]

    final_fake_phone = fakephone_obj[phone_item]

    groupfakedetail_serialized = GroupFakeDetailSerializer(
        data={
            "groups": group_id,
            "fnamefamily": f"{final_fake_name.fname} {final_fake_familyname.f_lname}",
            "enamefamily": f"{final_fake_name.ename.title()} {final_fake_familyname.e_lname.title()}",
            'phone_number': f"{final_fake_phone.phone}"
        }
    )
    if not groupfakedetail_serialized.is_valid():
        return validation_error(groupfakedetail_serialized)
    groupfakedetail_serialized.save()

    response_json = {
        "succeeded": True
    }
    return Response(response_json, status=200)

        