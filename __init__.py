from . import OctoprintUpload

def getMetaData():
    return {
        "plugin": {
            "name": "Octoprint Uploader Output Device",
            "description": "Enables uploading to an octoprint server",
            "author": "Adam Goldsmith",
            "version": "1.0",
            "api": 2,
        }
    }

def register(app):
    return { "output_device": OctoprintUpload.OctoprintUploadOutputDevicePlugin() }
