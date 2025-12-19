"""Convert PNG icon to ICO format for PyInstaller"""
from PIL import Image

# Open the PNG image
img = Image.open('Icon/ic_launcher.png')

# Convert to ICO with multiple sizes
img.save('icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

print("✓ Icon converted successfully: icon.ico")
