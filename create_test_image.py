#!/usr/bin/env python3
"""
Create a simple test PNG image for testing the converter.
"""

from PIL import Image, ImageDraw

# Create a simple logo-like image
img = Image.new('RGB', (200, 200), color='white')
draw = ImageDraw.Draw(img)

# Draw a simple shape (circle with text-like elements)
draw.ellipse([50, 50, 150, 150], fill='#3498db', outline='#2980b9', width=3)
draw.rectangle([90, 80, 110, 120], fill='white')
draw.ellipse([85, 95, 95, 105], fill='white')
draw.ellipse([105, 95, 115, 105], fill='white')

# Save the test image
img.save('test_logo.png')
print("✓ Created test_logo.png")
