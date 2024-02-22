import os
import requests
import logging
import magic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarathonDeviceService:
    def __init__(self):
        self.endpoint = os.getenv('CAMERA_SERVICE_ENDPOINT')
        if not self.endpoint:
            raise EnvironmentError("""
CAMERA_SERVICE_ENDPOINT environment variable is not set. 
Most likely, the library was used not in Marathon Cloud environment. 
Please contact the development team for assistance.""")
        self.camera = self.Camera(self.endpoint)

    class Camera:
        def __init__(self, endpoint):
            self.endpoint = endpoint

        def uploadMedia(self, file_path):
            assert self.endpoint is not None, "CAMERA_SERVICE_ENDPOINT must be set."

            mime_type = magic.Magic(mime=True).from_file(file_path)
            logger.info(f"Using determined MIME type: {mime_type} for file: {file_path}")

            files = {'file': (os.path.basename(file_path), open(file_path, 'rb'), mime_type)}
            logger.info("Start the request to upload the new media for camera...")
            response = requests.post(self.endpoint, files=files)
            
            # Log the status code, message, and body of the response
            logger.info(f"Upload Status: {response.status_code}")
            if response.text:
                logger.info(f"Response Body: {response.text}")
            else:
                logger.info("Response Body is empty.")
