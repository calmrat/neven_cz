from pydantic import BaseModel
from typing import List, Optional

from datetime import datetime

class PaymentType(BaseModel):
    paymentType: str

class Address(BaseModel):
    company: str
    city: str
    street: str
    zip: str
    ico: Optional[str] = None
    dic: Optional[str] = None
    icDph: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    www: Optional[str] = None
    country: Optional[str] = None

class Identity(BaseModel):
    address: Address
    shipToAddress: Optional[Address] = None

class InvoiceHeader(BaseModel):
    invoiceType: str
    number: str
    numberOrder: str
    symVar: str
    symConst: Optional[str] = None
    symPar: Optional[str] = None
    date: datetime
    dateTax: datetime
    dateAccounting: Optional[datetime] = None
    dateDue: datetime
    accounting: Optional[str] = None
    classificationVAT: Optional[str] = None
    classificationKVDPH: Optional[str] = None
    paymentType: PaymentType
    text: Optional[str] = None
    myIdentity: Identity
    partnerIdentity: Identity
    dateOrder: Optional[datetime] = None
    note: Optional[str] = None
    intNote: Optional[str] = None

class HomeCurrency(BaseModel):
    unitPrice: float

class StockItem(BaseModel):
    ids: Optional[str] = None

class InvoiceItem(BaseModel):
    text: str
    note: Optional[str] = None
    code: Optional[str] = None
    quantity: float
    unit: Optional[str] = None
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
    roundingDocument: Optional[str] = None
    homeCurrency: InvoiceSummaryCurrency

class Invoice(BaseModel):
    version: str
    invoiceHeader: InvoiceHeader
    invoiceDetail: InvoiceDetail
    invoiceSummary: InvoiceSummary

class Invoices(BaseModel):
    invoices: List[Invoice]