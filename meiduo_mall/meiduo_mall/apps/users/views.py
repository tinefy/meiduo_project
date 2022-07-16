from django.shortcuts import render

# Create your views here.
from django.views import View


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username=request.POST.get('username')
        print(username)
        return render(request, 'register.html')
