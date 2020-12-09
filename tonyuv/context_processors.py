from accounts.models import Profile
from cart.models import CartItem
def addDropdownCartToContext(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        print(request.user)
        user_profile = Profile.objects.get(user=request.user)
        cart = CartItem.objects.filter(user=user_profile).all()
        return {
            'cart': cart
        }
    else:
        return {
            'cart': None
        }