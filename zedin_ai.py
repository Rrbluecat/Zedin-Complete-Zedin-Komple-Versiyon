#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ZEDİN AI ASISTANI - Yapay Zeka Kod Analizi
Hata açıklama, kod tamamlama, öneriler
"""

import re
from typing import List, Dict, Tuple, Optional
from enum import Enum


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


class ZedinAI:
    """Zedin AI Asistanı"""
    
    def __init__(self):
        self.komut_seti = {
            "BITIR", "YAZDIR", "TOPLA", "SAKLA", "GETIR", "EGER_ESITSE",
            "BUYUKSE", "KUCUKSE", "CIKAR", "CARP", "BOL", "GIT", "SAKLA_CEBI",
            "PUSH", "POP", "CALL", "RET", "OKU", "INT", "YUKLE", "VE", "VEYA",
            "MOD", "DEGIL", "XOR", "SOLA_KAYDIR", "SAGA_KAYDIR", "KARSI_LASTIR",
            "PAKET_GUNCELLE", "PAKET_YUKLE", "PAKET_KALDIR", "PAKET_YUKSELT",
            "AG_ISTEK", "GRAFIK_CIZ", "NESNE_OLUSTUR", "LISTE_EKLE",
            "EGER_DEGILSE", "SAKLA_IND", "GETIR_IND", "SAKLA_B", "GETIR_B"
        }
        
        self.komut_parametreleri = {
            "BITIR": 0, "YAZDIR": 0, "POP": 0, "RET": 0, "DEGIL": 0,
            "TOPLA": 1, "CIKAR": 1, "CARP": 1, "BOL": 1, "MOD": 1,
            "PUSH": 1, "OKU": 1, "INT": 1, "YUKLE": 1, "VE": 1, "VEYA": 1,
            "XOR": 1, "SOLA_KAYDIR": 1, "SAGA_KAYDIR": 1,
            "SAKLA": 2, "EGER_ESITSE": 2, "BUYUKSE": 2, "KUCUKSE": 2,
            "EGER_DEGILSE": 2, "SAKLA_IND": 2, "GETIR_IND": 2,
            "SAKLA_B": 2, "GETIR_B": 2, "GIT": 1, "SAKLA_CEBI": 1,
            "CALL": 1, "GETIR": 1
        }
        
        self.komut_aciklamalari = {
            "YUKLE": "CEB'e değer yükle - Merkezi Elektronik Birimini başlat",
            "SAKLA": "RAM'e veri yaz - Belleğe değer depola",
            "GETIR": "RAM'den veri oku - Bellekten değer al",
            "TOPLA": "CEB'e değer ekle - Toplama işlemi yap",
            "CIKAR": "CEB'den değer çıkar - Çıkarma işlemi yap",
            "CARP": "CEB'i değerle çarp - Çarpma işlemi yap",
            "BOL": "CEB'i değere böl - Bölme işlemi yap",
            "MOD": "CEB'in kalanını al - Modulo işlemi yap",
            "GIT": "Etiket adresine atla - Şartlı/şartsız atlama",
            "EGER_ESITSE": "Eşitse atla - Koşullu atlama (==)",
            "BUYUKSE": "Büyükse atla - Koşullu atlama (>)",
            "KUCUKSE": "Küçükse atla - Koşullu atlama (<)",
            "PUSH": "Stack'e değer it - Yığına veri ekle",
            "POP": "Stack'ten değer al - Yığından veri çıkar",
            "CALL": "Fonksiyon çağır - Subroutine'e git",
            "RET": "Fonksiyondan dön - Subroutine'den geri dön",
            "INT": "Sistem kesmesi - İşletim sistemi çağrısı",
            "YAZDIR": "CEB'i ekrana bas - Çıktı ver",
            "BITIR": "Programı durdur - Çalıştırmayı sonlandır"
        }
    
    # ─────────────────────────────────────────────────────────────
    # HATA ANALIZI
    # ─────────────────────────────────────────────────────────────
    
    def hata_analiz_et(self, kod: str) -> List[Dict]:
        """Kodu analiz et ve hataları bul"""
        hatalar = []
        satirlar = kod.strip().split("\n")
        
        for satir_no, satir in enumerate(satirlar, 1):
            satir = satir.strip()
            
            if not satir or satir.startswith(";"):
                continue
            
            # Komut kontrolü
            parcalar = satir.split()
            if parcalar:
                komut = parcalar[0].upper()
                
                # Bilinmeyen komut
                if komut not in self.komut_seti and not komut.startswith("@") and not komut.startswith("DATA"):
                    hatalar.append({
                        "tip": "HATA",
                        "satir": satir_no,
                        "mesaj": f"Bilinmeyen komut: {komut}",
                        "oneri": self._komut_oneri_bul(komut),
                        "cozum": f"Lütfen '{komut}' yerine doğru komut adını yazın"
                    })
                
                # Parametre sayısı kontrolü
                elif komut in self.komut_parametreleri:
                    beklenen = self.komut_parametreleri[komut]
                    gercek = len(parcalar) - 1
                    
                    if beklenen != gercek and komut not in ["GIT", "CALL"]:
                        hatalar.append({
                            "tip": "HATA",
                            "satir": satir_no,
                            "mesaj": f"'{komut}' {beklenen} parametre gerektirir, {gercek} verildi",
                            "oneri": None,
                            "cozum": f"Doğru kullanım: {komut} " + ("#değer " * beklenen).strip()
                        })
                
                # Sayı formatı kontrolü
                for param in parcalar[1:]:
                    if param.startswith("#"):
                        try:
                            int(param[1:])
                        except:
                            hatalar.append({
                                "tip": "HATA",
                                "satir": satir_no,
                                "mesaj": f"Geçersiz sayı formatı: {param}",
                                "oneri": None,
                                "cozum": f"Sayılar #123 formatında yazılmalı"
                            })
        
        return hatalar
    
    def _komut_oneri_bul(self, yanlış_komut: str) -> Optional[str]:
        """Benzer komut önerileri bul"""
        from difflib import get_close_matches
        
        öneriler = get_close_matches(yanlış_komut, self.komut_seti, n=1, cutoff=0.6)
        return öneriler[0] if öneriler else None
    
    # ─────────────────────────────────────────────────────────────
    # KOD TAMAMLAMA
    # ─────────────────────────────────────────────────────────────
    
    def kod_tamamla(self, satir: str, konum: int) -> List[str]:
        """Kod tamamlama önerileri"""
        öneriler = []
        satir = satir[:konum]
        
        # Komut tamamlama
        if satir.startswith(satir.strip()):
            kısmi = satir.strip().upper()
            
            for komut in sorted(self.komut_seti):
                if komut.startswith(kısmi):
                    öneriler.append(komut)
            
            # En fazla 5 öneri
            return öneriler[:5]
        
        return öneriler
    
    # ─────────────────────────────────────────────────────────────
    # KOD ÖRNEKLERİ
    # ─────────────────────────────────────────────────────────────
    
    def ornek_kod_olustur(self, konu: str) -> Optional[str]:
        """Konu için örnek kod oluştur"""
        
        örnekler = {
            "toplama": """; Sayıları toplama
@BASLA
YUKLE #5
TOPLA #3
YAZDIR
BITIR
""",
            
            "dongu": """; 1'den 5'e kadar say
@BASLA
YUKLE #1
@DONGU
YAZDIR
TOPLA #1
KUCUKSE #5 $DONGU
BITIR
""",
            
            "bellek": """; RAM'e yazma ve okuma
@BASLA
YUKLE #42
SAKLA #42 #100
GETIR #100
YAZDIR
BITIR
""",
            
            "fonksiyon": """; Fonksiyon çağrısı
@BASLA
CALL $TOPLAMA
BITIR

@TOPLAMA
YUKLE #10
TOPLA #20
YAZDIR
RET
""",
            
            "kosullu": """; Koşullu atlama
@BASLA
YUKLE #10
SAKLA #5 #100
EGER_ESITSE #100 $ESIT
YAZDIR
GIT $BITTI
@ESIT
YAZDIR
@BITTI
BITIR
""",
            
            "stack": """; Stack kullanımı
@BASLA
YUKLE #10
PUSH #10
YUKLE #20
PUSH #20
POP
YAZDIR
BITIR
"""
        }
        
        return örnekler.get(konu.lower())
    
    # ─────────────────────────────────────────────────────────────
    # HATA AÇIKLAMA
    # ─────────────────────────────────────────────────────────────
    
    def hata_acikla(self, hata_mesaji: str) -> Dict:
        """Hata mesajını açıkla"""
        
        açıklamalar = {
            "Bellek erişim hatası": {
                "açıklama": "Geçersiz bellek adresine erişilmeye çalışıldı",
                "neden": "Çok yüksek veya negatif bir adres kullanıldı",
                "çözüm": "Bellek adreslerini kontrol edin (0-32767 arası)"
            },
            "Stack Overflow": {
                "açıklama": "Stack'in kapasitesi aşıldı",
                "neden": "Çok fazla PUSH veya iç içe CALL yapıldı",
                "çözüm": "Stack kullanımını azaltın veya POP/RET ekleyin"
            },
            "Sıfıra bölme": {
                "açıklama": "Bir sayı sıfıra bölünmeye çalışıldı",
                "neden": "BOL veya MOD komutunda bölen sıfır",
                "çözüm": "Bölen değerini kontrol edin, sıfır olmamalı"
            },
            "Bilinmeyen komut": {
                "açıklama": "Tanınmayan bir komut yazıldı",
                "neden": "Komut adı yanlış yazılmış",
                "çözüm": "Komut adını kontrol edin (YUKLE, SAKLA, vb.)"
            }
        }
        
        for anahtar, bilgi in açıklamalar.items():
            if anahtar.lower() in hata_mesaji.lower():
                return bilgi
        
        return {
            "açıklama": "Bilinmeyen hata",
            "neden": "Hata nedeni belirlenemedi",
            "çözüm": "Kodu adım adım kontrol edin"
        }
    
    # ─────────────────────────────────────────────────────────────
    # KOMUT AÇIKLAMA
    # ─────────────────────────────────────────────────────────────
    
    def komut_acikla(self, komut: str) -> Optional[Dict]:
        """Komut hakkında bilgi ver"""
        komut = komut.upper()
        
        if komut not in self.komut_seti:
            return None
        
        açıklama = self.komut_aciklamalari.get(komut, "Bilgi yok")
        
        return {
            "komut": komut,
            "açıklama": açıklama,
            "parametreler": self.komut_parametreleri.get(komut, 0),
            "örnek": self._komut_ornegi(komut)
        }
    
    def _komut_ornegi(self, komut: str) -> str:
        """Komut örneği"""
        
        örnekler = {
            "YUKLE": "YUKLE #42",
            "SAKLA": "SAKLA #42 #100",
            "GETIR": "GETIR #100",
            "TOPLA": "TOPLA #5",
            "CIKAR": "CIKAR #3",
            "CARP": "CARP #2",
            "BOL": "BOL #2",
            "MOD": "MOD #10",
            "GIT": "GIT $ETIKET",
            "EGER_ESITSE": "EGER_ESITSE #100 $ESIT",
            "BUYUKSE": "BUYUKSE #100 $BUYUK",
            "KUCUKSE": "KUCUKSE #100 $KUCUK",
            "PUSH": "PUSH #10",
            "POP": "POP",
            "CALL": "CALL $FONKSIYON",
            "RET": "RET",
            "INT": "INT #22",
            "YAZDIR": "YAZDIR",
            "BITIR": "BITIR"
        }
        
        return örnekler.get(komut, komut)
    
    # ─────────────────────────────────────────────────────────────
    # PERFORMANS ANALIZI
    # ─────────────────────────────────────────────────────────────
    
    def performans_analiz_et(self, kod: str) -> Dict:
        """Kod performansını analiz et"""
        satirlar = kod.strip().split("\n")
        
        istatistikler = {
            "toplam_komut": 0,
            "dongu_sayisi": 0,
            "fonksiyon_sayisi": 0,
            "bellek_kullanimi": 0,
            "stack_kullanimi": 0,
            "uyarilar": []
        }
        
        for satir in satirlar:
            satir = satir.strip()
            
            if not satir or satir.startswith(";"):
                continue
            
            if satir.startswith("@"):
                if "DONGU" in satir.upper():
                    istatistikler["dongu_sayisi"] += 1
                else:
                    istatistikler["fonksiyon_sayisi"] += 1
            else:
                istatistikler["toplam_komut"] += 1
            
            # Uyarılar
            if "PUSH" in satir:
                istatistikler["stack_kullanimi"] += 1
            if "SAKLA" in satir:
                istatistikler["bellek_kullanimi"] += 1
        
        # Performans önerileri
        if istatistikler["dongu_sayisi"] > 5:
            istatistikler["uyarilar"].append("Çok fazla döngü - performans düşebilir")
        
        if istatistikler["stack_kullanimi"] > 10:
            istatistikler["uyarilar"].append("Stack kullanımı yüksek - Stack Overflow riski")
        
        if istatistikler["toplam_komut"] > 1000:
            istatistikler["uyarilar"].append("Çok uzun program - daha kısa yazın")
        
        return istatistikler
    
    # ─────────────────────────────────────────────────────────────
    # GÖRSEL ÇIKTI
    # ─────────────────────────────────────────────────────────────
    
    def hata_göster(self, hata: Dict):
        """Hatayı güzel şekilde göster"""
        print(f"""
{Renk.PARLAK_KIRMIZI}✗ {hata['tip']}{Renk.SIFIRLA} (Satır {hata['satir']})
{Renk.KIRMIZI}→ {hata['mesaj']}{Renk.SIFIRLA}

{Renk.PARLAK_SARI}💡 Çözüm:{Renk.SIFIRLA}
  {hata['cozum']}
""")
        
        if hata['oneri']:
            print(f"{Renk.PARLAK_CYAN}💭 Öneri:{Renk.SIFIRLA} '{hata['oneri']}' kullanmayı deneyin\n")
    
    def komut_bilgisi_göster(self, komut_info: Dict):
        """Komut bilgisini göster"""
        print(f"""
{Renk.PARLAK_CYAN}╔════════════════════════════════════════╗{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}║{Renk.SIFIRLA} {Renk.PARLAK_YESIL}{komut_info['komut']:<36}{Renk.SIFIRLA} {Renk.PARLAK_CYAN}║{Renk.SIFIRLA}
{Renk.PARLAK_CYAN}╚════════════════════════════════════════╝{Renk.SIFIRLA}

{Renk.CYAN}Açıklama:{Renk.SIFIRLA}
  {komut_info['açıklama']}

{Renk.CYAN}Parametre Sayısı:{Renk.SIFIRLA}
  {komut_info['parametreler']}

{Renk.CYAN}Örnek:{Renk.SIFIRLA}
  {Renk.PARLAK_YESIL}{komut_info['örnek']}{Renk.SIFIRLA}
""")


# Test
if __name__ == "__main__":
    ai = ZedinAI()
    
    # Test kodu
    test_kodu = """
; Test programı
@BASLA
YUKLE #5
TOPLA #3
YAZDIR
BITIR
"""
    
    # Hata analizi
    print(f"{Renk.PARLAK_CYAN}=== HATA ANALIZI ==={Renk.SIFIRLA}")
    hatalar = ai.hata_analiz_et(test_kodu)
    if hatalar:
        for hata in hatalar:
            ai.hata_göster(hata)
    else:
        print(f"{Renk.PARLAK_YESIL}✓ Hata bulunamadı{Renk.SIFIRLA}\n")
    
    # Komut bilgisi
    print(f"{Renk.PARLAK_CYAN}=== KOMUT BİLGİSİ ==={Renk.SIFIRLA}")
    komut_info = ai.komut_acikla("YUKLE")
    if komut_info:
        ai.komut_bilgisi_göster(komut_info)
    
    # Performans analizi
    print(f"{Renk.PARLAK_CYAN}=== PERFORMANS ANALİZİ ==={Renk.SIFIRLA}")
    perf = ai.performans_analiz_et(test_kodu)
    print(f"Toplam komut: {perf['toplam_komut']}")
    print(f"Döngü sayısı: {perf['dongu_sayisi']}")
    print(f"Fonksiyon sayısı: {perf['fonksiyon_sayisi']}\n")
