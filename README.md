# Warehouse Management Toolkit

Bu layihə anbar idarəetməsi üçün sadə CLI alətini və onu dəstəkləyən nüvə kitabxanasını təqdim edir.
Məhsulların və anbarların qeydiyyatı, ehtiyat səviyyələrinin idarə olunması və hərəkət tarixçəsinin
çıxarılması üçün funksionallıq daxildir.

## Qurulum
Layihə standart Python kitabxanalarından istifadə edir, əlavə paket quraşdırmağa ehtiyac yoxdur.

## İstifadə
```
python main.py <əmr> [seçimlər]
```

### Məhsul əlavə etmək
```
python main.py add-product SKU123 "Məhsul adı" --description "Qısa təsvir"
```

### Anbar yaratmaq
```
python main.py add-warehouse WH1 "Mərkəzi anbar" --location "Bakı"
```

### Ehtiyat səviyyəsini dəyişmək
```
python main.py adjust WH1 SKU123 10 "Yeni mal qəbulu"
```

### Məhsulları göstərmək
```
python main.py products
```

### Anbarları və ehtiyatları göstərmək
```
python main.py warehouses
```

### Hərəkət tarixçəsi
```
python main.py history WH1 SKU123
```

## Testlər
```
pytest
```
