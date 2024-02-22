# Marathon Device Service Library

The Marathon Device Service library facilitates easy uploading of media files to Marathon Cloud devices. It's designed to seamlessly integrate into the Marathon Cloud ecosystem, enabling efficient media management.

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

# Upload a media file
service.camera.uploadMedia('/path/to/media/file.mp4')
```

Replace the file path with the actual media file you wish to upload.

## Support

For issues or feature requests, please contact our support team.
