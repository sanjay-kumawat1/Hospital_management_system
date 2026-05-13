import json

from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from billing.models import Invoice
from datetime import datetime, date

def book_appointment(request):

    doctors = Doctor.objects.all()
    today = date.today().strftime('%Y-%m-%d')

    # ✅ GET DATA FROM URL (after Razorpay redirect)
    doctor_id = request.GET.get('doctor')
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')

    # ✅ If data comes from URL → process booking
    if doctor_id and date_str and time_str:

        try:
            patient = request.user.patient
        except:
            patient = Patient.objects.first()

        if not patient:
            return render(request, 'appointmentform.html', {
                'doctors': doctors,
                'today': today,
                'error': 'No patients found'
            })

        doctor = get_object_or_404(Doctor, id=doctor_id)

        date_time = datetime.strptime(
            f"{date_str} {time_str}",
            "%Y-%m-%d %H:%M"
        )

        # ❌ prevent double booking
        if Appointment.objects.filter(doctor=doctor, date_time=date_time).exists():
            return render(request, 'appointmentform.html', {
                'doctors': doctors,
                'today': today,
                'error': 'Doctor not available at this time'
            })

        # ✅ create appointment
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date_time=date_time
        )

        patient_name = patient.user.username if hasattr(patient, 'user') else str(patient)

        Invoice.objects.create(
            patient_name=patient_name,
            patient_phone=getattr(patient, "phone", ""),
            appointment_details=f"Dr. {doctor.user.username} | {date_time.strftime('%d/%m/%Y %I:%M %p')}",
            amount=doctor.fee,
            due_date=date_time.date()
        )

        return redirect('invoices')

    # ✅ normal page load (GET without params)
    return render(request, 'appointmentform.html', {
        'doctors': doctors,
        'today': today
    })



def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if not hasattr(request.user, 'patient'):
        return redirect('/login')

    if appointment.patient != request.user.patient:
        return redirect('/dashboard')

    if appointment.status != 'booked':
        return redirect('/dashboard')

    appointment.status = 'cancelled'
    appointment.save()

    return redirect('/dashboard')