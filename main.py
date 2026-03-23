import cv2
import os
import json
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import threading
from pathlib import Path
import numpy as np
from dynamsoft_barcode_reader_bundle import *

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

# Dynamsoft Litsents
DYNAMSOFT_LICENSE = "t0084YQEAAIUx4hU4EqEOu9FaT9GprNtmXmbGA7IcvmG7V7l1yrR4WjV1JWPPrLuJoJN4HXVvqroIag2MeSFUJlbpkh0vhl8/Nrk3lffN1GzB7BvBtkl5"
LicenseManager.init_license(DYNAMSOFT_LICENSE)

# Initsialiseerime triipkoodi lugeja (Router), sätime seaded nii nagu Demo alusel otsustasime
router = CaptureVisionRouter()

template_path = "template/minimal_template.json"
if not os.path.exists(template_path):
    print(f"Error: Could not find the JSON template at '{template_path}'")
    exit()

err_code, err_msg = router.init_settings_from_file(template_path)
if err_code != EnumErrorCode.EC_OK:
    print(f"Failed to load JSON settings from file: {err_msg}")
    exit()


# --- KONFIGURATSIOON ---
# STREAM_URL = "rtsp://172.17.37.81:8554/salami"
# STREAM_URL = "rtsp://172.17.37.81:8554/veis"
STREAM_URL = "rtsp://172.17.37.81:8554/kalkun"
#STREAM_URL = "rtsp://172.17.37.81:8554/rulaad"

# vigased
#STREAM_URL = "rtsp://172.17.37.81:8554/empty"
#STREAM_URL = "rtsp://172.17.37.81:8554/false_alarm"

MOTION_THRESHOLD = 15.0  # Lävend, millest suurem muutus loetakse liikumiseks
CAPTURE_DELAY = 3      # Sekundid, mida oodatakse peale liikumise algust enne pildi tegemist

folder_name = STREAM_URL.split('/')[-1].strip()
folder = Path("pictures") / folder_name
folder.mkdir(parents=True, exist_ok=True)

def is_green_screen(frame):
    """ Tuvastab rohelise märguande (eelmise ülesande lahendus). """
    if frame is None: return False
    small = cv2.resize(frame, (64, 64))
    avg_color = np.mean(small, axis=(0, 1))
    return avg_color[1] > 200 and avg_color[0] < 50 and avg_color[2] < 50

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

data_path = "template/barcode_data.json"
if not os.path.exists(data_path):
    print(f"Error: Could not find the JSON template at '{data_path}'")
    exit()

with open(data_path) as f:    
    product_db = json.load(f)

# Märgime video salvestamise ajaks päeva, mil see tegelikult lindistati 14.02.2026  
capture_date = datetime(2026, 2, 14)

folder_path = "pictures/rulaad" 
file_prefix = "frame"
files = sorted([f for f in os.listdir(folder_path) if f.startswith(file_prefix) and f.endswith(".jpg")])

print(f"Töötlen tooteid kuupäevaga: {capture_date.strftime('%d.%m.%Y')}")

stream = RTSPStreamReader(STREAM_URL)
time.sleep(2)
if not stream.ret:
    print(f"Viga ühendusega: {STREAM_URL}")
    exit()

print(f"Seadistatud: Lävend {MOTION_THRESHOLD}, viivitus {CAPTURE_DELAY}s")

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

                result = router.capture(str(failinimi), "ReadBarcodes_Default")
                codes = []

                toode = "Tundmatu"
                sailivus = None

                if not result:
                    print(f"[{failinimi}] Triipkoodi ei leitud.")
                else:
                    items = result.get_items()
                    if items:
                        for item in items:
                            if item.get_type() == EnumCapturedResultItemType.CRIT_BARCODE:
                                ean = item.get_text()
                                codes.append(ean)

                                if ean in product_db:
                                    toode = product_db[ean]["ITEMNAME"]
                                    sailivus = product_db[ean]["BESTBEFOREDAYS"]

                    if len(codes) == 0:
                        print(f"[{failinimi}] Triipkoodi ei leitud.")
                    else:
                        koodid = ", ".join(codes)
                        aeg_ms = (time.perf_counter() - loop_start) * 1000

                        if sailivus is not None:
                            kuupaev = capture_date + timedelta(days=sailivus)
                            print(f"{failinimi}, aeg: {aeg_ms:.2f} ms, leitud {len(codes)}, triipkoodid: {koodid}, Toode: {toode}, Säilivus kuni: {kuupaev}")
                        else:
                            print(f"{failinimi}, aeg: {aeg_ms:.2f} ms, leitud {len(codes)}, triipkoodid: {koodid}, Toode andmebaasis puudub")


        loop_end = time.perf_counter()
        fps = 1 / (loop_end - loop_start)
        # print(fps)


except KeyboardInterrupt:
    print("\nClosing program.")            

finally:
    stream.stop()
    graph_folder = Path("graphs")
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