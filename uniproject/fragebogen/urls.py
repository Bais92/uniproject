from django.urls import path

# own imports
from .views import formlist_wizard, ThankYouView

# In diesem Skript werden die jeweiligen URL gerouted, d. h. eine Anfrage wird hier auf den jeweiligen View
# weitergeleitet. Der Code der Views liegt unter fragebogen.views

app_name = "fragebogen"
urlpatterns = [
    path("<int:pk>/", formlist_wizard, name="wizzard"),
    path('thank-you/', ThankYouView.as_view(), name="thank-you")
]
