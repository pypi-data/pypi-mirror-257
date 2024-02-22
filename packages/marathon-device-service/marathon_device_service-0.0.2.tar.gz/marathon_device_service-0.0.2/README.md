# Marathon Device Service Library

The Marathon Device Service library provides a streamlined approach for managing Marathon Cloud devices exclusively within the Marathon Cloud ecosystem. 
For additional details about the Marathon Cloud, please visit [MarathonLabs site](https://marathonlabs.io).

## Installation

Ensure you have Python 3.6+ installed, then use pip to install:

```bash
pip install marathon-device-service
```

## Quick Start

To use the library:
```python
from marathon_device_service import MarathonDeviceService

# Initialize the service
service = MarathonDeviceService()

# Upload a media file to the device's camera
service.camera.uploadMedia('/path/to/media/file.mp4')
```

Replace the file path with the actual media file you wish to upload.

## Support

For issues or feature requests, please contact our support team (em@marathonlabs.io).
