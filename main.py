# Esempio 1: generare una singola targa, al, file name = digit.
from DxfNumberedPlates import DxfTag

# digit = 6
# height = 100
# tag = DxfTag()
# tag.generate_single_tag(6)
DxfTag.generate_single_tag(6)

# # Esempio 2: generare una sequenza di targhe
# from DxfNumberedPlates import DxfTag  

# DxfTag.generate_tag_sequence(0, 25, high=250, holes=True, radius=10)