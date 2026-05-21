#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
libZED - Zedin Standart Kütüphanesi
Türkçe yazılı sistem kütüphanesi
"""

from typing import Optional, List, Dict
import os
import time


class libZED:
    """Zedin Standart Kütüphanesi"""
    
    def __init__(self, vm=None):
        """
        libZED başlatıcısı
        
        Args:
            vm: Zedin VM örneği
        """
        self.vm = vm
        self.dosyalar = {}
        self.dosya_sayacı = 0
        self.bellek_blokları = {}
        self.blok_sayacı = 0
    
    # ─────────────────────────────────────────────────────────────
    # GİRİŞ/ÇIKIS FONKSIYONLARI
    # ─────────────────────────────────────────────────────────────
    
    def YAZI_YAZ(self, ram: List[int], adres: int) -> None:
        """
        RAM'deki string'i ekrana bas
        
        Args:
            ram: RAM belleği
            adres: String başlangıç adresi
        """
        metin = ""
        i = 0
        while i < 256:
            if adres + i >= len(ram):
                break
            karakter = ram[adres + i]
            if karakter == 0:
                break
            metin += chr(karakter) if 32 <= karakter < 127 else f"[{karakter}]"
            i += 1
        print(metin, end="")
    
    def SAYI_YAZ(self, sayi: int) -> None:
        """
        Sayıyı ekrana bas
        
        Args:
            sayi: Yazılacak sayı
        """
        print(sayi, end="")
    
    def SAYI_OKU(self) -> int:
        """
        Klavyeden sayı oku
        
        Returns:
            Okunan sayı
        """
        try:
            return int(input())
        except:
            return 0
    
    def KATAR_OKU(self, ram: List[int], adres: int, max_uzunluk: int) -> int:
        """
        Klavyeden string oku ve RAM'e yaz
        
        Args:
            ram: RAM belleği
            adres: Yazılacak adres
            max_uzunluk: Maksimum uzunluk
        
        Returns:
            Okunan karakter sayısı
        """
        try:
            metin = input()[:max_uzunluk - 1]
            for i, karakter in enumerate(metin):
                if adres + i < len(ram):
                    ram[adres + i] = ord(karakter)
            if adres + len(metin) < len(ram):
                ram[adres + len(metin)] = 0
            return len(metin)
        except:
            return 0
    
    # ─────────────────────────────────────────────────────────────
    # BELLEK YÖNETIMI FONKSIYONLARI
    # ─────────────────────────────────────────────────────────────
    
    def BELLEK_AYIR(self, boyut: int) -> int:
        """
        Heap'ten bellek ayır
        
        Args:
            boyut: Ayırılacak bellek boyutu
        
        Returns:
            Bellek bloğu ID'si
        """
        blok_id = self.blok_sayacı
        self.bellek_blokları[blok_id] = {
            "boyut": boyut,
            "veri": [0] * boyut,
            "zaman": time.time()
        }
        self.blok_sayacı += 1
        return blok_id
    
    def BELLEK_BOSALT(self, blok_id: int) -> bool:
        """
        Bellek bloğunu serbest bırak
        
        Args:
            blok_id: Serbest bırakılacak blok ID'si
        
        Returns:
            Başarı durumu
        """
        if blok_id in self.bellek_blokları:
            del self.bellek_blokları[blok_id]
            return True
        return False
    
    def BELLEK_DURUM(self) -> Dict:
        """
        Bellek durumunu göster
        
        Returns:
            Bellek istatistikleri
        """
        toplam_bellek = sum(blok["boyut"] for blok in self.bellek_blokları.values())
        return {
            "toplam_blok": len(self.bellek_blokları),
            "toplam_bellek": toplam_bellek,
            "bloklar": self.bellek_blokları
        }
    
    # ─────────────────────────────────────────────────────────────
    # STRING İŞLEMLERİ FONKSIYONLARI
    # ─────────────────────────────────────────────────────────────
    
    def KATAR_UZUNLUK(self, ram: List[int], adres: int) -> int:
        """
        String uzunluğunu hesapla
        
        Args:
            ram: RAM belleği
            adres: String başlangıç adresi
        
        Returns:
            String uzunluğu
        """
        uzunluk = 0
        while adres + uzunluk < len(ram) and ram[adres + uzunluk] != 0:
            uzunluk += 1
        return uzunluk
    
    def KATAR_KOPYALA(self, ram: List[int], kaynak: int, hedef: int) -> int:
        """
        String kopyala
        
        Args:
            ram: RAM belleği
            kaynak: Kaynak adres
            hedef: Hedef adres
        
        Returns:
            Kopyalanan karakter sayısı
        """
        i = 0
        while kaynak + i < len(ram) and hedef + i < len(ram) and ram[kaynak + i] != 0:
            ram[hedef + i] = ram[kaynak + i]
            i += 1
        if hedef + i < len(ram):
            ram[hedef + i] = 0
        return i
    
    def SAYI_KATARA(self, ram: List[int], sayi: int, adres: int) -> int:
        """
        Sayıyı string'e dönüştür
        
        Args:
            ram: RAM belleği
            sayi: Dönüştürülecek sayı
            adres: Yazılacak adres
        
        Returns:
            Yazılan karakter sayısı
        """
        metin = str(sayi)
        for i, karakter in enumerate(metin):
            if adres + i < len(ram):
                ram[adres + i] = ord(karakter)
        if adres + len(metin) < len(ram):
            ram[adres + len(metin)] = 0
        return len(metin)
    
    # ─────────────────────────────────────────────────────────────
    # DOSYA İŞLEMLERİ FONKSIYONLARI
    # ─────────────────────────────────────────────────────────────
    
    def DOSYA_AC(self, ram: List[int], adres: int) -> int:
        """
        Okuma için dosya aç
        
        Args:
            ram: RAM belleği
            adres: Dosya adı adresi
        
        Returns:
            Dosya tanımlayıcısı (başarılıysa) veya -1 (hata)
        """
        dosya_adi = ""
        i = 0
        while adres + i < len(ram) and ram[adres + i] != 0:
            dosya_adi += chr(ram[adres + i])
            i += 1
        
        try:
            fd = self.dosya_sayacı
            self.dosyalar[fd] = {
                "dosya": open(dosya_adi, "r"),
                "mod": "oku",
                "adi": dosya_adi
            }
            self.dosya_sayacı += 1
            return fd
        except:
            return -1
    
    def DOSYA_YAZ_AC(self, ram: List[int], adres: int) -> int:
        """
        Yazma için dosya aç
        
        Args:
            ram: RAM belleği
            adres: Dosya adı adresi
        
        Returns:
            Dosya tanımlayıcısı (başarılıysa) veya -1 (hata)
        """
        dosya_adi = ""
        i = 0
        while adres + i < len(ram) and ram[adres + i] != 0:
            dosya_adi += chr(ram[adres + i])
            i += 1
        
        try:
            fd = self.dosya_sayacı
            self.dosyalar[fd] = {
                "dosya": open(dosya_adi, "w"),
                "mod": "yaz",
                "adi": dosya_adi
            }
            self.dosya_sayacı += 1
            return fd
        except:
            return -1
    
    def DOSYA_OKU(self, fd: int) -> int:
        """
        Dosyadan karakter oku
        
        Args:
            fd: Dosya tanımlayıcısı
        
        Returns:
            Okunan karakter (ASCII) veya 0 (EOF/hata)
        """
        if fd not in self.dosyalar:
            return 0
        
        try:
            karakter = self.dosyalar[fd]["dosya"].read(1)
            return ord(karakter) if karakter else 0
        except:
            return 0
    
    def DOSYA_YAZ(self, fd: int, karakter: int) -> bool:
        """
        Dosyaya karakter yaz
        
        Args:
            fd: Dosya tanımlayıcısı
            karakter: Yazılacak karakter (ASCII)
        
        Returns:
            Başarı durumu
        """
        if fd not in self.dosyalar:
            return False
        
        try:
            self.dosyalar[fd]["dosya"].write(chr(karakter))
            return True
        except:
            return False
    
    def DOSYA_KAPAT(self, fd: int) -> bool:
        """
        Dosyayı kapat
        
        Args:
            fd: Dosya tanımlayıcısı
        
        Returns:
            Başarı durumu
        """
        if fd not in self.dosyalar:
            return False
        
        try:
            self.dosyalar[fd]["dosya"].close()
            del self.dosyalar[fd]
            return True
        except:
            return False
    
    def DOSYA_YAZ_STR(self, fd: int, ram: List[int], adres: int) -> int:
        """
        Dosyaya string yaz
        
        Args:
            fd: Dosya tanımlayıcısı
            ram: RAM belleği
            adres: String başlangıç adresi
        
        Returns:
            Yazılan karakter sayısı
        """
        if fd not in self.dosyalar:
            return 0
        
        yazılan = 0
        i = 0
        try:
            while adres + i < len(ram) and ram[adres + i] != 0:
                self.dosyalar[fd]["dosya"].write(chr(ram[adres + i]))
                yazılan += 1
                i += 1
            return yazılan
        except:
            return 0
    
    # ─────────────────────────────────────────────────────────────
    # YARDIMCI FONKSIYONLAR
    # ─────────────────────────────────────────────────────────────
    
    def tüm_dosyaları_kapat(self):
        """Tüm açık dosyaları kapat"""
        for fd in list(self.dosyalar.keys()):
            self.DOSYA_KAPAT(fd)
    
    def tüm_belleği_temizle(self):
        """Tüm bellek bloklarını serbest bırak"""
        self.bellek_blokları.clear()
        self.blok_sayacı = 0


# ─────────────────────────────────────────────────────────────
# MAKRO TANIMLAMALARI (C'deki gibi)
# ─────────────────────────────────────────────────────────────

def YAZI_YAZ(lib: libZED, ram: List[int], adres: int):
    """Makro: String'i ekrana bas"""
    lib.YAZI_YAZ(ram, adres)

def SAYI_YAZ(lib: libZED, sayi: int):
    """Makro: Sayıyı ekrana bas"""
    lib.SAYI_YAZ(sayi)

def SAYI_OKU(lib: libZED) -> int:
    """Makro: Sayı oku"""
    return lib.SAYI_OKU()

def KATAR_OKU(lib: libZED, ram: List[int], adres: int, max_uzunluk: int) -> int:
    """Makro: String oku"""
    return lib.KATAR_OKU(ram, adres, max_uzunluk)

def BELLEK_AYIR(lib: libZED, boyut: int) -> int:
    """Makro: Bellek ayır"""
    return lib.BELLEK_AYIR(boyut)

def BELLEK_BOSALT(lib: libZED, blok_id: int) -> bool:
    """Makro: Bellek serbest bırak"""
    return lib.BELLEK_BOSALT(blok_id)

def BELLEK_DURUM(lib: libZED) -> Dict:
    """Makro: Bellek durumu"""
    return lib.BELLEK_DURUM()

def KATAR_UZUNLUK(lib: libZED, ram: List[int], adres: int) -> int:
    """Makro: String uzunluğu"""
    return lib.KATAR_UZUNLUK(ram, adres)

def KATAR_KOPYALA(lib: libZED, ram: List[int], kaynak: int, hedef: int) -> int:
    """Makro: String kopyala"""
    return lib.KATAR_KOPYALA(ram, kaynak, hedef)

def SAYI_KATARA(lib: libZED, ram: List[int], sayi: int, adres: int) -> int:
    """Makro: Sayıyı string'e dönüştür"""
    return lib.SAYI_KATARA(ram, sayi, adres)

def DOSYA_AC(lib: libZED, ram: List[int], adres: int) -> int:
    """Makro: Dosya aç (okuma)"""
    return lib.DOSYA_AC(ram, adres)

def DOSYA_YAZ_AC(lib: libZED, ram: List[int], adres: int) -> int:
    """Makro: Dosya aç (yazma)"""
    return lib.DOSYA_YAZ_AC(ram, adres)

def DOSYA_OKU(lib: libZED, fd: int) -> int:
    """Makro: Dosyadan oku"""
    return lib.DOSYA_OKU(fd)

def DOSYA_YAZ(lib: libZED, fd: int, karakter: int) -> bool:
    """Makro: Dosyaya yaz"""
    return lib.DOSYA_YAZ(fd, karakter)

def DOSYA_KAPAT(lib: libZED, fd: int) -> bool:
    """Makro: Dosyayı kapat"""
    return lib.DOSYA_KAPAT(fd)

def DOSYA_YAZ_STR(lib: libZED, fd: int, ram: List[int], adres: int) -> int:
    """Makro: Dosyaya string yaz"""
    return lib.DOSYA_YAZ_STR(fd, ram, adres)
