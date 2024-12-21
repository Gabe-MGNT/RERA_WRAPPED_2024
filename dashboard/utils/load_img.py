from PIL import Image

# Charger l'image de la ligne de métro
image_path = 'assets/plan_rer__a.png'
img = Image.open(image_path)
img_width, img_height = img.size