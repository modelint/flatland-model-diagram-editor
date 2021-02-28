"""
resource.py - Table of resources and their locators
"""

from pathlib import Path

image_path = Path.home() / '.flatland' / 'images'
resource_locator = {
    'MIT': image_path / 'MIT boilerplate.png',
    'mint_large': image_path / 'mint logo large.png',
}