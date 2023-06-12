from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import View


class WorkerActivateView(View):
    success_message = "You successfully confirmed your email. Please login."
    error_message = "Link is invalid. Please contact administrator."

    def get(self, request, *args, **kwargs):
        worker = get_user_model().objects.filter(verification_token=request.GET['verification_token']).last()
        if not worker or worker.verification_token.created < timezone.now() - timedelta(minutes=15):
            messages.error(request, self.error_message)
            return redirect('member:login')
        if not worker.is_active:
            worker.is_active = True
            worker.save()
            worker.verification_token.delete()
        messages.success(request, self.success_message)
        return redirect('member:login')
