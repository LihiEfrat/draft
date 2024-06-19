from django.shortcuts import render
import json
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Therapist, Patient, ProfessionalDetails, Preferences, Exercise,Training,ExercisePlan
from .serializers import TherapistRegistrationSerializer,TherapistSerializer, PatientRegisterSerializer, PatientSerializer, ProfessionalDetailsSerializer, PreferencesSerializer, ExerciseSerializer,TrainingSerializer, ExercisePlanSerializer

from django.contrib.auth.hashers import check_password

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ExerciseSerializer
from rest_framework.exceptions import ValidationError

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .upload_video import upload_video_to_youtube
from django.core.files.storage import default_storage
import os


class CustomLoginView(APIView):
    def match_passwords(self, input_password, obj):
        if check_password(input_password, obj.password):
            return obj
        else:
            return None
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Attempt to authenticate the user
        therapist = Therapist.objects.filter(email=email).first()
        patient = Patient.objects.filter(email=email).first()
        if therapist:
            user = self.match_passwords(password, therapist)
            is_therapist = True
        elif patient:
            user = self.match_passwords(password, patient)
            is_therapist = False
        else:
            # User with the provided email does not exist
            return Response({'detail': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if user is not None:
            # Authentication successful
            return Response({'is_therapist': is_therapist}, status=status.HTTP_200_OK)
        else:
            # Invalid credentials
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class TherapistRegistrationView(APIView):
    def post(self, request):
        serializer = TherapistRegistrationSerializer(data=request.data)
        print(serializer)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)

class PatientRegistrationView(APIView):
    def post(self, request):

        # Convert request data to dict if it is not already
        data = request.data.dict() if isinstance(request.data, dict) else request.data
        
        # Parse the preferences JSON string to a dictionary
        if 'preferences' in data:
            try:
                data['preferences'] = json.loads(data['preferences'])
            except json.JSONDecodeError:
                return Response({'error': 'Invalid JSON for preferences field'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PatientRegisterSerializer(data=data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TherapistViewSet(viewsets.ModelViewSet):
    queryset = Therapist.objects.all()
    serializer_class = TherapistSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class ProfessionalDetailsViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalDetails.objects.all()
    serializer_class = ProfessionalDetailsSerializer

class PreferencesViewSet(viewsets.ModelViewSet):
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer

# class TrainingView(APIView):
#     def post(self, request):
#         serializer = TrainingSerializer(data=request.data)
#         if serializer.is_valid():
#             training = serializer.save()
#             return Response(TrainingSerializer(training).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TrainingView(APIView):
    def post(self, request):
        print('Request data:', request.data)  # Add this line to print the request.data
        serializer = TrainingSerializer(data=request.data)
        if serializer.is_valid():
            training = serializer.save()
            return Response(TrainingSerializer(training).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
class ExercisePlanView(APIView):
    def post(self, request):
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

class ExercisePlanViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ExerciseViewSet(viewsets.ModelViewSet): 
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    


@api_view(['POST'])
def create_exercise(request):
    if request.method == 'POST':
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def upload_video_view(request):
    if request.method == 'POST':
        video = request.FILES['file']
        file_name = default_storage.save(video.name, video)
        file_url = default_storage.path(file_name)
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        tags = request.POST.get('tags', [])

        try:
            video_id = upload_video_to_youtube(file_url, title, description, "22", tags)
    
            exercise = Exercise(
                name=title,
                category=category,
                description=description,
                videoUrl=video_id,  # Store the YouTube video ID
                approval=False  # Assuming approval is False initially
            )
            exercise.save()

            return JsonResponse({'video_id': video_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        finally:  
            if os.path.exists(file_url):
                os.remove(file_url)

    if os.path.exists(file_url):
       os.remove(file_url)

    return JsonResponse({'error': 'Invalid request method'}, status=400)  

