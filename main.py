# Esempio 2: generare una sequenza di targhe
from DxfNumberedPlates import DxfTag  

DxfTag.generate_tag_sequence(0, 25, high=250, holes=True, radius=10)