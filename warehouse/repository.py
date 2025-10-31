from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .models import Product, StockMovement, Warehouse, WarehouseInventory


class InventoryRepository:
    """Persist warehouse and product data using a JSON document."""

    def __init__(self, storage_path: str | Path = "warehouse_data.json") -> None:
        self.path = Path(storage_path)
        self.path.touch(exist_ok=True)
        if self.path.stat().st_size == 0:
            self._write({"warehouses": {}, "products": {}})

    def _read(self) -> dict[str, Any]:
        with self.path.open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def _write(self, data: dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

    # Product operations
    def list_products(self) -> list[Product]:
        data = self._read()
        return [Product(**entry) for entry in data["products"].values()]

    def save_product(self, product: Product) -> None:
        data = self._read()
        if product.sku in data["products"]:
            raise ValueError("Product already exists")
        data["products"][product.sku] = {
            "sku": product.sku,
            "name": product.name,
            "description": product.description,
        }
        self._write(data)

    # Warehouse operations
    def list_warehouses(self) -> list[WarehouseInventory]:
        data = self._read()
        return [self._deserialize_inventory(code, payload) for code, payload in data["warehouses"].items()]

    def save_warehouse(self, warehouse: Warehouse) -> WarehouseInventory:
        data = self._read()
        if warehouse.code in data["warehouses"]:
            raise ValueError("Warehouse already exists")
        data["warehouses"][warehouse.code] = {
            "name": warehouse.name,
            "location": warehouse.location,
            "stock_levels": {},
            "movements": [],
        }
        self._write(data)
        return WarehouseInventory(warehouse=warehouse)

    def load_inventory(self, code: str) -> WarehouseInventory:
        data = self._read()
        try:
            payload = data["warehouses"][code]
        except KeyError as exc:
            raise KeyError("Warehouse not found") from exc
        return self._deserialize_inventory(code, payload)

    def update_inventory(self, inventory: WarehouseInventory) -> None:
        data = self._read()
        data["warehouses"][inventory.warehouse.code] = {
            "name": inventory.warehouse.name,
            "location": inventory.warehouse.location,
            "stock_levels": inventory.stock_levels,
            "movements": [
                {
                    "product_sku": movement.product_sku,
                    "warehouse_code": movement.warehouse_code,
                    "change": movement.change,
                    "reason": movement.reason,
                    "created_at": movement.created_at.isoformat(),
                }
                for movement in inventory.movements
            ],
        }
        self._write(data)

    def clear(self) -> None:
        self._write({"warehouses": {}, "products": {}})

    def _deserialize_inventory(self, code: str, payload: dict[str, Any]) -> WarehouseInventory:
        warehouse = Warehouse(code=code, name=payload["name"], location=payload.get("location"))
        inventory = WarehouseInventory(warehouse=warehouse)
        inventory.stock_levels.update(payload.get("stock_levels", {}))
        for movement_data in payload.get("movements", []):
            inventory.movements.append(
                StockMovement(
                    product_sku=movement_data["product_sku"],
                    warehouse_code=movement_data.get("warehouse_code", code),
                    change=movement_data["change"],
                    reason=movement_data["reason"],
                    created_at=datetime.fromisoformat(movement_data["created_at"])
                    if "created_at" in movement_data
                    else datetime.utcnow(),
                )
            )
        return inventory
