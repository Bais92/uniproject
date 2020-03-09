from django.db import models
from django.contrib.auth import settings
from django.shortcuts import reverse

User = settings.AUTH_USER_MODEL

# models sind der Ort, an dem das Datenbankschema in Pythoncode dargestellt wird.
# WICHTIG: Sollten Änderungen direkt an der Datenbank durchgeführt werden, müssen diese zwingend auch hier
# geändert werden!!! Grundsätzlich ist von diesen Maßnahmen abzuraten. Dies betrifft inbesondere Änderungen an
# der Struktur der Datenbank bzw. der Tabellen. Hinzufügen von Zeilen sollte grundsätzlich endweder im Adminbereich
# oder über die Konsole durchgeführt werden (Über die Console funktioniert das wie folgt:
# 1. docker-compose -f local.yml run django python manage.py shell
# 2. from uniproject.fragebogen.models import Error
# 3. Error.objects.create(name="ich bin ein neuer Fehler").


# Create your models here.
class TimeStampedModel(models.Model):
    """
    Eine Klasse (Datenbankvorlage), die ein created und updated Field hinzufügt.
    """
    # ein abstract Model besitzt die Besonderheit bei der Initierung keine Datenbanktablle zu schreiben. Vielmehr wird
    # eine Datenbanktabelle erst dann erstellt, wenn eine Childclass erstellt wird. Vorteilhaft daran ist, dass
    # verschiedene Charakterisitka über mehrere Models hinweg geteilt und somit abstrahiert werden können.
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Benutzer(TimeStampedModel):
    """
    Datenbank für die Benutzer (Der Standard-User des Frameworks ist weiterhin vorhanden, hat aber einige weitere
    Restriktionen die nicht benötigt werden.
    """
    vorname = models.CharField(max_length=50)
    nachname = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        # als best practice empfiehlt es sich, immer eine __str__ Methode zu erstellen. Die standard Implementiertung
        # ist __repr__, welche wiederum "%s(%r)" % (self.__class__, self.__dict__) returnen sollte. Um einen lesbaren
        # Namen zu erhalten ist die __str__ Methode zu überschreiben (self ist hierbei der Pointer aud den
        # Instance und eine Besonderheit von Python).
        return '%s %s' % (self.nachname, self.email)


class Error(TimeStampedModel):
    """
    Datenbankmodel für die Verzerrung (Error ist in diesem Zusammenhang eventuell ein wenig missverständlich
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return '%s' % self.name


class Experiment(TimeStampedModel):
    """
    Datenbankmodel für die Experimente. An einem Experiment hängt der Hinweis (nudge) und eine Verzerrung (error)
    """
    # Hier wird ein "ManyToMany" Relation aufgebaut. Im Hintergrund wird eine Zwischentabelle erstellt, die die Tabellen
    # Benutzer und Experiment miteinander verbindet und jeweils mit einem Foreignkey contraint versieht. Hier ist eine
    # "ManyToMany Beziehung sinnvoll, da ein Benutzer mehrere Experimente ausfüllen kann und ein Experiment von mehreren
    # Benutzern ausgefüllt werden soll.
    error = models.ForeignKey(Error, on_delete=models.CASCADE)
    nudge = models.ForeignKey('Nudge', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s %s' % (self.error, self.nudge)

    def get_absolute_url(self):
        # diese Mehtode wird verwendet, wenn im Adminbereich eine Seitenansicht zur Erstell- und Updateansicht hinzu-
        # gefügt werden soll (Es gibt noch weitere Anwendungsfälle, wie den Redirect von Class Based Views, aber
        # das ist außerhalb der Thematik).
        return reverse('fragebogen:wizzard', kwargs={'pk': self.id})


class Question(TimeStampedModel):
    """
    Datenbank zum speichern der Fragen
    """
    question_type = models.CharField(max_length=30, help_text="Question Type", default='estimation')
    question = models.TextField()
    experiment = models.ManyToManyField(Experiment, through='QuestionExperiment')
    correct_answer_number = models.IntegerField()

    def __str__(self):
        return "%s %s " % (self.question_type, self.question)


class QuestionExperiment(TimeStampedModel):
    """
    Datenbank zum speichern
    """
    page = models.PositiveSmallIntegerField()
    # Falls das Experiment gelöscht wird, bleiben die Ergebnisse erhalten (SQL: "ON DELETE SET NULL". Alternativ kann
    # models.CASCADE verwendet werden welches dem SQL Statement "ON DELETE CASCADE" entspricht
    experiment = models.ForeignKey(Experiment, on_delete=models.SET_NULL, null=True, related_name='results')
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)

    class Meta:
        # hier wird ein SQL UNIQUE TOGETHER constraint eingeführt, um sicherzustellen, dass die SQL Abfragen
        # funktionieren
        unique_together = [('page', 'experiment', 'question'), ('page', 'experiment'), ('question', 'experiment')]

    def __str__(self):
        return '%s %s %s' % (self.experiment, self.question, self.page)

    def calculate_error_per_instance_number(self, answer):
        # benutzerdefinierte Methode, welche auf einer Zeile der Datenbank operiert. Custom Methods sollten immer dann
        # verwendet werden, wenn nur eine Zeile der Datenbank in Python verändert werden soll. Andernfalls ist
        # ein Custom Manager anzuwenden.
        correct_answer = self.question.correct_answer_number
        return answer - correct_answer


class Results(TimeStampedModel):
    user = models.ForeignKey(Benutzer, on_delete=models.SET_NULL, null=True, blank=True)
    questionexperiment = models.ForeignKey(QuestionExperiment, on_delete=models.CASCADE)
    # Antwort einer Schätzfrage. In der Datenbank muss sichergestellt sein, dass der Wert NULL annehmen kann (das ist
    # wichtig, falls andere Fragetypen hinzugefügt werden sollen und keine weitere Datenbank erstellt werden soll.
    # blank=True erlaubt Formularen einen leere Eingabe (diese wird bei der Initialisierung des Formulares
    # wieder aufgehoben, ist hier aber wichtig.
    answer_number = models.IntegerField(null=True, blank=True)
    # zur Zeit ist dieser Fehler nicht benutzt und wurde nur vorsorglich angelegt
    error = models.ForeignKey(Error, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s Experiment_id: %s' % (self.user, self.questionexperiment.experiment.id)


class Nudge(TimeStampedModel):
    # Definition von Auswahlmöglichkeiten (diese können als List (veränderbar) oder Tupel (unveränderbares) Object
    # angegeben werden. Die einzige Voraussetzung ist, dass es sich um ein iterierbares Object handelt (Dictionaries
    # sind im engeren Sinne nicht als iterierbar anzusehen, da hier das Problem der Insertionorder besteht).
    CHOICES_PRESENTATION_TYPE = [
        (None, 'Keine Hilfe'),
        (False, 'Falscher Hinweis (Umkekehrung des Vorzeichens)'),
        (True, 'Richtiger Hinweis')
    ]
    nudge_type = models.CharField(max_length=32)
    presentation_type = models.BooleanField(blank=True, null=True, default=None, choices=CHOICES_PRESENTATION_TYPE)

    def __str__(self):
        return '%s %s' % (self.nudge_type, self.get_presentation_type_display())


