import cv2
import base64
import numpy as np
from typing import List
from langchain_core.documents import Document
import logging
import json
log = logging.getLogger(__name__)

class VideoLoader:
    def __init__(self, file_path: str, num_frames: int = 32):
        """
        Initialize the VideoLoader.
        
        Args:
            file_path (str): Path to the video file
            num_frames (int): Number of frames to extract from the video
        """
        self.file_path = file_path
        self.num_frames = num_frames

    def _frame_to_base64(self, frame: np.ndarray) -> str:
        """
        Convert a frame to base64 encoded string.
        
        Args:
            frame (np.ndarray): The frame to convert
            
        Returns:
            str: Base64 encoded string of the frame
        """
        _, buffer = cv2.imencode('.jpg', frame)
        # {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,/9j
        ret = dict(type='image_url', image_url={'url': f'data:image/jpeg;base64,{base64.b64encode(buffer).decode("utf-8")}'})
        return ret

    def load(self) -> List[Document]:
        """
        Load the video file and extract frames.
        
        Returns:
            List[Document]: List of documents containing base64 encoded frames
        """
        try:
            # Open the video file
            cap = cv2.VideoCapture(self.file_path)
            
            if not cap.isOpened():
                raise Exception(f"Error opening video file: {self.file_path}")
            
            # Get video properties
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = total_frames / fps
            
            # Calculate frame intervals
            interval = total_frames / (self.num_frames + 1)
            
            frames = []
            for i in range(self.num_frames):
                # Set frame position
                frame_pos = int((i + 1) * interval)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
                
                # Read frame
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Convert frame to base64
                frame_base64 = self._frame_to_base64(frame)
                frames.append(frame_base64)
            
            # Release video capture
            cap.release()
            
            # Create metadata
            metadata = {
                "source": self.file_path,
                "total_frames": total_frames,
                "fps": fps,
                "duration": duration,
                "extracted_frames": len(frames)
            }
            
            # Create document with frames
            return [Document(page_content=json.dumps(frames), metadata=metadata)]
            
        except Exception as e:
            log.error(f"Error processing video file: {str(e)}")
            raise Exception(f"Failed to process video file: {str(e)}") 