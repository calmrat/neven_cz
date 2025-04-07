# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
This module defines data models for handling invoices in the Pohoda accounting system.

Classes:
    PaymentType: Represents the type of payment.
    Address: Represents an address with optional fields for additional details.
    Identity: Represents an identity with an address and an optional shipping address.
    InvoiceHeader: Represents the header information of an invoice.
    HomeCurrency: Represents the home currency details.
    StockItem: Represents a stock item with an optional ID.
    InvoiceItem: Represents an item in an invoice.
    InvoiceDetail: Represents the details of an invoice, including a list of invoice items.
    InvoiceSummaryCurrency: Represents the summary of an invoice in home currency.
    InvoiceSummary: Represents the summary of an invoice.
    Invoice: Represents an invoice with header, detail, and summary information.
    Invoices: Represents a list of invoices.

Usage:

    # Example of creating an invoice
    invoice = Invoice(
        version="1.0",
        invoiceHeader=InvoiceHeader(
            invoiceType="issuedInvoice",
            number="2021001",
            numberOrder="2021001",
            symVar="2021001",
            date=datetime.now(),
            dateTax=datetime.now(),
            dateDue=datetime.now(),
            paymentType=PaymentType(paymentType="transfer"),
            myIdentity=Identity(
                address=Address(
                    company="My Company",
                    city="My City",
                    street="My Street",
                    zip="12345"
                )
            ),
            partnerIdentity=Identity(
                address=Address(
                    company="Partner Company",
                    city="Partner City",
                    street="Partner Street",
                    zip="54321"
                )
            )
        ),
        invoiceDetail=InvoiceDetail(
            invoiceItems=[
                InvoiceItem(
                    text="Item 1",
                    quantity=1,
                    payVAT=True,
                    rateVAT="high",
                    homeCurrency=HomeCurrency(unitPrice=100.0)
                )
            ]
        ),
        invoiceSummary=InvoiceSummary(
            homeCurrency=InvoiceSummaryCurrency(
                priceHigh=100.0,
                priceHighVAT=21.0,
                priceHighSum=121.0,
                priceNone=0.0
            )
        )
    )
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


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


class ForeignCurrency(BaseModel):
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
    foreignCurrency: Optional[ForeignCurrency] = None
    stockItem: Optional[StockItem] = None


class InvoiceDetail(BaseModel):
    invoiceItems: Optional[List[InvoiceItem]] = None


class InvoiceSummaryHomeCurrency(BaseModel):
    priceHigh: float
    priceHighVAT: float
    priceHighSum: float
    priceNone: float


class InvoiceSummaryForeignCurrencyCurrency(BaseModel):
    ids: str


class InvoiceSummaryForeignCurrency(BaseModel):
    currency: InvoiceSummaryForeignCurrencyCurrency
    rate: float


class InvoiceSummary(BaseModel):
    roundingDocument: Optional[str] = None
    homeCurrency: InvoiceSummaryHomeCurrency
    foreignCurrency: InvoiceSummaryForeignCurrency


class Invoice(BaseModel):
    version: str
    invoiceHeader: InvoiceHeader
    invoiceDetail: InvoiceDetail
    invoiceSummary: InvoiceSummary


class Invoices(BaseModel):
    invoices: List[Invoice]


if __name__ == "__main__":
    pass
