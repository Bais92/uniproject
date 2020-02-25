from django.urls import path

# own imports
from .views import formlist_wizard, ThankYouView


app_name = "fragebogen"
urlpatterns = [
    path("<int:pk>/", formlist_wizard, name="wizzard"),
    path('thank-you/', ThankYouView.as_view(), name="thank-you")
]
