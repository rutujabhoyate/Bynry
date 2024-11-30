from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ServiceRequest
from .forms import ServiceRequestForm
from django.contrib.auth.decorators import login_required

# Customer views
@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user
            service_request.save()
            return redirect('track_requests')
    else:
        form = ServiceRequestForm()
    return render(request, 'submit_request.html', {'form': form})

@login_required
def track_requests(request):
    service_requests = ServiceRequest.objects.filter(customer=request.user)
    return render(request, 'track_requests.html', {'service_requests': service_requests})

# Admin views (staff only)
@login_required
def manage_requests(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)

    service_requests = ServiceRequest.objects.all()
    return render(request, 'manage_requests.html', {'service_requests': service_requests})

@login_required
def resolve_request(request, request_id):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=401)

    service_request = ServiceRequest.objects.get(id=request_id)
    service_request.resolve()
    return redirect('manage_requests')

