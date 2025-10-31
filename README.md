# github-optima-cloud.com

This repository contains sample 1C:Enterprise modules for a warehouse management workflow. The focus is on purchase and sales operations that update inventory and revenue registers.

## Modules

- `src/PurchaseModule.bsl` implements procedures to create and post purchase documents, updating the inventory accumulation register.
- `src/SalesModule.bsl` provides procedures for sales documents, writing both inventory and revenue register movements.

Each module exposes helper procedures (`CreateAndPostPurchase` and `CreateAndPostSale`) that orchestrate the document creation and posting lifecycle for a single line item.
