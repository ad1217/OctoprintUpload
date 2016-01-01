# OctoPrint Upload #

This is a plugin for Cura (> 15.06) that allows uploading to an Octoprint server.

## Installation ##
Install [Requests](http://docs.python-requests.org/en/latest/) for python 3.

Clone this reposiory (or [download it as a zip](https://github.com/ad1217/OctoprintUpload/archive/master.zip) and extract it) to Cura's `plugins` directory. This directory wont exist if you don't already have plugins, but it should be in the same place as the [settings directory](https://github.com/Ultimaker/Cura/wiki/Cura-Preferences-and-Settings-Locations). For example, in Linux you should put it here:

    $HOME/.local/share/cura/plugins/OctoprintUpload

## Configuration ##
There isn't any GUI configuration yet, so for the moment you will need to add the following to the [Preferences file](https://github.com/Ultimaker/Cura/wiki/Cura-Preferences-and-Settings-Locations).

```
[octoprint]
base_url = http://your.server:port/
api_key = YOUR_OCTOPRINT_API_KEY
```

Note that the trailing `/` in `base_url` is required.

There are two other options that can also be set (see [the Octoprint documentation](http://docs.octoprint.org/en/master/api/fileops.html#upload-file) for more details):

| Key    | Description                                               | Default Value |
| ------ | --------------------------------------------------------- | ------------- |
| select | Whether to select the file directly after upload.         | True          |
| print  | Whether to start printing the file directly after upload. | False         |

## Todo ##
  * GUI Configuration
  * Progress bar
  * (Maybe) remove dependency on requests (it would make it easier to install, but much more complicated to write)
