from django.test import TestCase

from . import models


class BatchModelTests(TestCase):
    def setUp(self):
        self.species = models.BirdSpecies.objects.create(code='BRD', name='Broiler')
        self.location = models.FarmLocation.objects.create(code='INC-01', name='İnkubator 1')

    def test_current_quantity_defaults_to_initial(self):
        batch = models.Batch.objects.create(
            code='BATCH-001',
            species=self.species,
            location=self.location,
            arrival_date='2025-01-01',
            initial_quantity=500,
        )
        self.assertEqual(batch.current_quantity, 500)
