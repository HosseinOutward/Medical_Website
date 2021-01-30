def overwriteTempDicom(image_data):

    # *************
    from django.core.files.temp import NamedTemporaryFile
    import pydicom
    import numpy as np
    import cv2

    ds = pydicom.dcmread(image_data)

    # get header data
    fieldnames = ['SpecificCharacterSet', 'SOPClassUID', 'SOPInstanceUID', 'StudyDate', 'StudyTime', 'AccessionNumber',
                  'Modality', 'ConversionType', 'ReferringPhysicianName', 'SeriesDescription', 'PatientName', 'PatientID',
                  'PatientBirthDate', 'PatientSex', 'PatientAge', 'BodyPartExamined', 'ViewPosition', 'StudyInstanceUID',
                  'SeriesInstanceUID', 'StudyID', 'SeriesNumber', 'InstanceNumber', 'PatientOrientation', 'SamplesperPixel',
                  'PhotometricInterpretation', 'Rows', 'Columns', 'PixelSpacing', 'BitsAllocated', 'BitsStored', 'HighBit',
                  'PixelRepresentation', 'LossyImageCompression', 'LossyImageCompressionMethod', 'PixelData']
    header_data = []
    for field in fieldnames:
        try:
            header_data.append(ds.data_element(field))
        except KeyError:
            header_data.append(None)

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
