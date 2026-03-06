# 1C Bux 3.0 üçün HR (Kadr) modulu — Genişlənmə üzrə texniki plan

Bu sənəd aşağıdakı qəbul edilmiş tələblərə əsaslanır:
- Əhatə dairəsi: tam (işə qəbul, işdən çıxarma, ştat cədvəli, məzuniyyət, ezamiyyət, tabel, müqavilələr, kadr əmrləri).
- İnteqrasiya: Bux daxilində.
- Lokallaşdırma: Azərbaycan (AZ).
- Rollar: HR, mühasib, rəhbər.
- Dil: AZ və RU.
- Texniki yanaşma: tipik konfiqurasiyaya toxunmadan `Genişlənmə (расширение)`.

## 1) Memarlıq prinsipləri

1. Tipik Bux 3.0 obyektləri dəyişdirilmir, yalnız genişlənmə obyektləri və abunə mexanizmləri istifadə olunur.
2. HR sənədlərinin maliyyə təsiri üçün posting məntiqi Bux-un mövcud mexanizmlərinə inteqrasiya olunan servis qatından çağırılır.
3. Bütün istifadəçi formaları ikidilli resurslarla (AZ/RU) işləyir.
4. Audit izləri və status keçidləri registrlərdə saxlanılır.

## 2) Obyekt modeli (1C metadata)

### 2.1 Sorğular (Catalogs)
- `HR_Əməkdaşlar` — şəxsi kart, VÖEN/FİN, əlaqə, bölmə, vəzifə, status.
- `HR_Bölmələr` — təşkilati struktur.
- `HR_Vəzifələr` — vəzifə kodu, dərəcə, tarif parametrləri.
- `HR_ŞtatCədvəli` — bölmə + vəzifə + ştat vahidi + baza maaş intervalı.
- `HR_ƏməkMüqaviləŞablonları` — müqavilə şablonları və versiyalar.
- `HR_İcazəNövləri` — məzuniyyət, ödənişsiz məzuniyyət, xəstəlik və s.

### 2.2 Sənədlər (Documents)
- `HR_İşəQəbul` — işə qəbul əmri.
- `HR_İşdənÇıxarma` — işdən ayrılma əmri.
- `HR_KadrDəyişikliyi` — vəzifə/bölmə/şərt dəyişiklikləri.
- `HR_Məzuniyyət` — məzuniyyət əmri və müddət.
- `HR_Ezamiyyət` — ezamiyyət əmri.
- `HR_Tabel` — aylıq iş vaxtı uçotu.
- `HR_ƏməkMüqaviləsi` — müqavilənin özü və əlavələr.

### 2.3 Registrlər (Registers)
- `HR_İşTarixçəsi` (Information register) — əməkdaşın status və vəzifə tarixçəsi.
- `HR_ŞtatMəşğulluq` (Accumulation register) — ştat vahidlərinin doluluq vəziyyəti.
- `HR_İşVaxtı` (Accumulation register) — tabel saat/gün göstəriciləri.
- `HR_MəzuniyyətQalıqları` (Accumulation register) — məzuniyyət balansı.
- `HR_Razılaşdırmaİzləri` (Information register) — təsdiq marşrutu və audit.

### 2.4 Məlumat emalları / hesabatlar
- `HR_ŞtatStrukturuHesabatı`
- `HR_ƏməkdaşHərəkətiHesabatı`
- `HR_MəzuniyyətBalansıHesabatı`
- `HR_TabelYekunHesabatı`

## 3) Biznes proses və statuslar

### 3.1 Tipik status axını
`Layihə -> Razılaşdırmada -> Təsdiq edildi -> İcra edildi -> Arxiv`

### 3.2 Razılaşdırma marşrutu
- HR yaradır.
- Rəhbər təsdiq edir.
- Mühasib maliyyə təsirini yoxlayır (yalnız tələb olunan sənədlərdə).
- Sistem posting/i̇cra edir və audit yazır.

## 4) Rol modeli və icazələr

- `HR_Mütəxəssis`
  - Kadr sənədlərini yaratmaq/redaktə.
  - Şəxsi kart və müqavilə məlumatlarını idarə etmək.
- `Mühasib`
  - Maliyyə təsiri olan sənədləri görmək/təsdiq etmək.
  - Tabel və məzuniyyət əsasında hesablamalara nəzarət.
- `Rəhbər`
  - Yalnız təsdiq və analitik hesabatlara baxış.
- `Admin`
  - Rolların və lokalizasiya resurslarının idarəsi.

## 5) AZ lokallaşdırma tələbləri

1. Tarix, valyuta, ad-soyad ata adı formatları AZ qaydalarına uyğun.
2. AZ qanunvericiliyinə uyğun məzuniyyət növləri və minimum sahələr.
3. Kadr əmrləri üçün daxili blank şablonları (AZ və RU).
4. XML/Excel ixracında AZ şrift/əlifba uyğunluğu.

## 6) İkidilli (AZ/RU) UI strategiyası

- Bütün formaların caption və mesajları resurs sətirləri ilə verilir.
- Sistem dili əsasında avtomatik seçim + istifadəçi override seçimi.
- Hesabat başlıqları və çap formaları üçün ayrıca lüğət qatından istifadə.

## 7) Bux daxilində inteqrasiya nöqtələri

1. Tabel nəticələri maaş hesablaması üçün daxili mexanizmə ötürülür.
2. Məzuniyyət sənədi üzrə ödəniş günləri mühasibat hesablamasına bağlanır.
3. İşə qəbul/çıxarma dəyişiklikləri analitik kəsiklərdə görünür.
4. Mövcud Bux obyektlərinə birbaşa müdaxilə edilmədən event subscription tətbiq edilir.

## 8) Mərhələli tətbiq planı (Sprint)

### Sprint 1 (2 həftə)
- Metadata karkasının yaradılması (catalog/document/register).
- HR_İşəQəbul və HR_İşdənÇıxarma sənədləri.
- Əsas rol modeli.
- AZ/RU resurs skeleti.

### Sprint 2 (2 həftə)
- Ştat cədvəli + məşğulluq registri.
- Kadr dəyişiklikləri və tarixçə registri.
- Təsdiq marşrutu (HR -> Rəhbər).

### Sprint 3 (2 həftə)
- Məzuniyyət və ezamiyyət sənədləri.
- Məzuniyyət qalıqları registri.
- Mühasib təsdiq addımı və Bux inteqrasiya bağlayıcıları.

### Sprint 4 (2 həftə)
- Tabel sənədi və iş vaxtı registri.
- Hesabatlar (4 əsas hesabat).
- İstifadəçi qəbul testi (UAT), performans və audit yoxlaması.

## 9) Qəbul meyarları

- Genişlənmə söndürüləndə tipik Bux davranışı dəyişməməlidir.
- HR sənədlərinin status keçidləri tam audit olunmalıdır.
- AZ/RU dillərində bütün UI elementləri boş açar olmadan göstərilməlidir.
- Ən azı 500 əməkdaşlıq test datasetində siyahı formaları qəbul edilən sürətdə açılmalıdır.

## 10) Risklər və qarşısının alınması

- **Risk:** Tipik konfiqurasiya yenilənməsi ilə toqquşma.
  - **Mitigasiya:** Yalnız extension point və subscription istifadəsi.
- **Risk:** İkidilli mətnlərin natamam qalması.
  - **Mitigasiya:** release checklist-ə localization completeness maddəsi.
- **Risk:** Məzuniyyət hesablamasında qayda fərqləri.
  - **Mitigasiya:** parametrik qayda cədvəlləri + test ssenariləri.

## 11) Növbəti addım (icra üçün)

1. Bu sənədi təsdiqləyin.
2. Prioriteti Sprint 1 üzrə yekunlaşdırın.
3. Sonra genişlənmə skeleton-u (metadata + role + empty forms) yığılsın.
