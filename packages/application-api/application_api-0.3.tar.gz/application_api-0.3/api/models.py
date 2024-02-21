from django.db import models
from .validators import validate_passport_photo, validate_document

DOCUMENT_TYPES = (
    ("transcript", "Transcript"),
    ("wassce_certificate", "WASSCE Certificate"),
    ("hnd_certificate", "HND Certificate"),
    ("degree_certificate", "Degree Certificate"),
)
APPLICATION_STATUS = (
    ("pending", "Pending"),
    ("submitted", "Submitted"),
    ("rejected", "Rejected"),
)
GENDER_CHOICES = (("male", "Male"), ("female", "Female"))


# voucher model
class Voucher(models.Model):
    code = models.CharField(max_length=16, unique=True)
    active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code + " - " + str(self.active) + " - " + str(self.expiry_date)


# applicant model
class Applicant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100, null=True, blank=False)
    phone_number = models.CharField(max_length=16)
    nationality = models.CharField(max_length=100)
    email = models.EmailField()
    home_address = models.CharField(max_length=100)
    government_id_photo = models.FileField(upload_to="documents/")
    passport_photo = models.FileField(
        upload_to="documents/", validators=[validate_passport_photo]
    )

    def __str__(self):
        return self.first_name + " " + self.last_name 

    def get_passport_photo(self):
        if self.passport_photo:
            return "http://127.0.0.1:8000" + self.passport_photo.url
        return ""

    def get_government_id_photo(self):
        if self.government_id_photo:
            return "http://127.0.0.1:8000" + self.government_id_photo.url
        return ""


# program model
class Program(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    tuition_fee = models.IntegerField()

    def __str__(self):
        return self.name


# application model
class Application(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    voucher = models.OneToOneField(
        Voucher, null=False, unique=True, on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100, choices=APPLICATION_STATUS)


# document model
class Document(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/", validators=[validate_document])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
