from django.urls import path

# own imports
from .views import formlist_wizard


app_name = "fragebogen"
urlpatterns = [
    path("<int:pk>/", formlist_wizard, name="wizzard")
]
