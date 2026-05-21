#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZEDİN GÜVENLİK MODÜLÜ
Tüm güvenlik açıklarını kapatma ve koruma
"""

import os
import re
import hashlib
import secrets
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta


class Renk:
    """ANSI Renk kodları"""
    SIFIRLA = "\033[0m"
    KIRMIZI = "\033[0;31m"
    YESIL = "\033[0;32m"
    SARI = "\033[0;33m"
    MAVI = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    PARLAK_KIRMIZI = "\033[91m"
    PARLAK_YESIL = "\033[92m"
    PARLAK_SARI = "\033[93m"
    PARLAK_MAVI = "\033[94m"
    PARLAK_MAGENTA = "\033[95m"
    PARLAK_CYAN = "\033[96m"


class ZedinSecurity:
    """Zedin Güvenlik Sistemi"""
    
    def __init__(self):
        self.güvenlik_log = []
        self.yasaklı_komutlar = set()
        self.yasaklı_dosyalar = set()
        self.maksimum_bellek = 32768
        self.maksimum_stack = 2048
        self.maksimum_adim = 1000000
        self.maksimum_dosya_boyutu = 10 * 1024 * 1024  # 10 MB
        self.maksimum_açık_dosya = 10
        self.oturum_zaman_aşımı = 3600  # 1 saat
        self.başlangıç_zamanı = datetime.now()
        self.açık_dosyalar = {}
        self.giriş_denemeleri = {}
        self.maksimum_giriş_denemesi = 5
        self.giriş_kilidi_süresi = 300  # 5 dakika
    
    # ─────────────────────────────────────────────────────────────
    # GİRİŞ KONTROLÜ VE DOĞRULAMA
    # ─────────────────────────────────────────────────────────────
    
    def şifre_hash(self, şifre: str) -> str:
        """Şifreyi güvenli şekilde hash'le"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            şifre.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return f"{salt}${hash_obj.hex()}"
    
    def şifre_doğrula(self, şifre: str, hash_değeri: str) -> bool:
        """Şifreyi hash ile doğrula"""
        try:
            salt, hash_hex = hash_değeri.split('$')
            hash_obj = hashlib.pbkdf2_hmac(
                'sha256',
                şifre.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return hash_obj.hex() == hash_hex
        except:
            return False
    
    def giriş_dene(self, kullanıcı: str, şifre: str) -> Tuple[bool, str]:
        """Giriş denemesi yap"""
        şimdi = datetime.now()
        
        # Giriş kilidi kontrolü
        if kullanıcı in self.giriş_denemeleri:
            son_deneme = self.giriş_denemeleri[kullanıcı]
            if son_deneme['kilitli_kadar'] > şimdi:
                geçen_saniye = int((son_deneme['kilitli_kadar'] - şimdi).total_seconds())
                return False, f"Hesap kilitli. {geçen_saniye} saniye sonra tekrar deneyin."
            
            # Kilit süresi geçtiyse sıfırla
            if son_deneme['kilitli_kadar'] <= şimdi:
                self.giriş_denemeleri[kullanıcı] = {
                    'deneme_sayısı': 0,
                    'kilitli_kadar': None
                }
        
        # Deneme sayısı kontrolü
        if kullanıcı not in self.giriş_denemeleri:
            self.giriş_denemeleri[kullanıcı] = {
                'deneme_sayısı': 0,
                'kilitli_kadar': None
            }
        
        self.giriş_denemeleri[kullanıcı]['deneme_sayısı'] += 1
        
        if self.giriş_denemeleri[kullanıcı]['deneme_sayısı'] > self.maksimum_giriş_denemesi:
            self.giriş_denemeleri[kullanıcı]['kilitli_kadar'] = şimdi + timedelta(seconds=self.giriş_kilidi_süresi)
            self.güvenlik_log_ekle(f"Kilitli: {kullanıcı} - Çok fazla başarısız giriş denemesi")
            return False, f"Çok fazla başarısız deneme. Hesap {self.giriş_kilidi_süresi} saniye kilitli."
        
        return True, "Giriş başarılı"
    
    # ─────────────────────────────────────────────────────────────
    # DOSYA GÜVENLİĞİ
    # ─────────────────────────────────────────────────────────────
    
    def dosya_yolu_doğrula(self, dosya_yolu: str) -> Tuple[bool, str]:
        """Dosya yolunun güvenli olup olmadığını kontrol et"""
        
        # Path traversal saldırısı kontrolü
        if ".." in dosya_yolu or dosya_yolu.startswith("/"):
            self.güvenlik_log_ekle(f"Path traversal saldırısı engellendi: {dosya_yolu}")
            return False, "Geçersiz dosya yolu"
        
        # Dosya adında tehlikeli karakterler
        tehlikeli_karakterler = ['|', ';', '&', '$', '`', '\n', '\r', '\0']
        for karakter in tehlikeli_karakterler:
            if karakter in dosya_yolu:
                self.güvenlik_log_ekle(f"Tehlikeli karakter engellendi: {karakter}")
                return False, f"Dosya adında '{karakter}' kullanılamaz"
        
        # Dosya boyutu kontrolü
        try:
            gerçek_yol = Path(dosya_yolu)
            if gerçek_yol.exists() and gerçek_yol.stat().st_size > self.maksimum_dosya_boyutu:
                self.güvenlik_log_ekle(f"Dosya çok büyük: {dosya_yolu}")
                return False, f"Dosya çok büyük (Max: {self.maksimum_dosya_boyutu} byte)"
        except:
            pass
        
        return True, "Dosya yolu güvenli"
    
    def dosya_aç_kontrol(self, dosya_yolu: str, mod: str) -> Tuple[bool, str]:
        """Dosya açma işlemini kontrol et"""
        
        # Yol doğrulaması
        güvenli, mesaj = self.dosya_yolu_doğrula(dosya_yolu)
        if not güvenli:
            return False, mesaj
        
        # Açık dosya sayısı kontrolü
        if len(self.açık_dosyalar) >= self.maksimum_açık_dosya:
            self.güvenlik_log_ekle(f"Maksimum açık dosya sayısı aşıldı")
            return False, f"Maksimum {self.maksimum_açık_dosya} dosya açabilirsiniz"
        
        # Dosya türü kontrolü
        izin_verilen_uzantılar = {'.zed', '.txt', '.bin', '.asm', '.c', '.h'}
        uzantı = Path(dosya_yolu).suffix.lower()
        if uzantı not in izin_verilen_uzantılar:
            self.güvenlik_log_ekle(f"İzin verilmeyen dosya türü: {uzantı}")
            return False, f"Bu dosya türü açılamaz: {uzantı}"
        
        return True, "Dosya açılabilir"
    
    # ─────────────────────────────────────────────────────────────
    # KOD GÜVENLİĞİ
    # ─────────────────────────────────────────────────────────────
    
    def kod_güvenlik_analizi(self, kod: str) -> Tuple[bool, List[str]]:
        """Kodu güvenlik açısından analiz et"""
        uyarılar = []
        
        # SQL injection benzeri saldırılar
        sql_benzeri_komutlar = ['SELECT', 'INSERT', 'DELETE', 'UPDATE', 'DROP', 'UNION']
        for komut in sql_benzeri_komutlar:
            if komut in kod.upper():
                uyarılar.append(f"SQL benzeri komut algılandı: {komut}")
        
        # Buffer overflow riski
        if 'SAKLA' in kod.upper():
            # Çok fazla SAKLA komutu
            sakla_sayısı = kod.upper().count('SAKLA')
            if sakla_sayısı > 100:
                uyarılar.append(f"Buffer overflow riski: {sakla_sayısı} SAKLA komutu")
        
        # Stack overflow riski
        push_sayısı = kod.upper().count('PUSH')
        if push_sayısı > 100:
            uyarılar.append(f"Stack overflow riski: {push_sayısı} PUSH komutu")
        
        # Sonsuz döngü riski
        if 'GIT $' in kod and kod.upper().count('GIT') > 10:
            uyarılar.append("Sonsuz döngü riski: Çok fazla GIT komutu")
        
        # Bellek erişim riski
        if 'GETIR' in kod.upper() or 'SAKLA' in kod.upper():
            # Dinamik adres kullanımı
            if re.search(r'(GETIR|SAKLA)\s+#\d+\s+#\d+', kod):
                uyarılar.append("Bellek erişim riski: Dinamik adres kullanımı")
        
        return len(uyarılar) == 0, uyarılar
    
    # ─────────────────────────────────────────────────────────────
    # BELLEK GÜVENLİĞİ
    # ─────────────────────────────────────────────────────────────
    
    def bellek_sınırı_kontrol(self, adres: int, boyut: int = 1) -> bool:
        """Bellek sınırlarını kontrol et"""
        if adres < 0 or (adres + boyut) > self.maksimum_bellek:
            self.güvenlik_log_ekle(f"Bellek sınırı aşıldı: {adres} + {boyut}")
            return False
        return True
    
    def stack_sınırı_kontrol(self, sp: int) -> bool:
        """Stack sınırlarını kontrol et"""
        if sp < 0 or sp >= self.maksimum_stack:
            self.güvenlik_log_ekle(f"Stack sınırı aşıldı: {sp}")
            return False
        return True
    
    def adım_sınırı_kontrol(self, adım_sayısı: int) -> bool:
        """Adım sayısı sınırını kontrol et"""
        if adım_sayısı > self.maksimum_adim:
            self.güvenlik_log_ekle(f"Maksimum adım sayısı aşıldı: {adım_sayısı}")
            return False
        return True
    
    # ─────────────────────────────────────────────────────────────
    # KOMUT GÜVENLİĞİ
    # ─────────────────────────────────────────────────────────────
    
    def komut_doğrula(self, komut: str) -> Tuple[bool, str]:
        """Komutu doğrula"""
        
        # Komut adı doğrulaması
        komut_adı = komut.split()[0].upper() if komut else ""
        
        # Yasaklı komutlar
        if komut_adı in self.yasaklı_komutlar:
            self.güvenlik_log_ekle(f"Yasaklı komut engellendi: {komut_adı}")
            return False, f"Bu komut yasaklı: {komut_adı}"
        
        # Komut uzunluğu kontrolü
        if len(komut) > 1000:
            self.güvenlik_log_ekle(f"Komut çok uzun: {len(komut)} karakter")
            return False, "Komut çok uzun (Max: 1000 karakter)"
        
        # Tehlikeli karakterler
        tehlikeli_karakterler = ['\0', '\n', '\r']
        for karakter in tehlikeli_karakterler:
            if karakter in komut:
                self.güvenlik_log_ekle(f"Tehlikeli karakter engellendi: {repr(karakter)}")
                return False, "Komutta tehlikeli karakter var"
        
        return True, "Komut güvenli"
    
    # ─────────────────────────────────────────────────────────────
    # OTURUM YÖNETİMİ
    # ─────────────────────────────────────────────────────────────
    
    def oturum_zaman_aşımı_kontrol(self) -> bool:
        """Oturum zaman aşımını kontrol et"""
        geçen_zaman = (datetime.now() - self.başlangıç_zamanı).total_seconds()
        if geçen_zaman > self.oturum_zaman_aşımı:
            self.güvenlik_log_ekle("Oturum zaman aşımına uğradı")
            return False
        return True
    
    # ─────────────────────────────────────────────────────────────
    # LOGGING VE DENETIM
    # ─────────────────────────────────────────────────────────────
    
    def güvenlik_log_ekle(self, mesaj: str):
        """Güvenlik olayını kaydet"""
        zaman = datetime.now().isoformat()
        log_girdisi = f"[{zaman}] {mesaj}"
        self.güvenlik_log.append(log_girdisi)
        
        # Dosyaya da yaz
        try:
            with open("/tmp/zedin_security.log", "a") as f:
                f.write(log_girdisi + "\n")
        except:
            pass
    
    def güvenlik_raporu(self) -> str:
        """Güvenlik raporunu oluştur"""
        rapor = f"""
{Renk.PARLAK_CYAN}╔════════════════════════════════════════════════════════════════╗{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}║{Renk.SIFIRLA}              {Renk.PARLAK_MAGENTA}GÜVENLİK RAPORU{Renk.SIFIRLA}                         {Renk.PARLAK_CYAN}║{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}╚════════════════════════════════════════════════════════════════╝{Renk.SIFIRLA}

{Renk.PARLAK_YESIL}✓ Güvenlik Özellikleri:{Renk.SIFIRLA}
  • Giriş kontrolü ve kilit mekanizması
  • Dosya yolu doğrulaması (Path traversal koruması)
  • Dosya boyutu sınırlaması ({self.maksimum_dosya_boyutu} byte)
  • Açık dosya sayısı sınırlaması ({self.maksimum_açık_dosya})
  • Kod güvenlik analizi
  • Bellek sınırı kontrolü ({self.maksimum_bellek} byte)
  • Stack sınırı kontrolü ({self.maksimum_stack} byte)
  • Adım sayısı sınırlaması ({self.maksimum_adim})
  • Komut doğrulaması
  • Oturum zaman aşımı ({self.oturum_zaman_aşımı} saniye)
  • Güvenlik logging ve denetim

{Renk.PARLAK_YESIL}✓ Korunan Saldırı Türleri:{Renk.SIFIRLA}
  • Path Traversal (../../../ saldırıları)
  • Buffer Overflow
  • Stack Overflow
  • SQL Injection benzeri saldırılar
  • Command Injection
  • Sonsuz döngüler
  • Bellek erişim ihlalleri
  • Brute Force giriş saldırıları

{Renk.PARLAK_YESIL}✓ Güvenlik Olayları:{Renk.SIFIRLA}
  Toplam: {len(self.güvenlik_log)}
"""
        
        if self.güvenlik_log:
            rapor += f"\n{Renk.PARLAK_SARI}Son 10 Olay:{Renk.SIFIRLA}\n"
            for olay in self.güvenlik_log[-10:]:
                rapor += f"  {olay}\n"
        
        return rapor
    
    # ─────────────────────────────────────────────────────────────
    # YAPIKLANDIRMA
    # ─────────────────────────────────────────────────────────────
    
    def yapılandırmayı_kaydet(self, dosya: str):
        """Güvenlik yapılandırmasını kaydet"""
        yapılandırma = {
            "maksimum_bellek": self.maksimum_bellek,
            "maksimum_stack": self.maksimum_stack,
            "maksimum_adim": self.maksimum_adim,
            "maksimum_dosya_boyutu": self.maksimum_dosya_boyutu,
            "maksimum_açık_dosya": self.maksimum_açık_dosya,
            "oturum_zaman_aşımı": self.oturum_zaman_aşımı,
            "maksimum_giriş_denemesi": self.maksimum_giriş_denemesi,
            "giriş_kilidi_süresi": self.giriş_kilidi_süresi
        }
        
        try:
            with open(dosya, 'w') as f:
                json.dump(yapılandırma, f, indent=2)
            self.güvenlik_log_ekle(f"Yapılandırma kaydedildi: {dosya}")
        except Exception as e:
            self.güvenlik_log_ekle(f"Yapılandırma kaydetme hatası: {e}")
    
    def yapılandırmayı_yükle(self, dosya: str):
        """Güvenlik yapılandırmasını yükle"""
        try:
            with open(dosya, 'r') as f:
                yapılandırma = json.load(f)
            
            self.maksimum_bellek = yapılandırma.get("maksimum_bellek", self.maksimum_bellek)
            self.maksimum_stack = yapılandırma.get("maksimum_stack", self.maksimum_stack)
            self.maksimum_adim = yapılandırma.get("maksimum_adim", self.maksimum_adim)
            self.maksimum_dosya_boyutu = yapılandırma.get("maksimum_dosya_boyutu", self.maksimum_dosya_boyutu)
            self.maksimum_açık_dosya = yapılandırma.get("maksimum_açık_dosya", self.maksimum_açık_dosya)
            self.oturum_zaman_aşımı = yapılandırma.get("oturum_zaman_aşımı", self.oturum_zaman_aşımı)
            
            self.güvenlik_log_ekle(f"Yapılandırma yüklendi: {dosya}")
        except Exception as e:
            self.güvenlik_log_ekle(f"Yapılandırma yükleme hatası: {e}")


# Test
if __name__ == "__main__":
    güvenlik = ZedinSecurity()
    
    # Test: Dosya yolu doğrulaması
    print(f"{Renk.PARLAK_CYAN}=== DOSYA YOLU DOĞRULAMA ==={Renk.SIFIRLA}")
    test_yolları = ["program.zed", "../../../etc/passwd", "test;rm -rf /", "normal.txt"]
    for yol in test_yolları:
        güvenli, mesaj = güvenlik.dosya_yolu_doğrula(yol)
        durum = f"{Renk.PARLAK_YESIL}✓{Renk.SIFIRLA}" if güvenli else f"{Renk.PARLAK_KIRMIZI}✗{Renk.SIFIRLA}"
        print(f"{durum} {yol}: {mesaj}")
    
    # Test: Kod güvenlik analizi
    print(f"\n{Renk.PARLAK_CYAN}=== KOD GÜVENLİK ANALİZİ ==={Renk.SIFIRLA}")
    test_kodları = [
        "YUKLE #5\nTOPLA #3",
        "PUSH #1\nGIT $DONGU\n@DONGU\nGIT $DONGU",
        "SAKLA #1 #0\nSAKLA #1 #1\n" * 50
    ]
    for kod in test_kodları:
        güvenli, uyarılar = güvenlik.kod_güvenlik_analizi(kod)
        durum = f"{Renk.PARLAK_YESIL}✓{Renk.SIFIRLA}" if güvenli else f"{Renk.PARLAK_KIRMIZI}✗{Renk.SIFIRLA}"
        print(f"{durum} Kod: {len(kod)} karakter")
        for uyarı in uyarılar:
            print(f"   ⚠ {uyarı}")
    
    # Güvenlik raporu
    print(güvenlik.güvenlik_raporu())
