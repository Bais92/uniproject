from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(QuestionExperiment)

admin.site.register(Error)
admin.site.register(Results)
admin.site.register(Nudge)
admin.site.register(Benutzer)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


class QuestionExperimentReadOnlyInline(admin.StackedInline):
    """Object für die Darstellung des QuestionExperiment im Adminbereich"""
    model = QuestionExperiment
    extra = 0
    readonly_fields = ['id', 'page', 'experiment', 'question']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


class QuestionExperimentInline(admin.StackedInline):
    """Object für die Darstellung des QuestionExperiment im Adminbereich"""
    model = QuestionExperiment


class ExperimentAdmin(admin.ModelAdmin):
    view_on_site = False
    search_fields = ['id']
    inlines = [
        QuestionExperimentInline
    ]
    list_display = (
        'URL',
    )
    readonly_fields = (
        'URL',
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        # access the request object when in the change view
        self.request = request
        return super(ExperimentAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def changelist_view(self, request, extra_context=None):
        # access the request object when in the list view
        self.request = request
        return super(ExperimentAdmin, self).changelist_view(request, extra_context=extra_context)

    def URL(self, obj):
        if obj.pk is None:
            return 'Bitte erst das Experiment speichern. Die URL wird dann angezeigt'

        else:
            return u'{url}'.format(
                # access the request object through self.request, as set by the two view functions
                # this is actually a bad practice, however sufficent.
                url=self.request.build_absolute_uri(reverse('fragebogen:wizzard', args=(obj.pk,)))
            )

    URL.allow_tags = True


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        QuestionExperimentReadOnlyInline
    ]


admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Question, QuestionAdmin)
