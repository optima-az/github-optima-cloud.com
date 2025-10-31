from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from warehouse import InventoryRepository, InventoryService


def test_inventory_flow(tmp_path: Path):
    storage = tmp_path / "data.json"
    repository = InventoryRepository(storage)
    service = InventoryService(repository)

    service.register_product("SKU1", "Printer")
    service.register_warehouse("WH1", "Main", "Baku")

    level = service.adjust_stock("WH1", "SKU1", 15, "Initial load")
    assert level == 15

    level = service.adjust_stock("WH1", "SKU1", -5, "Shipment")
    assert level == 10

    history = service.movement_history("WH1", "SKU1")
    assert len(history) == 2
    assert history[0]["change"] == 15
    assert history[1]["change"] == -5

    report = service.stock_report()
    assert report == [{"warehouse": "WH1", "product": "SKU1", "quantity": 10}]

    with storage.open() as fh:
        saved = json.load(fh)
    assert saved["warehouses"]["WH1"]["stock_levels"]["SKU1"] == 10
