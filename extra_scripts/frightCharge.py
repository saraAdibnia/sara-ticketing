import datetime
from re import I
from price.models.third_party_price import ThirdPartyRow, ThirdPartyTable
from offices.models.office_models import (
    Office,
    OfficeDutyTax,
    OfficeExcludeTaxDutyCountry,
)
from extra_scripts.EMS import existence_error
from price.models.fright_charge import FrightCharge, FrightVolumeWeight, FrightWeight
import math
from extra_scripts import roundNumber
from django.db.models.query_utils import Q
from places.models import Zone
from icecream import ic

def lastFrightChargeRateWithoutDate(
    originCountry, destCountry, originAirport, destAirport, kind=1, weight=None
):
    """[return last FrightCharge with WeightFrightCharge and/or VolWeightFrightCharge for given Weight :)]

    Args:
        originAirport ([int]): [description]
        destAirport ([int]): [description]
        kind ([int]): [kind=1 => both Weight and VolWeight  kind=2 => only Weight  kind =3 => only VolWeight]
        weight ([float]: [weight that we want to find rate of that])
    """
    rWeight = 0
    frightWeightRate = 0
    frightWeightCurrency = 0
    frightVolWeightRate = 0
    frightVolWeightCurrency = 0
    frightChargeRound = 0
    is_round_point_five = False

    if originAirport is not None and destAirport is not None:
        lastFrightChargObj = FrightCharge.objects.filter(
            from_airport=originAirport, to_airport=destAirport, granted=True
        ).last()

        frightChargeRound = lastFrightChargObj.round
        is_round_point_five = lastFrightChargObj.is_round_point_five

        if frightChargeRound == 0:
            """round up"""
            if is_round_point_five:
                rWeight = roundNumber(kind=1, weight=weight)
            else:
                rWeight = roundNumber(kind=0, weight=weight)
        elif frightChargeRound == 1:
            """round Down"""
            if is_round_point_five:
                rWeight = roundNumber(kind=3, weight=weight)
            else:
                rWeight = roundNumber(kind=2, weight=weight)

        if kind == 2 or kind == 1:
            lastFrightWeightObj = FrightWeight.objects.filter(
                FrightCharge=lastFrightChargObj.id,
                weight_start__lt=rWeight,
                weight_end__gte=rWeight,
            )
            frightWeightRate = lastFrightWeightObj.fright_charge_rate
            frightWeightCurrency = lastFrightWeightObj.currency
        if kind == 3 or kind == 1:
            lasrVolFrightWeight = FrightVolumeWeight.objects.filter(
                FrightCharge=lastFrightChargObj.id,
                volume_weight_start__lt=rWeight,
                volume_weight_start__gte=rWeight,
            )
            frightVolWeightRate = lasrVolFrightWeight.fright_charge_rate
            frightVolWeightCurrency = lasrVolFrightWeight.currency
    elif originCountry is not None and destCountry is not None:

        lastFrightChargObj = FrightCharge.objects.filter(
            from_country=originCountry, to_country=destCountry, granted=True
        ).last()

        frightChargeRound = lastFrightChargObj.round
        is_round_point_five = lastFrightChargObj.is_round_point_five

        if frightChargeRound == 0:
            """round up"""
            if is_round_point_five:
                rWeight = roundNumber(kind=1, weight=weight)
            else:
                rWeight = roundNumber(kind=0, weight=weight)
        elif frightChargeRound == 1:
            """round Down"""
            if is_round_point_five:
                rWeight = roundNumber(kind=3, weight=weight)
            else:
                rWeight = roundNumber(kind=2, weight=weight)

        if kind == 2 or kind == 1:
            lastFrightWeightObj = FrightWeight.objects.filter(
                FrightCharge=lastFrightChargObj.id,
                weight_start__lt=rWeight,
                weight_end__gte=rWeight,
            )
            frightWeightRate = lastFrightWeightObj.fright_charge_rate
            frightWeightCurrency = lastFrightWeightObj.currency
        if kind == 3 or kind == 1:
            lasrVolFrightWeight = FrightVolumeWeight.objects.filter(
                FrightCharge=lastFrightChargObj.id,
                volume_weight_start__lt=rWeight,
                volume_weight_start__gte=rWeight,
            )
            frightVolWeightRate = lasrVolFrightWeight.fright_charge_rate
            frightVolWeightCurrency = lasrVolFrightWeight.currency

    result = {
        "frightChargeRound": frightChargeRound,
        "isRoundPointFive": is_round_point_five,
        "roundedWeight": rWeight,
        "frightWeightRate": frightWeightRate,
        "frightWeightCurrency": frightWeightCurrency,
        "frightVolWeightRate": frightVolWeightRate,
        "frightVolWeightCurrency": frightVolWeightCurrency,
    }
    return result



# kind 1 : Weight
# kind2 : VolumeWeight
# kin 3 : Full (Vol And Weight)
def calculateFrightCharge(
    from_country,
    to_country,
    from_airport=None,
    to_airport=None,
    total_massweight=0,
    total_volumeweight=0,
    waybill_date=None,
    kind=1,
):
    result = {"roundType": 0, "isRoundPointFive": True}
    # 111-first : find FrightCharge Object
    if from_country is not None and to_country is not None:
        frightChargeObj = (
            FrightCharge.objects.filter(
                from_country=from_country, to_country=to_country, granted=True
            )
            .filter(Q(start_date__lte=waybill_date, end_date__gte=waybill_date))
            .last()
        )
        
        if not frightChargeObj:
            result["error"] = "نرخ قیمتی پیدا نشد"
            # return existence_error("frightCharge")
            if 'WfrightRate' not in result:
                result['WfrightRate'] = 0
            if 'WfrightCurrency' not in result:
                result['WfrightCurrency'] = 3
            if 'WtotalPrice' not in result:
                result['WtotalPrice'] = 0
            if 'VfrightRate' not in result:
                result['VfrightRate'] = 0
            if 'VfrightCurrency' not in result:
                result['VfrightCurrency'] = 3
            if 'VSpareTotalPrice' not in result:
                result['VSpareTotalPrice'] = 0
            if 'VtotalPrice' not in result:
                result['VtotalPrice'] = 0
            return result

    else:
        frightChargeObj = (
            FrightCharge.objects.filter(
                from_airport=from_airport, to_airport=to_airport, granted=True
            )
            .filter(Q(start_date__lte=waybill_date, end_date__gte=waybill_date))
            .last()
        )
    roundType = frightChargeObj.round
    isRoundPointFive = frightChargeObj.is_round_point_five
    result["roundType"] = roundType
    result["isRoundPointFive"] = isRoundPointFive
    round_kind = roundNumber.findRoundKind(roundType, isRoundPointFive)
    # 222-second : find FrightWeight or FrightVolumeWeight
    # only weight need to calculate
    if kind == 1 or kind == 3:
        if frightChargeObj is not None:
            frightWeightObj = (
                FrightWeight.objects.filter(FrightCharge_id=frightChargeObj.id)
                .filter(
                    weight_start__lte=total_massweight, weight_end__gte=total_massweight
                )
                .last()
            )
            WfrightRate = frightWeightObj.fright_charge_rate
            WfrightIsFixed = frightWeightObj.is_fixed_rate
            WfrightCurrency = frightWeightObj.currency.id

            result["WfrightRate"] = WfrightRate

            result["WfrightCurrency"] = WfrightCurrency
            print(
                f'222 2222222  ****8{roundNumber.rounding(round_kind, total_massweight)}  ')
            if WfrightIsFixed:
                result["WtotalPrice"] = WfrightRate
                result["is_fixed_rate"] = True
            else:
                result["WtotalPrice"] = WfrightRate * roundNumber.rounding(
                    round_kind, total_massweight
                )
                result["is_fixed_rate"] = False

        else:
            # return False , 0
            # return result
            pass

    # only VolWeight Need to calculate
    if kind == 2 or kind == 3:
        if frightChargeObj is not None:
            frightVolWeightObj = (
                FrightVolumeWeight.objects.filter(
                    FrightCharge_id=frightChargeObj.id)
                .filter(
                    volume_weight_start__lte=total_volumeweight,
                    volume_weight_end__gte=total_volumeweight,
                )
                .first()
            )
            if not frightVolWeightObj:
                result["error"] = "بازه برای نرخ قیمتی پیدا نشد"
                # return existence_error("frightCharge")
                # return result

            VfrightRate = frightVolWeightObj.fright_charge_rate
            vfrightRateIsFixed = frightVolWeightObj.is_fixed_rate

            VfrightCurrency = frightVolWeightObj.currency.id
            result["VfrightRate"] = VfrightRate
            result["VfrightCurrency"] = VfrightCurrency
            # اگر لوازم یدکی بود و وزن حجمی از جرمی بیشتر بود، وزن جرمی محسابه و تفاضل وزن حجمی و جرمی نیز با جدول حجمی حساب و با قیمت وزن جرمی جمع می شود
            # if kind == 3:
            #     result["VSpareTotalPrice"] = VfrightRate * roundNumber.rounding(
            #         round_kind, abs(total_volumeweight - total_massweight)
            #     )

            if vfrightRateIsFixed:
                if kind == 3:
                    result["VSpareTotalPrice"] = VfrightRate

                result["VtotalPrice"] = VfrightRate
                result["v_is_fixed_rate"] = True
            else:
                if kind == 3:
                    result["VSpareTotalPrice"] = VfrightRate * roundNumber.rounding(
                        round_kind, abs(total_volumeweight - total_massweight)
                    )
                result["VtotalPrice"] = VfrightRate * roundNumber.rounding(
                    round_kind, total_volumeweight
                )
                result["v_is_fixed_rate"] = False

        else:
            # return False , 0

            pass
    else:
        # return False ,
        pass

    if 'WfrightRate' not in result:
        result['WfrightRate'] = 0
    if 'WfrightCurrency' not in result:
        result['WfrightCurrency'] = 3
    if 'WtotalPrice' not in result:
        result['WtotalPrice'] = 0
    if 'VfrightRate' not in result:
        result['VfrightRate'] = 0
    if 'VfrightCurrency' not in result:
        result['VfrightCurrency'] = 3
    if 'VSpareTotalPrice' not in result:
        result['VSpareTotalPrice'] = 0
    if 'VtotalPrice' not in result:
        result['VtotalPrice'] = 0

    return result


def calculateFrenchise(
    officeId=None, hubCountryId=None, originCountryId=None, date=datetime.date.today()
):
    result = {}
    result["excludeCountry"] = False
    # دفتر را با توجه به کشور هاب انتخاب می کنیم و اولین دفتر اون کشور رو به عنوان هاب انتخاب می کنیم
    if officeId == None:
        office_obj = Office.objects.filter(country_id=hubCountryId).first()
        if not office_obj:
            # return existence_error("office_obj")
            result["officeDuty"] = 0
            result["officeTax"] = 0
            result["office_tax_duty_desc"] = "برای نقطه میانی مورد نظر جدول یا یا ردیف جدولی تعریف نشده است"
            return result
        officeId = office_obj.id
    result["office"] = officeId
    # آیا کشور مبدا جزو کشور های معاف از مالیات هاب مورد نظر می باشد؟
    officeExcludeDuty_count = 0
    officeExcludeDuty_count = OfficeExcludeTaxDutyCountry.objects.filter(
        office=officeId, country=originCountryId
    ).count()
    if officeExcludeDuty_count > 0:
        result["officeDuty"] = 0
        result["officeTax"] = 0
        result["excludeCountry"] = True
    else:
        officeDutyTasx_obj = (
            OfficeDutyTax.objects.filter(
                active=True,
                office=officeId,
            )
            .filter(
                Q(
                    start_date__lte=date,
                    end_date__gte=date,
                )
            )
            .last()
        )
        if not officeDutyTasx_obj:
            result["officeDuty"] = 0
            result["officeTax"] = 0
            result["office_tax_duty_desc"] = "برای نقطه میانی مورد نظر جدول یا یا ردیف جدولی تعریف نشده است"
        else:
            result["officeDuty"] = officeDutyTasx_obj.duty
            result["officeTax"] = officeDutyTasx_obj.tax
    return result


def calculateThirdPartyPrice(date, zone, kind, weight):
    result = {}

    # TODO: باید بفهمیم هاب یا نقطه میانی کجا هست تا با توجه به اون از نرخ جدول ثالث استفاده کنیم با نکنیم و چطور استفاده کنیم
    # در حال حاضر چون فقز هاب امارات را داریم، هاب را امارات انتخاب می کنیم
    result["hub"] = "UAE"
    result["date"] = date
    if zone == 0:
        result["zone"] = "عدم پوشش"
    else:
        result["ezone"] = f"{zone.ename}"
        result["fzone"] = f"{zone.fname}"
    result["kind"] = kind
    
    # جدول حامل ثالث با توجه به زون، تاریخ و نوع(سند (۲)، بسته یا سند بیش از ۵ کیلو و نامه(۱)) بدست می آید
    specific_weight_table = ThirdPartyTable.objects.filter(
        zone=zone, 
        start_date__lte=datetime.date.today(), 
        end_date__gte=datetime.date.today(), 
        kind=4,
        granted = True).order_by('created').last()
    if weight > specific_weight_table.specific_weight:
        specific_weight = True
        thirdPartyTable_obj = specific_weight_table

        thirdPartyRow_obj = ThirdPartyRow.objects.filter(ThirdPartyTable=thirdPartyTable_obj.id).last()
        # calculate price:

        if thirdPartyRow_obj.is_fixed_rate:
            main_price = thirdPartyRow_obj.rate
        else:
            if thirdPartyRow_obj.minimum and thirdPartyRow_obj.minimum > 0:
                main_price =  thirdPartyRow_obj.minimum + ((weight - thirdPartyTable_obj.specific_weight)*thirdPartyRow_obj.rate)
            else:
                main_price = weight * thirdPartyRow_obj.rate
            # if (main_price:= weight * thirdPartyRow_obj.rate) < thirdPartyRow_obj.minimum : # if calculated price is less than minimun price in row model , use the  
            #     main_price = thirdPartyRow_obj.minimum

    else:
        thirdPartyTable_obj = ThirdPartyTable.objects.filter(zone=zone, start_date__lte=datetime.date.today(
        ), end_date__gte=datetime.date.today(), kind=kind, granted = True).order_by('created').last()


        thirdPartyRow_obj = ThirdPartyRow.objects.filter(from_weight__lt = weight , to_weight__gte=weight, ThirdPartyTable=thirdPartyTable_obj.id).order_by('to_weight').last()

        # calculate price:
        if thirdPartyRow_obj.is_fixed_rate:
            main_price= thirdPartyRow_obj.rate 
        else:
            main_price= weight * thirdPartyRow_obj.rate 


    result["Table"] = True
    result[
        "Table_desc"
    ] = "Congratulated, we find appropriate ThirdParty Table with given zone, date and kind"

    thirdRoundType = thirdPartyTable_obj.round
    thirdIsRoundPointFive = thirdPartyTable_obj.is_round_point_five
    thirdCurrency = thirdPartyTable_obj.currency.id
    thirdRoundKind = roundNumber.findRoundKind(
        thirdRoundType, thirdIsRoundPointFive
    )
    result["currency"] = thirdCurrency
    result["roundType"] = thirdRoundType
    result["isRoundPointFive"] = thirdIsRoundPointFive
    weight = roundNumber.rounding(thirdRoundKind, weight)
    result["roundWeight"] = weight
    result["Row"] = True
    result[
        "Row_desc"
    ] = "Congratulated we find ThirdParty Row with given weight"
    thirdIsFixedRate = thirdPartyRow_obj.is_fixed_rate
    thirdRate = thirdPartyRow_obj.rate
    result["thirdIsFixedRate"] = thirdIsFixedRate
    result["thirdRate"] = thirdRate
    # اگر قیمت به صورت فیکس به ازای بازه بود، نرخ مستقیم به عنوان هزینه در نظر گرفته می شود،
    # اگر به صورت فیکس نبود، هزینه می شود وزن ضربدر ضریب نرخ    
    
    result["thirdPrice"] = round(main_price, 1)

    result['hub'] = ["Dubai", 17] #TODO: make it dynamic not hard coded
    return result



