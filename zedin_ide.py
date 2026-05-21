#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔════════════════════════════════════════════════════════════════╗
║     ZEDİN TÜRKÇE ASSEMBLY IDE - KOMUT SATIRI ARAYÜZÜ         ║
║                                                                ║
║  Tüm kodlar Türkçe - Tüm özellikler entegre                  ║
║  VM Simülatörü | Assembler | Linker | Kernel                ║
╚════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import json
import time
import struct
import random
from enum import IntEnum
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import readline  # Komut satırı geçmişi için

try:
    from zedin_ai import ZedinAI
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

try:
    from zedin_security import ZedinSecurity
    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False

# ─────────────────────────────────────────────────────────────
# ZEDIN OPCODE TANIMLARI
# ─────────────────────────────────────────────────────────────

class ZedOpcode(IntEnum):
    """Zedin Assembly Opcode'ları"""
    DUR = 0x00
    YAZDIR = 0x01
    TOPLA = 0x02
    SAKLA = 0x04
    GETIR = 0x05
    EGER_ESITSE = 0x06
    BUYUKSE = 0x07
    KUCUKSE = 0x08
    CIKAR = 0x09
    CARP = 0x0A
    BOL = 0x0B
    GIT = 0x0C
    SAKLA_CEBI = 0x0D
    PUSH = 0x0E
    POP = 0x10
    CALL = 0x11
    RET = 0x12
    OKU = 0x13
    INT = 0x14
    SAKLA_IND = 0x15
    GETIR_IND = 0x16
    SAKLA_B = 0x17
    GETIR_B = 0x18
    EGER_DEGILSE = 0x19
    VE = 0x1A
    VEYA = 0x1B
    MOD = 0x1C
    DEGIL = 0x1D
    YUKLE = 0x1E
    XOR = 0x1F
    SOLA_KAYDIR = 0x20
    SAGA_KAYDIR = 0x21
    KARSI_LASTIR = 0x22
    PAKET_GUNCELLE = 0x23
    PAKET_YUKLE = 0x24
    PAKET_KALDIR = 0x25
    PAKET_YUKSELT = 0x26
    AG_ISTEK = 0x27
    GRAFIK_CIZ = 0x28
    NESNE_OLUSTUR = 0x29
    LISTE_EKLE = 0x2A


# Komut tanımlamaları
KOMUT_SETI = {
    "BITIR": (ZedOpcode.DUR, 1),
    "YAZDIR": (ZedOpcode.YAZDIR, 1),
    "TOPLA": (ZedOpcode.TOPLA, 2),
    "SAKLA": (ZedOpcode.SAKLA, 3),
    "GETIR": (ZedOpcode.GETIR, 2),
    "EGER_ESITSE": (ZedOpcode.EGER_ESITSE, 3),
    "BUYUKSE": (ZedOpcode.BUYUKSE, 3),
    "KUCUKSE": (ZedOpcode.KUCUKSE, 3),
    "CIKAR": (ZedOpcode.CIKAR, 2),
    "CARP": (ZedOpcode.CARP, 2),
    "BOL": (ZedOpcode.BOL, 2),
    "GIT": (ZedOpcode.GIT, 2),
    "SAKLA_CEBI": (ZedOpcode.SAKLA_CEBI, 2),
    "PUSH": (ZedOpcode.PUSH, 2),
    "POP": (ZedOpcode.POP, 1),
    "CALL": (ZedOpcode.CALL, 2),
    "RET": (ZedOpcode.RET, 1),
    "OKU": (ZedOpcode.OKU, 2),
    "INT": (ZedOpcode.INT, 2),
    "YUKLE": (ZedOpcode.YUKLE, 2),
    "VE": (ZedOpcode.VE, 2),
    "VEYA": (ZedOpcode.VEYA, 2),
    "MOD": (ZedOpcode.MOD, 2),
    "DEGIL": (ZedOpcode.DEGIL, 1),
    "XOR": (ZedOpcode.XOR, 2),
    "SOLA_KAYDIR": (ZedOpcode.SOLA_KAYDIR, 2),
    "SAGA_KAYDIR": (ZedOpcode.SAGA_KAYDIR, 2),
}

# Kesme tablosu
KESME_TABLOSU = {
    0x14: "KAR_BAS",           # ASCII karakteri bas
    0x15: "KAR_OKU",           # Karakteri oku
    0x16: "STR_BAS",           # String'i bas
    0x17: "SAY_BAS",           # Sayıyı bas
    0x19: "RASTGELE",          # Rastgele sayı
    0x1A: "ZAMAN",             # Zaman damgası
    0x1E: "DOS_AC_OKU",        # Dosya aç (okuma)
    0x1F: "DOS_OKU_KAR",       # Dosyadan karakter oku
    0x20: "DOS_AC_YAZ",        # Dosya aç (yazma)
    0x21: "DOS_YAZ_KAR",       # Dosyaya karakter yaz
    0x22: "DOS_KAPAT",         # Dosyaları kapat
    0x23: "DOS_YAZ_STR",       # Dosyaya string yaz
    0x28: "BELLEK_AYIR",       # Bellek ayır
    0x29: "BELLEK_SIFIRLA",    # Bellek sıfırla
    0x2E: "STR_KARSI_LASTIR",  # String karşılaştır
    0x32: "PROG_YUKLE",        # Program yükle ve çalıştır
}

# ANSI Renkler
class Renk:
    SIFIRLA = "\033[0m"
    KOYU_KIRMIZI = "\033[0;31m"
    KOYU_YESIL = "\033[0;32m"
    KOYU_SARI = "\033[0;33m"
    KOYU_MAVI = "\033[0;34m"
    KOYU_MAGENTA = "\033[0;35m"
    KOYU_CYAN = "\033[0;36m"
    GRIS = "\033[0;37m"
    
    PARLAK_KIRMIZI = "\033[1;31m"
    PARLAK_YESIL = "\033[1;32m"
    PARLAK_SARI = "\033[1;33m"
    PARLAK_MAVI = "\033[1;34m"
    PARLAK_MAGENTA = "\033[1;35m"
    PARLAK_CYAN = "\033[1;36m"
    BEYAZ = "\033[1;37m"


# ─────────────────────────────────────────────────────────────
# ZEDIN SANAL MAKİNESİ
# ─────────────────────────────────────────────────────────────

class ZedinVM:
    """Zedin Türkçe Assembly Sanal Makinesi"""
    
    def __init__(self, bellek_boyutu: int = 32768, stack_boyutu: int = 2048):
        self.bellek_boyutu = bellek_boyutu
        self.stack_boyutu = stack_boyutu
        
        # Sanal bellek (kod)
        self.sanal_bellek = [0] * bellek_boyutu
        
        # RAM (veri)
        self.ram = [0] * bellek_boyutu
        
        # Stack
        self.stack = [0] * stack_boyutu
        
        # Yazmaçlar
        self.ceb = 0  # Merkezi Elektronik Birimi
        self.ip = 0   # Komut İşaretçisi
        self.sp = 0   # Stack İşaretçisi
        
        # Dosya yönetimi
        self.dosya_okuma = None
        self.dosya_yazma = None
        
        # Heap yönetimi
        self.heap_baslangic = 16000
        self.heap_isaretci = 16000
        
        # Çalıştırma durumu
        self.calisiyormu = False
        self.max_adim = 1000000
        self.adim_sayisi = 0
        self.cikti = ""
        self.hata_mesaji = None
        
    def hata(self, mesaj: str):
        """Hata mesajı göster ve çalıştırmayı durdur"""
        self.hata_mesaji = mesaj
        self.calisiyormu = False
        
    def bellek_kontrol(self, adres: int) -> bool:
        """Bellek erişimini kontrol et"""
        if adres < 0 or adres >= self.bellek_boyutu:
            self.hata(f"Bellek erişim hatası: {adres} (Segmentation Fault)")
            return False
        return True
    
    def stack_kontrol(self, boyut: int) -> bool:
        """Stack overflow kontrolü"""
        if self.sp + boyut >= self.stack_boyutu:
            self.hata("Stack Overflow - Çok fazla PUSH veya iç içe CALL")
            return False
        return True
    
    def ram_string_al(self, adres: int, max_uzunluk: int = 256) -> str:
        """RAM'den string al"""
        sonuc = ""
        for i in range(max_uzunluk):
            if not self.bellek_kontrol(adres + i):
                break
            karakter = self.ram[adres + i]
            if karakter == 0:
                break
            sonuc += chr(karakter) if 32 <= karakter < 127 else f"[{karakter}]"
        return sonuc
    
    def ram_string_yaz(self, adres: int, metin: str):
        """RAM'e string yaz"""
        for i, karakter in enumerate(metin):
            if not self.bellek_kontrol(adres + i):
                break
            self.ram[adres + i] = ord(karakter)
        if self.bellek_kontrol(adres + len(metin)):
            self.ram[adres + len(metin)] = 0  # Null terminator
    
    def binary_yukle(self, dosya_adi: str) -> bool:
        """Binary dosyasını yükle"""
        try:
            with open(dosya_adi, "rb") as f:
                # Magic number
                magic_bytes = f.read(4)
                if len(magic_bytes) < 4:
                    self.hata("Geçersiz binary dosyası")
                    return False
                
                magic = struct.unpack("<I", magic_bytes)[0]
                if magic != 0x5A454400:  # ZED Magic
                    self.hata("Geçersiz ZED magic number")
                    return False
                
                # Kod uzunluğu
                kod_uzunlugu = struct.unpack("<I", f.read(4))[0]
                ram_bas = struct.unpack("<I", f.read(4))[0]
                ram_uzunlugu = struct.unpack("<I", f.read(4))[0]
                
                # Kodu yükle
                for i in range(kod_uzunlugu):
                    if i >= self.bellek_boyutu:
                        break
                    self.sanal_bellek[i] = struct.unpack("<I", f.read(4))[0]
                
                # RAM'i yükle
                for i in range(ram_uzunlugu):
                    if ram_bas + i >= self.bellek_boyutu:
                        break
                    self.ram[ram_bas + i] = struct.unpack("<I", f.read(4))[0]
                
                return True
        except Exception as e:
            self.hata(f"Binary yükleme hatası: {e}")
            return False
    
    def calistir(self):
        """Programı çalıştır"""
        self.calisiyormu = True
        self.adim_sayisi = 0
        self.cikti = ""
        
        while self.calisiyormu and self.adim_sayisi < self.max_adim:
            if not self.bellek_kontrol(self.ip):
                break
            
            opcode = self.sanal_bellek[self.ip]
            self.ip += 1
            self.adim_sayisi += 1
            
            # Komutları işle
            if opcode == ZedOpcode.DUR or opcode == ZedOpcode.BITIR:
                self.calisiyormu = False
            
            elif opcode == ZedOpcode.YAZDIR:
                self.cikti += chr(self.ceb) if 32 <= self.ceb < 127 else f"[{self.ceb}]"
            
            elif opcode == ZedOpcode.YUKLE:
                deger = self.sanal_bellek[self.ip]
                self.ip += 1
                self.ceb = deger
            
            elif opcode == ZedOpcode.TOPLA:
                deger = self.sanal_bellek[self.ip]
                self.ip += 1
                self.ceb += deger
            
            elif opcode == ZedOpcode.CIKAR:
                deger = self.sanal_bellek[self.ip]
                self.ip += 1
                self.ceb -= deger
            
            elif opcode == ZedOpcode.CARP:
                deger = self.sanal_bellek[self.ip]
                self.ip += 1
                self.ceb *= deger
            
            elif opcode == ZedOpcode.BOL:
                deger = self.sanal_bellek[self.ip]
                self.ip += 1
                if deger == 0:
                    self.hata("Sıfıra bölme hatası")
                    break
                self.ceb //= deger
            
            elif opcode == ZedOpcode.MOD:
                deger = self.sanal_bellek[self.ip]
                self.ip += 1
                if deger == 0:
                    self.hata("Sıfıra bölme hatası (MOD)")
                    break
                self.ceb %= deger
            
            elif opcode == ZedOpcode.SAKLA:
                deger = self.sanal_bellek[self.ip]
                adres = self.sanal_bellek[self.ip + 1]
                self.ip += 2
                if self.bellek_kontrol(adres):
                    self.ram[adres] = deger
            
            elif opcode == ZedOpcode.GETIR:
                adres = self.sanal_bellek[self.ip]
                self.ip += 1
                if self.bellek_kontrol(adres):
                    self.ceb = self.ram[adres]
            
            elif opcode == ZedOpcode.SAKLA_CEBI:
                adres = self.sanal_bellek[self.ip]
                self.ip += 1
                if self.bellek_kontrol(adres):
                    self.ram[adres] = self.ceb
            
            elif opcode == ZedOpcode.PUSH:
                deger = self.sanal_bellek[self.ip]
                self.ip += 1
                if self.stack_kontrol(1):
                    self.stack[self.sp] = deger
                    self.sp += 1
            
            elif opcode == ZedOpcode.POP:
                if self.sp > 0:
                    self.sp -= 1
                    self.ceb = self.stack[self.sp]
            
            elif opcode == ZedOpcode.GIT:
                adres = self.sanal_bellek[self.ip]
                self.ip = adres
            
            elif opcode == ZedOpcode.CALL:
                adres = self.sanal_bellek[self.ip]
                self.ip += 1
                if self.stack_kontrol(1):
                    self.stack[self.sp] = self.ip
                    self.sp += 1
                    self.ip = adres
            
            elif opcode == ZedOpcode.RET:
                if self.sp > 0:
                    self.sp -= 1
                    self.ip = self.stack[self.sp]
            
            elif opcode == ZedOpcode.INT:
                kesme_no = self.sanal_bellek[self.ip]
                self.ip += 1
                self.kesme_isle(kesme_no)
            
            elif opcode == ZedOpcode.EGER_ESITSE:
                adres = self.sanal_bellek[self.ip]
                hedef = self.sanal_bellek[self.ip + 1]
                self.ip += 2
                if self.bellek_kontrol(adres):
                    if self.ceb == self.ram[adres]:
                        self.ip = hedef
            
            elif opcode == ZedOpcode.BUYUKSE:
                adres = self.sanal_bellek[self.ip]
                hedef = self.sanal_bellek[self.ip + 1]
                self.ip += 2
                if self.bellek_kontrol(adres):
                    if self.ceb > self.ram[adres]:
                        self.ip = hedef
            
            elif opcode == ZedOpcode.KUCUKSE:
                adres = self.sanal_bellek[self.ip]
                hedef = self.sanal_bellek[self.ip + 1]
                self.ip += 2
                if self.bellek_kontrol(adres):
                    if self.ceb < self.ram[adres]:
                        self.ip = hedef
            
            elif opcode == ZedOpcode.EGER_DEGILSE:
                adres = self.sanal_bellek[self.ip]
                hedef = self.sanal_bellek[self.ip + 1]
                self.ip += 2
                if self.bellek_kontrol(adres):
                    if self.ceb != self.ram[adres]:
                        self.ip = hedef
            
            else:
                self.hata(f"Bilinmeyen opcode: 0x{opcode:02X}")
                break
        
        if self.adim_sayisi >= self.max_adim:
            self.hata(f"Maksimum adım sayısına ulaşıldı ({self.max_adim})")
    
    def kesme_isle(self, kesme_no: int):
        """Sistem kesmesini işle"""
        if kesme_no == 0x14:  # KAR_BAS
            self.cikti += chr(self.ceb) if 32 <= self.ceb < 127 else f"[{self.ceb}]"
        
        elif kesme_no == 0x15:  # KAR_OKU
            try:
                self.ceb = ord(input())
            except:
                self.ceb = 0
        
        elif kesme_no == 0x16:  # STR_BAS
            metin = self.ram_string_al(self.ceb)
            self.cikti += metin
        
        elif kesme_no == 0x17:  # SAY_BAS
            self.cikti += str(self.ceb)
        
        elif kesme_no == 0x19:  # RASTGELE
            self.ceb = random.randint(0, 255)
        
        elif kesme_no == 0x1A:  # ZAMAN
            self.ceb = int(time.time())
        
        elif kesme_no == 0x1E:  # DOS_AC_OKU
            dosya_adi = self.ram_string_al(self.ceb)
            try:
                self.dosya_okuma = open(dosya_adi, "r")
                self.ceb = 1  # Başarı
            except:
                self.ceb = 0  # Hata
        
        elif kesme_no == 0x1F:  # DOS_OKU_KAR
            if self.dosya_okuma:
                karakter = self.dosya_okuma.read(1)
                self.ceb = ord(karakter) if karakter else 0
        
        elif kesme_no == 0x20:  # DOS_AC_YAZ
            dosya_adi = self.ram_string_al(self.ceb)
            try:
                self.dosya_yazma = open(dosya_adi, "w")
                self.ceb = 1  # Başarı
            except:
                self.ceb = 0  # Hata
        
        elif kesme_no == 0x21:  # DOS_YAZ_KAR
            if self.dosya_yazma:
                self.dosya_yazma.write(chr(self.ceb))
        
        elif kesme_no == 0x22:  # DOS_KAPAT
            if self.dosya_okuma:
                self.dosya_okuma.close()
                self.dosya_okuma = None
            if self.dosya_yazma:
                self.dosya_yazma.close()
                self.dosya_yazma = None
        
        elif kesme_no == 0x23:  # DOS_YAZ_STR
            metin = self.ram_string_al(self.ceb)
            if self.dosya_yazma:
                self.dosya_yazma.write(metin)
        
        elif kesme_no == 0x28:  # BELLEK_AYIR
            boyut = self.ceb
            if self.heap_isaretci + boyut < self.bellek_boyutu:
                self.ceb = self.heap_isaretci
                self.heap_isaretci += boyut
            else:
                self.hata("Heap bellek yetersiz")
        
        elif kesme_no == 0x29:  # BELLEK_SIFIRLA
            self.heap_isaretci = self.heap_baslangic
        
        elif kesme_no == 0x2E:  # STR_KARSI_LASTIR
            str1 = self.ram_string_al(self.ceb)
            str2 = self.ram_string_al(self.ram[self.ceb + 1]) if self.bellek_kontrol(self.ceb + 1) else ""
            self.ceb = 1 if str1 == str2 else 0


# ─────────────────────────────────────────────────────────────
# ZEDIN ASSEMBLER
# ─────────────────────────────────────────────────────────────

class ZedinAssembler:
    """Zedin Assembly Derleyicisi"""
    
    def __init__(self):
        self.etiketler = {}
        self.degiskenler = {}
        self.veriler = {}
        self.kod = []
        self.satir_no = 0
        self.hatalar = []
    
    def derle(self, kaynak: str) -> Optional[List[int]]:
        """Kaynak kodu derle"""
        satirlar = kaynak.strip().split("\n")
        
        # İlk geçiş: Etiketleri ve verileri bul
        adres = 0
        for satir in satirlar:
            satir = satir.strip()
            if not satir or satir.startswith(";"):
                continue
            
            if satir.startswith("@"):
                # Etiket
                etiket_adi = satir[1:].split()[0]
                self.etiketler[etiket_adi] = adres
            elif satir.startswith("DATA"):
                # Veri tanımlaması
                parcalar = satir.split()
                if len(parcalar) >= 3:
                    veri_adres = int(parcalar[1])
                    veri_degeri = " ".join(parcalar[2:]).strip('"')
                    self.veriler[veri_adres] = veri_degeri
            else:
                # Komut
                adres += 1
        
        # İkinci geçiş: Kodu derle
        adres = 0
        for satir in satirlar:
            satir = satir.strip()
            if not satir or satir.startswith(";") or satir.startswith("@") or satir.startswith("DATA"):
                continue
            
            if not self.komut_derle(satir, adres):
                return None
            
            adres += 1
        
        return self.kod
    
    def komut_derle(self, komut_satiri: str, adres: int) -> bool:
        """Tek bir komut derle"""
        parcalar = komut_satiri.split()
        if not parcalar:
            return True
        
        komut = parcalar[0].upper()
        
        if komut not in KOMUT_SETI:
            self.hatalar.append(f"Bilinmeyen komut: {komut}")
            return False
        
        opcode, boyut = KOMUT_SETI[komut]
        self.kod.append(opcode)
        
        # Parametreleri işle
        for i in range(1, len(parcalar)):
            param = parcalar[i]
            
            if param.startswith("#"):
                # Sayısal değer
                try:
                    deger = int(param[1:])
                    self.kod.append(deger)
                except:
                    self.hatalar.append(f"Geçersiz sayı: {param}")
                    return False
            
            elif param.startswith("$"):
                # Etiket referansı
                etiket_adi = param[1:]
                if etiket_adi in self.etiketler:
                    self.kod.append(self.etiketler[etiket_adi])
                else:
                    self.hatalar.append(f"Bilinmeyen etiket: {etiket_adi}")
                    return False
            
            else:
                self.hatalar.append(f"Geçersiz parametre: {param}")
                return False
        
        return True


# ─────────────────────────────────────────────────────────────
# KOMUT SATIRI ARAYÜZÜ
# ─────────────────────────────────────────────────────────────

class ZedinIDE:
    """Zedin Komut Satırı IDE"""
    
    def __init__(self):
        self.vm = None
        self.assembler = ZedinAssembler()
        self.mevcut_dosya = None
        self.editör_içeriği = ""
        self.geçmiş = []
        self.ai = ZedinAI() if AI_AVAILABLE else None
        self.güvenlik = ZedinSecurity() if SECURITY_AVAILABLE else None
    
    def hoşgeldiniz(self):
        """Hoşgeldiniz mesajı"""
        print(f"""
{Renk.PARLAK_CYAN}╔════════════════════════════════════════════════════════════════╗{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}║{Renk.SIFIRLA}     {Renk.PARLAK_MAGENTA}ZEDİN TÜRKÇE ASSEMBLY IDE - KOMUT SATIRI{Renk.SIFIRLA}              {Renk.PARLAK_CYAN}║{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}║{Renk.SIFIRLA}                                                                {Renk.PARLAK_CYAN}║{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}║{Renk.SIFIRLA}  {Renk.KOYU_YESIL}Tüm kodlar Türkçe - Tüm özellikler entegre{Renk.SIFIRLA}               {Renk.PARLAK_CYAN}║{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}║{Renk.SIFIRLA}  {Renk.KOYU_YESIL}VM | Assembler | Linker | Kernel{Renk.SIFIRLA}                    {Renk.PARLAK_CYAN}║{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}╚════════════════════════════════════════════════════════════════╝{Renk.SIFIRLA}

{Renk.KOYU_CYAN}Komutlar:{Renk.SIFIRLA}
  {Renk.PARLAK_YESIL}yardim{Renk.SIFIRLA}              - Komut listesini göster
  {Renk.PARLAK_YESIL}yeni{Renk.SIFIRLA}                - Yeni dosya oluştur
  {Renk.PARLAK_YESIL}aç{Renk.SIFIRLA} <dosya>         - Dosya aç
  {Renk.PARLAK_YESIL}kaydet{Renk.SIFIRLA}              - Dosyayı kaydet
  {Renk.PARLAK_YESIL}derle{Renk.SIFIRLA}               - Kodu derle
  {Renk.PARLAK_YESIL}çalıştır{Renk.SIFIRLA}            - Programı çalıştır
  {Renk.PARLAK_YESIL}ai{Renk.SIFIRLA}                 - AI Asistanı (Hata analizi, tamamlama)
  {Renk.PARLAK_YESIL}temizle{Renk.SIFIRLA}             - Ekranı temizle
  {Renk.PARLAK_YESIL}çıkış{Renk.SIFIRLA}               - Programdan çık

""")
    
    def yardim(self):
        """Yardım mesajı"""
        print(f"""
{Renk.PARLAK_CYAN}═══════════════════════════════════════════════════════════════{Renk.SIFIRLA}
{Renk.PARLAK_YESIL}KOMUT REFERANSI{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}═══════════════════════════════════════════════════════════════{Renk.SIFIRLA}

{Renk.KOYU_YESIL}BELLEK KOMUTLARI:{Renk.SIFIRLA}
  YUKLE #değer         - CEB'e değer yükle
  SAKLA #değer #adres  - RAM'e yaz
  GETIR #adres         - RAM'den oku
  SAKLA_CEBI #adres    - CEB'i RAM'e yaz

{Renk.KOYU_YESIL}ARİTMETİK KOMUTLARI:{Renk.SIFIRLA}
  TOPLA #değer         - CEB += değer
  CIKAR #değer         - CEB -= değer
  CARP #değer          - CEB *= değer
  BOL #değer           - CEB /= değer
  MOD #değer           - CEB %= değer

{Renk.KOYU_YESIL}KONTROL KOMUTLARI:{Renk.SIFIRLA}
  GIT $etiket          - Etiket adresine atla
  EGER_ESITSE #ad $et  - CEB == RAM[ad] ise atla
  BUYUKSE #ad $et      - CEB > RAM[ad] ise atla
  KUCUKSE #ad $et      - CEB < RAM[ad] ise atla

{Renk.KOYU_YESIL}STACK KOMUTLARI:{Renk.SIFIRLA}
  PUSH #değer          - Stack'e it
  POP                  - Stack'ten al
  CALL $etiket         - Fonksiyon çağır
  RET                  - Fonksiyondan dön

{Renk.KOYU_YESIL}GİRİŞ/ÇIKIS KOMUTLARI:{Renk.SIFIRLA}
  YAZDIR               - CEB'i ekrana bas
  INT #kesme           - Sistem kesmesi çağır
  BITIR                - Programı durdur

{Renk.PARLAK_CYAN}═══════════════════════════════════════════════════════════════{Renk.SIFIRLA}
""")
    
    def yeni_dosya(self):
        """Yeni dosya oluştur"""
        self.editör_içeriği = ""
        self.mevcut_dosya = None
        print(f"{Renk.PARLAK_YESIL}✓ Yeni dosya oluşturuldu{Renk.SIFIRLA}")
    
    def dosya_aç(self, dosya_adi: str):
        """Dosya aç"""
        # Güvenlik kontrolü
        if self.güvenlik:
            güvenli, mesaj = self.güvenlik.dosya_aç_kontrol(dosya_adi, "r")
            if not güvenli:
                print(f"{Renk.PARLAK_KIRMIZI}✗ {mesaj}{Renk.SIFIRLA}")
                return
        
        try:
            with open(dosya_adi, "r", encoding="utf-8") as f:
                self.editör_içeriği = f.read()
            self.mevcut_dosya = dosya_adi
            print(f"{Renk.PARLAK_YESIL}✓ Dosya açıldı: {dosya_adi}{Renk.SIFIRLA}")
        except FileNotFoundError:
            print(f"{Renk.PARLAK_KIRMIZI}✗ Dosya bulunamadı: {dosya_adi}{Renk.SIFIRLA}")
        except Exception as e:
            print(f"{Renk.PARLAK_KIRMIZI}✗ Hata: {e}{Renk.SIFIRLA}")
    
    def dosya_kaydet(self):
        """Dosyayı kaydet"""
        if not self.mevcut_dosya:
            dosya_adi = input(f"{Renk.KOYU_CYAN}Dosya adı: {Renk.SIFIRLA}")
            if not dosya_adi:
                print(f"{Renk.PARLAK_KIRMIZI}✗ Dosya adı boş{Renk.SIFIRLA}")
                return
            self.mevcut_dosya = dosya_adi
        
        # Güvenlik kontrolü
        if self.güvenlik:
            güvenli, mesaj = self.güvenlik.dosya_aç_kontrol(self.mevcut_dosya, "w")
            if not güvenli:
                print(f"{Renk.PARLAK_KIRMIZI}✗ {mesaj}{Renk.SIFIRLA}")
                return
        
        try:
            with open(self.mevcut_dosya, "w", encoding="utf-8") as f:
                f.write(self.editör_içeriği)
            print(f"{Renk.PARLAK_YESIL}✓ Dosya kaydedildi: {self.mevcut_dosya}{Renk.SIFIRLA}")
        except Exception as e:
            print(f"{Renk.PARLAK_KIRMIZI}✗ Kaydetme hatası: {e}{Renk.SIFIRLA}")
    
    def kodu_derle(self):
        """Kodu derle"""
        if not self.editör_içeriği:
            print(f"{Renk.PARLAK_KIRMIZI}✗ Editör boş{Renk.SIFIRLA}")
            return False
        
        if self.güvenlik:
            güvenli, uyarılar = self.güvenlik.kod_güvenlik_analizi(self.editör_içeriği)
            if uyarılar:
                print(f"{Renk.PARLAK_SARI}Güvenlik Uyarıları:{Renk.SIFIRLA}")
                for uyarı in uyarılar:
                    print(f"  • {uyarı}")
        
        print(f"{Renk.KOYU_CYAN}Derleniyor...{Renk.SIFIRLA}")
        
        assembler = ZedinAssembler()
        kod = assembler.derle(self.editör_içeriği)
        
        if kod is None or assembler.hatalar:
            print(f"{Renk.PARLAK_KIRMIZI}✗ Derleme hataları:{Renk.SIFIRLA}")
            for hata in assembler.hatalar:
                print(f"  {Renk.KOYU_KIRMIZI}• {hata}{Renk.SIFIRLA}")
            return False
        
        # VM'i hazırla
        self.vm = ZedinVM()
        
        # Kodu VM'e yükle
        for i, komut in enumerate(kod):
            if i < self.vm.bellek_boyutu:
                self.vm.sanal_bellek[i] = komut
        
        # Verileri RAM'e yükle
        for adres, veri in assembler.veriler.items():
            self.vm.ram_string_yaz(adres, veri)
        
        print(f"{Renk.PARLAK_YESIL}✓ Derleme başarılı ({len(kod)} komut){Renk.SIFIRLA}")
        return True
    
    def programı_çalıştır(self):
        """Programı çalıştır"""
        if not self.vm:
            if not self.kodu_derle():
                return
        
        print(f"{Renk.KOYU_CYAN}Çalıştırılıyor...{Renk.SIFIRLA}")
        self.vm.calistir()
        
        if self.vm.hata_mesaji:
            print(f"{Renk.PARLAK_KIRMIZI}✗ Hata: {self.vm.hata_mesaji}{Renk.SIFIRLA}")
        else:
            print(f"{Renk.PARLAK_YESIL}✓ Program başarıyla tamamlandı{Renk.SIFIRLA}")
        
        if self.vm.cikti:
            print(f"\n{Renk.KOYU_YESIL}Çıktı:{Renk.SIFIRLA}")
            print(self.vm.cikti)
        
        print(f"\n{Renk.KOYU_CYAN}İstatistikler:{Renk.SIFIRLA}")
        print(f"  Adım sayısı: {self.vm.adim_sayisi}")
        print(f"  CEB değeri: {self.vm.ceb}")
        print(f"  Stack işaretçisi: {self.vm.sp}")
    
    def ai_menu(self):
        """AI Asistanı menüsü"""
        if not self.ai:
            print(f"{Renk.PARLAK_KIRMIZI}✗ AI modülü yüklenmedi{Renk.SIFIRLA}")
            return
        
        while True:
            print(f"""
{Renk.PARLAK_CYAN}╔════════════════════════════════════════╗{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}║{Renk.SIFIRLA} {Renk.PARLAK_MAGENTA}AI ASISTANI MENÜSÜ{Renk.SIFIRLA}                    {Renk.PARLAK_CYAN}║{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}╚════════════════════════════════════════╝{Renk.SIFIRLA}

1. {Renk.PARLAK_YESIL}Hata Analizi{Renk.SIFIRLA}
2. {Renk.PARLAK_YESIL}Komut Bilgisi{Renk.SIFIRLA}
3. {Renk.PARLAK_YESIL}Örnek KodÖnerı{Renk.SIFIRLA}
4. {Renk.PARLAK_YESIL}Performans Analizi{Renk.SIFIRLA}
5. {Renk.PARLAK_YESIL}Geri Dön{Renk.SIFIRLA}
""")
            
            seçim = input(f"{Renk.PARLAK_MAGENTA}ai> {Renk.SIFIRLA}").strip()
            
            if seçim == "1":
                hatalar = self.ai.hata_analiz_et(self.editör_içeriği)
                if hatalar:
                    print(f"\n{Renk.PARLAK_KIRMIZI}Hatalar bulundu:{Renk.SIFIRLA}")
                    for hata in hatalar:
                        self.ai.hata_göster(hata)
                else:
                    print(f"\n{Renk.PARLAK_YESIL}✓ Hata bulunamadı{Renk.SIFIRLA}")
            
            elif seçim == "2":
                komut = input(f"{Renk.PARLAK_MAGENTA}Komut adı: {Renk.SIFIRLA}").strip().upper()
                komut_info = self.ai.komut_acikla(komut)
                if komut_info:
                    self.ai.komut_bilgisi_göster(komut_info)
                else:
                    print(f"{Renk.PARLAK_KIRMIZI}✗ Komut bulunamadı: {komut}{Renk.SIFIRLA}")
            
            elif seçim == "3":
                konu = input(f"{Renk.PARLAK_MAGENTA}Konu (toplama/dongu/bellek/fonksiyon/kosullu/stack): {Renk.SIFIRLA}").strip().lower()
                ornek = self.ai.ornek_kod_olustur(konu)
                if ornek:
                    print(f"\n{Renk.PARLAK_YESIL}Örnek Kod:{Renk.SIFIRLA}")
                    print(f"{Renk.KOYU_GRIS}{ornek}{Renk.SIFIRLA}")
                    self.editör_içeriği = ornek
                    print(f"{Renk.PARLAK_YESIL}✓ Kod editöre yüklendi{Renk.SIFIRLA}")
                else:
                    print(f"{Renk.PARLAK_KIRMIZI}✗ Bilinmeyen konu{Renk.SIFIRLA}")
            
            elif seçim == "4":
                perf = self.ai.performans_analiz_et(self.editör_içeriği)
                print(f"""
{Renk.PARLAK_CYAN}Performans İstatistikleri:{Renk.SIFIRLA}
  Toplam komut: {perf['toplam_komut']}
  Döngü sayısı: {perf['dongu_sayisi']}
  Fonksiyon sayısı: {perf['fonksiyon_sayisi']}
  Bellek kullanımı: {perf['bellek_kullanimi']}
  Stack kullanımı: {perf['stack_kullanimi']}
""")
                if perf['uyarilar']:
                    print(f"{Renk.PARLAK_SARI}⚠ Uyarılar:{Renk.SIFIRLA}")
                    for uyarı in perf['uyarilar']:
                        print(f"  • {uyarı}")
            
            elif seçim == "5":
                break
            
            else:
                print(f"{Renk.PARLAK_KIRMIZI}✗ Geçersiz seçim{Renk.SIFIRLA}")
    
    def editör_aç(self):
        """Basit editör aç"""
        print(f"\n{Renk.KOYU_CYAN}Editör (Çıkmak için 'ÇIKIS' yazın):{Renk.SIFIRLA}")
        satirlar = []
        while True:
            try:
                satir = input(f"{Renk.KOYU_MAVI}>{Renk.SIFIRLA} ")
                if satir.upper() == "ÇIKIS":
                    break
                satirlar.append(satir)
            except KeyboardInterrupt:
                break
        
        self.editör_içeriği = "\n".join(satirlar)
        print(f"{Renk.PARLAK_YESIL}✓ Editör kapatıldı{Renk.SIFIRLA}")
    
    def ana_döngü(self):
        """Ana komut döngüsü"""
        self.hoşgeldiniz()
        
        while True:
            try:
                komut = input(f"{Renk.PARLAK_MAGENTA}zedin> {Renk.SIFIRLA}").strip().lower()
                
                if not komut:
                    continue
                
                if komut == "yardim":
                    self.yardim()
                
                elif komut == "yeni":
                    self.yeni_dosya()
                
                elif komut.startswith("aç "):
                    dosya_adi = komut[3:].strip()
                    self.dosya_aç(dosya_adi)
                
                elif komut == "kaydet":
                    self.dosya_kaydet()
                
                elif komut == "derle":
                    self.kodu_derle()
                
                elif komut == "çalıştır":
                    self.programı_çalıştır()
                
                elif komut == "editör":
                    self.editör_aç()
                
                elif komut == "ai" and self.ai:
                    self.ai_menu()
                
                elif komut == "temizle":
                    os.system("clear" if os.name != "nt" else "cls")
                
                elif komut == "çıkış" or komut == "exit":
                    print(f"{Renk.PARLAK_CYAN}Hoşça kalın!{Renk.SIFIRLA}")
                    break
                
                else:
                    print(f"{Renk.PARLAK_KIRMIZI}✗ Bilinmeyen komut: {komut}{Renk.SIFIRLA}")
            
            except KeyboardInterrupt:
                print(f"\n{Renk.PARLAK_CYAN}Hoşça kalın!{Renk.SIFIRLA}")
                break
            except Exception as e:
                print(f"{Renk.PARLAK_KIRMIZI}✗ Hata: {e}{Renk.SIFIRLA}")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    ide = ZedinIDE()
    ide.ana_döngü()
