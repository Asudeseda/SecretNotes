import tkinter
from tkinter import messagebox
import base64
from PIL import Image, ImageTk

# --- 1. ŞİFRELEME MOTORU (YENİ EKLENEN KISIM) ---
def encode(key, clear):
    # Bu fonksiyon mesajı alır, anahtar ile karıştırır ve şifreli hale getirir.
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    # Bu fonksiyon şifreli mesajı çözer (Decrypt butonu için lazım olacak)
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


# --- 3. KAYDET VE ŞİFRELE FONKSİYONU ---
# --- 3. KAYDET VE ŞİFRELE FONKSİYONU (DÜZELTİLMİŞ HALİ) ---
def save_and_encrypt():
    title = title_entry.get()
    message = secret_entry.get("1.0", tkinter.END)
    master_secret = master_key_entry.get()

    # 1. Temel Kontrol: Kutular boş mu?
    if len(title) == 0 or len(message) == 1 or len(master_secret) == 0:
        messagebox.showinfo(title="Hata!", message="Lütfen tüm bilgileri giriniz.")
    else:
        # --- ŞİFRELEME ÖNCESİ BAŞLIK KONTROLÜ (DEDEKTİF KISMI) ---
        title_used = False

        try:
            with open("secret.txt", "r") as check_file:
                lines = check_file.readlines()
                for line in lines:
                    # Dosyadaki başlık ile girilen başlık aynı mı?
                    if line.strip() == title:
                        title_used = True
                        break  # Bulduysak aramaya devam etmeye gerek yok
        except FileNotFoundError:
            # Dosya yoksa zaten başlık da kullanılmış olamaz, devam et.
            pass

        # --- KARAR ANI ---
        if title_used:
            # Eğer başlık bulunduysa hata ver ve kaydetme!
            messagebox.showinfo(title="Hata!", message="Bu başlıkta bir not zaten var! Lütfen başka bir başlık girin.")
        else:
            # --- ŞİFRELEME VE KAYDETME (SADECE BAŞLIK YOKSA ÇALIŞIR) ---
            message_encrypted = encode(master_secret, message)

            try:
                with open("secret.txt", "a") as data_file:
                    data_file.write(f"\n{title}\n{message_encrypted}")
                messagebox.showinfo(title="Başarılı", message="Notunuz şifrelenerek kaydedildi!")
            except FileNotFoundError:
                with open("secret.txt", "w") as data_file:
                    data_file.write(f"\n{title}\n{message_encrypted}")
                messagebox.showinfo(title="Başarılı", message="Dosya oluşturuldu ve şifrelendi.")

            # Temizlik (Sadece başarılı kayıttan sonra silersek daha iyi olur)
            title_entry.delete(0, tkinter.END)
            secret_entry.delete("1.0", tkinter.END)
            master_key_entry.delete(0, tkinter.END)

def decrypt():
    # 1. Metni alırken sonundaki görünmez '\n' karakterinden kurtulmak için .strip() ekledik
    message_encrypted = secret_entry.get("1.0", tkinter.END).strip()
    master_secret = master_key_entry.get()

    if len(master_secret) == 0 or len(message_encrypted) == 0:
        messagebox.showinfo(title="Hata!", message="Lütfen şifreli metni ve anahtarı giriniz.")
    else:
        try:
            decrypted_message = decode(master_secret, message_encrypted)

            secret_entry.delete("1.0", tkinter.END)
            secret_entry.insert("1.0", decrypted_message)
        except Exception as e:
            # Hatanın tam olarak ne olduğunu görmek için (geliştirme aşamasında) konsola yazdırıyoruz
            print(f"Hata detayı: {e}")
            messagebox.showinfo(title="Hata!", message="Şifre çözülemedi. Lütfen anahtarın doğruluğundan emin olun.")






window = tkinter.Tk()
window.title("Secret Notes")
window.config(padx=80,pady= 50)


image = Image.open("secretnote.png")


resized_image = image.resize((80, 80))
image = ImageTk.PhotoImage(resized_image)

image_label = tkinter.Label(window, image=image)
image_label.pack()

title_info_label = tkinter.Label(text="Enter your title")
title_info_label.pack()

title_entry = tkinter.Entry(width=40)
title_entry.pack()

secret_entry_label = tkinter.Label(text="Enter your secret")
secret_entry_label.pack()


secret_entry = tkinter.Text(height=5, width=60)
secret_entry.pack()
secret_entry.pack(ipady=200)

master_key_label = tkinter.Label(text="Enter your master key")
master_key_label.pack()

master_key_entry = tkinter.Entry(width=40)
master_key_entry.pack()


save_encrypt_button = tkinter.Button(width=50,text="Save&Encrypt", command=save_and_encrypt)
save_encrypt_button.pack()

decrypt_button = tkinter.Button(width=40,text="Decrypt", command=decrypt)
decrypt_button.pack()






window.mainloop()
