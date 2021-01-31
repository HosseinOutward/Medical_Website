from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from patient.models import ImagePatient
from django.shortcuts import redirect
import json
from django.shortcuts import get_object_or_404

base_url = "http://127.0.0.1:8000"


@login_required
def image_data_api(request, pk=None):
    if request.method == 'GET':
        obj=get_object_or_404(ImagePatient,pk=pk)

    if request.method == 'PUT':
        obj=get_object_or_404(ImagePatient,pk=pk)

    if request.method == 'POST':
        from django import forms
        class MyModelForm(forms.ModelForm):
            class Meta:
                model = ImagePatient
                fields = ['class_type_imag', 'label_string_imag']

        form = MyModelForm(request.POST)
        if form.is_valid():
          form.save()
          return HttpResponse(status_code=200)

    return HttpResponse(status_code=400)


from patient.serializers import ImageSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class ImageDataAPI(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer
    queryset = ImagePatient.objects.all()


# @login_required
# def getImage(request, patient_id, image_id):
#     object=ImagePatient.objects.filter(patient_imag=patient_id)
#     if len(object)<=image_id: return HttpResponse("")
#
#     object = object[image_id]
#     if object.patient_imag.doctor_pati != request.user: return HttpResponse("")
#
#     image_url=object.image_imag.url
#     return redirect(base_url+image_url)
#     # return HttpResponse(base_url+image_url)
#
#
# @login_required
# def getImageList(request, patient_id):
#     objectList=ImagePatient.objects.filter(patient_imag=patient_id)
#     if objectList[0] and objectList[0].patient_imag.doctor_pati != request.user: return True
#
#     urlList=[base_url+ImClass.image_imag.url for ImClass in objectList]
#     return JsonResponse(json.dumps(urlList), safe=False)
#
#
# @login_required
# def getPoints(request, patient_id, image_id):
#     object=ImagePatient.objects.filter(patient_imag=patient_id)[image_id]
#     if object.patient_imag.doctor_pati != request.user: return True
#
#     points = object.points_imag
#     return JsonResponse(json.dumps(points), safe=False)
#
# @login_required
# def setPoints(request, patient_id, image_id):
#     object=ImagePatient.objects.filter(patient_imag=patient_id)[image_id]
#     if object.patient_imag.doctor_pati != request.user: return True
#
#     if request.method == 'POST':
#         import json
#         object.points_imag=[ [j["xpos"], j["ypos"]] for j in json.loads(request.body)["POINTS"] ]
#         object.save()
#     return HttpResponse('')
#
#
# # new stuff
# @login_required
# def getLabel(request, patient_id, image_id):
#     object = ImagePatient.objects.filter(patient_imag=patient_id)[image_id]
#     if object.patient_imag.doctor_pati != request.user: return True
#
#     img_label = object.label_string_imag
#     return JsonResponse(json.dumps(img_label), safe=False)
#
#
# @login_required
# def setLabel(request, patient_id, image_id):
#     object=ImagePatient.objects.filter(patient_imag=patient_id)[image_id]
#     if object.patient_imag.doctor_pati != request.user: return True
#
#     if request.method == 'POST':
#         import json
#         object.label_string_imag = json.loads(request.body)["LABEL"]
#         object.save()
#     return HttpResponse('')
#
#
# @login_required
# def getList(request, patient_id):
#     objectList=ImagePatient.objects.filter(patient_imag=patient_id)
#     if objectList[0] and objectList[0].patient_imag.doctor_pati != request.user: return True
#
#     list_of_all=[]
#     for i, img in enumerate(objectList):
#         img_format = img.image_imag.url.split(".")[-1]
#         img_class = img.class_type_imag
#         img_editor_link = base_url+"/patient/"+str(patient_id)+"/"+str(i)+"/"
#         list_of_all.append(json.dumps({"link": img_editor_link, "class": img_class, "format": img_format}))
#     return JsonResponse(json.dumps(list_of_all), safe=False)
