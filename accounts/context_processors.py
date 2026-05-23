from .models import Address

def default_address(request):
    if request.user.is_authenticated:
        address = Address.objects.filter(
            user=request.user,
            is_default=True
        ).first()
    else:
        address = None

    return {
        "default_address": address
    }
