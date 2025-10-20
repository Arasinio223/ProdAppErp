
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from .models import Uzytkownik, ZlecenieProdukcyjne, DziennikZdarzenRCP, StatusPracy
from .serializers import DziennikZdarzenRCPSerializer
from rest_framework import permissions

@api_view(['GET'])
def user_view(request):
    user = request.user
    return Response({
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
    })

@api_view(['GET'])
def status_view(request, user_id):
    try:
        ostatnie_zdarzenie = DziennikZdarzenRCP.objects.filter(uzytkownik__id=user_id).latest('timestamp')
        return Response({'status': ostatnie_zdarzenie.status.nazwa})
    except DziennikZdarzenRCP.DoesNotExist:
        return Response({'status': 'Brak'})

@api_view(['GET'])
def zlecenia_view(request):
    zlecenia = ZlecenieProdukcyjne.objects.filter(aktywne=True)
    return Response([{'id': z.id, 'nazwa': z.nazwa} for z in zlecenia])

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    login_val = request.data.get('login')
    pin = request.data.get('pin')
    try:
        user = Uzytkownik.objects.get(username=login_val)
        if check_password(pin, user.pin):
            login(request, user)
            return Response({'message': 'Login successful'})
    except Uzytkownik.DoesNotExist:
        pass

    # Handle RFID login
    rfid_id = request.data.get('rfid_id')
    if rfid_id:
        try:
            user = Uzytkownik.objects.get(rfid_id=rfid_id)
            login(request, user)
            return Response({'message': 'Login successful'})
        except Uzytkownik.DoesNotExist:
            pass
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def change_status_view(request):
    user_id = request.data.get('user_id')
    status_nazwa = request.data.get('status')
    zlecenie_id = request.data.get('zlecenie_id')
    try:
        user = Uzytkownik.objects.get(id=user_id)
        status_pracy = StatusPracy.objects.get(nazwa=status_nazwa)
        zlecenie = None
        if zlecenie_id:
            zlecenie = ZlecenieProdukcyjne.objects.get(id=zlecenie_id)
        DziennikZdarzenRCP.objects.create(uzytkownik=user, status=status_pracy, zlecenie=zlecenie)
        return Response({'message': 'Status changed successfully'})
    except (Uzytkownik.DoesNotExist, StatusPracy.DoesNotExist, ZlecenieProdukcyjne.DoesNotExist):
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

class DziennikZdarzenRCPViewSet(viewsets.ModelViewSet):
    queryset = DziennikZdarzenRCP.objects.all()
    serializer_class = DziennikZdarzenRCPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        employee_id = self.request.query_params.get('employee_id')
        # department filtering would require adding a department field to the user model
        if start_date and end_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        if employee_id:
            queryset = queryset.filter(uzytkownik__id=employee_id)
        return queryset

import pandas as pd
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .forms import UploadFileForm
from .models import Uzytkownik, ZlecenieProdukcyjne

def import_zlecenia(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                # Assuming Excel columns are: Nazwa, Numer, Klient
                zlecenie, created = ZlecenieProdukcyjne.objects.get_or_create(
                    numer=row['Numer'],
                    defaults={
                        'nazwa': row['Nazwa'],
                        'klient': row['Klient'],
                    }
                )
            return render(request, 'import_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'import_form.html', {'form': form})

def import_users(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                # Assuming Excel columns are: Imie, Nazwisko, Dzial, Login, PIN, RFID_ID, Stawka_godzinowa
                user, created = Uzytkownik.objects.get_or_create(
                    username=row['Login'],
                    defaults={
                        'first_name': row['Imie'],
                        'last_name': row['Nazwisko'],
                        'pin': make_password(str(row['PIN'])),
                        'rfid_id': row.get('RFID_ID'),
                        'stawka_godzinowa': row.get('Stawka_godzinowa'),
                    }
                )
            return render(request, 'import_success.html')
    else:
        form = UploadFileForm()
    return render(request, 'import_form.html', {'form': form})
