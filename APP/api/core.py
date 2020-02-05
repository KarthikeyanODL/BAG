import os
from zipfile import ZipFile

import settings
import yaml
from werkzeug.utils import secure_filename


# Method to delete all known-images/csv from file disk
def delete_files(file_path):
    try:

        for the_file in os.listdir(file_path):
            path = os.path.join(file_path, the_file)
            try:
                if os.path.isfile(path):
                    os.remove(path)
            except Exception:
                raise Exception("Unable to remove the Files")

    except Exception:
        raise Exception("Unable to delete all known-images from File Disk ")


# Method to create bundle
def convert_yaml(json_object):
    try:
        manifest_path = os.path.join(settings.DATA_PATH, "manifest.yaml")
        manifest_file = open(manifest_path, 'w')
        yaml.dump(json_object, manifest_file)

    except Exception as exc:
        print(exc)
        raise Exception("Unable to create bundle")


def create_bundle(request):
    try:
        convert_yaml(request.json)
        print(get_encoded_zip_file())
    except Exception as exc:
        print(exc)
        raise Exception("Unable to create bundle")


# Method to save the zip file
def save_file_to_disk(request):
    try:

        response = request.files['file']
        os.chdir(settings.BUNDLE_PATH)
        response.save(secure_filename(response.filename))
        file_path = os.path.join(settings.BUNDLE_PATH, response.filename)

     except Exception :
         raise  Exception("Unable to save the zip file")
     try:
        extract_all(file_path)
        #os.remove(file_path)
     except Exception as exception :
        print ("zipfile") 
        #raise Exception(exception)


# Method to extract all known-images from the zip file
def extract_all(file_path):
    try:
        zip_ref = ZipFile(file_path, 'r')
        zip_ref.extractall(settings.BUNDLE_PATH)
        zip_ref.close()
    except Exception:
        raise Exception("Unable to extract the ZIP file")


# Method to get all files path
def get_all_file_paths(directory):

    file_paths = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_paths.append(os.path.join(directory, file))
    return file_paths


# Method to zip the encoded files
def get_encoded_zip_file():

    try:
        directory = settings.DATA_PATH
        file_paths = get_all_file_paths(directory)
        zip_file_name = 'bundle_files.zip'

        os.chdir(directory)
        with ZipFile(zip_file_name, 'w') as zip:
            for file in file_paths:
                zip.write(file,file[file.rfind('/'):])
    except Exception:
        raise Exception("Unable to zip the encoded files")
    return os.path.join(directory, zip_file_name)
