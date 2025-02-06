from pydantic import BaseModel
from typing import List, Optional

class PaymentType(BaseModel):
    name: str

class Address(BaseModel):
    company: str
    city: str
    street: str
    zip: str
    ico: Optional[str] = None
    dic: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    www: Optional[str] = None
    country: Optional[str] = None

class Identity(BaseModel):
    address: Address

class InvoiceHeader(BaseModel):
    invoiceType: str
    number: str
    numberOrder: str
    symVar: str
    date: str
    dateTax: str
    dateDue: str
    paymentType: PaymentType
    myIdentity: Identity
    partnerIdentity: Identity

class HomeCurrency(BaseModel):
    unitPrice: float

class StockItem(BaseModel):
    ids: str

class InvoiceItem(BaseModel):
    text: str
    code: Optional[str] = None
    quantity: int
    unit: str
    payVAT: bool
    rateVAT: str
    homeCurrency: HomeCurrency
    stockItem: Optional[StockItem] = None

class InvoiceDetail(BaseModel):
    invoiceItems: Optional[List[InvoiceItem]] = None

class InvoiceSummaryCurrency(BaseModel):
    priceHigh: float
    priceHighVAT: float
    priceHighSum: float
    priceNone: float

class InvoiceSummary(BaseModel):
    roundingDocument: str
    homeCurrency: InvoiceSummaryCurrency

class Invoice(BaseModel):
    version: str
    invoiceHeader: InvoiceHeader
    invoiceDetail: InvoiceDetail
    invoiceSummary: InvoiceSummary