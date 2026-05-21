#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZEDİN KERNEL - Sistem Yönetimi
Türkçe komut satırı çekirdeği
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict
import struct


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


class ZedinKernel:
    """Zedin İşletim Sistemi Çekirdeği"""
    
    def __init__(self):
        self.isim = "ZED_OS"
        self.surum = "1.0"
        self.baslangiç_zamanı = time.time()
        self.çalışan_program = None
        self.program_sayacı = 0
        self.dosya_sistemi = Path.home() / ".zedin"
        self.dosya_sistemi.mkdir(exist_ok=True)
    
    def hoşgeldiniz(self):
        """Kernel başlangıç mesajı"""
        print(f"""
{Renk.CYAN}╔════════════════════════════════════════════════════════════════╗{Renk.SIFIRLA}
{Renk.CYAN}║{Renk.SIFIRLA}                  {Renk.MAGENTA}ZED_OS v{self.surum}{Renk.SIFIRLA}                          {Renk.CYAN}║{Renk.SIFIRLA}
{Renk.CYAN}║{Renk.SIFIRLA}           Zedin Türkçe Assembly İşletim Sistemi          {Renk.CYAN}║{Renk.SIFIRLA}
{Renk.CYAN}╚════════════════════════════════════════════════════════════════╝{Renk.SIFIRLA}

{Renk.YESIL}✓ Kernel yüklendi{Renk.SIFIRLA}
{Renk.YESIL}✓ Dosya sistemi başlatıldı{Renk.SIFIRLA}
{Renk.YESIL}✓ Sistem hazır{Renk.SIFIRLA}

Komutlar: {Renk.CYAN}yardim{Renk.SIFIRLA}
""")
    
    def yardim(self):
        """Kernel komutları"""
        print(f"""
{Renk.CYAN}═══════════════════════════════════════════════════════════════{Renk.SIFIRLA}
{Renk.MAGENTA}KERNEL KOMUTLARI{Renk.SIFIRLA}
{Renk.CYAN}═══════════════════════════════════════════════════════════════{Renk.SIFIRLA}

{Renk.YESIL}calistir{Renk.SIFIRLA}           - Program yükle ve çalıştır
{Renk.YESIL}listele{Renk.SIFIRLA}           - Programları listele
{Renk.YESIL}temizle{Renk.SIFIRLA}           - Ekranı temizle
{Renk.YESIL}surum{Renk.SIFIRLA}            - Sistem bilgisi
{Renk.YESIL}yardim{Renk.SIFIRLA}           - Bu mesajı göster
{Renk.YESIL}cikis{Renk.SIFIRLA}            - Sistemi kapat

{Renk.CYAN}═══════════════════════════════════════════════════════════════{Renk.SIFIRLA}
""")
    
    def sistem_bilgisi(self):
        """Sistem bilgilerini göster"""
        çalışma_süresi = time.time() - self.baslangiç_zamanı
        saat = int(çalışma_süresi // 3600)
        dakika = int((çalışma_süresi % 3600) // 60)
        saniye = int(çalışma_süresi % 60)
        
        print(f"""
{Renk.CYAN}═══════════════════════════════════════════════════════════════{Renk.SIFIRLA}
{Renk.MAGENTA}SİSTEM BİLGİSİ{Renk.SIFIRLA}
{Renk.CYAN}═══════════════════════════════════════════════════════════════{Renk.SIFIRLA}

{Renk.YESIL}İşletim Sistemi:{Renk.SIFIRLA}    {self.isim} v{self.surum}
{Renk.YESIL}Çalışma Süresi:{Renk.SIFIRLA}     {saat:02d}:{dakika:02d}:{saniye:02d}
{Renk.YESIL}Çalıştırılan Programlar:{Renk.SIFIRLA} {self.program_sayacı}
{Renk.YESIL}Dosya Sistemi:{Renk.SIFIRLA}      {self.dosya_sistemi}

{Renk.CYAN}═══════════════════════════════════════════════════════════════{Renk.SIFIRLA}
""")
    
    def programları_listele(self):
        """Dosya sistemindeki programları listele"""
        programlar = list(self.dosya_sistemi.glob("*.zed"))
        
        if not programlar:
            print(f"{Renk.SARI}! Hiçbir program bulunamadı{Renk.SIFIRLA}")
            return
        
        print(f"\n{Renk.CYAN}Mevcut Programlar:{Renk.SIFIRLA}")
        for i, prog in enumerate(programlar, 1):
            boyut = prog.stat().st_size
            print(f"  {i}. {Renk.YESIL}{prog.name}{Renk.SIFIRLA} ({boyut} byte)")
    
    def program_çalıştır(self, dosya_adi: str):
        """Program çalıştır"""
        dosya_yolu = self.dosya_sistemi / dosya_adi
        
        if not dosya_yolu.exists():
            # Mevcut dizinde ara
            dosya_yolu = Path(dosya_adi)
        
        if not dosya_yolu.exists():
            print(f"{Renk.KIRMIZI}✗ Program bulunamadı: {dosya_adi}{Renk.SIFIRLA}")
            return
        
        print(f"{Renk.YESIL}✓ Program yükleniyor: {dosya_yolu.name}{Renk.SIFIRLA}")
        self.program_sayacı += 1
        
        # Program çalıştırma simülasyonu
        print(f"{Renk.MAVI}[Program çalışıyor...]{Renk.SIFIRLA}")
        time.sleep(0.5)
        print(f"{Renk.YESIL}✓ Program tamamlandı{Renk.SIFIRLA}")
    
    def ana_döngü(self):
        """Kernel ana döngüsü"""
        self.hoşgeldiniz()
        
        while True:
            try:
                komut = input(f"{Renk.MAGENTA}zed_os> {Renk.SIFIRLA}").strip().lower()
                
                if not komut:
                    continue
                
                if komut == "yardim":
                    self.yardim()
                
                elif komut == "surum":
                    self.sistem_bilgisi()
                
                elif komut == "listele":
                    self.programları_listele()
                
                elif komut.startswith("calistir"):
                    parçalar = komut.split()
                    if len(parçalar) > 1:
                        dosya_adi = parçalar[1]
                        self.program_çalıştır(dosya_adi)
                    else:
                        print(f"{Renk.SARI}Kullanım: calistir <dosya>{Renk.SIFIRLA}")
                
                elif komut == "temizle":
                    os.system("clear" if os.name != "nt" else "cls")
                
                elif komut == "cikis":
                    print(f"{Renk.CYAN}Sistem kapatılıyor...{Renk.SIFIRLA}")
                    time.sleep(0.5)
                    print(f"{Renk.YESIL}✓ Hoşça kalın!{Renk.SIFIRLA}")
                    break
                
                else:
                    print(f"{Renk.KIRMIZI}✗ Bilinmeyen komut: {komut}{Renk.SIFIRLA}")
            
            except KeyboardInterrupt:
                print(f"\n{Renk.CYAN}Sistem kapatılıyor...{Renk.SIFIRLA}")
                break
            except Exception as e:
                print(f"{Renk.KIRMIZI}✗ Hata: {e}{Renk.SIFIRLA}")


if __name__ == "__main__":
    kernel = ZedinKernel()
    kernel.ana_döngü()
