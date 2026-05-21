# ZEDİN TÜRKÇE ASSEMBLY IDE

**Python Tabanlı Komut Satırı Geliştirme Ortamı**

Tüm kodlar Türkçe - Tüm özellikler entegre

## 🚀 Özellikler

### ✅ Zedin VM Simülatörü
- Türkçe komutlarla yazılmış bytecode sanal makinesi
- 20+ Türkçe komut desteği
- 16 sistem kesmesi (INT)
- Stack ve Heap yönetimi
- Dosya I/O işlemleri

### ✅ Assembler
- Türkçe Assembly kodunu bytecode'a dönüştür
- Etiket ve veri tanımlaması
- Hata raporlama ve uyarılar

### ✅ Komut Satırı IDE
- Editör, derleyici, çalıştırıcı entegre
- Dosya yönetimi
- Kod kaydetme/yükleme
- İnteraktif komut satırı

### ✅ Sözdizim Vurgulama
- Türkçe komutlar (yeşil)
- Etiketler (cyan)
- Sayılar (sarı)
- Yorumlar (gri)
- Kesme numaraları (kırmızı)

### ✅ Kernel
- Sistem yönetimi
- Program çalıştırma
- Dosya sistemi

### ✅ libZED Standart Kütüphanesi
- Giriş/Çıkış işlemleri
- Bellek yönetimi
- String işlemleri
- Dosya işlemleri

## 📦 Kurulum

```bash
# Dosyaları indir
cd /home/ubuntu

# Çalıştırılabilir yap
chmod +x zedin zedin_ide.py zedin_kernel.py zedin_editor.py
```

## 🎮 Kullanım

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

### Ana Menü
```bash
./zedin
```

## 📝 Komutlar

### IDE Komutları

```
yardim              - Komut listesini göster
yeni                - Yeni dosya oluştur
aç <dosya>          - Dosya aç
kaydet              - Dosyayı kaydet
derle               - Kodu derle
çalıştır            - Programı çalıştır
editör              - Editör aç
temizle             - Ekranı temizle
çıkış               - Programdan çık
```

### Zedin Assembly Komutları

#### Bellek Komutları
```
YUKLE #değer         - CEB'e değer yükle
SAKLA #değer #adres  - RAM'e yaz
GETIR #adres         - RAM'den oku
SAKLA_CEBI #adres    - CEB'i RAM'e yaz
```

#### Aritmetik Komutları
```
TOPLA #değer         - CEB += değer
CIKAR #değer         - CEB -= değer
CARP #değer          - CEB *= değer
BOL #değer           - CEB /= değer
MOD #değer           - CEB %= değer
```

#### Kontrol Komutları
```
GIT $etiket          - Etiket adresine atla
EGER_ESITSE #ad $et  - CEB == RAM[ad] ise atla
BUYUKSE #ad $et      - CEB > RAM[ad] ise atla
KUCUKSE #ad $et      - CEB < RAM[ad] ise atla
EGER_DEGILSE #ad $et - CEB != RAM[ad] ise atla
```

#### Stack Komutları
```
PUSH #değer          - Stack'e it
POP                  - Stack'ten al
CALL $etiket         - Fonksiyon çağır
RET                  - Fonksiyondan dön
```

#### Giriş/Çıkış Komutları
```
YAZDIR               - CEB'i ekrana bas
INT #kesme           - Sistem kesmesi çağır
BITIR                - Programı durdur
```

## 📚 Örnek Program

### Merhaba Dünya
```zedin
; Merhaba Dünya - Zedin Assembly
DATA 100 "Merhaba_Dunya"
@BASLA
YUKLE #100
INT #22
YUKLE #10
INT #20
BITIR
```

### Sayıları Toplama
```zedin
; 5 + 3 = 8
@BASLA
YUKLE #5
TOPLA #3
YAZDIR
BITIR
```

### Döngü
```zedin
; 1'den 5'e kadar say
@BASLA
YUKLE #1
@DONGU
YAZDIR
TOPLA #1
KUCUKSE #6 $DONGU
BITIR
```

## 🔧 Kesme Tablosu (INT)

| Kesme | Açıklama |
|-------|----------|
| #20   | ASCII karakteri bas |
| #21   | Karakteri oku |
| #22   | String'i bas |
| #23   | Sayıyı bas |
| #25   | Rastgele sayı üret |
| #26   | Zaman damgası al |
| #30   | Dosya aç (okuma) |
| #31   | Dosyadan karakter oku |
| #32   | Dosya aç (yazma) |
| #33   | Dosyaya karakter yaz |
| #34   | Dosyaları kapat |
| #35   | Dosyaya string yaz |
| #40   | Bellek ayır |
| #41   | Bellek sıfırla |
| #46   | String karşılaştır |
| #50   | Program yükle ve çalıştır |

## 📊 Yazmaçlar

| Yazmaç | Açıklama |
|--------|----------|
| CEB    | Merkezi Elektronik Birimi (Accumulator) |
| IP     | Komut İşaretçisi (Instruction Pointer) |
| SP     | Stack İşaretçisi (Stack Pointer) |

## 💾 Bellek Yapısı

- **Sanal Bellek:** 32 KB (Kod)
- **RAM:** 32 KB (Veri)
- **Stack:** 8 KB
- **Heap:** 16 KB (Dinamik bellek)

## 🐛 Hata Ayıklama

IDE hata mesajlarını Türkçe olarak gösterir:

```
✗ Hata: Bellek erişim hatası (Segmentation Fault)
✗ Hata: Stack Overflow
✗ Hata: Sıfıra bölme hatası
```

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

## 📖 libZED Kütüphanesi

### Giriş/Çıkış
```python
YAZI_YAZ(lib, ram, adres)      # String'i bas
SAYI_YAZ(lib, sayi)             # Sayıyı bas
SAYI_OKU(lib)                   # Sayı oku
KATAR_OKU(lib, ram, adres, max) # String oku
```

### Bellek Yönetimi
```python
BELLEK_AYIR(lib, boyut)         # Bellek ayır
BELLEK_BOSALT(lib, blok_id)     # Bellek serbest bırak
BELLEK_DURUM(lib)               # Bellek durumu
```

### String İşlemleri
```python
KATAR_UZUNLUK(lib, ram, adres)  # String uzunluğu
KATAR_KOPYALA(lib, ram, kay, hdf) # String kopyala
SAYI_KATARA(lib, ram, sayi, adr)  # Sayıyı string'e dönüştür
```

### Dosya İşlemleri
```python
DOSYA_AC(lib, ram, adres)       # Dosya aç (okuma)
DOSYA_YAZ_AC(lib, ram, adres)   # Dosya aç (yazma)
DOSYA_OKU(lib, fd)              # Dosyadan oku
DOSYA_YAZ(lib, fd, karakter)    # Dosyaya yaz
DOSYA_KAPAT(lib, fd)            # Dosyayı kapat
DOSYA_YAZ_STR(lib, fd, ram, ad) # Dosyaya string yaz
```

## 🎨 Renk Şeması

- 🟢 **Yeşil:** Komutlar
- 🔵 **Cyan:** Etiketler
- 🟡 **Sarı:** Sayılar
- 🔴 **Kırmızı:** Kesmeler
- ⚪ **Gri:** Yorumlar

## 📋 Dosya Yapısı

```
/home/ubuntu/
├── zedin                 # Ana başlatıcı
├── zedin_ide.py         # IDE modülü
├── zedin_kernel.py      # Kernel modülü
├── zedin_editor.py      # Editör modülü
└── libzed.py            # Standart kütüphane
```

## 🔗 Bağlantılar

- **Orijinal Zedin:** /home/ubuntu/README.md
- **Örnek Programlar:** /home/ubuntu/*.zed
- **Kernel Kodu:** /home/ubuntu/kernel.zed

## 📝 Lisans

Zedin Türkçe Assembly - Eğitim ve Araştırma Amaçlı

## 👨‍💻 Geliştirici

Zedin - 10. sınıf öğrencisi tarafından Termux'ta geliştirildi
Python IDE - Manus tarafından geliştirildi

## 🎯 Sonraki Adımlar

- [ ] VS Code sözdizimi desteği
- [ ] Debugger entegrasyonu
- [ ] Grafik modülü
- [ ] Ağ işlemleri
- [ ] Çoklu görev desteği

---

**Hoşça kalın!** 🚀
