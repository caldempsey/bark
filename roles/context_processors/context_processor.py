from roles.models import UserRoles


def user_roles(request):
    user = request.user
    if user.is_authenticated():
        user = request.user
        roles = UserRoles.objects.filter(user=user).values_list('role', flat=True)
    else:
        roles = []
    return {'roles': roles}
