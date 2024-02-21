from datetime import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import *
from .serializers import *
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


# api view for submitting and retrieving applicant passport photo
class SubmitApplicantBioData(APIView):
    def post(self, request):
        serializer = ApplicantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        data = Applicant.objects.all()
        serializer = ApplicantSerializer(data, many=True)
        return Response(serializer.data)


# api for adding and retriving all programs
class ProgramView(APIView):
    permission_classes = (AllowAny, IsAuthenticated, IsAdminUser)

    def get(self, request):
        data = Program.objects.all()
        serializer = ProgramSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api for submitting application
class ApplicantRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Validate applicant data
        serializer = ApplicantSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # Check if voucher code is valid
        voucher_code = request.data.get("voucher_code")
        if not voucher_code:
            return Response(
                {"error": "Voucher code is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            voucher = Voucher.objects.get(
                code=voucher_code, active=True, expiry_date__gt=timezone.now()
            )
        except Voucher.DoesNotExist:
            return Response(
                {"error": "Invalid or expired voucher code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if program exists
        try:
            program = Program.objects.get(pk=request.data.get("program"))
        except Program.DoesNotExist:
            return Response(
                {"error": "Invalid program ID"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if start date is in the future
        if request.data.get("start_date") < timezone.now().date():
            return Response(
                {"error": "Start date must be in the future"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if uploaded documents are valid
        for document_type, file in request.FILES.items():
            if document_type not in [
                "transcript",
                "wassce_certificate",
                "hnd_certificate",
                "degree_certificate",
            ]:
                return Response(
                    {"error": f"Invalid document type: {document_type}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                file.content_type
            except ValidationError:
                return Response(
                    {"error": f"Invalid file format for {document_type}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Create applicant
        applicant = serializer.save()

        # Create application
        application_data = {
            "applicant": applicant.id,
            "program": program.id,
            "voucher": voucher.id,
            "start_date": request.data.get("start_date"),
            "status": "pending",
        }
        application_serializer = ApplicationSerializer(data=application_data)
        try:
            application_serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        application = application_serializer.save()

        # Save uploaded documents (if there are any)
        for document_type, file in request.FILES.items():
            Document.objects.create(
                applicant=applicant,
                application=application,
                document_type=document_type,
                file=file,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
