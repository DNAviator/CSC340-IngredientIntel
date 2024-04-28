from .forms import SearchForm
from .models import Profile

def user_color_mode(request):
  """
  Context processor to add user color mode to templates.
  """
  user = request.user
  user_color_mode = 'light'  # Default to light mode
  if user.is_authenticated:
    profile = Profile.objects.get_or_create(pk=user.id)
    user_color_mode = profile[0].color_mode
  return {'user_color_mode': user_color_mode}

def search_form(request):
    return {'search_form' : SearchForm() }

