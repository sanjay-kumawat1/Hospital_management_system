from django.contrib import admin
from django.urls import path
from core import views as c
from accounts import views as a
from appointments import views as ap
from billing import views as b
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', c.home, name='home'),

    path('register/', a.register, name='register'),
    path('login/', a.login_view, name='login'),
    path('logout/', a.logout_view, name='logout'),

    path('dashboard/', c.dashboard, name='dashboard'),

    path('create/', ap.book_appointment, name='create'),
    # path('create-order/', ap.create_order, name='create_order'),
    # path('confirm-booking/', ap.confirm_booking, name='confirm_booking'),

    path('invoices/', b.invoices, name='invoices'),
    path('cancel/<int:appointment_id>/', ap.cancel_appointment, name='cancel_appointment')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)