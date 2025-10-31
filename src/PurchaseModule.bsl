&AtClient
Procedure CreatePurchaseDocument(Item, Quantity, Price, Warehouse)
Document = Documents.Purchase.CreateDocument();
Document.Date = CurrentDate();
Document.Supplier = Item.Supplier;
Document.Warehouse = Warehouse;
Line = Document.Items.Add();
Line.Nomenclature = Item;
Line.Quantity = Quantity;
Line.Price = Price;
Line.Total = Quantity * Price;
Document.Write();
EndProcedure

&AtServer
Procedure PostPurchaseDocument(DocumentObject)
InventoryRecord = Registers.Accumulation.Inventory.CreateRecord();
InventoryRecord.RecordType = RecordType.Incoming;
InventoryRecord.Period = DocumentObject.Date;
InventoryRecord.Warehouse = DocumentObject.Warehouse;
InventoryRecord.Item = DocumentObject.Items[0].Nomenclature;
InventoryRecord.Quantity = DocumentObject.Items[0].Quantity;
InventoryRecord.Write();
EndProcedure

Procedure CreateAndPostPurchase(Item, Quantity, Price, Warehouse)
CreatePurchaseDocument(Item, Quantity, Price, Warehouse);
DocumentObject = Documents.Purchase.FindByNumber(Documents.Purchase.GetLastNumber()).GetObject();
PostPurchaseDocument(DocumentObject);
EndProcedure
