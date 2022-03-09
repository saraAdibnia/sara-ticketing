import random
from user.models.quotations_model import Quotations
from user.models.faalHafez import Faals

# get random faal from Hafez
def RandomFaalHafez():

    randomNumber = random.randint(1, 495)
    Faal_obj = Faals.objects.filter(id=randomNumber).first()
    result = {
        "Poem": Faal_obj.poem,
        "Interpretion": Faal_obj.interpretion,
    }
    return result


# get random Quotation
def RandomQuote():
    randomNumber = random.randint(1, 2000)
    Quotaion_obj = Quotations.objects.filter(id=randomNumber).first()
    result = {
        "author": Quotaion_obj.author,
        "quotation": Quotaion_obj.quotation,
    }
    return result
