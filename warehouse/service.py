from __future__ import annotations

from .models import Product, Warehouse, WarehouseInventory
from .repository import InventoryRepository


class InventoryService:
    """High level operations for managing warehouse inventory."""

    def __init__(self, repository: InventoryRepository) -> None:
        self.repository = repository

    # Product operations
    def register_product(self, sku: str, name: str, description: str | None = None) -> Product:
        product = Product(sku=sku, name=name, description=description)
        self.repository.save_product(product)
        return product

    def products(self) -> list[Product]:
        return self.repository.list_products()

    # Warehouse operations
    def register_warehouse(self, code: str, name: str, location: str | None = None) -> Warehouse:
        warehouse = Warehouse(code=code, name=name, location=location)
        self.repository.save_warehouse(warehouse)
        return warehouse

    def warehouses(self) -> list[WarehouseInventory]:
        return self.repository.list_warehouses()

    def adjust_stock(
        self,
        warehouse_code: str,
        product_sku: str,
        change: int,
        reason: str,
    ) -> int:
        inventory = self.repository.load_inventory(warehouse_code)
        product = next(
            (product for product in self.products() if product.sku == product_sku), None
        )
        if product is None:
            raise ValueError("Product not found")
        new_level = inventory.adjust_stock(product, change, reason)
        self.repository.update_inventory(inventory)
        return new_level

    def stock_report(self) -> list[dict]:
        report: list[dict] = []
        for inventory in self.repository.list_warehouses():
            for sku, quantity in inventory.stock_levels.items():
                report.append(
                    {
                        "warehouse": inventory.warehouse.code,
                        "product": sku,
                        "quantity": quantity,
                    }
                )
        return report

    def movement_history(self, warehouse_code: str, product_sku: str) -> list[dict]:
        inventory = self.repository.load_inventory(warehouse_code)
        product = next(
            (product for product in self.products() if product.sku == product_sku), None
        )
        if product is None:
            raise ValueError("Product not found")
        return [
            {
                "change": movement.change,
                "reason": movement.reason,
                "created_at": movement.created_at.isoformat(),
            }
            for movement in inventory.movement_history(product)
        ]
