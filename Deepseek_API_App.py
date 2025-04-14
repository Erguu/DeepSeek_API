import json
import os
import openai
from colorama import Fore, Style

# DeepSeek API Key
API_KEY = "sk-5410a2f808f94139ab18dbac40c32e00"
BASE_URL = "https://api.deepseek.com"

# OpenAI client setup
openai.api_key = API_KEY

# Klasör ve dosya yolları
SOHBET_KLASORU = "C:/Users/PC/Documents/Python_Projects/Deepseek/Chats"
AYAR_DOSYASI = os.path.join(SOHBET_KLASORU, "ayarlar.json")

# Asistan karakterini belirle
def asistan_karakterini_belirle():
    if os.path.exists(AYAR_DOSYASI):
        with open(AYAR_DOSYASI, "r", encoding="utf-8") as f:
            ayarlar = json.load(f)
            if ayarlar.get("system_prompt"):
                return ayarlar["system_prompt"]

    # Varsayılan karakter
    return "Sen teknik konularda yardımcı olan bir asistansın."

# Asistan karakterini değiştirme
def asistan_karakterini_degistir():
    if os.path.exists(AYAR_DOSYASI):
        with open(AYAR_DOSYASI, "r", encoding="utf-8") as f:
            ayarlar = json.load(f)
            if ayarlar.get("system_prompt"):
                print(Fore.YELLOW + f"\n[!] Mevcut karakter: {ayarlar['system_prompt']}\n" + Style.RESET_ALL)

    print("\nYeni bir asistan karakteri seç:\n")
    print("1 - Teknik mühendis (kısa, öz, bol terim)")
    print("2 - Sabırlı öğretmen (açıklayıcı, örnekli)")
    print("3 - Mizahi dost (arada espri yapar)")
    print("4 - Kendi tanımımı yazmak istiyorum")

    secim = input("\nYeni karakter seçiminiz (1-4): ")

    karakterler = {
        "1": "Sen teknik konularda kısa, öz ve bolca terim kullanarak konuşan bir mühendissin.",
        "2": "Sen sabırlı bir öğretmensin, teknik konuları açık ve örneklerle anlatırsın.",
        "3": "Sen bol teknik bilgiye sahip, arada esprili cevaplar veren yardımcı bir asistansın.",
    }

    if secim in karakterler:
        prompt = karakterler[secim]
    elif secim == "4":
        prompt = input("\nYeni asistan tanımını yaz: ")
    else:
        print("Geçersiz seçim. Varsayılan karakter kullanılıyor.")
        prompt = "Sen teknik konularda yardımcı olan bir asistansın."

    os.makedirs(SOHBET_KLASORU, exist_ok=True)
    with open(AYAR_DOSYASI, "w", encoding="utf-8") as f:
        json.dump({"system_prompt": prompt}, f, ensure_ascii=False, indent=2)

    print(Fore.GREEN + "\n[!] Karakter başarıyla değiştirildi.\n" + Style.RESET_ALL)
    return prompt

# Geçmiş sohbeti yükle
def sohbet_gecmisini_yukle(konu):
    dosya_yolu = os.path.join(SOHBET_KLASORU, f"{konu}.json")
    if os.path.exists(dosya_yolu):
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Sohbeti kaydet
def sohbeti_kaydet(konu, mesajlar):
    dosya_yolu = os.path.join(SOHBET_KLASORU, f"{konu}.json")
    with open(dosya_yolu, "w", encoding="utf-8") as f:
        json.dump(mesajlar, f, ensure_ascii=False, indent=2)

# Kullanıcı ve asistan mesajlarını renkli yazdır
def yazdir_renkli(kim, mesaj):
    if kim == "user":
        print(Fore.LIGHTCYAN_EX + f"\nSen: {mesaj}" + Style.RESET_ALL)
    else:
        print(Fore.LIGHTGREEN_EX + f"\nAsistan: {mesaj}" + Style.RESET_ALL)

# Sohbet başlatma
def sohbet_baslat():
    os.makedirs(SOHBET_KLASORU, exist_ok=True)
    print("\nMevcut karakterinizi değiştirmek ister misiniz?")
    degistir = input("Evet (y) / Hayır (n): ").strip().lower()

    if degistir == "y":
        system_prompt = asistan_karakterini_degistir()
    else:
        system_prompt = asistan_karakterini_belirle()

    konu = input("\nSohbet konusu (dosya adı olacak): ").strip()

    mesajlar = [{"role": "system", "content": system_prompt}]
    mesajlar += sohbet_gecmisini_yukle(konu)

    while True:
        user_input = input(Fore.LIGHTCYAN_EX + "\nSen: " + Style.RESET_ALL)
        if user_input.lower() in ["exit", "quit", "çık", "q"]:
            print(Fore.YELLOW + "\n[!] Sohbet sonlandırıldı.\n" + Style.RESET_ALL)
            break

        mesajlar.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=mesajlar,
                stream=False
            )
            cevap = response['choices'][0]['message']['content'].strip()
        except Exception as e:
            cevap = f"[Hata] API isteği başarısız: {e}"

        mesajlar.append({"role": "assistant", "content": cevap})
        yazdir_renkli("assistant", cevap)
        sohbeti_kaydet(konu, mesajlar)

# Başlatma fonksiyonu
if __name__ == "__main__":
    sohbet_baslat()
