from django.urls import path
from .views import *

urlpatterns = [
    # endpoint for submitting applicant data
    path("submit_applicant/", SubmitApplicantBioData.as_view()),
    #endpoint for applying
    path("apply/", ApplicantRegistrationAPIView.as_view()),
]
