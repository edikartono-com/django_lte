from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

def handle_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})