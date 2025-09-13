from .ProfileUrls import urlpatterns as ProfileUrls
from .AuthUrls import urlpatterns as AuthUrls
from .PasswordResetUrls import urlpatterns as PasswordResetUrls
from .FacilityUrls import urlpatterns as FacilityUrls
from .AppointmentUrls import urlpatterns as AppointmentUrls
from .ConsultationUrls import urlpatterns as ConsultationUrls
from .PrescriptionUrls import urlpatterns as PrescriptionUrls
from .SymptomUrls import urlpatterns as SymptomUrls  # add this

urlpatterns = (
    ProfileUrls 
    + AuthUrls 
    + PasswordResetUrls 
    + FacilityUrls 
    + AppointmentUrls 
    + ConsultationUrls 
    + PrescriptionUrls
    + SymptomUrls 
)
