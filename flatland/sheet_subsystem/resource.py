"""
resource.py - Table of resources and their locators
"""

from pathlib import Path

image_path = Path.home() / '.flatland' / 'images'
resource_locator = {
    'MIT_large_portrait': image_path / 'MIT_boilerplate_large.png',
    'MIT_large_landscape': image_path / 'MIT_boilerplate_large.png',
    'MIT_medium_portrait': image_path / 'MIT_boilerplate_medium.png',
    'MIT_medium_landscape': image_path / 'MIT_boilerplate_medium.png',
    'MIT_small_portrait': image_path / 'MIT_boilerplate_small.png',
    'MIT_small_landscape': image_path / 'MIT_boilerplate_small.png',
    'mint_large_portrait': image_path / 'mint_logo_large.png',
    'mint_large_landscape': image_path / 'mint_logo_large.png',
    'mint_medium_portrait': image_path / 'mint_logo_medium.png',
    'mint_medium_landscape': image_path / 'mint_logo_medium.png',
    'mint_small_portrait': image_path / 'mint_logo_small.png',
    'mint_small_landscape': image_path / 'mint_logo_small.png',
    'Toyota_large_portrait': image_path / 'Toyota_logo_large.png',
    'Toyota_large_landscape': image_path / 'Toyota_logo_large.png',
    'Toyota_medium_portrait': image_path / 'Toyota_logo_medium.png',
    'Toyota_medium_landscape': image_path / 'Toyota_logo_medium.png',
    'Toyota_small_portrait': image_path / 'Toyota_logo_small.png',
    'Toyota_small_landscape': image_path / 'Toyota_logo_small.png',
}