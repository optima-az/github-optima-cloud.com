# 1C Bux 3.0 HR Genişlənməsi — Test ssenariləri (Sprint 1)

## Ssenari 1: İşə qəbul sənədinin tam axını

**Given:** HR istifadəçisi aktivdir və əməkdaş kartı mövcuddur.  
**When:** `HR_İşəQəbul` sənədi yaradılır, `Razılaşdırmada` statusuna göndərilir, rəhbər təsdiqləyir, HR posting edir.  
**Then:** sənəd statusu `İcraEdildi` olur və `HR_İşTarixçəsi` registrində “İşəQəbul” hadisəsi yaranır.

## Ssenari 2: İşdən çıxarma sənədi ilə status yenilənməsi

**Given:** əməkdaşın statusu `Aktiv`-dir.  
**When:** `HR_İşdənÇıxarma` sənədi təsdiq və posting olunur.  
**Then:** `HR_Əməkdaşlar.Status = Pasiv` olur və `HR_İşTarixçəsi`-nə “İşdənÇıxarma” yazılır.

## Ssenari 3: İcazə yoxlaması

**Given:** `Rəhbər` rolunda istifadəçi sistemə daxil olub.  
**When:** sənədi redaktə etməyə və posting etməyə cəhd edir.  
**Then:** sistem əməliyyatı rədd edir (yalnız təsdiq edə bilir).

## Ssenari 4: Status qadağası

**Given:** sənəd `Layihə` statusundadır.  
**When:** posting əmri verilir.  
**Then:** sistem “status uyğun deyil” xətası qaytarır.

## Ssenari 5: Lokalizasiya yoxlaması

**Given:** UI dili AZ-dır.  
**When:** HR forması açılır.  
**Then:** caption-lar AZ görünür.

**Given:** UI dili RU-dur.  
**When:** eyni forma açılır.  
**Then:** caption-lar RU görünür.

## Test data minimumu

- 3 bölmə
- 5 vəzifə
- 20 əməkdaş kartı
- 10 işə qəbul sənədi
- 5 işdən çıxarma sənədi

## Uğur meyarı

- Kritik ssenarilərdən (1–4) 100% keçid.
- Lokalizasiya ssenarisində boş label olmamalıdır.
