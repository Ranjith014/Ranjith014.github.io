from PIL import Image
import torchvision.transforms as transforms

class ImagePreprocessor:
    def __init__(self, image_size=(224, 224)):
        self.transform = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def preprocess(self, image_path):
        """Loads and preprocesses an image from a given path."""
        image = Image.open(image_path).convert("RGB")
        return self.transform(image).unsqueeze(0)