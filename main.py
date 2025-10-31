from __future__ import annotations

import argparse
from pathlib import Path

from warehouse import InventoryRepository, InventoryService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Warehouse management CLI")
    parser.add_argument(
        "--storage",
        type=Path,
        default=Path("warehouse_data.json"),
        help="Path to JSON storage file",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    product_parser = subparsers.add_parser("add-product", help="Register new product")
    product_parser.add_argument("sku")
    product_parser.add_argument("name")
    product_parser.add_argument("--description", default=None)

    warehouse_parser = subparsers.add_parser("add-warehouse", help="Register new warehouse")
    warehouse_parser.add_argument("code")
    warehouse_parser.add_argument("name")
    warehouse_parser.add_argument("--location", default=None)

    adjust_parser = subparsers.add_parser("adjust", help="Adjust stock level")
    adjust_parser.add_argument("warehouse_code")
    adjust_parser.add_argument("product_sku")
    adjust_parser.add_argument("change", type=int)
    adjust_parser.add_argument("reason")

    subparsers.add_parser("products", help="List products")
    subparsers.add_parser("warehouses", help="List warehouses and stock levels")

    history_parser = subparsers.add_parser("history", help="Show movement history")
    history_parser.add_argument("warehouse_code")
    history_parser.add_argument("product_sku")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    repository = InventoryRepository(args.storage)
    service = InventoryService(repository)

    if args.command == "add-product":
        service.register_product(args.sku, args.name, args.description)
        print(f"Product {args.sku} qeydiyyata alındı.")
    elif args.command == "add-warehouse":
        service.register_warehouse(args.code, args.name, args.location)
        print(f"Anbar {args.code} yaradıldı.")
    elif args.command == "adjust":
        level = service.adjust_stock(args.warehouse_code, args.product_sku, args.change, args.reason)
        print(f"Yeni ehtiyat səviyyəsi: {level}")
    elif args.command == "products":
        for product in service.products():
            print(f"{product.sku}: {product.name}")
    elif args.command == "warehouses":
        for inventory in service.warehouses():
            print(f"{inventory.warehouse.code} - {inventory.warehouse.name}")
            for sku, quantity in inventory.stock_levels.items():
                print(f"  {sku}: {quantity}")
    elif args.command == "history":
        history = service.movement_history(args.warehouse_code, args.product_sku)
        for entry in history:
            print(f"{entry['created_at']}: {entry['change']} ({entry['reason']})")


if __name__ == "__main__":
    main()
