from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict
import json


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_count', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


def is_labeled(image_imag):
    label_string = image_imag.label_data_imag
    if label_string == None: return "No Label"

    data_label = json.loads(label_string)
    label_fields = {
        "keypointlabels": ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12",
                           "T13", "Max Aortic diameter dorsal", "Max Aortic diameter ventral", "carina",
                           "Apex", "Dorsal border of CVC", "ventral CVC", "Cranial"],
        "polygonlabels": ["Heart", "CVC", "Aorta"],
        "rectanglelabels": ["region 1", "region 2", "region 3"]
    }

    for label in data_label[:-1]:
        try:
            label_type = label["type"]
            label_name = label['value'][label_type][0]
            if not label_name in label_fields[label_type]: return "Wrong Label Type"
        except: return "Wrong Label Type"

    should_be_len = 1 + sum([len(label_fields[a]) for a in label_fields.keys()])
    if len(data_label) != should_be_len: return "Wrong Count"

    return "Image Labeled"


def overwriteTempDicom(image_data):
    # *************
    from django.core.files.temp import NamedTemporaryFile
    import pydicom
    import numpy as np
    import cv2

    ds = pydicom.dcmread(image_data)

    # get header data
    # fieldnames = ['SpecificCharacterSet', 'SOPClassUID', 'SOPInstanceUID', 'StudyDate', 'StudyTime', 'AccessionNumber',
    #               'Modality', 'ConversionType', 'ReferringPhysicianName', 'SeriesDescription', 'PatientName', 'PatientID',
    #               'PatientBirthDate', 'PatientSex', 'PatientAge', 'BodyPartExamined', 'ViewPosition', 'StudyInstanceUID',
    #               'SeriesInstanceUID', 'StudyID', 'SeriesNumber', 'InstanceNumber', 'PatientOrientation', 'SamplesperPixel',
    #               'PhotometricInterpretation', 'Rows', 'Columns', 'PixelSpacing', 'BitsAllocated', 'BitsStored', 'HighBit',
    #               'PixelRepresentation', 'LossyImageCompression', 'LossyImageCompressionMethod', 'PixelData']
    # header_data = []
    # for field in fieldnames:
    #     try:
    #         header_data.append(ds.data_element(field))
    #     except KeyError:
    #         header_data.append(None)

    # fix DICOM data
    image_2d = ds.pixel_array.astype(float)
    image_2d = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
    image_2d = np.uint8(image_2d)
    _, image_2d = cv2.imencode(".png", image_2d)
    # *************
    image_data.close()

    png_file=NamedTemporaryFile()
    png_file.write(image_2d)

    return png_file


def load_images(initial_path, name_ext):
    from os import listdir
    from os.path import isfile, join
    from PIL.Image import open as open_image
    from patient.models import ImagePatient
    from Medical_Website.settings import MEDIA_ROOT
    from datetime import datetime
    from django.utils.timezone import make_aware
    from shutil import copyfile
    from os.path import join as path_join
    from os import listdir

    current_objects = ImagePatient.objects.all()
    current_objects = [e.image_imag.name for e in current_objects]

    current_folder = listdir(path_join(MEDIA_ROOT,
                ImagePatient.image_imag.field.upload_to.replace("\\\\", "/")))

    list_files = [f for f in listdir(initial_path)
                  if isfile(join(initial_path, f))]
    animal_type_choices={a[1]:a[0] for a in ImagePatient.animal_type.field.choices}

    print("starting to load images one by one")
    for file_name in list_files:
        print()
        print(file_name)

        if file_name.endswith('.dcm'):
            print("is DCM file")
            continue
        if len([e for e in current_objects if file_name in e])!=0 \
           or file_name in current_folder:
            print("already in db")
            continue

        try:
            upload_to_path = path_join(
                ImagePatient.image_imag.field.upload_to.replace("\\\\", "/"),
                name_ext+file_name)
            path_to_save = path_join(MEDIA_ROOT, upload_to_path)

            open_image(path_join(initial_path, file_name))
            copyfile(path_join(initial_path, file_name), path_to_save)

            name_parsed=file_name.split(".")[0]
            if name_parsed.count("^")==1:
                name_parsed=name_parsed.split("^")
                owner_name=name_parsed[0]
                if owner_name.count("_")==1:
                    pet_name=owner_name.split("_")[1]
                    owner_name=owner_name.split("_")[0]
                else: pet_name=None
                name_parsed=name_parsed[1]
            name_parsed=name_parsed.split("_")
            animal_type= name_parsed[0]
            real_id=name_parsed[1]

            real_time=name_parsed[2].split("-")
            real_time=[int(a) for a in real_time]
            real_time=make_aware(datetime(real_time[0],real_time[1],real_time[2]))

            real_counter=name_parsed[3]

            ImagePatient.objects.create(
                image_imag=upload_to_path, owner_name_imag=owner_name,
                pet_name_imag=pet_name, real_id_imag=real_id,
                animal_type=animal_type_choices[animal_type.lower()],
                real_time_imag=real_time, real_id_count_imag=real_counter)
        except Exception as e:
            print("***error processing this file***:" + file_name)
            print(repr(e))
            print(e)
            print(e.args)


# from rest_framework.decorators import api_view
# @api_view(['GET'])
# def aasdasd(request):
#     from rest_framework.response import Response
#     from rest_framework import status
#
#     # from patient.models import ImagePatient
#     # obj=ImagePatient.objects.first()
#     # obj.thumbnail_imag = ""
#     # obj.save()
#     load_images(r"/root/97_res", "")
#
#     from timeit import default_timer as timer
#     start = timer()
#     load_images(r"C:\Users\No1\Desktop\a", "")
#     print(timer() - start)
#
    # return Response(status=status.HTTP_200_OK)