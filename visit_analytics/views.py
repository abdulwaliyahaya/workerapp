from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from visit_analytics.models import Worker, Unit, Visit
import json



@csrf_exempt
def get_units(request):
    phone_number = request.POST.get('number')
    try:
        worker = Worker.objects.get(phone_number=phone_number)
    except Worker.DoesNotExist:
        return JsonResponse({'message': 'worker with phone number does not exist'}, safe=False, status=404)

    units = Unit.objects.filter(worker=worker).values('pk', 'name')
    if units:
        serialized_units = json.dumps(list(units))
        return JsonResponse({'units': serialized_units}, safe=False, status=200)
    else:
        return JsonResponse({'message': 'user does not have units associated yet'}, safe=False, status=200)

@csrf_exempt
def make_visit(request, pk, longitude, latitude):
    phone_number = request.POST.get('number').strip()
    try:
        unit = Unit.objects.get(pk=pk)
    except Unit.DoesNotExist:
        return JsonResponse({'message': 'Unit does not exist'}, safe=False, status=404)
    unit_worker_phonenumber = unit.worker.phone_number.strip()
    if unit_worker_phonenumber != phone_number:
        return JsonResponse({'message': 'You are not associated with this unit'}, safe=False, status=403)
    else:
        new_visit = Visit()
        new_visit.unit = unit
        new_visit.longitude = longitude
        new_visit.latitude = latitude
        new_visit.save()
        return JsonResponse({'message': 'visit created successfully'}, safe=False, status=200)
