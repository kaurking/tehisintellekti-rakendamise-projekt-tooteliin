import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import threading
from pathlib import Path

# NB Tegelikult peaks võtma nt 6 ala, kus kõik muutuvad. Kui kõik muutuvad, siis võt miinimumväärtus nendest?

class RTSPStreamReader:
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url)
        self.ret = False
        self.frame = None
        self.running = True
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not self.running: break
            with self.lock:
                self.ret = ret
                self.frame = frame
            if not ret: break

    def read(self):
        with self.lock:
            if self.frame is None: return self.ret, None
            return self.ret, self.frame.copy()

    def stop(self):
        self.running = False
        self.thread.join(timeout=1.0)
        self.cap.release()

"""
TÖÖ ENNE SEMINARI 3: Liikumise tuvastamine ja viivitusega salvestamine.

Eesmärk: Tuvastada konveieril liikumine, oodata pildi stabiliseerumist ja salvestada kaader.
"""

# --- KONFIGURATSIOON ---
# STREAM_URL = "rtsp://172.17.37.81:8554/salami"
# STREAM_URL = "rtsp://172.17.37.81:8554/veis"
# STREAM_URL = "rtsp://172.17.37.81:8554/kalkun"
# STREAM_URL = "rtsp://172.17.37.81:8554/rulaad"

# vigased
# STREAM_URL = "rtsp://172.17.37.81:8554/empty"
STREAM_URL = "rtsp://172.17.37.81:8554/false_alarm"

MOTION_THRESHOLD = 15.0  # Lävend, millest suurem muutus loetakse liikumiseks
CAPTURE_DELAY = 3      # Sekundid, mida oodatakse peale liikumise algust enne pildi tegemist

# Kausta loomine (eelmise ülesande lahendus)
folder_name = STREAM_URL.split('/')[-1].strip()
folder = Path("../pictures") / folder_name
folder.mkdir(parents=True, exist_ok=True)

def is_green_screen(frame):
    """ Tuvastab rohelise märguande (eelmise ülesande lahendus). """
    if frame is None: return False
    small = cv2.resize(frame, (64, 64))
    avg_color = np.mean(small, axis=(0, 1))
    return avg_color[1] > 200 and avg_color[0] < 50 and avg_color[2] < 50

# --- ÜLESANNE: Muutuse mõõtmine ---
def measure_change(f1, f2):
    """
    Arvutab kahe kaadri vahelise erinevuse.
    Sinu ülesanne: 
    1. Mõõda funktsiooni täitmise aega.
    2. Testi arvutuse kiirust: kas piltide muutmine halltoonidesse ja väiksemaks annab olulist võitu?
    3. Arvuta MAE (Mean Absolute Error), MSE või mõni muu ise välja mõeldud erinevuse või liikumise mõõdik
    4. Prindi välja kulunud aeg ja tagasta arvutatud skoor.
    """
    small1 = cv2.resize(f1, (64, 64))
    small2 = cv2.resize(f2, (64, 64))
    avrg = np.mean(cv2.absdiff(small1, small2))
    return avrg

stream = RTSPStreamReader(STREAM_URL)
time.sleep(2)
if not stream.ret:
    print(f"Viga ühendusega: {STREAM_URL}")
    exit()

print(f"Seadistatud: Lävend {MOTION_THRESHOLD}, viivitus {CAPTURE_DELAY}s")

# --- ÜLESANNE: Logi salvestamine
# loo siin tühjad listid, et talletada info "muutuse graafik üle aja" jaoks ---

kaadrivahed = []
tuvastusajad = []

started = False
green_cooldown = False
motion_triggered = False
trigger_time = 0
cycle_start_time = 0
frame_count = 0

try:
    while True:
        loop_start = time.perf_counter()
        # Loeme kaks järjestikust kaadrit
        ret1, frame1 = stream.read()
        time.sleep(0.02) # Väike paus, et kaadrid jõuaksid muutuda
        ret2, frame2 = stream.read()
        
        if not ret1 or not ret2: break

        now = time.time()
        current_is_green = is_green_screen(frame2)

        if not started:
            if current_is_green:
                print(">>> Alustame tsüklit!")
                started = True
                green_cooldown = True
        else:
            if not current_is_green:
                green_cooldown = False

            if current_is_green and not green_cooldown:
                print(">>> Lõpetame tsükli.")
                break

            # --- ÜLESANNE: Liikumise tuvastamine ja ajastus ---
            # 1. Kutsu välja measure_change() ja salvesta tulemus ka listi. salvesta ka ajahetk.
            # 2. Kui muutus ületab MOTION_THRESHOLD ja 'motion_triggered' on False:
            #    - Märgi liikumine tuvastatuks, salvesta hetke aeg 'trigger_time' muutujasse.
            # 3. Kui 'motion_triggered' on True ja 'CAPTURE_DELAY' aeg on täis:
            #    - Salvesta pilt (cv2.imwrite).
            #    - Reseti 'motion_triggered', et oodata järgmist liikumist.
            

            start = time.perf_counter()
            vahe = measure_change(frame1, frame2)
            aeg_frame = time.time()
            end = time.perf_counter()
            aeg = end - start
            #print(aeg)
            kaadrivahed.append(vahe)
            tuvastusajad.append(aeg_frame)

            if vahe > MOTION_THRESHOLD and not motion_triggered:
                motion_triggered = True
                trigger_time = time.time()
            
            if motion_triggered and now - trigger_time > CAPTURE_DELAY:
                failinimi = folder / f"frame{frame_count}.jpg"
                cv2.imwrite(failinimi, frame1) # Vahet pole, kas 1 voi 2?
                frame_count += 1
                motion_triggered = False

        loop_end = time.perf_counter()
        fps = 1 / (loop_end - loop_start)
        # print(fps)


except KeyboardInterrupt:
    print("\nClosing program.")            

finally:
    stream.stop()
    # ÜLESANNE: joonista graafik, kasuta näiteks plt.plot(), plt.axhline()(lävendi jaoks), 
    # pane ka nimi ja telgede nimed. salvesta graafik faili
    graph_folder = Path("../graphs")
    graph_folder.mkdir(parents=True, exist_ok=True)

    graph_file = graph_folder / f"{folder_name}_graafik.png"

    if len(kaadrivahed) > 0 and len(tuvastusajad) > 0:
        plt.figure(figsize=(12, 6))

        # joonistame muutuse väärtused
        plt.plot(tuvastusajad, kaadrivahed, label="Kaadrite erinevus")

        # joonistame lävendi joone
        plt.axhline(
            y=MOTION_THRESHOLD,
            linestyle="--",
            label=f"Lävend ({MOTION_THRESHOLD})"
        )

        plt.title(f"Liikumise tuvastus - {folder_name}")
        plt.xlabel("Mõõtmise järjekorranumber")
        plt.ylabel("Muutuse suurus")
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(graph_file)
        plt.close()

        print(f"Graafik salvestatud faili: {graph_file}")
    else:
        print("Graafikut ei salvestatud, sest andmelistid on tühjad.")
    

