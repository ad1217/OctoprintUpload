#!/usr/bin/env python3

import requests
import random
import string
from io import StringIO

from UM.Application import Application
from UM.Preferences import Preferences
from UM.Logger import Logger
from UM.Mesh.MeshWriter import MeshWriter
from UM.Mesh.WriteMeshJob import WriteMeshJob
from UM.OutputDevice.OutputDevicePlugin import OutputDevicePlugin
from UM.OutputDevice.OutputDevice import OutputDevice
from UM.OutputDevice import OutputDeviceError
from UM.Message import Message

##  Implements an OutputDevicePlugin that provides a single instance of OctoprintUploadOutputDevice
class OctoprintUploadOutputDevicePlugin(OutputDevicePlugin):
    def __init__(self):
        super().__init__()

        Preferences.getInstance().addPreference("octoprint/select", True)
        Preferences.getInstance().addPreference("octoprint/print", False)
        Preferences.getInstance().addPreference("octoprint/base_url", "")
        Preferences.getInstance().addPreference("octoprint/api_key", "")

    def start(self):
        self.getOutputDeviceManager().addOutputDevice(OctoprintUploadOutputDevice())

    def stop(self):
        self.getOutputDeviceManager().removeOutputDevice("octoprint")

##  Implements an OutputDevice that supports saving to arbitrary local files.
class OctoprintUploadOutputDevice(OutputDevice):
    stream = None
    def __init__(self):
        super().__init__("octoprint")

        self.setName("Octoprint")
        self.setShortDescription("Upload to Octoprint")
        self.setDescription("Upload to Octoprint")
        self.setIconName("save")

        self._writing = False

    def requestWrite(self, node, file_name = None):
        if self._writing:
            raise OutputDeviceError.DeviceBusyError()

        self.writeStarted.emit(self)
        mesh_writer = Application.getInstance().getMeshFileHandler().getWriterByMimeType("text/x-gcode")
        self.stream = StringIO()

        job = WriteMeshJob(mesh_writer, self.stream, node, MeshWriter.OutputMode.TextMode)
        job.setFileName(file_name + ".gcode")
        job.progress.connect(self._onJobProgress)
        job.finished.connect(self._onWriteJobFinished)

        message = Message("Uploading as {0}".format(file_name), 2)
        message.show()

        job._message = message
        self._writing = True
        job.start()

    def _onJobProgress(self, job, progress):
        if hasattr(job, "_message"):
            job._message.setProgress(progress)
        self.writeProgress.emit(self, progress)

    def _onWriteJobFinished(self, job):
        if hasattr(job, "_message"):
            job._message.hide()
            job._message = None

        self._writing = False
        self.writeFinished.emit(self)
        if job.getResult():
            self.writeSuccess.emit(self)
            self.stream.seek(0)
            gcode = self.stream
            fileName = job.getFileName()
            selectBool = str(Preferences.getInstance().getValue("octoprint/select")).lower()
            printBool = str(Preferences.getInstance().getValue("octoprint/print")).lower()
            r = requests.post(Preferences.getInstance().getValue("octoprint/base_url") + "api/files/local",
                              files = {'file': (fileName, gcode),
                                       'select': ('', selectBool),
                                       'print': ('', printBool)},
                              headers={'User-agent': 'Cura AutoUploader Plugin',
                                       'X-Api-Key': Preferences.getInstance().getValue("octoprint/api_key")})

            message = Message("Succesfully Uploaded {0}, Response Code {1}".format(job.getFileName(), r.status_code))
            message.show()

        else:
            message = Message("Failed to upload {0}".format(job.getFileName()))
            message.show()
            self.writeError.emit(self)
        job.getStream().close()