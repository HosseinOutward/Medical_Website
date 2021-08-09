from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from base_app.CustomStuff import overwriteTempDicom
from user.models import UserProfile
from .serializers import *
from rest_framework import viewsets
from base_app.permissions import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import filters


class ImageDataAPI(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_queryset(self):
        queryset=ImagePatient.objects.all().order_by('real_time_imag').order_by('-label_data_imag')

        if self.suffix.lower() == 'list' and IsLabeler().has_permission(self.request, None):
            queryset = queryset.filter(assigned_doc_imag=self.request.user)
        elif IsUploader().has_permission(self.request, None):
            queryset = queryset.filter(label_data_imag=None)
        return queryset

    def get_serializer_class(self):
        serializer_class = ImageSerializer
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = ImageSerializerUpdate
        return serializer_class

    def get_permissions(self):
        permission_classes = [IsAuthenticated & (IsBoss | IsLabeler | IsUploader)]
        try: action = self.action.upper()
        except AttributeError: action = None
        if self.suffix == 'list' or action == 'PUT' or action == 'PATCH':
            permission_classes = [IsAuthenticated & (IsBoss | IsLabeler)]
        return [permission() for permission in permission_classes]

    def create(self, request):
        if request.FILES['image_imag'].name.lower().endswith('.dcm'):
            from sys import getsizeof
            pngTempFile = overwriteTempDicom(request.FILES['image_imag'].file)
            request.FILES['image_imag'].file = pngTempFile
            request.FILES['image_imag'].name = pngTempFile.name + ".png"
            request.FILES['image_imag'].size = getsizeof(pngTempFile)
        return super(ImageDataAPI, self).create(request)

    def update(self, request, pk, *args, **kwargs):
        object = ImagePatient.objects.filter(pk=pk).get()
        object.last_edited_by_imag = request.user
        object.save()
        return super(ImageDataAPI, self).update(request, *args, **kwargs)


class ImageListAPI(generics.ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated & (IsBoss | IsLabeler)]
    serializer_class = ImageSerializer
    queryset=ImagePatient.objects.all().order_by('-label_data_imag')
    filter_backends = [filters.SearchFilter]
    search_fields = ["real_id_imag", "owner_name_imag", "pet_name_imag"]


class Panel(LoginRequiredMixin, CreateView):
    model = ImagePatient
    fields = ['image_imag']
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Panel, self).get_context_data(**kwargs)
        context["imagepatient_list"] = ImagePatient.objects.all()
        # for a in context["imagepatient_list"]:
        #     a.creator_imag=UserProfile.objects.filter(pk=a.creator_imag).first().name_prof
        context["all_images_count"]=len(context["imagepatient_list"])
        context["labeled_images_count"]=len([0 for a in context["imagepatient_list"] if a.label_data_imag is not None])
        context["UserProfile"] = UserProfile.objects.filter(user_profile=self.request.user).get()

        context["isBoss"]=self.request.user.groups.filter(name='boss').exists()
        context["isUploader"]=self.request.user.groups.filter(name='uploader').exists()
        context["isLabeler"]=self.request.user.groups.filter(name='labeler').exists()

        return context

    def post(self, request, *args, **kwargs):
        if request.FILES['image_imag'].name.endswith('.dcm'):
            from sys import getsizeof
            pngTempFile = overwriteTempDicom(request.FILES['image_imag'].file)
            request.FILES['image_imag'].file = pngTempFile
            request.FILES['image_imag'].name = pngTempFile.name+".png"
            request.FILES['image_imag'].size = getsizeof(pngTempFile)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        # form.instance.patient_imag = Patient.objects.filter(pk=self.kwargs["patient_id"]).first()
        form.instance.creator_imag = self.request.user.pk
        form.instance.points_imag = []
        a = super().form_valid(form)
        # nnService(self.object.image_imag.url, self.kwargs['patient_id'], len(ImagePatient.objects.filter(patient_imag=self.kwargs["patient_id"]))-1)
        # nnService.delay(self.object.image_imag.url, self.kwargs['patient_id'], len(ImagePatient.objects.filter(patient_imag=self.kwargs["patient_id"]))-1)
        return a


@login_required
@api_view(['GET'])
def next_to_label(request):
    queryset=ImagePatient.objects.all().order_by('-label_data_imag')
    if IsBoss().has_permission(request, None):
        pass
    elif IsLabeler().has_permission(request, None):
        queryset = queryset.filter(assigned_doc_imag=request.user)
    else: return Response(status=status.HTTP_403_FORBIDDEN)

    next_url=queryset[0].get_absolute_url()

    return Response({"next_url": next_url}, status=status.HTTP_200_OK)


@login_required
@api_view(['GET'])
def round_robin(request):
    from math import ceil

    if not(request.user and request.user.groups.filter(name='boss')):
        return Response(status=status.HTTP_403_FORBIDDEN)

    all_obj=[img.pk for img in
             ImagePatient.objects.filter(label_data_imag=None)]
    all_labeler=User.objects.filter(groups__name='labeler')
    count=ceil(len(all_obj)/len(all_labeler))
    count=[[j for j in all_obj[i*count:(i+1)*count]]
           for i in range(len(all_labeler))]
    for pk_list, labeler in zip(count,all_labeler):
        ImagePatient.objects.filter(pk__in=pk_list).update(assigned_doc_imag=labeler)

    return Response(status=status.HTTP_200_OK)


def gen_context(request):
    userP = UserProfile.objects.filter(user_profile=request.user).get()
    isBoss=request.user.groups.filter(name='boss').exists()
    isUploader=request.user.groups.filter(name='uploader').exists()
    isLabeler=request.user.groups.filter(name='labeler').exists()
    return {"UserProfile": userP, "isBoss":isBoss, "isUploader":isUploader, "isLabeler":isLabeler}


def user_assignment_view(request, *args, **kwargs):
    return render(request, 'user_assignment.html', gen_context(request))


def edit_image_data_view(request, pk, *args, **kwargs):
    context=gen_context(request)
    context["object"]=ImagePatient.objects.filter(pk=pk).get()
    return render(request, 'edit_initial_image_data.html', context)


def labeling_view(request, pk, *args, **kwargs):
    context=gen_context(request)
    context["object"]=ImagePatient.objects.filter(pk=pk).get()
    return render(request, 'label.html', context)


def list_all_view(request, *args, **kwargs):
    return render(request, 'listing.html', gen_context(request))


def upload_view(request, *args, **kwargs):
    return render(request, 'uploader.html', gen_context(request))
