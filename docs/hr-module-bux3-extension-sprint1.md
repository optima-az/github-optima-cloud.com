# 1C Bux 3.0 HR Genişlənməsi — Sprint 1 başlanğıc paketi

Bu sənəd əvvəlki yüksək-səviyyəli planı **icraya hazır** formatda tamamlayır.

## 1) Sprint 1 məqsədi (2 həftə)

Aşağıdakı minimum işlək hissə (MVP) təhvil verilməlidir:
- `HR_Əməkdaşlar` sorğusu (şəxsi kartın əsas sahələri ilə).
- `HR_İşəQəbul` sənədi (yaratma, təsdiq, icra).
- `HR_İşdənÇıxarma` sənədi (yaratma, təsdiq, icra).
- `HR_İşTarixçəsi` registrinə avtomatik yazı.
- Rol bazası: `HR_Mütəxəssis`, `Rəhbər`, `Mühasib`.
- AZ/RU interfeys resurs skeleti.

## 2) Metadata üzrə konkret minimum sahələr

### 2.1 Catalog: `HR_Əməkdaşlar`
- `Kod` (string, avtomatik)
- `Soyad` (string, required)
- `Ad` (string, required)
- `AtaAdı` (string)
- `FIN` (string 7, unique)
- `VÖEN` (string 10, optional)
- `DoğumTarixi` (date)
- `Bölmə` (ref `HR_Bölmələr`, required)
- `Vəzifə` (ref `HR_Vəzifələr`, required)
- `İşəGirişTarixi` (date)
- `Status` (enum: Aktiv, Pasiv)

### 2.2 Document: `HR_İşəQəbul`
Başlıq sahələri:
- `Əməkdaş` (ref `HR_Əməkdaşlar`, required)
- `Tarix` (date, required)
- `Bölmə` (ref `HR_Bölmələr`, required)
- `Vəzifə` (ref `HR_Vəzifələr`, required)
- `ƏməkHaqqıTipi` (enum)
- `ƏsasMaaş` (number 15.2)
- `Status` (enum: Layihə, Razılaşdırmada, TəsdiqEdildi, İcraEdildi)

Posting zamanı:
- `HR_İşTarixçəsi` registrinə “İşə qəbul” hadisəsi yazılır.

### 2.3 Document: `HR_İşdənÇıxarma`
Başlıq sahələri:
- `Əməkdaş` (ref `HR_Əməkdaşlar`, required)
- `Tarix` (date, required)
- `Səbəb` (string, required)
- `ƏmrNömrəsi` (string)
- `Status` (enum: Layihə, Razılaşdırmada, TəsdiqEdildi, İcraEdildi)

Posting zamanı:
- `HR_İşTarixçəsi` registrinə “İşdən çıxarma” hadisəsi yazılır.
- `HR_Əməkdaşlar.Status = Pasiv` yenilənir.

### 2.4 Information register: `HR_İşTarixçəsi`
Ölçülər:
- `Əməkdaş`
- `Tarix`

Resurslar:
- `HadisəNövü` (enum: İşəQəbul, İşdənÇıxarma, Dəyişiklik)
- `Bölmə`
- `Vəzifə`
- `Sənəd` (DocumentRef)

## 3) İş axını (workflow)

1. HR sənədi yaradır (`Layihə`).
2. Rəhbərə göndərir (`Razılaşdırmada`).
3. Rəhbər təsdiq edir (`TəsdiqEdildi`).
4. HR icra edir (`İcraEdildi`) və posting baş verir.

Qadağalar:
- `İcraEdildi` statusunda redaktə qadağandır.
- `Layihə` statusunda posting qadağandır.

## 4) Rol matrisi (Sprint 1)

| Əməliyyat | HR_Mütəxəssis | Rəhbər | Mühasib |
|---|---:|---:|---:|
| HR_İşəQəbul yaratmaq/redaktə | ✅ | ❌ | ❌ |
| HR_İşdənÇıxarma yaratmaq/redaktə | ✅ | ❌ | ❌ |
| Sənədi təsdiq etmək | ❌ | ✅ | ❌ |
| Sənədi icra etmək (posting) | ✅ | ❌ | ❌ |
| Hesabatlara baxış | ✅ | ✅ | ✅ |

## 5) AZ/RU lüğət üçün minimal açarlar

- `HR.Hire.Title` = `İşə qəbul` / `Прием на работу`
- `HR.Fire.Title` = `İşdən çıxarma` / `Увольнение`
- `HR.Status.Draft` = `Layihə` / `Черновик`
- `HR.Status.Approval` = `Razılaşdırmada` / `На согласовании`
- `HR.Status.Approved` = `Təsdiq edildi` / `Согласовано`
- `HR.Status.Posted` = `İcra edildi` / `Проведено`

## 6) Sprint 1 tapşırıq planı (icra)

1. Extension metadata skeletini yarat.
2. Enum-ları və rolları əlavə et.
3. `HR_Əməkdaşlar` sorğusu və forma.
4. `HR_İşəQəbul` sənədi + posting proseduru.
5. `HR_İşdənÇıxarma` sənədi + posting proseduru.
6. `HR_İşTarixçəsi` registri və yazı mexanizmi.
7. AZ/RU resurs fayllarını bağla.
8. Smoke test ssenarilərini icra et.

## 7) Sprint 1 “Definition of Done”

- Hər iki sənəd (`İşəQəbul`, `İşdənÇıxarma`) status axınını keçməlidir.
- Posting nəticəsində registr yazıları yaradılmalıdır.
- Səlahiyyətsiz rol təsdiq/posting edə bilməməlidir.
- AZ və RU dillərində əsas caption-lar boş qalmamalıdır.
