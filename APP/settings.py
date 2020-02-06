import os

# Settings for file path
APP_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
BUNDLE_PATH = os.path.join(APP_ROOT_PATH, "bundles")
DATA_PATH = os.path.join(BUNDLE_PATH, "inventory")
ZIP_PATH = os.path.join(BUNDLE_PATH, "robin-bundle")
