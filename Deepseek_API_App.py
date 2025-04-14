import os
import json
from datetime import datetime
from openai import OpenAI
from colorama import Fore, Style, init

# Renkleri başlat
init(autoreset=True)

# API Key ve sohbet klasörü
API_KEY = "sk-5410a2f808f94139ab18dbac40c32e00"  # ← kendi key'ini buraya gir
SOHBET_KLASORU = "D:/Automation/Projects/Python/sohbetler"

# Klasörü oluştur
os.makedirs(SOHBET_KLASORU, exist_ok=True)

# DeepSeek istemcisi
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

# ✅ Konu başlığı sor ve dosya adını ona göre ayarla
konu = input(Fore.YELLOW + "Sohbet konusu (örnek: yapay_zeka, tarih_vs_mitoloji): " + Style.RESET_ALL).strip()
if not konu:
    konu = datetime.now().strftime("sohbet_%Y-%m-%d")

# Dosya adı
dosya_yolu = os.path.join(SOHBET_KLASORU, f"{konu}.json")

# Önceki mesajlar varsa yükle
if os.path.exists(dosya_yolu):
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        mesajlar = json.load(f)
else:
    mesajlar = [{"role": "system", "content": "You are a helpful assistant."}]

# Başlangıç mesajı
print(Fore.GREEN + f"DeepSeek Asistanı ({konu}) hazır. Çıkmak için 'exit' yazabilirsin.\n" + Style.RESET_ALL)

# Ana döngü
while True:
    user_input = input(Fore.CYAN + "Sen: " + Style.RESET_ALL)
    if user_input.lower() in ["exit", "quit", "çık", "çıkış"]:
        print(Fore.YELLOW + "Görüşmek üzere!" + Style.RESET_ALL)
        break

    # Kullanıcı mesajını ekle
    mesajlar.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=mesajlar,
            stream=False
        )
        yanit = response.choices[0].message.content
        mesajlar.append({"role": "assistant", "content": yanit})

        # Renkli çıktı (kim ne dediyse ona göre)
        print(Fore.MAGENTA + "Asistan: " + Style.RESET_ALL + yanit)

        # Sohbeti kaydet
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            json.dump(mesajlar, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(Fore.RED + f"Hata oluştu: {e}" + Style.RESET_ALL)
