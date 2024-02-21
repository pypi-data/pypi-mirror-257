from PIL import Image
from django.core.exceptions import ValidationError


# passport photo validation
def validate_passport_photo(value):
    image = Image.open(value).convert("RGB")
    # check if the file is an image
    try:
        Image.open(value)
    except IOError:
        raise ValidationError("File is not an image")

    # make sure that the file is less than 4MB
    try:
        if value.size > 4 * 1024 * 1024:
            raise ValidationError("Passport Photo file size must not exceed 4MB")
    except AttributeError:
        pass

    width, height = image.size
    if width != 5184 or height != 3456:
        raise ValidationError("Photo must be 3456x5184 in width and height")

    # photo should have a white background
    if image.getpixel((0, 0)) > (246, 245, 253):
        raise ValidationError("Photo should have a white background")
    


# wassce, GCE, national_id validation
def validate_document(value):
    if value.size > 10 * 1024 * 1024:
        raise ValidationError("Document file size must not exceed 10MB")
    return value
