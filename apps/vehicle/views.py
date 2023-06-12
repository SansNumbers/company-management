from django.shortcuts import render, redirect
from django.views.generic import ListView


class Vehicles(ListView):
    template_name = 'vehicles/vehicles.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('member:login')
        if request.user.company:
            return redirect('poll:index')
        return render(request, self.template_name, {})
