#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZEDİN EDITÖR - Sözdizim Vurgulama ve Düzenleme
Türkçe Assembly için gelişmiş editör
"""

import re
from typing import List, Tuple, Optional
from enum import Enum


class TokenTipi(Enum):
    """Token türleri"""
    YORUM = "yorum"
    KOMUT = "komut"
    ETIKET = "etiket"
    VERI = "veri"
    SAYI = "sayi"
    KESME = "kesme"
    DIZE = "dize"
    NORMAL = "normal"


class Renk:
    """ANSI Renk kodları"""
    SIFIRLA = "\033[0m"
    KIRMIZI = "\033[0;31m"
    YESIL = "\033[0;32m"
    SARI = "\033[0;33m"
    MAVI = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    BEYAZ = "\033[1;37m"
    KOYU_GRIS = "\033[90m"
    PARLAK_KIRMIZI = "\033[91m"
    PARLAK_YESIL = "\033[92m"
    PARLAK_SARI = "\033[93m"
    PARLAK_MAVI = "\033[94m"
    PARLAK_MAGENTA = "\033[95m"
    PARLAK_CYAN = "\033[96m"


class ZedinEditör:
    """Zedin Assembly Editörü"""
    
    # Türkçe komutlar
    KOMUTLAR = {
        "BITIR", "YAZDIR", "TOPLA", "SAKLA", "GETIR", "EGER_ESITSE",
        "BUYUKSE", "KUCUKSE", "CIKAR", "CARP", "BOL", "GIT", "SAKLA_CEBI",
        "PUSH", "POP", "CALL", "RET", "OKU", "INT", "YUKLE", "VE", "VEYA",
        "MOD", "DEGIL", "XOR", "SOLA_KAYDIR", "SAGA_KAYDIR", "KARSI_LASTIR",
        "PAKET_GUNCELLE", "PAKET_YUKLE", "PAKET_KALDIR", "PAKET_YUKSELT",
        "AG_ISTEK", "GRAFIK_CIZ", "NESNE_OLUSTUR", "LISTE_EKLE",
        "EGER_DEGILSE", "SAKLA_IND", "GETIR_IND", "SAKLA_B", "GETIR_B"
    }
    
    # Anahtar kelimeler
    ANAHTAR_KELIMELER = {
        "DATA", "BASLA", "BITIR", "FONK", "ZIPLA", "DUR", "AKTAR"
    }
    
    # Kesme numaraları
    KESMELER = {
        "0x14", "0x15", "0x16", "0x17", "0x19", "0x1A", "0x1E", "0x1F",
        "0x20", "0x21", "0x22", "0x23", "0x28", "0x29", "0x2E", "0x32",
        "#20", "#21", "#22", "#23", "#25", "#26", "#30", "#31",
        "#32", "#33", "#34", "#35", "#40", "#41", "#46", "#50"
    }
    
    def __init__(self):
        self.hatalar = []
        self.uyarılar = []
    
    def tokenize(self, satir: str) -> List[Tuple[str, TokenTipi]]:
        """Satırı token'lara ayır"""
        tokens = []
        satir = satir.strip()
        
        if not satir:
            return tokens
        
        # Yorum kontrolü
        if satir.startswith(";"):
            tokens.append((satir, TokenTipi.YORUM))
            return tokens
        
        # Etiket kontrolü (@BASLA)
        if satir.startswith("@"):
            tokens.append((satir, TokenTipi.ETIKET))
            return tokens
        
        # DATA kontrolü
        if satir.startswith("DATA"):
            tokens.append((satir, TokenTipi.VERI))
            return tokens
        
        # Kelime kelime işle
        kelimeler = satir.split()
        for kelime in kelimeler:
            if kelime.startswith(";"):
                tokens.append((kelime, TokenTipi.YORUM))
                break
            elif kelime.startswith('"') and kelime.endswith('"'):
                tokens.append((kelime, TokenTipi.DIZE))
            elif kelime.startswith("#") and kelime[1:].isdigit():
                tokens.append((kelime, TokenTipi.SAYI))
            elif kelime.startswith("$"):
                tokens.append((kelime, TokenTipi.ETIKET))
            elif kelime.startswith("#0x"):
                tokens.append((kelime, TokenTipi.KESME))
            elif kelime.upper() in self.KOMUTLAR:
                tokens.append((kelime, TokenTipi.KOMUT))
            elif kelime.upper() in self.ANAHTAR_KELIMELER:
                tokens.append((kelime, TokenTipi.KOMUT))
            else:
                tokens.append((kelime, TokenTipi.NORMAL))
        
        return tokens
    
    def renklendir(self, satir: str) -> str:
        """Satırı renklendir"""
        tokens = self.tokenize(satir)
        renkli_satir = ""
        
        for kelime, tür in tokens:
            if tür == TokenTipi.YORUM:
                renkli_satir += f"{Renk.KOYU_GRIS}{kelime}{Renk.SIFIRLA} "
            elif tür == TokenTipi.KOMUT:
                renkli_satir += f"{Renk.PARLAK_YESIL}{kelime}{Renk.SIFIRLA} "
            elif tür == TokenTipi.ETIKET:
                renkli_satir += f"{Renk.PARLAK_CYAN}{kelime}{Renk.SIFIRLA} "
            elif tür == TokenTipi.VERI:
                renkli_satir += f"{Renk.PARLAK_MAGENTA}{kelime}{Renk.SIFIRLA} "
            elif tür == TokenTipi.SAYI:
                renkli_satir += f"{Renk.PARLAK_SARI}{kelime}{Renk.SIFIRLA} "
            elif tür == TokenTipi.KESME:
                renkli_satir += f"{Renk.PARLAK_KIRMIZI}{kelime}{Renk.SIFIRLA} "
            elif tür == TokenTipi.DIZE:
                renkli_satir += f"{Renk.PARLAK_YESIL}{kelime}{Renk.SIFIRLA} "
            else:
                renkli_satir += f"{kelime} "
        
        return renkli_satir.rstrip()
    
    def kontrol_et(self, kod: str) -> Tuple[List[str], List[str]]:
        """Kodu kontrol et ve hata/uyarı bul"""
        self.hatalar = []
        self.uyarılar = []
        
        satirlar = kod.strip().split("\n")
        etiketler = set()
        
        # İlk geçiş: Etiketleri topla
        for satir_no, satir in enumerate(satirlar, 1):
            satir = satir.strip()
            if satir.startswith("@"):
                etiket_adi = satir[1:].split()[0]
                etiketler.add(etiket_adi)
        
        # İkinci geçiş: Kontrol et
        for satir_no, satir in enumerate(satirlar, 1):
            satir = satir.strip()
            
            if not satir or satir.startswith(";"):
                continue
            
            tokens = self.tokenize(satir)
            
            # Komut kontrolü
            if tokens and tokens[0][1] == TokenTipi.KOMUT:
                komut = tokens[0][0].upper()
                
                # Parametre sayısı kontrolü
                param_sayisi = len(tokens) - 1
                
                if komut in ["BITIR", "YAZDIR", "POP", "RET", "DEGIL"]:
                    if param_sayisi > 0:
                        self.uyarılar.append(
                            f"Satır {satir_no}: '{komut}' parametresiz olmalı"
                        )
                
                elif komut in ["TOPLA", "CIKAR", "CARP", "BOL", "MOD", "PUSH", "OKU", "INT", "YUKLE"]:
                    if param_sayisi != 1:
                        self.hatalar.append(
                            f"Satır {satir_no}: '{komut}' 1 parametre gerektirir"
                        )
                
                elif komut in ["SAKLA", "EGER_ESITSE", "BUYUKSE", "KUCUKSE", "EGER_DEGILSE"]:
                    if param_sayisi != 2:
                        self.hatalar.append(
                            f"Satır {satir_no}: '{komut}' 2 parametre gerektirir"
                        )
            
            # Etiket referansı kontrolü
            for token, tür in tokens:
                if tür == TokenTipi.ETIKET and token.startswith("$"):
                    etiket_adi = token[1:]
                    if etiket_adi not in etiketler:
                        self.hatalar.append(
                            f"Satır {satir_no}: Bilinmeyen etiket: {etiket_adi}"
                        )
        
        return self.hatalar, self.uyarılar
    
    def satırları_göster(self, kod: str, hata_vurgula: bool = True):
        """Kodu satır numarası ile göster"""
        satirlar = kod.strip().split("\n")
        hatalar, uyarılar = self.kontrol_et(kod) if hata_vurgula else ([], [])
        
        print(f"\n{Renk.PARLAK_CYAN}{'Satır':<6} {'Kod':<50}{Renk.SIFIRLA}")
        print(f"{Renk.PARLAK_CYAN}{'─' * 56}{Renk.SIFIRLA}")
        
        for satir_no, satir in enumerate(satirlar, 1):
            renkli = self.renklendir(satir)
            print(f"{Renk.KOYU_GRIS}{satir_no:<6}{Renk.SIFIRLA}{renkli}")
        
        if hatalar:
            print(f"\n{Renk.PARLAK_KIRMIZI}✗ Hatalar:{Renk.SIFIRLA}")
            for hata in hatalar:
                print(f"  {Renk.KIRMIZI}• {hata}{Renk.SIFIRLA}")
        
        if uyarılar:
            print(f"\n{Renk.PARLAK_SARI}⚠ Uyarılar:{Renk.SIFIRLA}")
            for uyarı in uyarılar:
                print(f"  {Renk.SARI}• {uyarı}{Renk.SIFIRLA}")
    
    def referans_göster(self):
        """Komut referansını göster"""
        print(f"""
{Renk.PARLAK_CYAN}╔════════════════════════════════════════════════════════════════╗{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}║{Renk.SIFIRLA}              {Renk.PARLAK_MAGENTA}ZEDIN KOMUT REFERANSI{Renk.SIFIRLA}                    {Renk.PARLAK_CYAN}║{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}╚════════════════════════════════════════════════════════════════╝{Renk.SIFIRLA}

{Renk.PARLAK_YESIL}BELLEK KOMUTLARI:{Renk.SIFIRLA}
  {Renk.YESIL}YUKLE #değer{Renk.SIFIRLA}          CEB'e değer yükle
  {Renk.YESIL}SAKLA #değer #adres{Renk.SIFIRLA}   RAM'e yaz
  {Renk.YESIL}GETIR #adres{Renk.SIFIRLA}          RAM'den oku
  {Renk.YESIL}SAKLA_CEBI #adres{Renk.SIFIRLA}     CEB'i RAM'e yaz

{Renk.PARLAK_YESIL}ARİTMETİK KOMUTLARI:{Renk.SIFIRLA}
  {Renk.YESIL}TOPLA #değer{Renk.SIFIRLA}          CEB += değer
  {Renk.YESIL}CIKAR #değer{Renk.SIFIRLA}          CEB -= değer
  {Renk.YESIL}CARP #değer{Renk.SIFIRLA}           CEB *= değer
  {Renk.YESIL}BOL #değer{Renk.SIFIRLA}            CEB /= değer
  {Renk.YESIL}MOD #değer{Renk.SIFIRLA}            CEB %= değer

{Renk.PARLAK_YESIL}KONTROL KOMUTLARI:{Renk.SIFIRLA}
  {Renk.YESIL}GIT $etiket{Renk.SIFIRLA}           Etiket adresine atla
  {Renk.YESIL}EGER_ESITSE #ad $et{Renk.SIFIRLA}   CEB == RAM[ad] ise atla
  {Renk.YESIL}BUYUKSE #ad $et{Renk.SIFIRLA}       CEB > RAM[ad] ise atla
  {Renk.YESIL}KUCUKSE #ad $et{Renk.SIFIRLA}       CEB < RAM[ad] ise atla

{Renk.PARLAK_YESIL}STACK KOMUTLARI:{Renk.SIFIRLA}
  {Renk.YESIL}PUSH #değer{Renk.SIFIRLA}           Stack'e it
  {Renk.YESIL}POP{Renk.SIFIRLA}                   Stack'ten al
  {Renk.YESIL}CALL $etiket{Renk.SIFIRLA}          Fonksiyon çağır
  {Renk.YESIL}RET{Renk.SIFIRLA}                   Fonksiyondan dön

{Renk.PARLAK_YESIL}GİRİŞ/ÇIKIS KOMUTLARI:{Renk.SIFIRLA}
  {Renk.YESIL}YAZDIR{Renk.SIFIRLA}                CEB'i ekrana bas
  {Renk.YESIL}INT #kesme{Renk.SIFIRLA}            Sistem kesmesi çağır
  {Renk.YESIL}BITIR{Renk.SIFIRLA}                 Programı durdur

{Renk.PARLAK_CYAN}════════════════════════════════════════════════════════════════{Renk.SIFIRLA}
""")


# Test
if __name__ == "__main__":
    editör = ZedinEditör()
    
    test_kodu = """
; Merhaba Dünya - Zedin Assembly
DATA 100 "Merhaba_Dunya"
@BASLA
YUKLE #100
INT #22
YUKLE #10
INT #20
BITIR
"""
    
    editör.satırları_göster(test_kodu)
    editör.referans_göster()
