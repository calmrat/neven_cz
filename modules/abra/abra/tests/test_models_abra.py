# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Unit tests for the abra models.

This module contains tests for the following models:
- InvoiceItem
- Invoice
- Invoices

Usage: `pytest` 
    
Filename: pytest modules/abra/abra/tests/test_models_abra.py
"""
import pytest

from datetime import datetime
from ..models.abra import Invoice, InvoiceItem, Invoices
from pydantic import ValidationError

def test_invoice_item_creation():
    item = InvoiceItem(
        ext_kod="123",
        ext_kod_k=1,
        id="item1",
        last_update=datetime.now(),
        kod="item_code",
        ean_kod="1234567890123",
        nazev="Item Name",
        cena_mj=100.0,
        mnoz_mj=2.0
    )
    assert item.ext_kod == "123"
    assert item.ext_kod_k == 1
    assert item.id == "item1"
    assert item.kod == "item_code"
    assert item.ean_kod == "1234567890123"
    assert item.nazev == "Item Name"
    assert item.cena_mj == 100.0
    assert item.mnoz_mj == 2.0

def test_invoice_creation():
    item = InvoiceItem(
        ext_kod="123",
        ext_kod_k=1,
        id="item1"
    )
    invoice = Invoice(
        ext_id="inv123",
        id="invoice1",
        polozky_faktury=[item]
    )
    assert invoice.ext_id == "inv123"
    assert invoice.id == "invoice1"
    assert len(invoice.polozky_faktury) == 1
    assert invoice.polozky_faktury[0].ext_kod == "123"

def test_invoices_creation():
    item = InvoiceItem(
        ext_kod="123",
        ext_kod_k=1,
        id="item1"
    )
    invoice = Invoice(
        ext_id="inv123",
        id="invoice1",
        polozky_faktury=[item]
    )
    invoices = Invoices(invoices=[invoice])
    assert len(invoices.invoices) == 1
    assert invoices.invoices[0].ext_id == "inv123"
    assert invoices.invoices[0].id == "invoice1"
    assert len(invoices.invoices[0].polozky_faktury) == 1
    assert invoices.invoices[0].polozky_faktury[0].ext_kod == "123"

def test_invoice_item_invalid_creation():
    with pytest.raises(ValidationError):
        InvoiceItem(
            ext_kod=123,  # Should be a string
            ext_kod_k="1",  # Should be an integer
            id=1  # Should be a string
        )

def test_invoice_invalid_creation():
    with pytest.raises(ValidationError):
        Invoice(
            ext_id=123,  # Should be a string
            id=1,  # Should be a string
            polozky_faktury="not_a_list"  # Should be a list
        )

def test_invoices_invalid_creation():
    with pytest.raises(ValidationError):
        Invoices(
            invoices="not_a_list"  # Should be a list
        )

def test_invoice_item_missing_attributes():
    with pytest.raises(ValidationError):
        InvoiceItem(
            ext_kod="123"
            # Missing other required attributes
        )

def test_invoice_missing_attributes():
    with pytest.raises(ValidationError):
        Invoice(
            ext_id="inv123"
            # Missing other required attributes
        )

def test_invoices_missing_attributes():
    with pytest.raises(ValidationError):
        Invoices(
            # Missing required attributes
        )