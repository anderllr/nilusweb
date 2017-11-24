from accounts.models import User
from nilusadm.models import Permissions
from principal.models import Instancia
from django.contrib.auth.decorators import login_required



def permissions(request):

    if request.user.is_authenticated():
        permissions = Permissions.objects.get(user=request.user)
        return {'permissions': permissions}
    else:
        return {'permissions':[]}



