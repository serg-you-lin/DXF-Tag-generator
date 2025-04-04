import math
import ezdxf

SPACE = .75
THICK_RATIO = 7.5
HOLES_MARGIN = 10             


class DxfTag:
    def __init__(self, digits, height, margin=None, holes=False, radius=2):
        self.height = height
        if not margin:
             self.margin = self.height/7.5
        else:
             self.margin = margin
        self.digits = [int(d) for d in str(digits)]  # Gestisce cifre multiple
        self.thick = (self.height/2) / THICK_RATIO
        self.height_line = (self.height/2) - self.margin - (self.thick*SPACE)
        self.line = self._center_line(self.height_line, self.thick)
        self.rotated_line = self._rotate_line(self.line, 90)
        self.shift = (self.height/2-self.margin) - self.thick/2
        self.cc = self.line
        self.bc = self._shift_line(self.line, 0, -1*self.shift) 
        self.tc = self._shift_line(self.line, 0, self.shift)
        self.bl = self._shift_line(self.rotated_line, -1*self.shift/2, -1*self.shift/2)
        self.tl = self._shift_line(self.rotated_line, -1*self.shift/2, self.shift/2)
        self.br = self._shift_line(self.rotated_line, self.shift/2, -1*self.shift/2)
        self.tr = self._shift_line(self.rotated_line, self.shift/2, self.shift/2)
        self.holes = holes
        self.radius = radius
        
        # Mappa delle cifre ai segmenti
        self.digit_map = {
            0: [self.bc, self.tc, self.bl, self.tl, self.br, self.tr],
            1: [self.br, self.tr],
            2: [self.tc, self.cc, self.bl, self.bc, self.tr],
            3: [self.tc, self.cc, self.bc, self.br, self.tr],
            4: [self.br, self.cc, self.tl, self.tr],
            5: [self.tc, self.cc, self.br, self.bc, self.tl],
            6: [self.tc, self.cc, self.bl, self.bc, self.br, self.tl],
            7: [self.tc, self.br, self.tr],
            8: [self.tc, self.cc, self.bc, self.bl, self.tl, self.br, self.tr],
            9: [self.tc, self.cc, self.br, self.bc, self.tl, self.tr]
        }
        
    # --- METODI PUBBLICI ---
    
    @staticmethod
    def generate_single_tag(digit, height=250, holes=False, radius = 5, dxf_file_name=None):
        """
        Genera e salva una singola targa numerata
        
        Args:
            number: Il numero da visualizzare sulla targa
            height: Altezza della targa in unità DXF
            holes: Se True, aggiunge i fori agli angoli della targa
            radius: Raggio dei fori in unità DXF (default: 5)
            dxf_file_name: Nome del file DXF da salvare. Se None, usa il numero come nome
        
        Returns:
            Il percorso del file salvato
        """
        doc = ezdxf.new()
        digit_obj = DxfTag(digit, height, holes=holes, radius=radius)
        digit_obj.generate_plate(doc)
            
        if dxf_file_name is None:
            dxf_file_name = f"{str(digit)}.dxf"
            
        doc.saveas(dxf_file_name)
        return dxf_file_name
    
    @staticmethod
    def generate_tag_sequence(start, end, height=250, holes=False, radius=5, prefix=""):
        """
        Genera e salva una sequenza numerata di targhe
        
        Args:
            start: Numero iniziale della sequenza
            end: Numero finale della sequenza (incluso)
            height: Altezza delle targhe in unità DXF
            holes: Se True, aggiunge i fori agli angoli delle targhe
            radius: Raggio dei fori in unità DXF (default: 2)
            prefix: Prefisso per i nomi dei file
            
        Returns:
            Lista dei percorsi dei file generati
        """
        file_generati = []
        for i in range(start, end + 1):
            doc = ezdxf.new()
            digit = DxfTag(i, height, holes=holes, radius=radius)
            digit.generate_plate(doc)
            
            nome_file = f"{prefix}{str(i)}.dxf"
            doc.saveas(nome_file)
            file_generati.append(nome_file)
            
        return file_generati
    
    def generate_plate(self, doc, layer='0'):
        """
        Genera la targa nel documento DXF specificato
        
        Args:
            doc: Documento DXF dove generare la targa
            layer: Layer DXF dove inserire gli elementi
        """
        msp = doc.modelspace()
        
        # Disegna la cornice
        self._draw_plate(msp, layer)
        
        # Posiziona i numeri
        num_digits = len(self.digits)
        spacing = self.height/2 - self.margin/5 if num_digits > 1 else 0  # Se c'è una sola cifra, nessun spostamento
        for i, digit in enumerate(self.digits):
            if num_digits > 1:
                shift_x = (i - (num_digits / 2) + 0.5) * spacing
            else:
                 shift_x = 0
            self._place_digit(msp, digit, shift_x, layer)

        # Nel caso aggiungi foratura
        if self.holes:
             self._add_holes(msp, self.radius)
    
    # --- METODI PRIVATI ---
    
    def _get_digit_segments(self, digit, shift_x=0):
        """Ottiene i segmenti per una cifra, con un eventuale spostamento orizzontale"""
        segments = self.digit_map[digit]
        if shift_x != 0:
            segments = [self._shift_line(segment, shift_x, 0) for segment in segments]
        return segments
    
    def _place_digit(self, msp, digit, shift_x=0, layer='0'):
        """Piazza una singola cifra sul disegno"""
        segments = self._get_digit_segments(digit, shift_x)
        if not segments:
            raise ValueError("La lista dei segmenti è vuota. Non ci sono segmenti da aggiungere.")
        for segment in segments:
            for i in range(len(segment) - 1):
                start_point = (segment[i][0], segment[i][1])
                end_point = (segment[i + 1][0], segment[i + 1][1])
                msp.add_line(start=start_point, end=end_point, dxfattribs={'layer': layer})

    def _draw_plate(self, msp, layer='0'):
        """Disegna il contorno della targa"""
        self.side = self.height / 2
        self.plate_to_gen = [(self.side, self.side), (self.side, -self.side), (-self.side, -self.side), (-self.side, self.side)]
        for i in range(len(self.plate_to_gen)):
            start_point = self.plate_to_gen[i]
            end_point = self.plate_to_gen[(i + 1) % len(self.plate_to_gen)]
            msp.add_line(start=start_point, end=end_point, dxfattribs={'layer': layer})

    def _add_holes(self, msp, radius):
        """Aggiunge i fori agli angoli della targa"""
        for x, y in self.plate_to_gen:
            if x >= 0 and y >= 0:  # Primo quadrante
                hole_center = (x - (self.radius + HOLES_MARGIN), y - (self.radius + HOLES_MARGIN))
            elif x >= 0 and y < 0:  # Quarto quadrante
                hole_center = (x - (self.radius + HOLES_MARGIN), y + (self.radius + HOLES_MARGIN))
            elif x < 0 and y >= 0:  # Secondo quadrante
                hole_center = (x + (self.radius + HOLES_MARGIN), y - (self.radius + HOLES_MARGIN))
            elif x < 0 and y < 0:  # Terzo quadrante
                hole_center = (x + (self.radius + HOLES_MARGIN), y + (self.radius + HOLES_MARGIN))
            msp.add_circle(center=hole_center, radius=radius)

    @staticmethod
    def _center_line(height, thick):
        """Genera una linea centrale con lo spessore specificato"""
        r = thick / 2
        l = r * -1
        t = height / 2
        b = t * -1
        segs = [((b + r), l), ((t - r), l), (t, 0), ((t - r), r), ((b + r), r), (b, 0), ((b + r), l)]
        return segs

    @staticmethod
    def _rotate_line(segs, angle):
        """Ruota una linea dell'angolo specificato"""
        angle_rad = math.radians(angle)
        rotated_segs = []
        for x, y in segs:
            # Applica la formula per la rotazione in senso antiorario
            x_rotated = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            y_rotated = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            rotated_segs.append((x_rotated, y_rotated))
        return rotated_segs

    @staticmethod
    def _shift_line(segs, x_shift, y_shift):
        """Sposta una linea delle coordinate specificate"""
        shifted_segs = [(seg[0] + x_shift, seg[1] + y_shift) for seg in segs]
        return shifted_segs