"""
Image Processing Service
Handles image validation, preprocessing, and optimization using Pillow
"""

from PIL import Image
import io
from typing import Tuple
from loguru import logger

from app.utils.error_handlers import ImageProcessingError


class ImageProcessor:
    """Service for processing uploaded images"""
    
    # Maximum dimensions for processed images
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1920
    
    # Supported formats
    SUPPORTED_FORMATS = {'JPEG', 'PNG', 'JPG', 'WEBP'}
    
    @staticmethod
    def validate_and_process_image(
        image_bytes: bytes,
        max_size_mb: int = 10
    ) -> Tuple[bytes, dict]:
        """
        Validate and process uploaded image
        
        Args:
            image_bytes: Raw image bytes
            max_size_mb: Maximum allowed file size in MB
            
        Returns:
            Tuple of (processed_image_bytes, metadata)
            
        Raises:
            ImageProcessingError: If image is invalid or processing fails
        """
        try:
            # Check file size
            size_mb = len(image_bytes) / (1024 * 1024)
            if size_mb > max_size_mb:
                raise ImageProcessingError(
                    f"Image too large. Maximum size: {max_size_mb}MB",
                    details={"size_mb": round(size_mb, 2)}
                )
            
            # Open image
            try:
                image = Image.open(io.BytesIO(image_bytes))
            except Exception as e:
                raise ImageProcessingError(
                    "Invalid image file",
                    details={"error": str(e)}
                )
            
            # Validate format
            if image.format not in ImageProcessor.SUPPORTED_FORMATS:
                raise ImageProcessingError(
                    f"Unsupported image format: {image.format}",
                    details={
                        "format": image.format,
                        "supported": list(ImageProcessor.SUPPORTED_FORMATS)
                    }
                )
            
            # Get original metadata
            metadata = {
                "original_width": image.width,
                "original_height": image.height,
                "format": image.format,
                "mode": image.mode,
                "size_mb": round(size_mb, 2)
            }
            
            # Process image
            processed_image = ImageProcessor._preprocess_image(image)
            
            # Convert to bytes
            output = io.BytesIO()
            processed_image.save(output, format='JPEG', quality=85, optimize=True)
            processed_bytes = output.getvalue()
            
            # Update metadata
            metadata["processed_width"] = processed_image.width
            metadata["processed_height"] = processed_image.height
            metadata["processed_size_mb"] = round(len(processed_bytes) / (1024 * 1024), 2)
            
            logger.info(f"✅ Image processed successfully: {metadata}")
            
            return processed_bytes, metadata
            
        except ImageProcessingError:
            raise
        except Exception as e:
            logger.error(f"Image processing failed: {e}")
            raise ImageProcessingError(
                "Failed to process image",
                details={"error": str(e)}
            )
    
    @staticmethod
    def _preprocess_image(image: Image.Image) -> Image.Image:
        """
        Preprocess image: resize, convert mode, optimize
        
        Args:
            image: PIL Image object
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert RGBA/LA/P to RGB
        if image.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            
            if image.mode == 'P':
                image = image.convert('RGBA')
            
            # Paste image on background
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[-1])
            else:
                background.paste(image)
            
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        if image.width > ImageProcessor.MAX_WIDTH or image.height > ImageProcessor.MAX_HEIGHT:
            # Calculate new size maintaining aspect ratio
            ratio = min(
                ImageProcessor.MAX_WIDTH / image.width,
                ImageProcessor.MAX_HEIGHT / image.height
            )
            new_width = int(image.width * ratio)
            new_height = int(image.height * ratio)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"Resized image to {new_width}x{new_height}")
        
        return image
    
    @staticmethod
    def create_thumbnail(
        image_bytes: bytes,
        size: Tuple[int, int] = (300, 300)
    ) -> bytes:
        """
        Create a thumbnail of the image
        
        Args:
            image_bytes: Original image bytes
            size: Thumbnail size (width, height)
            
        Returns:
            Thumbnail image bytes
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=80)
            
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Failed to create thumbnail: {e}")
            raise ImageProcessingError("Failed to create thumbnail")


# Global service instance
image_processor = ImageProcessor()

