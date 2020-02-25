# django imports
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# third party apps
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Row, Column, Div, HTML
from crispy_forms.bootstrap import PrependedText
# own apps

from uniproject.fragebogen.models import QuestionExperiment, Question, Results, Experiment, Benutzer

User = get_user_model()


class AntwortNummerForm(forms.ModelForm):
    page = None
    answer_number = forms.IntegerField()

    class Meta:
        model = Results
        fields = ['answer_number']

    def __init__(self, *args, **kwargs):
        self.experiment_id = kwargs.pop('experiment')
        super(AntwortNummerForm, self).__init__(*args, **kwargs)
        if not self.page:
            raise ImproperlyConfigured("Es wurde keine Seite (page) angegeben")
        experiment = Experiment.objects.get(id=self.experiment_id)
        self.questionexperiment = QuestionExperiment.objects.get(experiment=experiment, page=self.page)
        question = Question.objects.get(experiment=experiment, questionexperiment__page=self.page)
        self.fields['answer_number'].label = question.question
        self.helper = FormHelper()
        self.helper.form_tag = False

    def save(self, commit=True):
        instance = super(AntwortNummerForm, self).save(commit=False)
        instance.questionexperiment = self.questionexperiment
        if commit:
            instance.save()
        return instance




class Frage1Form(AntwortNummerForm):
    page = 1


class Frage2Form(AntwortNummerForm):
    page = 2


class Frage3Form(AntwortNummerForm):
    page = 3


class Frage4Form(AntwortNummerForm):
    page = 4


class Frage5Form(AntwortNummerForm):
    page = 5


class Frage6Form(AntwortNummerForm):
    page = 6


class Frage7Form(AntwortNummerForm):
    page = 7


class Frage8Form(AntwortNummerForm):
    page = 8


class Frage9Form(AntwortNummerForm):
    page = 9


class Frage10Form(AntwortNummerForm):
    page = 10


class Frage11Form(AntwortNummerForm):
    page = 11


class Frage12Form(AntwortNummerForm):
    page = 12


class Frage13Form(AntwortNummerForm):
    page = 13


class Frage14Form(AntwortNummerForm):
    page = 14


class Frage15Form(AntwortNummerForm):
    page = 15


class Frage16Form(AntwortNummerForm):
    page = 16


class Frage17Form(AntwortNummerForm):
    page = 17


class Frage18Form(AntwortNummerForm):
    page = 18


class Frage19Form(AntwortNummerForm):
    page = 19


class Frage20Form(AntwortNummerForm):
    page = 20



class NudgeForm(forms.Form):
    nudge = forms.CharField(label='Hinweis:', required=False)

    def __init__(self, *args, **kwargs):
        self.experiment_id = kwargs.pop('experiment', None)
        self.error = kwargs.pop('calculated_error', None)
        super(NudgeForm, self).__init__(*args, **kwargs)
        nudge = Experiment.objects.get(id=self.experiment_id).nudge.presentation_type
        if nudge is None:
            self.fields['nudge'].widget = forms.HiddenInput()
        elif self.error and nudge is False:
            self.error = - self.error
        if self.error:
            message = 'Sie haben bei den letzten Fragen eher zu %s geantwortet' % ('hoch' if self.error >= 0 else 'niedrig')
            self.fields['nudge'].initial = message
        self.fields['nudge'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False


class UserForm(forms.ModelForm):

    class Meta:
        model = Benutzer
        fields = ['vorname', 'nachname', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


fragen = [
    (0, Frage1Form),
    (1, Frage2Form),
    (2, Frage3Form),
    (3, Frage4Form),
    (4, Frage5Form),
    (5, Frage6Form),
    (6, Frage7Form),
    (7, Frage8Form),
    (8, Frage9Form),
    (9, Frage10Form),
    ('nudge', NudgeForm),
    (11, Frage11Form),
    (12, Frage12Form),
    (13, Frage13Form),
    (14, Frage14Form),
    (15, Frage15Form),
    (16, Frage16Form),
    (17, Frage17Form),
    (18, Frage18Form),
    (19, Frage19Form),
    (20, Frage20Form),
    ('name', UserForm)
]
