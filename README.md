# Quşçuluq Təsərrüfatı Platforması

Bu repozitoriyada quşçuluq təsərrüfatı proseslərinin (partiya uçotu, yemləmə, istehsal, tələfat və satış əməliyyatları) idarə edilməsi üçün hazırlanmış web əsaslı sistemin ilkin versiyası saxlanılır. Layihə Django + Django REST Framework üzərində qurulub və mobil uyğun Bootstrap interfeysi təklif edir.

## Əsas İmkanlar

- Partiyaların, quş növlərinin, təsərrüfat sahələrinin və yem növlərinin referens kataloqları
- İnkubasiya, yemləmə, istehsal, tələfat və satış sənədlərinin uçotu
- Partiya üzrə cari sayın avtomatik yenilənməsi (tələfat və quş satışı zamanı)
- Dashboard: son 7 gün göstəriciləri, aktiv partiyalar, son əməliyyatlar, tez əmr qısayolları
- REST API (autentifikasiya tələb edir) – mobil və ya digər sistemlərlə inteqrasiya üçün
- Çoxdilli dəstək (AZ, RU, EN)

## Texniki Tələblər

- Python 3.12+
- PostgreSQL 13+ (lokal və ya on-prem quraşdırma) — dev mühitində default olaraq SQLite dəstəklənir
- `pip` vasitəsilə asılılıqların quraşdırılması

## Qurulum

```bash
cd poultry_platform
python3 -m venv .venv  # əgər mümkündürsə
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env  # dəyişənləri öz mühitinizə uyğunlaşdırın
python manage.py migrate  # default olaraq SQLite istifadədədir
python manage.py createsuperuser
python manage.py runserver
```

Serverə giriş: [http://localhost:8000](http://localhost:8000)

- Admin paneli: `/admin`
- İstifadəçi girişi/formaları: `/accounts/login` və əsas dashboard
- REST API: `/api/` prefiksi ilə (məsələn: `/api/batches/`)

## Mühit Parametrləri

`.env` faylında nümunə dəyişənlər (bax `.env.example`):

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_DB_*` (PostgreSQL bağlantısı; əgər təyin edilməzsə SQLite işləyəcək)
- `DJANGO_CSRF_TRUSTED_ORIGINS`

## Lokalizasiya

Çoxdilli mətnlər üçün `LOCALE_PATHS` konfiquru edilmişdir. Yeni tərcümə faylları yaratmaq üçün:

```bash
django-admin makemessages -l az
django-admin makemessages -l ru
django-admin makemessages -l en
django-admin compilemessages
```

## Testlər

Hazırda nümunə testlər əlavə edilməyib. Əlavə mərhələdə `tests.py` faylında unit testlər və inteqrasiya testləri yazılması tövsiyə olunur.

## Növbəti Addımlar

- REST API üçün xüsusi icazə/rol siyasətinin hazırlanması
- Hesabatların (SP-29, SP-52 və s.) hazırlanması və ixrac funksiyaları
- Plan-fakt müqayisəsi və bildiriş mexanizmləri
- Mobil tətbiq/Progressive Web App üçün UI təkmilləşdirməsi
