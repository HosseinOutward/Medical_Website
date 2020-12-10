from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from patient.models import ImagePatient
from django.shortcuts import redirect
import json
import random

@login_required
def getImage(request, patient_id, image_id):
    object=ImagePatient.objects.filter(patient_imag=patient_id)[image_id]
    if object.patient_imag.doctor_pati != request.user: return True

    image_url=object.image_imag.url
    return redirect("http://127.0.0.1:8000"+image_url)
    # return HttpResponse("http://127.0.0.1:8000"+image_url)


@login_required
def getImageList(request, patient_id):
    objectList=ImagePatient.objects.filter(patient_imag=patient_id)
    if objectList[0] and objectList[0].patient_imag.doctor_pati != request.user: return True

    urlList=["http://127.0.0.1:8000"+ImClass.image_imag.url for ImClass in objectList]
    return JsonResponse(json.dumps(urlList), safe=False)


@login_required
def getPoints(request, patient_id, image_id):
    object=ImagePatient.objects.filter(patient_imag=patient_id)[image_id]
    if object.patient_imag.doctor_pati != request.user: return True
   
    points = object.points_imag   
    return JsonResponse(json.dumps(points), safe=False)

@login_required
def setPoints(request, patient_id, image_id):
    object=ImagePatient.objects.filter(patient_imag=patient_id)[image_id]
    if object.patient_imag.doctor_pati != request.user: return True

    if request.method == 'POST':
        import json
        object.points_imag=[ [j["xpos"], j["ypos"]] for j in json.loads(request.body)["POINTS"] ]
        object.save()
    return HttpResponse('')
