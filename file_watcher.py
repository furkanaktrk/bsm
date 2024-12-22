import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Dosya olaylarını işlemek için bir sınıf oluşturuyoruz
class IzleyiciHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"Değişiklik algılandı: {event.src_path}")  # Debug mesajı
        self.log_olayi("değiştirildi", event.src_path)
    
    def on_created(self, event):
        print(f"Oluşturma algılandı: {event.src_path}")  # Debug mesajı
        self.log_olayi("oluşturuldu", event.src_path)
    
    def on_deleted(self, event):
        print(f"Silme algılandı: {event.src_path}")  # Debug mesajı
        self.log_olayi("silindi", event.src_path)
    
    def log_olayi(self, eylem, dosya_yolu):
        log = {
            "eylem": eylem,
            "dosya": dosya_yolu,
            "zaman_damgasi": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"Log yazılıyor: {log}")  # Debug mesajı
        try:
            with open("/home/furkan/bsm/logs/degisiklikler.json", "a") as log_dosyasi:
                log_dosyasi.write(json.dumps(log) + "\n")
        except Exception as e:
            print(f"Log yazma hatası: {e}")  # Hata mesajı

# İzlenecek dizin
izlenecek_dizin = "/home/furkan/bsm/test"

# Observer (gözlemci) oluştur ve başlat
gozlemci = Observer()
olay_isleyici = IzleyiciHandler()
gozlemci.schedule(olay_isleyici, izlenecek_dizin, recursive=True)

try:
    gozlemci.start()
    print(f"İzlenen dizin: {izlenecek_dizin}")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    gozlemci.stop()
gozlemci.join()
