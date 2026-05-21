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
