"""
resource.py - Table of resources and their locators
"""

from pathlib import Path

image_path = Path.home() / '.flatland' / 'images'
resource_locator = {
    'MIT': image_path / 'MIT boilerplate.png',
    'MIT_small': image_path / 'MIT boilerplate small.png',
    'mint_large': image_path / 'mint logo large.png',
    'mint_small': image_path / 'mint logo small.png',
    'toyota_large': image_path / 'toyota logo large.png',
    'toyota_small': image_path / 'toyota logo small.png',
}