import os
import tarfile
from zipfile import ZipFile
import settings
import yaml
from werkzeug.utils import secure_filename

"""
1 Method to create bundle
"""
def create_bundle(request):
    try:
        convert_yaml(request.json)
        archieve_zip_file()
    except Exception as exc:
        print(exc)
        raise Exception("Unable to create bundle")

"""
2 Method to convert json to yaml
"""
def convert_yaml(json_object):
    try:
        manifest_path = os.path.join(settings.DATA_PATH, "manifest.yaml")
        # validate the  yaml
        try:
            yaml.safe_load(yaml.dump(json_object))
        except Exception:
            raise Exception("Yaml is not a Valid")
        manifest_file = open(manifest_path, 'w')
        yaml.dump(json_object, manifest_file)

    except Exception as exc:
        print(exc)
        raise Exception("Unable to create bundle")

"""
3 Method to create zip file
"""
def archieve_zip_file():
    try:
        os.chdir(settings.BUNDLE_PATH)
        with tarfile.open("./robin-bundle/bundle.tar.gz", "w:gz") as tar_handle:

            for root, dirs, files in os.walk('./inventory'):
                for file in files:
                     tar_handle.add(os.path.join(root, file))
    except Exception:
        raise Exception("Unable to zip the encoded files")
"""
3 Method to create zip file
"""
def get_bundle_zip():
    try:
        bundle_name = 'bundle.tar.gz'
        return os.path.join(settings.ZIP_PATH,bundle_name)
    except Exception:
        raise Exception("Unable to get the bundle")


"""
4 Method to delete all known-images/csv from file disk
"""
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



"""
5 Method to save the zip file
"""
def save_file_to_disk(request):
    try:

        response = request.files['file']
        os.chdir(settings.BUNDLE_PATH)
        response.save(secure_filename(response.filename))
        file_path = os.path.join(settings.BUNDLE_PATH, response.filename)

    except Exception:
        raise Exception("Unable to save the zip file")
    try:
        extract_all(file_path)
        # os.remove(file_path)
    except Exception as exception:
        print("zipfile")
        # raise Exception(exception)

"""
6 Method to extract all known-images from the zip file
"""
def extract_all(file_path):
    try:
        zip_ref = ZipFile(file_path, 'r')
        zip_ref.extractall(settings.BUNDLE_PATH)
        zip_ref.close()
    except Exception:
        raise Exception("Unable to extract the ZIP file")

"""
7 Method to get all files path
"""
def get_all_file_paths(directory):
    file_paths = []
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_paths.append(os.path.join(directory, file))
    return file_paths

