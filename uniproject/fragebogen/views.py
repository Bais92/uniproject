from django.shortcuts import render, redirect, render_to_response


from formtools.wizard.views import SessionWizardView
#own imports
from .forms import form_list


# Create your views here.
class FormListWizzard(SessionWizardView):
    def done(self, form_list, **kwargs):
        return render(self.request, 'fragebogen/done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

formlist_wizard = FormListWizzard.as_view(
    form_list=form_list,
    #condition_dict=condition_dict,
    template_name='fragebogen/fragebogen.html'
)
