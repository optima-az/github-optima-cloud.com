&AtClient
Procedure CreateSalesDocument(Customer, Item, Quantity, Price, Warehouse)
Document = Documents.Sales.CreateDocument();
Document.Date = CurrentDate();
Document.Customer = Customer;
Document.Warehouse = Warehouse;
Line = Document.Items.Add();
Line.Nomenclature = Item;
Line.Quantity = Quantity;
Line.Price = Price;
Line.Total = Quantity * Price;
Document.Write();
EndProcedure

&AtServer
Procedure PostSalesDocument(DocumentObject)
InventoryRecord = Registers.Accumulation.Inventory.CreateRecord();
InventoryRecord.RecordType = RecordType.Outgoing;
InventoryRecord.Period = DocumentObject.Date;
InventoryRecord.Warehouse = DocumentObject.Warehouse;
InventoryRecord.Item = DocumentObject.Items[0].Nomenclature;
InventoryRecord.Quantity = DocumentObject.Items[0].Quantity;
InventoryRecord.Write();

RevenueRecord = Registers.Accumulation.Revenue.CreateRecord();
RevenueRecord.RecordType = RecordType.Incoming;
RevenueRecord.Period = DocumentObject.Date;
RevenueRecord.Customer = DocumentObject.Customer;
RevenueRecord.Item = DocumentObject.Items[0].Nomenclature;
RevenueRecord.Amount = DocumentObject.Items[0].Total;
RevenueRecord.Write();
EndProcedure

Procedure CreateAndPostSale(Customer, Item, Quantity, Price, Warehouse)
CreateSalesDocument(Customer, Item, Quantity, Price, Warehouse);
DocumentObject = Documents.Sales.FindByNumber(Documents.Sales.GetLastNumber()).GetObject();
PostSalesDocument(DocumentObject);
EndProcedure
