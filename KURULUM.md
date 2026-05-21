# ZEDİN IDE - KURULUM VE BAŞLANGIÇ REHBERİ

## 📦 Dosyalar

Zedin IDE Python tabanlı komut satırı arayüzü aşağıdaki dosyalardan oluşur:

```
/home/ubuntu/
├── zedin                    # Ana başlatıcı script (3.2 KB)
├── zedin_ide.py            # IDE modülü (31 KB)
├── zedin_kernel.py         # Kernel modülü (7.5 KB)
├── zedin_editor.py         # Editör modülü (11 KB)
├── libzed.py               # Standart kütüphane (12 KB)
├── ZEDIN_IDE_README.md     # Tam dokümantasyon
└── KURULUM.md              # Bu dosya
```

## 🚀 Hızlı Başlangıç

### 1. IDE'yi Başlat
```bash
cd /home/ubuntu
./zedin ide
```

### 2. Yeni Dosya Oluştur
```
zedin> yeni
✓ Yeni dosya oluşturuldu
```

### 3. Editör Aç
```
zedin> editör
Editör (Çıkmak için 'ÇIKIS' yazın):
> YUKLE #72
> YAZDIR
> BITIR
> ÇIKIS
✓ Editör kapatıldı
```

### 4. Kodu Derle
```
zedin> derle
Derleniyor...
✓ Derleme başarılı (3 komut)
```

### 5. Programı Çalıştır
```
zedin> çalıştır
Çalıştırılıyor...
H
✓ Program başarıyla tamamlandı

İstatistikler:
  Adım sayısı: 3
  CEB değeri: 72
  Stack işaretçisi: 0
```

## 💻 Komut Satırı Kullanımı

### IDE Başlat
```bash
./zedin ide
# veya
python3 zedin_ide.py
```

### Kernel Başlat
```bash
./zedin kernel
# veya
python3 zedin_kernel.py
```

### Editör Başlat
```bash
./zedin editor
# veya
python3 zedin_editor.py
```

### Yardım Göster
```bash
./zedin --help
```

### Versiyon Göster
```bash
./zedin --version
```

## 📝 İlk Program: Merhaba Dünya

### 1. IDE'yi Başlat
```bash
./zedin ide
```

### 2. Yeni Dosya Oluştur
```
zedin> yeni
```

### 3. Editör Aç ve Kod Yaz
```
zedin> editör
Editör (Çıkmak için 'ÇIKIS' yazın):
> ; Merhaba Dünya
> DATA 100 "Merhaba_Dunya"
> @BASLA
> YUKLE #100
> INT #22
> BITIR
> ÇIKIS
```

### 4. Dosyayı Kaydet
```
zedin> kaydet
Dosya adı: merhaba.zed
✓ Dosya kaydedildi: merhaba.zed
```

### 5. Kodu Derle
```
zedin> derle
✓ Derleme başarılı
```

### 6. Programı Çalıştır
```
zedin> çalıştır
Merhaba_Dunya
✓ Program başarıyla tamamlandı
```

## 🎓 Öğrenme Yolu

### Seviye 1: Temel Komutlar
```zedin
; Basit toplama
@BASLA
YUKLE #5
TOPLA #3
YAZDIR
BITIR
```

### Seviye 2: Bellek İşlemleri
```zedin
; RAM'e yazma ve okuma
@BASLA
YUKLE #42
SAKLA #42 #100
GETIR #100
YAZDIR
BITIR
```

### Seviye 3: Kontrol Akışı
```zedin
; Etiketler ve atlamalar
@BASLA
YUKLE #1
@DONGU
YAZDIR
TOPLA #1
KUCUKSE #5 $DONGU
BITIR
```

### Seviye 4: Stack ve Fonksiyonlar
```zedin
; Fonksiyon çağrısı
@BASLA
CALL $TOPLAMA
BITIR

@TOPLAMA
YUKLE #10
TOPLA #20
YAZDIR
RET
```

## 🔍 Hata Ayıklama

### Derleme Hatası
```
✗ Derleme hataları:
  • Satır 3: Bilinmeyen komut: YÜKLR
```

### Çalışma Zamanı Hatası
```
✗ Hata: Bellek erişim hatası (Segmentation Fault)
```

### Çözüm
1. Komut adlarını kontrol et (YUKLE, SAKLA, vb.)
2. Parametre sayısını doğrula
3. Bellek adreslerini kontrol et
4. Etiket adlarını doğrula

## 📚 Komut Referansı

### Hızlı Referans
```
zedin> yardim
```

### Editör Referansı
```
zedin> editör
```

## 🛠️ Gelişmiş Kullanım

### Dosya Yönetimi
```
zedin> aç program.zed      # Dosya aç
zedin> kaydet              # Dosyayı kaydet
zedin> yeni                # Yeni dosya
```

### Kernel Komutları
```
zed_os> calistir program.bin    # Program çalıştır
zed_os> listele                 # Programları listele
zed_os> surum                   # Sistem bilgisi
zed_os> yardim                  # Yardım
```

## 🎨 Sözdizim Vurgulama

IDE otomatik olarak renk kodlaması yapar:

- 🟢 **Yeşil:** YUKLE, SAKLA, TOPLA, vb. komutlar
- 🔵 **Cyan:** @BASLA, $DONGU gibi etiketler
- 🟡 **Sarı:** #100, #5 gibi sayılar
- 🔴 **Kırmızı:** #22, #20 gibi kesme numaraları
- ⚪ **Gri:** ; Yorumlar

## 💡 İpuçları

1. **Komut Adlarını Kontrol Et:** Tüm komutlar büyük harfle yazılmalı
2. **Etiket Referansları:** Etiketler $ ile başlamalı (@BASLA → $BASLA)
3. **Sayılar:** Sayılar # ile başlamalı (#100, #5)
4. **Yorumlar:** Yorumlar ; ile başlamalı
5. **String'ler:** String'ler tırnak içinde yazılmalı ("Merhaba")

## 🐛 Yaygın Hatalar

### Hata 1: Bilinmeyen Komut
```
✗ Derleme hataları:
  • Bilinmeyen komut: YÜKLR
```
**Çözüm:** YUKLE yazın (YÜKLR değil)

### Hata 2: Yanlış Parametre Sayısı
```
✗ Derleme hataları:
  • Satır 2: 'TOPLA' 1 parametre gerektirir
```
**Çözüm:** TOPLA #5 yazın (TOPLA #5 #10 değil)

### Hata 3: Bilinmeyen Etiket
```
✗ Derleme hataları:
  • Satır 5: Bilinmeyen etiket: DONGU
```
**Çözüm:** @DONGU etiketini tanımla

## 📖 Daha Fazla Bilgi

- **Tam Dokümantasyon:** ZEDIN_IDE_README.md
- **Orijinal Zedin:** README.md
- **Örnek Programlar:** *.zed dosyaları

## 🎯 Sonraki Adımlar

1. Temel komutları öğren
2. Basit programlar yaz
3. Kontrol akışını kullan
4. Fonksiyonlar oluştur
5. Dosya I/O işlemleri yap

## 📞 Destek

Sorun yaşıyorsanız:
1. Hata mesajını oku
2. Komut referansını kontrol et
3. Örnek programları incele
4. Dokümantasyonu oku

---

**Hoşça kalın! Zedin ile programlamaya başla!** 🚀
