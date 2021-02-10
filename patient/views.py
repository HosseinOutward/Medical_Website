from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from base_app.CustomStuff import overwriteTempDicom
from user.models import UserProfile
from .serializers import *
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class ImageDataAPI(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return sorted(ImagePatient.objects.all(), key=lambda t: t.label_data_imag is None, reverse=True)

    def get_serializer_class(self):
        serializer_class = ImageSerializer
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = ImageSerializerUpdate
        return serializer_class

    def create(self, request):
        if request.FILES['image_imag'].name.lower().endswith('.dcm'):
            from sys import getsizeof
            pngTempFile = overwriteTempDicom(request.FILES['image_imag'].file)
            request.FILES['image_imag'].file = pngTempFile
            request.FILES['image_imag'].name = pngTempFile.name + ".png"
            request.FILES['image_imag'].size = getsizeof(pngTempFile)
        return super(ImageDataAPI, self).create(request)


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


class ImageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ImagePatient
    template_name = 'patient/image_confirm_delete.html'

    def get_object(self):
        object=ImagePatient.objects.filter(patient_imag=self.kwargs["patient_id"])[self.kwargs["image_id"]]
        self.pk=object.pk
        return object

    def get_success_url(self):
        return reverse('patient-detail', kwargs={'pk': self.kwargs["patient_id"]})

    def test_func(self):
        patient = self.get_object().patient_imag
        if patient.doctor_pati == self.request.user:
            return True
        return False


class LabelingView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = ImagePatient
    template_name = 'label.html'
    success_message = "label has been set"

    def get_queryset(self):
        return ImagePatient.objects.all()

    def get_context_data(self, **kwargs):
        context = super(LabelingView, self).get_context_data(**kwargs)
        context["UserProfile"] = UserProfile.objects.filter(user_profile=self.request.user).get()
        return context


class UploadView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = ImagePatient
    template_name = 'uploader.html'
    success_message = "Image has been added"

    def get_context_data(self, **kwargs):
        context = super(UploadView, self).get_context_data(**kwargs)
        context["UserProfile"] = UserProfile.objects.filter(user_profile=self.request.user).get()
        return context
