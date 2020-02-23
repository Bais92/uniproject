from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect, reverse


from formtools.wizard.views import SessionWizardView
# own imports
from .forms import fragen, Frage1Form, NudgeForm, UserForm
from .models import Question, QuestionExperiment


# Create views.
class FormListWizzard(SessionWizardView):
    """
    Um alle Forms anzugezeigen und das Management der Speicherung und weiterer essentieller Methoden zu gewährleisten
    wird hier eine Application verwendet (formtools: https://django-formtools.readthedocs.io/en/latest/wizard.html).
    """

    def get_form_kwargs(self, step=None):
        """
        Methode, um die Keywordarguments (**kwargs) der __init__ Methode der einzelnen Forms zu füllen. Hierbei muss
        beachtet werden, dass die verschiedenen Forms unterschiedliche kwargs benötigen. Deshalb werden diese hier
        konditional für die verschiedenen Forms befüllt
        für den Hinweis wird die Berechnung des Fehlers benötigt. Dieser setzt sich aus der Different der korrekten
        Antwort und der vom Ausfüller gegeben Antwort zusammen. Der Fehler ist additiv.
        Vorgehen:
        1. Die gegebene Antwort wird in einem for-loop ausgelesen
        2. Die jeweils richtige Antwort wird aus der Datenbank abgerufen. Zuerst:
        SELECT "fragebogen_questionexperiment"."id", "fragebogen_questionexperiment"."created",
        "fragebogen_questionexperiment"."modified", "fragebogen_questionexperiment"."page",
        "fragebogen_questionexperiment"."experiment_id", "fragebogen_questionexperiment"."question_id"
        FROM "fragebogen_questionexperiment" WHERE
        ("fragebogen_questionexperiment"."experiment_id" = 1 AND "fragebogen_questionexperiment"."page" = 1)
        SELECT fragebogen_question"."correct_answer_number" FROM "fragebogen_question"
        INNER JOIN "fragebogen_questionexperiment" ON
        ("fragebogen_question"."id" = "fragebogen_questionexperiment"."question_id")
        WHERE "fragebogen_questionexperiment"."id" = 1
        Die zweite SQL-Query wurde hier exemplarisch als Model Method durchgeführt. Model Methods werden dann benutzt,
        wenn man auf einem Instance des Models (einer einzelen Zeile in der Datenbanktablle) eine Operation
        durchführen will.
        (siehe auch: https://docs.djangoproject.com/en/3.0/topics/db/managers/#adding-extra-manager-methods).

        kwargs sind immer bzw. insbesondere in den aufrufenden Methoden immer Dictionaries. Damit andere Methoden
        keine Fehler auswerfen (z.B. wenn diese kwargs.update() abrufen) wird hier auch ein Dictionary verwendet.
        """
        kwargs = {}
        if step is 'nudge':
            error = 0
            for page in range(0, 2):
                answer = self.get_cleaned_data_for_step(str(page))['answer_number']
                correct_answer = QuestionExperiment.objects.get(experiment_id=self.kwargs['pk'], page=page)
                error += correct_answer.calculate_error_per_instance_number(answer)
            kwargs['calculated_error'] = error
            kwargs['experiment'] = self.kwargs['pk']
        if step == 'name':
            # Die Initialisierung (__init__ Mehtode) der UserForm (zum abfragen der Benutzerdaten) benötigt keine
            # weiteren kwargs. Deshalb werden die kwargs in diesem Schritt wieder "zurückgesetzt", bzw. überschrieben.
            kwargs = {}
        elif step is not 'nudge':
            # Die Initialisierung aller anderen Forms benötigt als **kwargs den Primary Key des Experiments. Deshalb
            # werden die kwargs in diesem Schritt mit dem pk aus der URL abgerufe (Django übernimmt hierbei in der
            # __init__ Methode der zugrundeliegden Base Class (Hier View) die Initialisierung der **kwargs aus den URL
            # Parametern.
            # nachzulesen hier: https://github.com/django/django/blob/master/django/views/generic/base.py)
            kwargs['experiment'] = self.kwargs['pk']
        # Da die Methode von anderen Methoden aufgerufen wird und diese darauf aufbauen muss hier auch ein return Value
        # gegeben werden. In diesem Fall wird das Dictionary der Keyword Arguments wiedergegeben.
        return kwargs

    def done(self, form_list, **kwargs):
        """
        diese Methode wird erst abgerufen, sobald die letzte Form abgeschickt wurde und alle Form Daten validiert und
        cleaned (durch die to_python Method im FormField) wurden. Diese Methode is ZWINGEND zu implementieren.

        im Falle dieses Fragebogens wird zuerst der Benutzer gespeichert. Hierfür eignet sich die get_form Methode,
        die als Argumente den step und die Daten benötigt. Der Name der Userform wurde in der form_list ("fragen") als
        'name' definiert und hier abgerufen. Der return Wert der get_form Methode is ein Form Instance der UserForm.
        Dieser wird mit den data, hier den POST Data "befüllt" und gespeichert. Jetzt wird der volle Umfang der
        ModelForm deutlich in genau einer Zeile werden die ausgefüllten Daten in der Datenbank gespeichert.
        Mit den weiteren Fragen wird ähnlich verfahren. Hierzu werden in einem for-loop die Forms aus der form_list
        (hier der "fragen") abgerufen und geprüft, dass es sich nicht um einen Instance der NudgeForm oder UserForm
        handelt. Falls dies der Fall ist, wird die Form gespeichert. Hierbei ist folgendes zu beachten: Im Falle von
        ModelForms ist das vorgehen von Django zweistufig. Zuerst werden die Daten in der Form gespeichert und
        validiert. In einem zweiten Schritt werden die Daten in die Datenbank gespeichert. Dies mag anfangs nicht viel
        Sinn ergeben, allerdings wird diese Vorgehen hier ausgenutzt. Durch das setzten des Arguments commit=False
        wird das Speichern in die Datenbank verhindert. Dies ermöglicht es weitere wichtige Informationen wie den
        Benutzer hinzuzufügen und in einem SQL Statement zu speichern ohne das Risiko einzugehen beim speichern etwas
        falsch angegeben zu haben.
        Zum Schluss wird der User noch umgeleitet. Hierbei wird die Klasse HttpResponseRedirect verwendet (falls Test
        geschrieben werden sollten, muss auf den Status Code 302 nicht 200 getestet werden). Die Funktion reverse
        ist auch eine Shortcut Funktion. Da in urls.py immer darauf geachtet wurde ein name Argument bzw. namespace
        Argument anzugeben.
        """
        user = self.get_form(step='name', data=self.request.POST).save()
        for form in form_list:
            if not isinstance(form, NudgeForm) and not isinstance(form, UserForm):
                result = form.save(commit=False)
                result.user = user
                result.save()
        return HttpResponseRedirect(reverse('home'))


# Da die Klasse zur Zeit nur eine Python Klasse ist, muss diese in den request-response Zyklus eingeführt werden. Hier
# verwenden alle Class Based Views (CBV) eine Form der Methode .as_view(), welche neben der initialisierung der
# Initialparameter auch den gesamten Setup der HTTP-Request und HTTP Response übernimmt. Das Modul SessionWizzard
# überschreibt die Methode der zugrundeliegenden Base Class allerdings und ermöglicht so weitere Argumente wie form_list
# auszufüllen (template_name ist eine Variable der Base Class TemplateView).
formlist_wizard = FormListWizzard.as_view(
    form_list=fragen,
    template_name='fragebogen/fragebogen.html'
)
