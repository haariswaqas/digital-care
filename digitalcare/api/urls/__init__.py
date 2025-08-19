from .ProfileUrls import urlpatterns as ProfileUrls
from .AuthUrls import urlpatterns as AuthUrls
from .PasswordResetUrls import urlpatterns as PasswordResetUrls

urlpatterns = (
    ProfileUrls + AuthUrls + PasswordResetUrls
    
)
