from django.db import models
from extra_scripts.timestampmodel import TimeStampedModel

class Country(TimeStampedModel):
    """کشور"""

    fname = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="country name in persian",
    )

    ename = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="country name in english",
    )

    code = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="country 2 digit code",
        unique= True ,
    )

    code3 = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="country 3 digit code",
    )

    capital = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="country capital city. not related to city. only characters",
    )

    postal_code_format = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="country postal code format",
    )

    postal_code_regex = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="country postal code regex",
    )

    def __str__(self):
        if self.ename:
            return self.ename
        else:
            return str(self.id)

class State(TimeStampedModel):
    """استان"""

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="specifies the country that state is in it.",
        related_name= 'state_country',
    )

    fname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="state name in persian",
    )

    ename = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="state name in english",
    )

    ename_std = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="standard form of state name in english (best practice and better than ename)",
    )

class City(TimeStampedModel):
    """شهر"""

    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="specifies the state that city is in it.",
    )


    fname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="persian name of the city",
    )

    ename = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="english name of the city",
    )

    timezone = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        help_text="city timezone in characters and not +- from greenwich?",
    )

    def __str__(self):
        return self.ename_std or ' '
        
class DialCode(TimeStampedModel):
    """
    this table contains info about dial codes for phone numbers in every country
    NOTE: no relationship with country table mentioned in place app. country names are stored here as charfield.
    NOTE: A dial code is not unique for every country.
    """

    fname = models.CharField(
        blank=True,
        null=True,
        max_length=225,
        help_text="persian name of the country",
    )

    ename = models.CharField(
        blank=True,
        null=True,
        max_length=225,
        help_text="standard english name of the country",
    )

    code = models.CharField(
        blank=True,
        null=True,
        max_length=225,
        help_text="2 digit code for the country",
    )

    dial_code = models.CharField(
        blank=True,
        null=True,
        max_length=225,
        help_text='dial code with a "+" at first and the rest of it is integer',
    )

    def __str__(self):
        return self.ename