"""
styledb_test.py – Ensure that we can build the drawing domain database
"""
# We might move this test elsewhere, so let's use absolute paths from the package root
from flatland.database.flatlanddb import FlatlandDB
from flatland.drawing_domain.styledb import StyleDB

fdb = FlatlandDB(rebuild=True)
sdb = StyleDB(drawing_type='Starr class diagram', presentation='diagnostic', layer='frame')
print("Finished")
