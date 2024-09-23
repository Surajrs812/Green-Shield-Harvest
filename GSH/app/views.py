from django.shortcuts import render
from django.http import JsonResponse

# Home view
def home_view(request):
    return render(request, 'home.html')

# Raspberry Pi camera view with JSON sidebar
def pi_view(request):
    # Assuming demo.json data
    demo_data = {
        "device": "Raspberry Pi",
        "status": "active",
        "temp": "55°C",
        "uptime": "3 days, 12:45"
    }
    return render(request, 'pi_view.html', {'demo_data': demo_data})

# JSON output for HTMX request
def demo_json_view(request):
    demo_data = {
        "device": "Raspberry Pi",
        "status": "active",
        "temp": "55°C",
        "uptime": "3 days, 12:45"
    }
    return JsonResponse(demo_data)
