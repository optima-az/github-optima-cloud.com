from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass(slots=True)
class Product:
    sku: str
    name: str
    description: str | None = None


@dataclass(slots=True)
class Warehouse:
    code: str
    name: str
    location: str | None = None


@dataclass(slots=True)
class StockMovement:
    product_sku: str
    warehouse_code: str
    change: int
    reason: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(slots=True)
class WarehouseInventory:
    warehouse: Warehouse
    stock_levels: dict[str, int] = field(default_factory=dict)
    movements: List[StockMovement] = field(default_factory=list)

    def adjust_stock(self, product: Product, change: int, reason: str) -> int:
        new_level = self.stock_levels.get(product.sku, 0) + change
        if new_level < 0:
            raise ValueError("Stock level cannot be negative")
        self.stock_levels[product.sku] = new_level
        movement = StockMovement(
            product_sku=product.sku,
            warehouse_code=self.warehouse.code,
            change=change,
            reason=reason,
        )
        self.movements.append(movement)
        return new_level

    def quantity(self, product: Product) -> int:
        return self.stock_levels.get(product.sku, 0)

    def movement_history(self, product: Product) -> list[StockMovement]:
        return [m for m in self.movements if m.product_sku == product.sku]
