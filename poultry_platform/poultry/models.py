from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BirdSpecies(TimeStampedModel):
    code = models.CharField(_('Kod'), max_length=20, unique=True)
    name = models.CharField(_('Adı'), max_length=255)
    breed = models.CharField(_('Cins'), max_length=255, blank=True)
    description = models.TextField(_('Təsvir'), blank=True)

    class Meta:
        verbose_name = _('Quş növü')
        verbose_name_plural = _('Quş növləri')
        ordering = ('name',)

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class FarmLocation(TimeStampedModel):
    class LocationType(models.TextChoices):
        INCUBATOR = 'incubator', _('İnkubator')
        BROODER = 'brooder', _('Yetişdirmə')
        PRODUCTION = 'production', _('İstehsal')
        FEED = 'feed', _('Yem anbarı')
        PROCESSING = 'processing', _('Ət emalı')
        OTHER = 'other', _('Digər')

    code = models.CharField(_('Kod'), max_length=30, unique=True)
    name = models.CharField(_('Adı'), max_length=255)
    location_type = models.CharField(
        _('Sahə tipi'), max_length=20, choices=LocationType.choices, default=LocationType.OTHER
    )
    capacity = models.PositiveIntegerField(_('Tutum (baş)'), null=True, blank=True)
    is_active = models.BooleanField(_('Aktivdir'), default=True)
    notes = models.TextField(_('Qeydlər'), blank=True)

    class Meta:
        verbose_name = _('Təsərrüfat sahəsi')
        verbose_name_plural = _('Təsərrüfat sahələri')
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class FeedType(TimeStampedModel):
    code = models.CharField(_('Kod'), max_length=30, unique=True)
    name = models.CharField(_('Adı'), max_length=255)
    description = models.TextField(_('Təsvir'), blank=True)
    energy_kcal = models.DecimalField(_('Enerji (kcal/kg)'), max_digits=8, decimal_places=2, default=0)
    protein_percent = models.DecimalField(_('Zülal %'), max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('Yem növü')
        verbose_name_plural = _('Yem növləri')
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Batch(TimeStampedModel):
    class BatchStatus(models.TextChoices):
        ACTIVE = 'active', _('Aktiv')
        SOLD = 'sold', _('Satılıb')
        DISPOSED = 'disposed', _('Tələf olub')
        ARCHIVED = 'archived', _('Arxiv')

    code = models.CharField(_('Partiya kodu'), max_length=50, unique=True)
    species = models.ForeignKey(BirdSpecies, on_delete=models.PROTECT, related_name='batches', verbose_name=_('Quş növü'))
    origin = models.CharField(_('Mənşə'), max_length=255, blank=True)
    arrival_date = models.DateField(_('Gətirilmə tarixi'))
    location = models.ForeignKey(
        FarmLocation,
        on_delete=models.PROTECT,
        related_name='batches',
        verbose_name=_('Cari sahə'),
    )
    initial_quantity = models.PositiveIntegerField(_('Başlanğıc say'))
    current_quantity = models.PositiveIntegerField(
        _('Cari say'), help_text=_('Sistem əməliyyatları əsasında yenilənir'), editable=False
    )
    status = models.CharField(
        _('Status'), max_length=20, choices=BatchStatus.choices, default=BatchStatus.ACTIVE
    )
    notes = models.TextField(_('Qeydlər'), blank=True)

    class Meta:
        verbose_name = _('Quş partiyası')
        verbose_name_plural = _('Quş partiyaları')
        ordering = ('-arrival_date', 'code')

    def __str__(self) -> str:
        return f"{self.code} - {self.species.name}"

    def save(self, *args, **kwargs):
        if self._state.adding and not self.current_quantity:
            self.current_quantity = self.initial_quantity
        super().save(*args, **kwargs)


class IncubationRecord(TimeStampedModel):
    class EggCategory(models.TextChoices):
        A = 'A', _('A')
        B = 'B', _('B')
        C = 'C', _('C')
        MIXED = 'mixed', _('Qarışıq')

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name='incubations',
        verbose_name=_('Bağlı partiya'),
    )
    incubator_section = models.CharField(_('İnkubator bölməsi'), max_length=100)
    egg_category = models.CharField(
        _('Yumurta kateqoriyası'), max_length=10, choices=EggCategory.choices, default=EggCategory.A
    )
    eggs_set = models.PositiveIntegerField(_('Qoyulan yumurta sayı'))
    set_date = models.DateField(_('Yerləşdirmə tarixi'))
    expected_hatch_date = models.DateField(_('Gözlənilən çıxış tarixi'), null=True, blank=True)
    hatched_chicks = models.PositiveIntegerField(_('Çıxan cücələr'), default=0)
    hatch_date = models.DateField(_('Faktiki çıxış tarixi'), null=True, blank=True)
    notes = models.TextField(_('Qeydlər'), blank=True)

    class Meta:
        verbose_name = _('İnkubasiya əməliyyatı')
        verbose_name_plural = _('İnkubasiya əməliyyatları')
        ordering = ('-set_date',)

    def __str__(self) -> str:
        return f"{self.batch.code} - {self.incubator_section}"


class FeedLog(TimeStampedModel):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='feed_logs', verbose_name=_('Partiya'))
    location = models.ForeignKey(
        FarmLocation,
        on_delete=models.PROTECT,
        related_name='feed_logs',
        verbose_name=_('Sahə'),
    )
    feed_type = models.ForeignKey(
        FeedType,
        on_delete=models.PROTECT,
        related_name='feed_logs',
        verbose_name=_('Yem növü'),
    )
    record_date = models.DateField(_('Tarix'))
    quantity_kg = models.DecimalField(_('Miqdar (kg)'), max_digits=10, decimal_places=2)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='feed_entries',
        verbose_name=_('Qeyd edən'),
    )
    note = models.TextField(_('Qeydlər'), blank=True)

    class Meta:
        verbose_name = _('Yemləmə qeydi')
        verbose_name_plural = _('Yemləmə qeydləri')
        ordering = ('-record_date', '-created_at')

    def __str__(self) -> str:
        return f"{self.batch.code} - {self.record_date}"


class ProductionLog(TimeStampedModel):
    class ProductionCategory(models.TextChoices):
        TABLE = 'table', _('Süfrə yumurtası')
        HATCHING = 'hatching', _('İnkubasiya yumurtası')
        INDUSTRIAL = 'industrial', _('Sənaye yumurtası')

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name='production_logs',
        verbose_name=_('Partiya'),
    )
    record_date = models.DateField(_('Tarix'))
    eggs_total = models.PositiveIntegerField(_('Yumurta sayı'))
    category = models.CharField(
        _('Kateqoriya'),
        max_length=20,
        choices=ProductionCategory.choices,
        default=ProductionCategory.TABLE,
    )
    storage_location = models.ForeignKey(
        FarmLocation,
        on_delete=models.PROTECT,
        related_name='production_logs',
        verbose_name=_('Saxlanma sahəsi'),
    )
    note = models.TextField(_('Qeydlər'), blank=True)

    class Meta:
        verbose_name = _('İstehsal qeydi')
        verbose_name_plural = _('İstehsal qeydləri')
        ordering = ('-record_date', '-created_at')

    def __str__(self) -> str:
        return f"{self.batch.code} - {self.eggs_total}"


class MortalityLog(TimeStampedModel):
    class MortalityType(models.TextChoices):
        DISEASE = 'disease', _('Xəstəlik')
        ACCIDENT = 'accident', _('Qəza')
        CULLING = 'culling', _('Seçmə (Cull)')
        OTHER = 'other', _('Digər')

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name='mortality_logs',
        verbose_name=_('Partiya'),
    )
    record_date = models.DateField(_('Tarix'))
    count = models.PositiveIntegerField(_('Sayı'))
    mortality_type = models.CharField(
        _('Səbəb'),
        max_length=20,
        choices=MortalityType.choices,
        default=MortalityType.OTHER,
    )
    reason = models.CharField(_('Ətraflı səbəb'), max_length=255, blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mortality_entries',
        verbose_name=_('Qeyd edən'),
    )
    note = models.TextField(_('Qeydlər'), blank=True)

    class Meta:
        verbose_name = _('Tələfat qeydi')
        verbose_name_plural = _('Tələfat qeydləri')
        ordering = ('-record_date', '-created_at')

    def __str__(self) -> str:
        return f"{self.batch.code} - {self.count}"


class SaleRecord(TimeStampedModel):
    class ItemType(models.TextChoices):
        BIRD = 'bird', _('Quş')
        EGG = 'egg', _('Yumurta')
        PRODUCT = 'product', _('Məhsul')

    batch = models.ForeignKey(
        Batch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sales',
        verbose_name=_('Partiya'),
    )
    record_date = models.DateField(_('Tarix'))
    item_type = models.CharField(_('Məhsul növü'), max_length=20, choices=ItemType.choices)
    quantity = models.DecimalField(_('Miqdar'), max_digits=12, decimal_places=2)
    unit = models.CharField(_('Ölçü vahidi'), max_length=20, default=_('ədəd'))
    unit_price = models.DecimalField(_('Vahid qiymət'), max_digits=12, decimal_places=2, default=Decimal('0.00'))
    customer_name = models.CharField(_('Müştəri'), max_length=255)
    document_number = models.CharField(_('Sənəd nömrəsi'), max_length=255, blank=True)
    note = models.TextField(_('Qeydlər'), blank=True)

    class Meta:
        verbose_name = _('Satış qeydi')
        verbose_name_plural = _('Satış qeydləri')
        ordering = ('-record_date', '-created_at')

    def __str__(self) -> str:
        return f"{self.customer_name} - {self.record_date}"


class DailyMetric(TimeStampedModel):
    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name='daily_metrics',
        verbose_name=_('Partiya'),
    )
    date = models.DateField(_('Tarix'))
    feed_used_kg = models.DecimalField(_('Yem (kg)'), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    eggs_collected = models.PositiveIntegerField(_('Toplanan yumurta'), default=0)
    mortality_count = models.PositiveIntegerField(_('Tələfat'), default=0)
    live_weight_kg = models.DecimalField(_('Canlı çəki (kg)'), max_digits=12, decimal_places=2, default=Decimal('0.00'))
    notes = models.TextField(_('Qeydlər'), blank=True)

    class Meta:
        verbose_name = _('Gündəlik göstərici')
        verbose_name_plural = _('Gündəlik göstəricilər')
        ordering = ('-date',)
        unique_together = ('batch', 'date')

    def __str__(self) -> str:
        return f"{self.batch.code} - {self.date}"

# Create your models here.
