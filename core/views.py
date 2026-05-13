from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from appointments.models import Appointment

def dashboard(request):
    try:
        patient = request.user.patient
    except:
        patient = None

    if patient:
        appointments = Appointment.objects.filter(patient=patient).order_by('-date_time')
    else:
        appointments = []

    context = {
        'appointments': appointments,
        'total_appointments': len(appointments),
        'has_appointments': len(appointments) > 0
    }

    return render(request, 'dashboard.html', context)