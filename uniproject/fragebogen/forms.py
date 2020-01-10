# django imports
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# third party apps
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Row, Column, Div, HTML
from crispy_forms.bootstrap import PrependedText
# own apps

User = get_user_model()

# Choice options
CHOICES_Boolean = [
    ('True', _('Yes')),
    ('False', _('No')),
]


# Schätzfragen
class SmartphoneForm(forms.Form):
    antwort = forms.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Wie viele Menschen in Deutschland nutzen ein Smartphone? (in Mio)")

    def __init__(self, *args, **kwargs):
        super(SmartphoneForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-control'
        self.helper.field_class = 'col'


class GrenzeForm(forms.Form):
    antwort = forms.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Wie lang ist die deutsche Grenze zu Österreich?"
    )

    def __init__(self, *args, **kwargs):
        super(GrenzeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-control'
        self.helper.field_class = 'col'


class ZugspitzForm(forms.Form):
    antwort = forms.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Wie hoch ist die Zugspitze?"
    )

    def __init__(self, *args, **kwargs):
        super(ZugspitzForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-control'
        self.helper.field_class = 'col'


class AnteilStadtbevoelkerungForm(forms.Form):
    antwort = forms.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=5,
        decimal_places=2,
        help_text="Wie hoch ist der Anteil der Stadtbewohner an der "
                  "Gesamtbevölkerung in Deutschland?"
    )

    def __init__(self, *args, **kwargs):
        super(AnteilStadtbevoelkerungForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-control'
        self.helper.field_class = 'col'


class AltersAnteilsForm(forms.Form):
    antwort = forms.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=5,
        decimal_places=2,
        help_text="Wie viele Menschen zwischen 20 und 30 Jahren leben in Deutschland "
                  "(in Mio. auf eine Dezimalstelle gerundet)?"
    )

    def __init__(self, *args, **kwargs):
        super(AltersAnteilsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-control'
        self.helper.field_class = 'col'


class VWAnteilsForm(forms.Form):
    antwort = forms.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=5,
        decimal_places=2,
        help_text="Wie hoch ist der Marktanteil von Volkswagen in Deutschland?"
    )

    def __init__(self, *args, **kwargs):
        super(VWAnteilsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.form_class = 'form-control'
        self.helper.field_class = 'col'


# BooleanForms
CHOICES_HOCH_RICHTIG_TIEF = (
    (1, 'zu hoch'),
    (0, 'stimmt'),
    (-1, 'zu niedrig'),
)


class LondonEinwohnerForm(forms.Form):
    antwort = forms.ChoiceField(
        choices=CHOICES_HOCH_RICHTIG_TIEF,
        widget=forms.RadioSelect,
        required=True,
        help_text="London hat ca. 10 Mio. Einwohner."
    )

    def __init__(self, *args, **kwargs):
        super(LondonEinwohnerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


CHOICES_LIKERT = (
    (1, "trifft überhaupt nicht zu"),
    (2, "trifft nicht zu"),
    (3, "unentschlossen"),
    (4, "trifft zu"),
    (5, "trifft vollkommen zu")
)


class LikertTestForm(forms.Form):
    antwort = forms.ChoiceField(
        choices=CHOICES_LIKERT,
        widget=forms.RadioSelect,
        required=True,
        help_text="London hat ca. 10 Mio. Einwohner."
    )

    def __init__(self, *args, **kwargs):
        super(LikertTestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


form_list = [
    ('smartphone', SmartphoneForm),
    ('londoneinwohner', LondonEinwohnerForm),
    ('likertest', LikertTestForm)
]
