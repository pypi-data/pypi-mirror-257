from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Voucher, Applicant, Application, Document, Program


# voucher serializer
class VoucherSerializer(ModelSerializer):
    class Meta:
        model = Voucher
        fields = "__all__"


# applicant serializer
class ApplicantSerializer(ModelSerializer):
    passport_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Applicant
        fields = "__all__"

    def get_passport_photo_url(self, obj):
        return obj.get_passport_photo()


# application serializer
class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"


# document serializer
class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"

class ProgramSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = "__all__"