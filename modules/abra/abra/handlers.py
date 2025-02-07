#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Invoice Handler Module

This module provides functionality to handle invoices, including parsing XML invoices,
synchronizing them with a DuckDB database, and migrating them to a different format.

Usage:
    1. Initialize the InvoiceHandler with the path to the DuckDB database.
    2. Call `init_tables` to create the necessary tables in the database.
    3. Use `parse_invoices` to parse invoices from an XML file.
    4. Call `sync_invoices` to synchronize the parsed invoices with the database.
    5. Use `load_invoices` to load invoices from the database.
    6. Call `migrate_invoices` to migrate the loaded invoices to a different format.
    7. Use `save_migrated_invoices` to save the migrated invoices to an XML file.

Example:

    db_path = Path("/path/to/your/database.duckdb")
    xml_file = Path("/path/to/your/invoices.xml")

    handler = InvoiceHandler(db_path)
    handler.init_tables()
    handler.parse_invoices(xml_file)
    handler.sync_invoices()
    handler.load_invoices()
    handler.migrate_invoices()
    handler.save_migrated_invoices()

File: /Users/cward/Repos/neven_cz/modules/abra/abra/handlers.py
"""

import re
import dateutil
import logging

import duckdb

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from xml.etree import ElementTree as ET

from abra.models import abra as a
from abra.models import pohoda as p
from abra import config

log = logging.getLogger()

IDENTITY_NEVEN = p.Identity(
    address=p.Address(
        company="Neven 7 s.r.o.",
        city="Brno",
        street="Zavřená 27",
        zip="634 00",
        ico="29318513",
        dic="CZ12345678",
        phone="CZ29318513",
        email="info@neven.cz"
    )
)

# Define the XML namespaces we use in the Pohoda schemas
NS = {
    "dat": "http://www.stormware.cz/schema/version_2/data.xsd",
    "inv": "http://www.stormware.cz/schema/version_2/invoice.xsd",
    "typ": "http://www.stormware.cz/schema/version_2/type.xsd"
}

# Register the namespaces so they appear with the correct prefixes
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


# FIXME: integrate this into a handler
def date_to_str(date_val: datetime) -> str:
    """
    Converts a Python datetime to 'YYYY-MM-DD'. Returns empty string if None.
    """
    if not date_val:
        return ""
    return date_val.strftime("%Y-%m-%d")

def map_invoice_type(invoice_type: str) -> str:
    """
    Map a user-supplied invoice type code to Pohoda's <inv:invoiceType>.
    Example: "code:FAKTURA" => "issuedInvoice"
    Adjust the logic as needed for your environment.
    """
    if invoice_type == "code:FAKTURA":
        return "issuedInvoice"
    # Add more mappings if needed:
    # elif invoice_type == "code:FAKTURAPR":
    #     return "receivedInvoice"
    return "issuedInvoice"  # fallback default

def map_payment_type(pay_type: str) -> str:
    """
    Map a user-supplied payment code to Pohoda's <typ:paymentType> text.
    Example: "code:PREVOD" => "transfer", "code:KARTA" => "card", etc.
    """
    mapping = {
        "code:PREVOD": "transfer",
        "code:KARTA": "card",
    }
    return mapping.get(pay_type, "transfer")  # default to 'transfer'

def map_rateVAT(rate_str: str) -> str:
    """
    Converts numeric VAT rate to one of: "high", "low", "none", etc.
    Adjust logic for your local rates:
      - 21.0 => 'high'
      - 15.0 => 'low'
      - 0.0  => 'none'
      - 23.0 => 'high' (if that's how you'd handle 23% in Pohoda).
    """
    try:
        rate_val = float(rate_str)
    except:
        # If parse fails or is missing, fallback
        return "none"

    if rate_val == 0.0:
        return "none"
    # For typical Czech rates: 10 => "low", 15 => "low", 21 => "high"
    if abs(rate_val - 10.0) < 0.01 or abs(rate_val - 15.0) < 0.01:
        return "low"
    # If 21 or 23, let's call it "high"
    if abs(rate_val - 21.0) < 0.01 or abs(rate_val - 23.0) < 0.01:
        return "high"
    return "none"  # fallback if unknown

def build_data_pack(invoices_data: dict) -> str:
    """
    Convert the given JSON dict with 'invoices' list into a Pohoda dataPack XML.
    Returns the entire XML as a string with Windows-1250 encoding declaration.
    """

    # NOTE: text fields as et.CDATA() ?

    # 🔹 1) Create the root dataPack element with the required attributes
    data_pack_attrib = {
        "id": f"neven_cz-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "ico": "29318513",       # NEVEN IČO / business ID
        "application": "StwTest (neven_cz)",
        "version": "2.0",
        "note": f"Prepared by Chris Ward <chris@calmrat.com> for Neven.cz on {datetime.now()}"
    }
    root = ET.Element(ET.QName(NS["dat"], "dataPack"), data_pack_attrib)

    # 🔹 2) Loop through each invoice and create a <dat:dataPackItem> node
    for inv_data in invoices_data.get("invoices", []):
        invoice_header = inv_data.get("invoiceHeader", {})
        invoice_detail = inv_data.get("invoiceDetail", {})
        invoice_summary = inv_data.get("invoiceSummary", {})

        # a) dataPackItem
        dp_item_attrib = {
            "id": str(invoice_header.get("number", "")),
            "version": inv_data.get("version", "2.0"),
        }
        data_pack_item_el = ET.SubElement(root, ET.QName(NS["dat"], "dataPackItem"), dp_item_attrib)

        # b) <inv:invoice>
        invoice_el = ET.SubElement(data_pack_item_el, ET.QName(NS["inv"], "invoice"), {"version": "2.0"})

        # ======================
        # invoiceHeader
        # ======================
        invoice_header_el = ET.SubElement(invoice_el, ET.QName(NS["inv"], "invoiceHeader"))

        # number => <inv:number>/<typ:numberRequested>
        number_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "number"))
        num_req_el = ET.SubElement(number_el, ET.QName(NS["typ"], "numberRequested"))
        num_req_el.text = str(invoice_header.get("number", ""))

        # invoiceType => map "code:FAKTURA" => "issuedInvoice"
        invoice_type_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "invoiceType"))
        invoice_type_el.text = map_invoice_type(invoice_header.get("invoiceType", "code:FAKTURA"))

        # symVar, symConst, symPar if not None
        sym_var = invoice_header.get("symVar")
        if sym_var:
            sv_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "symVar"))
            sv_el.text = str(sym_var)

        sym_const = invoice_header.get("symConst")
        if sym_const:
            sc_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "symConst"))
            sc_el.text = str(sym_const)

        sym_par = invoice_header.get("symPar")
        if sym_par:
            sp_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "symPar"))
            sp_el.text = str(sym_par)

        # date, dateTax, dateAccounting, dateDue
        date_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "date"))
        date_el.text = date_to_str(invoice_header.get("date"))

        date_tax_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "dateTax"))
        date_tax_el.text = date_to_str(invoice_header.get("dateTax"))

        # dateAccounting is optional
        if invoice_header.get("dateAccounting"):
            da_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "dateAccounting"))
            da_el.text = date_to_str(invoice_header["dateAccounting"])

        date_due_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "dateDue"))
        date_due_el.text = date_to_str(invoice_header.get("dateDue"))

        # numberOrder
        number_order = invoice_header.get("numberOrder")
        if number_order:
            no_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "numberOrder"))
            no_el.text = str(number_order)

        # classificationVAT (if you need a single rate code, e.g. "21")
        # We’ll do a rough guess if rate=21 => "21", 0 => "none", etc.
        # Or simply skip it if invoiceSummary/homeCurrency has multiple rates
        # (In real usage, you'd parse logic from invoiceDetail).
        # For demonstration, let's pick the main item’s rate if it’s > 0.
        # You can tailor this logic as you wish.

        # Find if there's at least one item with a numeric rate
        # to guess a single classification (not fully accurate for multi-rates).
        items_list = invoice_detail.get("invoiceItems", [])
        found_rate = None
        for it in items_list:
            try:
                rr = float(it.get("rateVAT", "0.0"))
                if rr > 0:
                    found_rate = rr
                    break
            except:
                pass

        if found_rate is not None:
            classification_vat_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "classificationVAT"))
            classification_ids_el = ET.SubElement(classification_vat_el, ET.QName(NS["typ"], "ids"))
            # If found_rate=21 => "21"
            classification_ids_el.text = str(int(found_rate))  # e.g. "21"
        else:
            # Potentially no VAT
            pass

        # Payment type => <inv:paymentType>/<typ:paymentType>
        payment_type = invoice_header.get("paymentType", {}).get("paymentType", "code:PREVOD")
        payment_type_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "paymentType"))
        typ_pay_el = ET.SubElement(payment_type_el, ET.QName(NS["typ"], "paymentType"))
        typ_pay_el.text = map_payment_type(payment_type)

        # text => <inv:text> (if present)
        invoice_text = invoice_header.get("text")
        if invoice_text:
            text_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "text"))
            text_el.text = invoice_text

        # partnerIdentity => <inv:partnerIdentity>/<typ:address>
        partner_identity = invoice_header.get("partnerIdentity", {})
        if partner_identity:
            p_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "partnerIdentity"))
            addr_el = ET.SubElement(p_el, ET.QName(NS["typ"], "address"))
            address_data = partner_identity.get("address", {})
            if "company" in address_data:
                company_el = ET.SubElement(addr_el, ET.QName(NS["typ"], "company"))
                company_el.text = address_data["company"]
            if "city" in address_data:
                city_el = ET.SubElement(addr_el, ET.QName(NS["typ"], "city"))
                city_el.text = address_data["city"]
            if "street" in address_data:
                street_el = ET.SubElement(addr_el, ET.QName(NS["typ"], "street"))
                street_el.text = address_data["street"]
            if "zip" in address_data:
                zip_el = ET.SubElement(addr_el, ET.QName(NS["typ"], "zip"))
                zip_el.text = address_data["zip"]
            if "ico" in address_data and address_data["ico"]:
                ico_el = ET.SubElement(addr_el, ET.QName(NS["typ"], "ico"))
                ico_el.text = address_data["ico"]
            if "dic" in address_data and address_data["dic"]:
                dic_el = ET.SubElement(addr_el, ET.QName(NS["typ"], "dic"))
                dic_el.text = address_data["dic"]

        # dateOrder => <inv:dateOrder> if present
        if invoice_header.get("dateOrder"):
            dor_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "dateOrder"))
            dor_el.text = date_to_str(invoice_header["dateOrder"])

        # note => <inv:note>, intNote => <inv:intNote> if present
        if invoice_header.get("note"):
            note_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "note"))
            note_el.text = invoice_header["note"]
        if invoice_header.get("intNote"):
            intnote_el = ET.SubElement(invoice_header_el, ET.QName(NS["inv"], "intNote"))
            intnote_el.text = invoice_header["intNote"]

        # ======================
        # invoiceDetail
        # ======================
        invoice_detail_el = ET.SubElement(invoice_el, ET.QName(NS["inv"], "invoiceDetail"))

        for item in items_list:
            inv_item_el = ET.SubElement(invoice_detail_el, ET.QName(NS["inv"], "invoiceItem"))

            # text
            if item.get("text"):
                text_i_el = ET.SubElement(inv_item_el, ET.QName(NS["inv"], "text"))
                text_i_el.text = item["text"]

            # note (optional)
            if item.get("note"):
                note_i_el = ET.SubElement(inv_item_el, ET.QName(NS["inv"], "note"))
                note_i_el.text = item["note"]

            # quantity => <inv:quantity>
            qty_el = ET.SubElement(inv_item_el, ET.QName(NS["inv"], "quantity"))
            qty_val = item.get("quantity", 1.0)
            qty_el.text = f"{qty_val:.4f}"

            # payVAT => <inv:payVAT>true/false</inv:payVAT>
            pay_vat_val = bool(item.get("payVAT", False))
            pay_vat_el = ET.SubElement(inv_item_el, ET.QName(NS["inv"], "payVAT"))
            pay_vat_el.text = "true" if pay_vat_val else "false"

            # rateVAT => <inv:rateVAT>high/low/none</inv:rateVAT>
            rate_vat_el = ET.SubElement(inv_item_el, ET.QName(NS["inv"], "rateVAT"))
            rate_str = item.get("rateVAT", "0.0")
            rate_vat_el.text = map_rateVAT(rate_str)

            # homeCurrency => <inv:homeCurrency>/<typ:unitPrice>
            home_curr_el = ET.SubElement(inv_item_el, ET.QName(NS["inv"], "homeCurrency"))
            unit_price_el = ET.SubElement(home_curr_el, ET.QName(NS["typ"], "unitPrice"))
            unit_price = item.get("homeCurrency", {}).get("unitPrice", 0.0)
            unit_price_el.text = f"{unit_price:.2f}"

            # code => <inv:code> if item has a code
            if item.get("code"):
                code_el = ET.SubElement(inv_item_el, ET.QName(NS["inv"], "code"))
                code_el.text = item["code"]

            # unit => <inv:unit> if item has a unit
            if item.get("unit"):
                unit_el = ET.SubElement(inv_item_el, ET.QName(NS["inv"], "unit"))
                unit_el.text = item["unit"]

            # stockItem => <inv:stockItem>/<typ:ids> if desired
            stock_item = item.get("stockItem", {})
            if "ids" in stock_item and stock_item["ids"]:
                stock_el = ET.SubElement(inv_item_el, ET.QName(NS["inv"], "stockItem"))
                stock_ids_el = ET.SubElement(stock_el, ET.QName(NS["typ"], "ids"))
                stock_ids_el.text = stock_item["ids"]

        # ======================
        # invoiceSummary (optional)
        # ======================
        # If we need to show totals in Pohoda:
        #   <inv:invoiceSummary>
        #       <inv:roundingDocument>...</inv:roundingDocument>
        #       <inv:homeCurrency>...</inv:homeCurrency>
        #   </inv:invoiceSummary>
        # Add if needed.

        # Example approach:
        # invoiceSummary_el = ET.SubElement(invoice_el, ET.QName(NS["inv"], "invoiceSummary"))
        # # Possibly <inv:roundingDocument>...
        # home_currency = invoice_summary.get("homeCurrency", {})
        # if home_currency:
        #     home_currency_el = ET.SubElement(invoiceSummary_el, ET.QName(NS["inv"], "homeCurrency"))
        #     # e.g. <inv:priceHigh> <inv:priceHighVAT> <inv:priceHighSum>
        #     price_high_el = ET.SubElement(home_currency_el, ET.QName(NS["inv"], "priceHigh"))
        #     price_high_el.text = f"{home_currency.get('priceHigh', 0.0):.2f}"
        #     # etc.

    ET.indent(root)
    xml_str = ET.tostring(root, encoding="unicode", method="xml")
    
    xml_declaration = """<?xml version="1.0" encoding="Windows-1250"?>"""
    xml_full = f"{xml_declaration}\n{xml_str}".encode('cp1250', "backslashreplace").decode('cp1250')
    return xml_full


class InvoiceHandler:
    conn = None
    invoices: a.Invoices | None = None
    migrated: p.Invoices | None = None

    def __init__(self, db_path : Path):
        # DuckDB connection
        self.conn = duckdb.connect(str(db_path))

    def _xml_get_bool(self, tag: str, element) -> Optional[bool]:
        text = element.findtext(tag)
        return bool(text.lower() in ("true", "1")) if text else False
    
    def _xml_get_float(self, tag: str, element) -> Optional[float]:
        text = element.findtext(tag)
        try:
            return float(text) if text not in (None, "") else None
        except ValueError:
            return None

    def _xml_get_text(self, tag: str, element) -> Optional[str]:
        text = element.findtext(tag)
        return text.strip() if text else None
    
    def _parse_date(self, text: str) -> Optional[str]:
        dt = None
        text = str(text).strip() if text else None
        if not text:
            log.debug("Date is empty.")
            return None
        
        try:
            dt = datetime.strptime(text, "%Y-%m-%dT%z")
            #logging.debug(f" 1️⃣ ✅ datetime.strptime(\"%Y-%m-%dT%z\", '{text}')")
        except (ValueError, TypeError):
            #logging.debug(f" ❌ datetime.strptime(\"%Y-%m-%dT%z\", '{text}')")
            pass

        try:
            dt = datetime.fromisoformat(text)
            #logging.debug(f" 2️⃣✅ datetime.fromisoformat('{text}')")
        except (ValueError, TypeError):
            #logging.debug(f" ❌ datetime.fromisoformat('{text}')")
            pass

        try:
            dt = dateutil.parser.parse(text)
            #logging.debug(f" 3️⃣✅ dateutil.parser.parse('{text}')")
        except (ValueError, TypeError):
            #logging.debug(f" ❌ dateutil.parser.parse('{text}')")
            pass

        match = re.match(r"(\d{4})-?(\d{2})-?(\d{2})", text)
        if match:
            dt = datetime.strptime(f"{match.group(1)}-{match.group(2)}-{match.group(3)}", "%Y-%m-%d")
            #logging.debug(f" 💠ℹ️  Force matched date: '{dt}' from '{text}'")
        else:
            raise ValueError(f"🔥 Invalid date: {text} (type({type(text)}))")
    
        #ASSUMED_TIMEZONE = "+01:00"
        dt_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
        #dt_str = f"{dt_str}{ASSUMED_TIMEZONE}"
        
        #logging.debug(f"{text} -> {dt_str}")
        return dt_str
    
    def _xml_get_date(self, tag: str, element) -> Optional[str]:
        text = element.findtext(tag).strip()
        if not text:
            log.debug(f"Missing date in the tag {tag}.")
            return None
        return self._parse_date(text)

    def __xml_extract_invoice_items(self, element: ET.Element) -> List[a.InvoiceItem]:
        items = []
        all_elements = element.findall(".//polozkyFaktury")
        for item_elements in all_elements:
            for _element in item_elements:
                _ids = _element.findall("id")
                ext_kod, ext_kod_k, _id = "", "", ""
                
                for _ in _ids:
                    if _.text.startswith("ext:"):
                        ext_kod = _.text.split(":")[-1]
                        ext_kod, ext_kod_k = ext_kod.split("-")
                        ext_kod_k = int(ext_kod_k)
                    else:
                        _id = _.text
                #import ipdb; ipdb.set_trace()
                logging.debug(f"Invoice Item: [{ext_kod}-{ext_kod_k}] | {_id}")

                # We will have always extracted the IDs by now
                if ext_kod == "" or ext_kod_k == "" or _id == "":
                    #raise ValueError("Missing ID in the invoice item.")
                    _nazev = self._xml_get_text("nazev", _element),
                    if _nazev:
                        log.error(f"🧯🧯🧯 [SKIPPED] {_.text}: ({_nazev}) 🧯🧯🧯")
                    else:
                        log.error(f"🔥🔥🔥 [SKIPPED] {_.text} Missing ext_kod/id. 🔥🔥🔥")
                    continue
                
                items.append(a.InvoiceItem(
                    id=_id,
                    ext_kod=ext_kod,
                    ext_kod_k=ext_kod_k,
                    last_update=self._xml_get_date("lastUpdate", _element),
                    kod=self._xml_get_text("kod", _element),
                    ean_kod=self._xml_get_text("eanKod", _element),
                    nazev=self._xml_get_text("nazev", _element),
                    nazev_a=self._xml_get_text("nazevA", _element),
                    nazev_b=self._xml_get_text("nazevB", _element),
                    nazev_c=self._xml_get_text("nazevC", _element),
                    cis_rad=self._xml_get_float("cisRad", _element),
                    typ_polozky_k=self._xml_get_text("typPolozkyK", _element),
                    baleni_id=self._xml_get_float("baleniId", _element),
                    mnoz_baleni=self._xml_get_float("mnozBaleni", _element),
                    mnoz_mj=self._xml_get_float("mnozMj", _element),
                    typ_ceny_dph_k=self._xml_get_text("typCenyDphK", _element),
                    typ_szb_dph_k=self._xml_get_text("typSzbDphK", _element),
                    szb_dph=self._xml_get_float("szbDph", _element),
                    cena_mj=self._xml_get_float("cenaMj", _element),
                    sleva_pol=self._xml_get_float("slevaPol", _element),
                    upl_sleva_dokl=self._xml_get_bool("uplSlevaDokl", _element),
                    sum_zkl=self._xml_get_float("sumZkl", _element),
                    sum_dph=self._xml_get_float("sumDph", _element),
                    sum_celkem=self._xml_get_float("sumCelkem", _element),
                    sum_zkl_men=self._xml_get_float("sumZklMen", _element),
                    sum_dph_men=self._xml_get_float("sumDphMen", _element),
                    sum_celkem_men=self._xml_get_float("sumCelkemMen", _element),
                    objem=self._xml_get_float("objem", _element),
                    cen_jednotka=self._xml_get_float("cenJednotka", _element),
                    typ_vyp_ceny_k=self._xml_get_text("typVypCenyK", _element),
                    cena_mj_nakup=self._xml_get_float("cenaMjNakup", _element),
                    cena_mj_prodej=self._xml_get_float("cenaMjProdej", _element),
                    cena_mj_cenik_tuz=self._xml_get_float("cenaMjCenikTuz", _element),
                    proc_zakl=self._xml_get_float("procZakl", _element),
                    sleva_mnoz=self._xml_get_float("slevaMnoz", _element),
                    zaokr_jak_k=self._xml_get_text("zaokrJakK", _element),
                    zaokr_na_k=self._xml_get_text("zaokrNaK", _element),
                    sarze=self._xml_get_text("sarze", _element),
                    expirace=self._xml_get_text("expirace", _element),
                    dat_trvan=self._xml_get_text("datTrvan", _element),
                    dat_vyroby=self._xml_get_text("datVyroby", _element),
                    stav_uziv_k=self._xml_get_text("stavUzivK", _element),
                    mnoz_mj_plan=self._xml_get_float("mnozMjPlan", _element),
                    mnoz_mj_real=self._xml_get_float("mnozMjReal", _element),
                    auto_zaokr=self._xml_get_bool("autoZaokr", _element),
                    autogen=self._xml_get_bool("autogen", _element),
                    poznam=self._xml_get_text("poznam", _element),
                    sleva_dokl=self._xml_get_float("slevaDokl", _element),
                    dat_vyst=self._xml_get_text("datVyst", _element),
                    kop_zkl_md_ucet=self._xml_get_bool("kopZklMdUcet", _element),
                    kop_zkl_dal_ucet=self._xml_get_bool("kopZklDalUcet", _element),
                    kop_dph_md_ucet=self._xml_get_bool("kopDphMdUcet", _element),
                    kop_dph_dal_ucet=self._xml_get_bool("kopDphDalUcet", _element),
                    kop_typ_uc_op=self._xml_get_bool("kopTypUcOp", _element),
                    kop_zakazku=self._xml_get_bool("kopZakazku", _element),
                    kop_stred=self._xml_get_bool("kopStred", _element),
                    kop_cinnost=self._xml_get_bool("kopCinnost", _element),
                    kop_klice=self._xml_get_bool("kopKlice", _element),
                    kop_clen_dph=self._xml_get_bool("kopClenDph", _element),
                    kop_dat_ucto=self._xml_get_bool("kopDatUcto", _element),
                    dat_ucto=self._xml_get_text("datUcto", _element),
                    storno=self._xml_get_bool("storno", _element),
                    storno_pol=self._xml_get_bool("stornoPol", _element),
                    sklad=self._xml_get_text("sklad", _element),
                    stredisko=self._xml_get_text("stredisko", _element),
                    cinnost=self._xml_get_text("cinnost", _element),
                    mena=self._xml_get_text("mena", _element),
                    typ_uc_op=self._xml_get_text("typUcOp", _element),
                    zkl_md_ucet=self._xml_get_text("zklMdUcet", _element),
                    zkl_dal_ucet=self._xml_get_text("zklDalUcet", _element),
                    dph_md_ucet=self._xml_get_text("dphMdUcet", _element),
                    dph_dal_ucet=self._xml_get_text("dphDalUcet", _element),
                    zakazka=self._xml_get_text("zakazka", _element),
                    dodavatel=self._xml_get_text("dodavatel", _element),
                    clen_dph=self._xml_get_text("clenDph", _element),
                    dph_pren=self._xml_get_text("dphPren", _element),
                    cenik=self._xml_get_text("cenik", _element),
                    cen_hlad=self._xml_get_text("cenHlad", _element),
                    mj=self._xml_get_text("mj", _element),
                    mj_objem=self._xml_get_text("mjObjem", _element),
                    sazba_dph=self._xml_get_text("sazbaDph", _element),
                    sazba_dph_puv=self._xml_get_text("sazbaDphPuv", _element),
                    vyrobni_cisla_ok=self._xml_get_bool("vyrobniCislaOk", _element),
                    id_pol_obch_zdroj=self._xml_get_text("idPolObchZdroj", _element),
                    skup_plneni=self._xml_get_text("skupPlneni", _element),
                    stitky=self._xml_get_text("stitky", _element),
                    source=self._xml_get_text("source", _element),
                    clen_kon_vyk_dph=self._xml_get_text("clenKonVykDph", _element),
                    kop_clen_kon_vyk_dph=self._xml_get_bool("kopClenKonVykDph", _element),
                    ciselny_kod_zbozi=self._xml_get_text("ciselnyKodZbozi", _element),
                    druh_zbozi=self._xml_get_text("druhZbozi", _element),
                    dokl_fak=self._xml_get_text("doklFak", _element),
                    poplatek_parent_pol_fak=self._xml_get_text("poplatekParentPolFak", _element),
                    zdroj_pro_skl=self._xml_get_text("zdrojProSkl", _element),
                    zaloha=self._xml_get_bool("zaloha", _element),
                    prodejka=self._xml_get_bool("prodejka", _element),
                    vyrobni_cisla_prijata=self._xml_get_text("vyrobniCislaPrijata", _element),
                    vyrobni_cisla_vydana=self._xml_get_text("vyrobniCislaVydana", _element)
                ))
        return items
    
    def from_xml(self, element: ET.Element) -> "a.Invoice":
        # Handling duplicate <id> elements: first for ext_kod, second for id
        ids = element.findall("id")
        ext_id = None
        _id = None
        for i in ids:
            text = i.text.strip() if i.text else ""
            if text.startswith("ext:"):
                ext_id = text.split("ext:")[-1]
            elif text.startswith("key:"):
                _id = text.split("key:")[-1]

        polozky_faktury = self.__xml_extract_invoice_items(element)

        return a.Invoice(
            ext_id=ext_id,
            id=_id,
            kod=self._xml_get_text("kod", element),
            last_update=self._xml_get_date("lastUpdate", element),
            dat_vyst=self._xml_get_date("datVyst", element),
            duzp_puv=self._xml_get_date("duzpPuv", element),
            duzp_ucto=self._xml_get_date("duzpUcto", element),
            dat_splat=self._xml_get_date("datSplat", element),
            dat_uhra=self._xml_get_date("datUhr", element),
            dat_termin=self._xml_get_date("datTermin", element),
            dat_real=self._xml_get_date("datReal", element),
            dat_sazby_dph=self._xml_get_date("datSazbyDph", element),
            popis=self._xml_get_text("popis", element),
            poznam=self._xml_get_text("poznam", element),
            uvod_txt=self._xml_get_text("uvodTxt", element),
            zav_txt=self._xml_get_text("zavTxt", element),
            sum_osv=self._xml_get_float("sumOsv", element),
            sum_zkl_sniz=self._xml_get_float("sumZklSniz", element),
            sum_zkl_sniz2=self._xml_get_float("sumZklSniz2", element),
            sum_zkl_zakl=self._xml_get_float("sumZklZakl", element),
            sum_zkl_celkem=self._xml_get_float("sumZklCelkem", element),
            sum_dph_sniz=self._xml_get_float("sumDphSniz", element),
            sum_dph_sniz2=self._xml_get_float("sumDphSniz2", element),
            sum_dph_zakl=self._xml_get_float("sumDphZakl", element),
            sum_dph_celkem=self._xml_get_float("sumDphCelkem", element),
            sum_celk_sniz=self._xml_get_float("sumCelkSniz", element),
            sum_celk_sniz2=self._xml_get_float("sumCelkSniz2", element),
            sum_celk_zakl=self._xml_get_float("sumCelkZakl", element),
            sum_celkem=self._xml_get_float("sumCelkem", element),
            sum_osv_men=self._xml_get_float("sumOsvMen", element),
            sum_zkl_sniz_men=self._xml_get_float("sumZklSnizMen", element),
            sum_zkl_sniz2_men=self._xml_get_float("sumZklSniz2Men", element),
            sum_zkl_zakl_men=self._xml_get_float("sumZklZaklMen", element),
            sum_zkl_celkem_men=self._xml_get_float("sumZklCelkemMen", element),
            sum_dph_zakl_men=self._xml_get_float("sumDphZaklMen", element),
            sum_dph_sniz_men=self._xml_get_float("sumDphSnizMen", element),
            sum_dph_sniz2_men=self._xml_get_float("sumDphSniz2Men", element),
            sum_dph_celkem_men=self._xml_get_float("sumDphCelkemMen", element),
            sum_celk_sniz_men=self._xml_get_float("sumCelkSnizMen", element),
            sum_celk_sniz2_men=self._xml_get_float("sumCelkSniz2Men", element),
            sum_celk_zakl_men=self._xml_get_float("sumCelkZaklMen", element),
            sum_celkem_men=self._xml_get_float("sumCelkemMen", element),
            sum_naklady=self._xml_get_float("sumNaklady", element),
            sleva_dokl=self._xml_get_float("slevaDokl", element),
            kurz=self._xml_get_float("kurz", element),
            kurz_mnozstvi=self._xml_get_float("kurzMnozstvi", element),
            stav_uziv_k=self._xml_get_text("stavUzivK", element),
            naz_firmy=self._xml_get_text("nazFirmy", element),
            ulice=self._xml_get_text("ulice", element),
            mesto=self._xml_get_text("mesto", element),
            psc=self._xml_get_text("psc", element),
            ean_kod=self._xml_get_text("eanKod", element),
            ic=self._xml_get_text("ic", element),
            dic=self._xml_get_text("dic", element),
            pocet_priloh=self._xml_get_float("pocetPriloh", element),
            postovni_shodna=self._xml_get_bool("postovniShodna", element),
            fa_nazev=self._xml_get_text("faNazev", element),
            fa_nazev2=self._xml_get_text("faNazev2", element),
            fa_ulice=self._xml_get_text("faUlice", element),
            fa_mesto=self._xml_get_text("faMesto", element),
            fa_psc=self._xml_get_text("faPsc", element),
            fa_ean_kod=self._xml_get_text("faEanKod", element),
            buc=self._xml_get_text("buc", element),
            iban=self._xml_get_text("iban", element),
            bic=self._xml_get_text("bic", element),
            spec_sym=self._xml_get_text("specSym", element),
            bez_polozek=self._xml_get_bool("bezPolozek", element),
            ucetni=self._xml_get_bool("ucetni", element),
            szb_dph_sniz=self._xml_get_float("szbDphSniz", element),
            szb_dph_sniz2=self._xml_get_float("szbDphSniz2", element),
            szb_dph_zakl=self._xml_get_float("szbDphZakl", element),
            uzp_tuzemsko=self._xml_get_bool("uzpTuzemsko", element),
            zuctovano=self._xml_get_bool("zuctovano", element),
            dat_ucto=self._xml_get_date("datUcto", element),
            vyloucit_saldo=self._xml_get_bool("vyloucitSaldo", element),
            storno=self._xml_get_bool("storno", element),
            zaokr_jak_sum_k=self._xml_get_text("zaokrJakSumK", element),
            zaokr_na_sum_k=self._xml_get_text("zaokrNaSumK", element),
            zaokr_jak_dph_k=self._xml_get_text("zaokrJakDphK", element),
            zaokr_na_dph_k=self._xml_get_text("zaokrNaDphK", element),
            metoda_zaokr_dokl_k=self._xml_get_text("metodaZaokrDoklK", element),
            vytvaret_kor_pol=self._xml_get_bool("vytvaretKorPol", element),
            stitky=self._xml_get_text("stitky", element),
            typ_dokl=self._xml_get_text("typDokl", element),
            mena=self._xml_get_text("mena", element),
            kon_sym=self._xml_get_text("konSym", element),
            firma=self._xml_get_text("firma", element),
            stat=self._xml_get_text("stat", element),
            fa_stat=self._xml_get_text("faStat", element),
            region=self._xml_get_text("region", element),
            fa_region=self._xml_get_text("faRegion", element),
            mist_urc=self._xml_get_text("mistUrc", element),
            ban_spoj_dod=self._xml_get_text("banSpojDod", element),
            bankovni_ucet=self._xml_get_text("bankovniUcet", element),
            typ_dokl_ban=self._xml_get_text("typDoklBan", element),
            typ_uc_op=self._xml_get_text("typUcOp", element),
            prim_ucet=self._xml_get_text("primUcet", element),
            proti_ucet=self._xml_get_text("protiUcet", element),
            dph_zakl_ucet=self._xml_get_text("dphZaklUcet", element),
            dph_sniz_ucet=self._xml_get_text("dphSnizUcet", element),
            dph_sniz2_ucet=self._xml_get_text("dphSniz2Ucet", element),
            smer_kod=self._xml_get_text("smerKod", element),
            stat_dph=self._xml_get_text("statDph", element),
            clen_dph=self._xml_get_text("clenDph", element),
            stredisko=self._xml_get_text("stredisko", element),
            cinnost=self._xml_get_text("cinnost", element),
            zakazka=self._xml_get_text("zakazka", element),
            uzivatel=self._xml_get_text("uzivatel", element),
            zodp_osoba=self._xml_get_text("zodpOsoba", element),
            kontakt_osoba=self._xml_get_text("kontaktOsoba", element),
            kontakt_jmeno=self._xml_get_text("kontaktJmeno", element),
            kontakt_email=self._xml_get_text("kontaktEmail", element),
            kontakt_tel=self._xml_get_text("kontaktTel", element),
            rada=self._xml_get_text("rada", element),
            forma_dopravy=self._xml_get_text("formaDopravy", element),
            uuid=self._xml_get_text("uuid", element),
            source=self._xml_get_text("source", element),
            clen_kon_vyk_dph=self._xml_get_text("clenKonVykDph", element),
            dat_up1=self._xml_get_date("datUp1", element),
            dat_up2=self._xml_get_date("datUp2", element),
            dat_smir=self._xml_get_date("datSmir", element),
            dat_penale=self._xml_get_date("datPenale", element),
            podpis_prik=self._xml_get_bool("podpisPrik", element),
            prikaz_sum=self._xml_get_float("prikazSum", element),
            prikaz_sum_men=self._xml_get_float("prikazSumMen", element),
            juh_sum=self._xml_get_float("juhSum", element),
            juh_sum_men=self._xml_get_float("juhSumMen", element),
            juh_dat=self._xml_get_float("juhDat", element),
            juh_dat_men=self._xml_get_float("juhDatMen", element),
            zbyva_uhradit=self._xml_get_float("zbyvaUhradit", element),
            zbyva_uhradit_men=self._xml_get_float("zbyvaUhraditMen", element),
            forma_uhrady_cis=self._xml_get_text("formaUhradyCis", element),
            stav_uhr_k=self._xml_get_text("stavUhrK", element),
            juh_sum_pp=self._xml_get_float("juhSumPp", element),
            juh_sum_pp_men=self._xml_get_float("juhSumPpMen", element),
            sum_prepl=self._xml_get_float("sumPrepl", element),
            sum_prepl_men=self._xml_get_float("sumPreplMen", element),
            sum_zalohy=self._xml_get_float("sumZalohy", element),
            sum_zalohy_men=self._xml_get_float("sumZalohyMen", element),
            stav_odpocet_k=self._xml_get_text("stavOdpocetK", element),
            generovat_skl=self._xml_get_bool("generovatSkl", element),
            zaokrouhlit_po_odpoctu=self._xml_get_bool("zaokrouhlitPoOdpoctu", element),
            hrom_fakt=self._xml_get_bool("hromFakt", element),
            zdroj_pro_skl=self._xml_get_text("zdrojProSkl", element),
            prodejka=self._xml_get_bool("prodejka", element),
            stav_mail_k=self._xml_get_text("stavMailK", element),
            dobropisovano=self._xml_get_bool("dobropisovano", element),
            sum_celkem_bez_zaloh=self._xml_get_float("sumCelkemBezZaloh", element),
            sum_celkem_bez_zaloh_men=self._xml_get_float("sumCelkemBezZalohMen", element),
            odpoc_auto=self._xml_get_bool("odpocAuto", element),
            cis_obj=self._xml_get_text("cisObj", element),
            var_sym=self._xml_get_text("varSym", element),
            polozky_faktury=polozky_faktury
        )
    
    def init_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
            ext_id TEXT,
            id TEXT,
            last_update TEXT,
            kod TEXT,
            zamek_k TEXT,
            cis_dosle TEXT,
            var_sym TEXT,
            cis_sml TEXT,
            cis_obj TEXT,
            dat_vyst TEXT,
            duzp_puv TEXT,
            duzp_ucto TEXT,
            dat_splat TEXT,
            dat_uhr TEXT,
            dat_termin TEXT,
            dat_real TEXT,
            dat_sazby_dph TEXT,
            popis TEXT,
            poznam TEXT,
            uvod_txt TEXT,
            zav_txt TEXT,
            sum_osv FLOAT,
            sum_zkl_sniz FLOAT,
            sum_zkl_sniz2 FLOAT,
            sum_zkl_zakl FLOAT,
            sum_zkl_celkem FLOAT,
            sum_dph_sniz FLOAT,
            sum_dph_sniz2 FLOAT,
            sum_dph_zakl FLOAT,
            sum_dph_celkem FLOAT,
            sum_celk_sniz FLOAT,
            sum_celk_sniz2 FLOAT,
            sum_celk_zakl FLOAT,
            sum_celkem FLOAT,
            sum_osv_men FLOAT,
            sum_zkl_sniz_men FLOAT,
            sum_zkl_sniz2_men FLOAT,
            sum_zkl_zakl_men FLOAT,
            sum_zkl_celkem_men FLOAT,
            sum_dph_zakl_men FLOAT,
            sum_dph_sniz_men FLOAT,
            sum_dph_sniz2_men FLOAT,
            sum_dph_celkem_men FLOAT,
            sum_celk_sniz_men FLOAT,
            sum_celk_sniz2_men FLOAT,
            sum_celk_zakl_men FLOAT,
            sum_celkem_men FLOAT,
            sum_naklady FLOAT,
            sleva_dokl FLOAT,
            kurz FLOAT,
            kurz_mnozstvi FLOAT,
            stav_uziv_k TEXT,
            naz_firmy TEXT,
            ulice TEXT,
            mesto TEXT,
            psc TEXT,
            ean_kod TEXT,
            ic TEXT,
            dic TEXT,
            pocet_priloh INTEGER,
            postovni_shodna BOOLEAN,
            fa_nazev TEXT,
            fa_nazev2 TEXT,
            fa_ulice TEXT,
            fa_mesto TEXT,
            fa_psc TEXT,
            fa_ean_kod TEXT,
            buc TEXT,
            iban TEXT,
            bic TEXT,
            spec_sym TEXT,
            bez_polozek BOOLEAN,
            ucetni BOOLEAN,
            szb_dph_sniz FLOAT,
            szb_dph_sniz2 FLOAT,
            szb_dph_zakl FLOAT,
            uzp_tuzemsko BOOLEAN,
            zuctovano BOOLEAN,
            dat_ucto TEXT,
            vyloucit_saldo BOOLEAN,
            storno BOOLEAN,
            zaokr_jak_sum_k TEXT,
            zaokr_na_sum_k TEXT,
            zaokr_jak_dph_k TEXT,
            zaokr_na_dph_k TEXT,
            metoda_zaokr_dokl_k TEXT,
            vytvaret_kor_pol BOOLEAN,
            stitky TEXT,
            typ_dokl TEXT,
            mena TEXT,
            kon_sym TEXT,
            firma TEXT,
            stat TEXT,
            fa_stat TEXT,
            region TEXT,
            fa_region TEXT,
            mist_urc TEXT,
            ban_spoj_dod TEXT,
            bankovni_ucet TEXT,
            typ_dokl_ban TEXT,
            typ_uc_op TEXT,
            prim_ucet TEXT,
            proti_ucet TEXT,
            dph_zakl_ucet TEXT,
            dph_sniz_ucet TEXT,
            dph_sniz2_ucet TEXT,
            smer_kod TEXT,
            stat_dph TEXT,
            clen_dph TEXT,
            stredisko TEXT,
            cinnost TEXT,
            zakazka TEXT,
            uzivatel TEXT,
            zodp_osoba TEXT,
            kontakt_osoba TEXT,
            kontakt_jmeno TEXT,
            kontakt_email TEXT,
            kontakt_tel TEXT,
            rada TEXT,
            forma_dopravy TEXT,
            uuid TEXT,
            source TEXT,
            clen_kon_vyk_dph TEXT,
            dat_up1 TEXT,
            dat_up2 TEXT,
            dat_smir TEXT,
            dat_penale TEXT,
            podpis_prik BOOLEAN,
            prikaz_sum FLOAT,
            prikaz_sum_men FLOAT,
            juh_sum FLOAT,
            juh_sum_men FLOAT,
            juh_dat FLOAT,
            juh_dat_men FLOAT,
            zbyva_uhradit FLOAT,
            zbyva_uhradit_men FLOAT,
            forma_uhrady_cis TEXT,
            stav_uhr_k TEXT,
            juh_sum_pp FLOAT,
            juh_sum_pp_men FLOAT,
            sum_prepl FLOAT,
            sum_prepl_men FLOAT,
            sum_zalohy FLOAT,
            sum_zalohy_men FLOAT,
            stav_odpocet_k TEXT,
            generovat_skl BOOLEAN,
            zaokrouhlit_po_odpoctu BOOLEAN,
            hrom_fakt BOOLEAN,
            zdroj_pro_skl TEXT,
            prodejka BOOLEAN,
            stav_mail_k TEXT,
            dobropisovano BOOLEAN,
            sum_celkem_bez_zaloh FLOAT,
            sum_celkem_bez_zaloh_men FLOAT,
            odpoc_auto BOOLEAN,
            UNIQUE(ext_id, id)
            )
        """)
        
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_invoices_ext_id ON invoices (ext_id)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_invoices_id ON invoices (id)")

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS invoice_items (
            ext_kod TEXT,
            ext_kod_k FLOAT,
            id TEXT UNIQUE,
            last_update TEXT,
            kod TEXT,
            ean_kod TEXT,
            nazev TEXT,
            nazev_a TEXT,
            nazev_b TEXT,
            nazev_c TEXT,
            cis_rad INTEGER,
            typ_polozky_k TEXT,
            baleni_id INTEGER,
            mnoz_baleni FLOAT,
            mnoz_mj FLOAT,
            typ_ceny_dph_k TEXT,
            typ_szb_dph_k TEXT,
            szb_dph FLOAT,
            cena_mj FLOAT,
            sleva_pol FLOAT,
            upl_sleva_dokl BOOLEAN,
            sum_zkl FLOAT,
            sum_dph FLOAT,
            sum_celkem FLOAT,
            sum_zkl_men FLOAT,
            sum_dph_men FLOAT,
            sum_celkem_men FLOAT,
            objem FLOAT,
            cen_jednotka FLOAT,
            typ_vyp_ceny_k TEXT,
            cena_mj_nakup FLOAT,
            cena_mj_prodej FLOAT,
            cena_mj_cenik_tuz FLOAT,
            proc_zakl FLOAT,
            sleva_mnoz FLOAT,
            zaokr_jak_k TEXT,
            zaokr_na_k TEXT,
            sarze TEXT,
            expirace TEXT,
            dat_trvan TEXT,
            dat_vyroby TEXT,
            stav_uziv_k TEXT,
            mnoz_mj_plan FLOAT,
            mnoz_mj_real FLOAT,
            auto_zaokr BOOLEAN,
            autogen BOOLEAN,
            poznam TEXT,
            sleva_dokl FLOAT,
            dat_vyst TEXT,
            kop_zkl_md_ucet BOOLEAN,
            kop_zkl_dal_ucet BOOLEAN,
            kop_dph_md_ucet BOOLEAN,
            kop_dph_dal_ucet BOOLEAN,
            kop_typ_uc_op BOOLEAN,
            kop_zakazku BOOLEAN,
            kop_stred BOOLEAN,
            kop_cinnost BOOLEAN,
            kop_klice BOOLEAN,
            kop_clen_dph BOOLEAN,
            kop_dat_ucto BOOLEAN,
            dat_ucto TEXT,
            storno BOOLEAN,
            storno_pol BOOLEAN,
            sklad TEXT,
            stredisko TEXT,
            cinnost TEXT,
            mena TEXT,
            typ_uc_op TEXT,
            zkl_md_ucet TEXT,
            zkl_dal_ucet TEXT,
            dph_md_ucet TEXT,
            dph_dal_ucet TEXT,
            zakazka TEXT,
            dodavatel TEXT,
            clen_dph TEXT,
            dph_pren TEXT,
            cenik TEXT,
            cen_hlad TEXT,
            mj TEXT,
            mj_objem TEXT,
            sazba_dph TEXT,
            sazba_dph_puv TEXT,
            vyrobni_cisla_ok BOOLEAN,
            id_pol_obch_zdroj TEXT,
            skup_plneni TEXT,
            stitky TEXT,
            source TEXT,
            clen_kon_vyk_dph TEXT,
            kop_clen_kon_vyk_dph BOOLEAN,
            ciselny_kod_zbozi TEXT,
            druh_zbozi TEXT,
            dokl_fak TEXT,
            poplatek_parent_pol_fak TEXT,
            zdroj_pro_skl TEXT,
            zaloha BOOLEAN,
            prodejka BOOLEAN,
            vyrobni_cisla_prijata TEXT,
            vyrobni_cisla_vydana TEXT,
            UNIQUE(ext_kod, id)
            )
        """)

        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_invoice_items_ext_kod ON invoice_items (ext_kod)")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_invoice_items_id ON invoice_items (id)")
            
    # Function to parse XML invoices
    def parse_invoices(self, xml_file: Path) -> List[a.Invoice]:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        invoices = []
        
        # Now matching the faktura-vydana elements as invoice sources
        for invoice in root.findall(".//faktura-vydana"):
            invoices.append(self.from_xml(invoice))

        self.invoices = a.Invoices(invoices=invoices)
        return self

    def sync_invoices(self):
        if not self.invoices:
            log.info("[bold red]No invoices to sync.[/bold red]")
            return

        log.info(f"Syncing [{len(self.invoices.model_dump()['invoices'])}] invoices to database.")
        for invoice in self.invoices.invoices:
            existing_invoice = self.conn.execute("SELECT 1 FROM invoices WHERE ext_id = ?", (invoice.ext_id,)).fetchone()
            if existing_invoice:
                log.info(f"🟣 SKIPPED: Invoice with ext_id {invoice.ext_id} already exists.")
                continue
            else:
                log.debug(f"🟢 INSERTING: Invoice with ext_id {invoice.ext_id}.")

            self.conn.execute("""
                INSERT INTO invoices (ext_id, id) 
                VALUES (?, ?)
                ON CONFLICT (ext_id, id) DO NOTHING
            """, (invoice.ext_id, invoice.id))

            #print (invoice.kod, invoice.cis_obj, invoice.var_sym, invoice.dat_splat)

            self.conn.execute("""
                UPDATE invoices
                SET
                    last_update = ?, kod = ?, zamek_k = ?, cis_dosle = ?, var_sym = ?, 
                    cis_sml = ?, cis_obj = ?, dat_vyst = ?, duzp_puv = ?, duzp_ucto = ?, 
                    dat_splat = ?, dat_uhr = ?, dat_termin = ?, dat_real = ?, dat_sazby_dph = ?, 
                    popis = ?, poznam = ?, uvod_txt = ?, zav_txt = ?, sum_osv = ?, 
                    sum_zkl_sniz = ?, sum_zkl_sniz2 = ?, sum_zkl_zakl = ?, sum_zkl_celkem = ?, 
                    sum_dph_sniz = ?, sum_dph_sniz2 = ?, sum_dph_zakl = ?, sum_dph_celkem = ?, 
                    sum_celk_sniz = ?, sum_celk_sniz2 = ?, sum_celk_zakl = ?, sum_celkem = ?, 
                    sum_osv_men = ?, sum_zkl_sniz_men = ?, sum_zkl_sniz2_men = ?, sum_zkl_zakl_men = ?, 
                    sum_zkl_celkem_men = ?, sum_dph_zakl_men = ?, sum_dph_sniz_men = ?, sum_dph_sniz2_men = ?, 
                    sum_dph_celkem_men = ?, sum_celk_sniz_men = ?, sum_celk_sniz2_men = ?, sum_celk_zakl_men = ?, 
                    sum_celkem_men = ?, sum_naklady = ?, sleva_dokl = ?, kurz = ?
                WHERE ext_id = ? AND id = ?
            """, (
                invoice.last_update, invoice.kod, invoice.zamek_k, invoice.cis_dosle, invoice.var_sym,
                invoice.cis_sml, invoice.cis_obj, invoice.dat_vyst, invoice.duzp_puv, invoice.duzp_ucto,
                invoice.dat_splat, invoice.dat_uhr, invoice.dat_termin, invoice.dat_real, invoice.dat_sazby_dph,
                invoice.popis, invoice.poznam, invoice.uvod_txt, invoice.zav_txt, invoice.sum_osv,
                invoice.sum_zkl_sniz, invoice.sum_zkl_sniz2, invoice.sum_zkl_zakl, invoice.sum_zkl_celkem,
                invoice.sum_dph_sniz, invoice.sum_dph_sniz2, invoice.sum_dph_zakl, invoice.sum_dph_celkem,
                invoice.sum_celk_sniz, invoice.sum_celk_sniz2, invoice.sum_celk_zakl, invoice.sum_celkem,
                invoice.sum_osv_men, invoice.sum_zkl_sniz_men, invoice.sum_zkl_sniz2_men, invoice.sum_zkl_zakl_men,
                invoice.sum_zkl_celkem_men, invoice.sum_dph_zakl_men, invoice.sum_dph_sniz_men, invoice.sum_dph_sniz2_men,
                invoice.sum_dph_celkem_men, invoice.sum_celk_sniz_men, invoice.sum_celk_sniz2_men, invoice.sum_celk_zakl_men,
                invoice.sum_celkem_men, invoice.sum_naklady, invoice.sleva_dokl, invoice.kurz,
                invoice.ext_id, invoice.id
            ))

            self.conn.execute("""
                UPDATE invoices
                SET
                    kurz_mnozstvi = ?,
                    stav_uziv_k = ?,
                    naz_firmy = ?,
                    ulice = ?,
                    mesto = ?,
                    psc = ?,
                    ean_kod = ?,
                    ic = ?,
                    dic = ?,
                    pocet_priloh = ?,
                    postovni_shodna = ?,
                    fa_nazev = ?,
                    fa_nazev2 = ?,
                    fa_ulice = ?,
                    fa_mesto = ?,
                    fa_psc = ?,
                    fa_ean_kod = ?,
                    buc = ?,
                    iban = ?,
                    bic = ?,
                    spec_sym = ?,
                    bez_polozek = ?,
                    ucetni = ?,
                    szb_dph_sniz = ?,
                    szb_dph_sniz2 = ?,
                    szb_dph_zakl = ?,
                    uzp_tuzemsko = ?,
                    zuctovano = ?,
                    dat_ucto = ?,
                    vyloucit_saldo = ?,
                    storno = ?,
                    zaokr_jak_sum_k = ?,
                    zaokr_na_sum_k = ?,
                    zaokr_jak_dph_k = ?,
                    zaokr_na_dph_k = ?,
                    metoda_zaokr_dokl_k = ?,
                    vytvaret_kor_pol = ?,
                    stitky = ?,
                    typ_dokl = ?,
                    mena = ?,
                    kon_sym = ?,
                    firma = ?,
                    stat = ?,
                    fa_stat = ?,
                    region = ?,
                    fa_region = ?,
                    mist_urc = ?,
                    ban_spoj_dod = ?,
                    bankovni_ucet = ?,
                    typ_dokl_ban = ?
                WHERE ext_id = ? AND id = ?
            """, (
                invoice.kurz_mnozstvi, invoice.stav_uziv_k, invoice.naz_firmy, invoice.ulice,
                invoice.mesto, invoice.psc, invoice.ean_kod, invoice.ic, invoice.dic,
                invoice.pocet_priloh, invoice.postovni_shodna, invoice.fa_nazev,
                invoice.fa_nazev2, invoice.fa_ulice, invoice.fa_mesto, invoice.fa_psc,
                invoice.fa_ean_kod, invoice.buc, invoice.iban, invoice.bic, invoice.spec_sym,
                invoice.bez_polozek, invoice.ucetni, invoice.szb_dph_sniz, invoice.szb_dph_sniz2,
                invoice.szb_dph_zakl, invoice.uzp_tuzemsko, invoice.zuctovano, invoice.dat_ucto,
                invoice.vyloucit_saldo, invoice.storno, invoice.zaokr_jak_sum_k, invoice.zaokr_na_sum_k,
                invoice.zaokr_jak_dph_k, invoice.zaokr_na_dph_k, invoice.metoda_zaokr_dokl_k,
                invoice.vytvaret_kor_pol, invoice.stitky, invoice.typ_dokl, invoice.mena,
                invoice.kon_sym, invoice.firma, invoice.stat, invoice.fa_stat, invoice.region,
                invoice.fa_region, invoice.mist_urc, invoice.ban_spoj_dod, invoice.bankovni_ucet,
                invoice.typ_dokl_ban,
                invoice.ext_id, invoice.id
            ))

            self.conn.execute("""
                UPDATE invoices
                SET
                    typ_uc_op = ?,
                    prim_ucet = ?,
                    proti_ucet = ?,
                    dph_zakl_ucet = ?,
                    dph_sniz_ucet = ?,
                    dph_sniz2_ucet = ?,
                    smer_kod = ?,
                    stat_dph = ?,
                    clen_dph = ?,
                    stredisko = ?,
                    cinnost = ?,
                    zakazka = ?,
                    uzivatel = ?,
                    zodp_osoba = ?,
                    kontakt_osoba = ?,
                    kontakt_jmeno = ?,
                    kontakt_email = ?,
                    kontakt_tel = ?,
                    rada = ?,
                    forma_dopravy = ?,
                    uuid = ?,
                    source = ?,
                    clen_kon_vyk_dph = ?,
                    dat_up1 = ?,
                    dat_up2 = ?,
                    dat_smir = ?,
                    dat_penale = ?,
                    podpis_prik = ?,
                    prikaz_sum = ?,
                    prikaz_sum_men = ?,
                    juh_sum = ?,
                    juh_sum_men = ?,
                    juh_dat = ?,
                    juh_dat_men = ?,
                    zbyva_uhradit = ?,
                    zbyva_uhradit_men = ?,
                    forma_uhrady_cis = ?,
                    stav_uhr_k = ?,
                    juh_sum_pp = ?,
                    juh_sum_pp_men = ?,
                    sum_prepl = ?,
                    sum_prepl_men = ?,
                    sum_zalohy = ?,
                    sum_zalohy_men = ?,
                    stav_odpocet_k = ?,
                    generovat_skl = ?,
                    zaokrouhlit_po_odpoctu = ?,
                    hrom_fakt = ?,
                    zdroj_pro_skl = ?,
                    prodejka = ?,
                    stav_mail_k = ?,
                    dobropisovano = ?,
                    sum_celkem_bez_zaloh = ?,
                    sum_celkem_bez_zaloh_men = ?,
                    odpoc_auto = ?
                WHERE ext_id = ? AND id = ?
            """, (
                invoice.typ_uc_op, invoice.prim_ucet, invoice.proti_ucet, invoice.dph_zakl_ucet,
                invoice.dph_sniz_ucet, invoice.dph_sniz2_ucet, invoice.smer_kod, invoice.stat_dph,
                invoice.clen_dph, invoice.stredisko, invoice.cinnost, invoice.zakazka, invoice.uzivatel,
                invoice.zodp_osoba, invoice.kontakt_osoba, invoice.kontakt_jmeno, invoice.kontakt_email,
                invoice.kontakt_tel, invoice.rada, invoice.forma_dopravy, invoice.uuid, invoice.source,
                invoice.clen_kon_vyk_dph, invoice.dat_up1, invoice.dat_up2, invoice.dat_smir,
                invoice.dat_penale, invoice.podpis_prik, invoice.prikaz_sum, invoice.prikaz_sum_men,
                invoice.juh_sum, invoice.juh_sum_men, invoice.juh_dat, invoice.juh_dat_men,
                invoice.zbyva_uhradit, invoice.zbyva_uhradit_men, invoice.forma_uhrady_cis,
                invoice.stav_uhr_k, invoice.juh_sum_pp, invoice.juh_sum_pp_men, invoice.sum_prepl,
                invoice.sum_prepl_men, invoice.sum_zalohy, invoice.sum_zalohy_men, invoice.stav_odpocet_k,
                invoice.generovat_skl, invoice.zaokrouhlit_po_odpoctu, invoice.hrom_fakt,
                invoice.zdroj_pro_skl, invoice.prodejka, invoice.stav_mail_k, invoice.dobropisovano,
                invoice.sum_celkem_bez_zaloh, invoice.sum_celkem_bez_zaloh_men, invoice.odpoc_auto,
                invoice.ext_id, invoice.id
            ))

            logging.debug (f" 📣 There are {len(invoice.polozky_faktury)} items in the invoice.")
            for item in invoice.polozky_faktury:
                existing_item = self.conn.execute("SELECT 1 FROM invoice_items WHERE ext_kod = ? AND ext_kod_k = ?", (item.ext_kod, item.ext_kod_k)).fetchone()
                #print (item)
                #print (existing_item)
                if existing_item:
                    log.debug(f"🟠 SKIPPED: Invoice item with ext_kod {item.ext_kod} and ext_kod_k {item.ext_kod_k} already exists.")
                    continue
                else:
                    log.debug(f"🟢🟢 INSERTING: Invoice item with ext_kod {item.ext_kod} and ext_kod_k {item.ext_kod_k}.")

                # NOTE: ext_id -> ext_kod
                self.conn.execute("""
                    INSERT INTO invoice_items (
                        ext_kod, ext_kod_k, id
                    ) VALUES (
                        ?, ?, ?
                    )
                    ON CONFLICT (id) DO NOTHING
                """, (
                    item.ext_kod, item.ext_kod_k, item.id
                ))

                self.conn.execute("""
                    UPDATE invoice_items
                    SET
                        last_update = ?, kod = ?, ean_kod = ?, nazev = ?, nazev_a = ?, nazev_b = ?, nazev_c = ?,
                        cis_rad = ?, typ_polozky_k = ?, baleni_id = ?, mnoz_baleni = ?, mnoz_mj = ?, typ_ceny_dph_k = ?,
                        typ_szb_dph_k = ?, szb_dph = ?, cena_mj = ?, sleva_pol = ?, upl_sleva_dokl = ?, sum_zkl = ?,
                        sum_dph = ?, sum_celkem = ?, sum_zkl_men = ?, sum_dph_men = ?, sum_celkem_men = ?, objem = ?,
                        cen_jednotka = ?, typ_vyp_ceny_k = ?, cena_mj_nakup = ?, cena_mj_prodej = ?, cena_mj_cenik_tuz = ?,
                        proc_zakl = ?, sleva_mnoz = ?, zaokr_jak_k = ?, zaokr_na_k = ?, sarze = ?, expirace = ?, dat_trvan = ?,
                        dat_vyroby = ?, stav_uziv_k = ?, mnoz_mj_plan = ?, mnoz_mj_real = ?, auto_zaokr = ?, autogen = ?, poznam = ?,
                        sleva_dokl = ?, dat_vyst = ?, kop_zkl_md_ucet = ?, kop_zkl_dal_ucet = ?, kop_dph_md_ucet = ?, kop_dph_dal_ucet = ?,
                        kop_typ_uc_op = ?, kop_zakazku = ?, kop_stred = ?, kop_cinnost = ?, kop_klice = ?, kop_clen_dph = ?, kop_dat_ucto = ?,
                        dat_ucto = ?, storno = ?, storno_pol = ?, sklad = ?, stredisko = ?, cinnost = ?, mena = ?, typ_uc_op = ?, zkl_md_ucet = ?,
                        zkl_dal_ucet = ?, dph_md_ucet = ?, dph_dal_ucet = ?, zakazka = ?, dodavatel = ?, clen_dph = ?, dph_pren = ?, cenik = ?,
                        cen_hlad = ?, mj = ?, mj_objem = ?, sazba_dph = ?, sazba_dph_puv = ?, vyrobni_cisla_ok = ?, id_pol_obch_zdroj = ?, skup_plneni = ?,
                        stitky = ?, source = ?, clen_kon_vyk_dph = ?, kop_clen_kon_vyk_dph = ?, ciselny_kod_zbozi = ?, druh_zbozi = ?, dokl_fak = ?,
                        poplatek_parent_pol_fak = ?, zdroj_pro_skl = ?, zaloha = ?, prodejka = ?, vyrobni_cisla_prijata = ?, vyrobni_cisla_vydana = ?
                    WHERE ext_kod = ? AND ext_kod_k = ? AND id = ?
                """, (
                    item.last_update, item.kod, item.ean_kod, item.nazev, item.nazev_a, item.nazev_b, item.nazev_c,
                    item.cis_rad, item.typ_polozky_k, item.baleni_id, item.mnoz_baleni, item.mnoz_mj, item.typ_ceny_dph_k,
                    item.typ_szb_dph_k, item.szb_dph, item.cena_mj, item.sleva_pol, item.upl_sleva_dokl, item.sum_zkl,
                    item.sum_dph, item.sum_celkem, item.sum_zkl_men, item.sum_dph_men, item.sum_celkem_men, item.objem,
                    item.cen_jednotka, item.typ_vyp_ceny_k, item.cena_mj_nakup, item.cena_mj_prodej, item.cena_mj_cenik_tuz,
                    item.proc_zakl, item.sleva_mnoz, item.zaokr_jak_k, item.zaokr_na_k, item.sarze, item.expirace, item.dat_trvan,
                    item.dat_vyroby, item.stav_uziv_k, item.mnoz_mj_plan, item.mnoz_mj_real, item.auto_zaokr, item.autogen, item.poznam,
                    item.sleva_dokl, item.dat_vyst, item.kop_zkl_md_ucet, item.kop_zkl_dal_ucet, item.kop_dph_md_ucet, item.kop_dph_dal_ucet,
                    item.kop_typ_uc_op, item.kop_zakazku, item.kop_stred, item.kop_cinnost, item.kop_klice, item.kop_clen_dph, item.kop_dat_ucto,
                    item.dat_ucto, item.storno, item.storno_pol, item.sklad, item.stredisko, item.cinnost, item.mena, item.typ_uc_op, item.zkl_md_ucet,
                    item.zkl_dal_ucet, item.dph_md_ucet, item.dph_dal_ucet, item.zakazka, item.dodavatel, item.clen_dph, item.dph_pren, item.cenik,
                    item.cen_hlad, item.mj, item.mj_objem, item.sazba_dph, item.sazba_dph_puv, item.vyrobni_cisla_ok, item.id_pol_obch_zdroj, item.skup_plneni,
                    item.stitky, item.source, item.clen_kon_vyk_dph, item.kop_clen_kon_vyk_dph, item.ciselny_kod_zbozi, item.druh_zbozi, item.dokl_fak,
                    item.poplatek_parent_pol_fak, item.zdroj_pro_skl, item.zaloha, item.prodejka, item.vyrobni_cisla_prijata, item.vyrobni_cisla_vydana,
                    item.ext_kod, item.ext_kod_k, item.id
                ))

        log.info("Invoices synced successfully.")
    
    def load_invoices(self) -> List[a.Invoice]:
        log.debug("Loading invoices from database.")
        rows = self.conn.execute("SELECT * FROM invoices").fetchall()
        invoices = []

        for row in rows:
            results = self.conn.execute("SELECT * FROM invoice_items WHERE ext_kod = ?", (row[3],)).fetchall()
            
            polozky_faktury = [a.InvoiceItem(
                id=item[2],
                ext_kod=item[0],
                ext_kod_k=item[1],
                last_update=self._parse_date(item[3]),
                kod=item[4],
                ean_kod=item[5],
                nazev=item[6],
                nazev_a=item[7],
                nazev_b=item[8],
                nazev_c=item[9],
                cis_rad=item[10],
                typ_polozky_k=item[11],
                baleni_id=item[12],
                mnoz_baleni=item[13],
                mnoz_mj=item[14],
                typ_ceny_dph_k=item[15],
                typ_szb_dph_k=item[16],
                szb_dph=item[17],
                cena_mj=item[18],
                sleva_pol=item[19],
                upl_sleva_dokl=item[20],
                sum_zkl=item[21],
                sum_dph=item[22],
                sum_celkem=item[23],
                sum_zkl_men=item[24],
                sum_dph_men=item[25],
                sum_celkem_men=item[26],
                objem=item[27],
                cen_jednotka=item[28],
                typ_vyp_ceny_k=item[29],
                cena_mj_nakup=item[30],
                cena_mj_prodej=item[31],
                cena_mj_cenik_tuz=item[32],
                proc_zakl=item[33],
                sleva_mnoz=item[34],
                zaokr_jak_k=item[35],
                zaokr_na_k=item[36],
                sarze=item[37],
                expirace=item[38],
                dat_trvan=item[39],
                dat_vyroby=item[40],
                stav_uziv_k=item[41],
                mnoz_mj_plan=item[42],
                mnoz_mj_real=item[43],
                auto_zaokr=item[44],
                autogen=item[45],
                poznam=item[46],
                sleva_dokl=item[47],
                dat_vyst=item[48],
                kop_zkl_md_ucet=item[49],
                kop_zkl_dal_ucet=item[50],
                kop_dph_md_ucet=item[51],
                kop_dph_dal_ucet=item[52],
                kop_typ_uc_op=item[53],
                kop_zakazku=item[54],
                kop_stred=item[55],
                kop_cinnost=item[56],
                kop_klice=item[57],
                kop_clen_dph=item[58],
                kop_dat_ucto=item[59],
                dat_ucto=item[60],
                storno=item[61],
                storno_pol=item[62],
                sklad=item[63],
                stredisko=item[64],
                cinnost=item[65],
                mena=item[66],
                typ_uc_op=item[67],
                zkl_md_ucet=item[68],
                zkl_dal_ucet=item[69],
                dph_md_ucet=item[70],
                dph_dal_ucet=item[71],
                zakazka=item[72],
                dodavatel=item[73],
                clen_dph=item[74],
                dph_pren=item[75],
                cenik=item[76],
                cen_hlad=item[77],
                mj=item[78],
                mj_objem=item[79],
                sazba_dph=item[80],
                sazba_dph_puv=item[81],
                vyrobni_cisla_ok=item[82],
                id_pol_obch_zdroj=item[83],
                skup_plneni=item[84],
                stitky=item[85],
                source=item[86],
                clen_kon_vyk_dph=item[87],
                kop_clen_kon_vyk_dph=item[88],
                ciselny_kod_zbozi=item[89],
                druh_zbozi=item[90],
                dokl_fak=item[91],
                poplatek_parent_pol_fak=item[92],
                zdroj_pro_skl=item[93],
                zaloha=item[94],
                prodejka=item[95],
                vyrobni_cisla_prijata=item[96],
                vyrobni_cisla_vydana=item[97]
            ) for item in results]

            invoices.append(a.Invoice(
                ext_id=row[0],
                id=row[1],
                last_update=self._parse_date(row[2]),
                kod=row[3],
                zamek_k=row[4],
                cis_dosle=row[5],
                var_sym=row[6],
                cis_sml=row[7],
                cis_obj=row[8],
                dat_vyst=self._parse_date(row[9]),
                duzp_puv=self._parse_date(row[10]),
                duzp_ucto=self._parse_date(row[11]),
                dat_splat=self._parse_date(row[12]),
                dat_uhra=self._parse_date(row[13]),
                dat_termin=self._parse_date(row[14]),
                dat_real=self._parse_date(row[15]),
                dat_sazby_dph=self._parse_date(row[16]),
                popis=row[17],
                poznam=row[18],
                uvod_txt=row[19],
                zav_txt=row[20],
                sum_osv=row[21],
                sum_zkl_sniz=row[22],
                sum_zkl_sniz2=row[23],
                sum_zkl_zakl=row[24],
                sum_zkl_celkem=row[25],
                sum_dph_sniz=row[26],
                sum_dph_sniz2=row[27],
                sum_dph_zakl=row[28],
                sum_dph_celkem=row[29],
                sum_celk_sniz=row[30],
                sum_celk_sniz2=row[31],
                sum_celk_zakl=row[32],
                sum_celkem=row[33],
                sum_osv_men=row[34],
                sum_zkl_sniz_men=row[35],
                sum_zkl_sniz2_men=row[36],
                sum_zkl_zakl_men=row[37],
                sum_zkl_celkem_men=row[38],
                sum_dph_zakl_men=row[39],
                sum_dph_sniz_men=row[40],
                sum_dph_sniz2_men=row[41],
                sum_dph_celkem_men=row[42],
                sum_celk_sniz_men=row[43],
                sum_celk_sniz2_men=row[44],
                sum_celk_zakl_men=row[45],
                sum_celkem_men=row[46],
                sum_naklady=row[47],
                sleva_dokl=row[48],
                kurz=row[49],
                kurz_mnozstvi=row[50],
                stav_uziv_k=row[51],
                naz_firmy=row[52],
                ulice=row[53],
                mesto=row[54],
                psc=row[55],
                ean_kod=row[56],
                ic=row[57],
                dic=row[58],
                pocet_priloh=row[59],
                postovni_shodna=row[60],
                fa_nazev=row[61],
                fa_nazev2=row[62],
                fa_ulice=row[63],
                fa_mesto=row[64],
                fa_psc=row[65],
                fa_ean_kod=row[66],
                buc=row[67],
                iban=row[68],
                bic=row[69],
                spec_sym=row[70],
                bez_polozek=row[71],
                ucetni=row[72],
                szb_dph_sniz=row[73],
                szb_dph_sniz2=row[74],
                szb_dph_zakl=row[75],
                uzp_tuzemsko=row[76],
                zuctovano=row[77],
                dat_ucto=self._parse_date(row[78]),
                vyloucit_saldo=row[79],
                storno=row[80],
                zaokr_jak_sum_k=row[81],
                zaokr_na_sum_k=row[82],
                zaokr_jak_dph_k=row[83],
                zaokr_na_dph_k=row[84],
                metoda_zaokr_dokl_k=row[85],
                vytvaret_kor_pol=row[86],
                stitky=row[87],
                typ_dokl=row[88],
                mena=row[89],
                kon_sym=row[90],
                firma=row[91],
                stat=row[92],
                fa_stat=row[93],
                region=row[94],
                fa_region=row[95],
                mist_urc=row[96],
                ban_spoj_dod=row[97],
                bankovni_ucet=row[98],
                typ_dokl_ban=row[99],
                typ_uc_op=row[100],
                prim_ucet=row[101],
                proti_ucet=row[102],
                dph_zakl_ucet=row[103],
                dph_sniz_ucet=row[104],
                dph_sniz2_ucet=row[105],
                smer_kod=row[106],
                stat_dph=row[107],
                clen_dph=row[108],
                stredisko=row[109],
                cinnost=row[110],
                zakazka=row[111],
                uzivatel=row[112],
                zodp_osoba=row[113],
                kontakt_osoba=row[114],
                kontakt_jmeno=row[115],
                kontakt_email=row[116],
                kontakt_tel=row[117],
                rada=row[118],
                forma_dopravy=row[119],
                uuid=row[120],
                source=row[121],
                clen_kon_vyk_dph=row[122],
                dat_up1=self._parse_date(row[123]),
                dat_up2=self._parse_date(row[124]),
                dat_smir=self._parse_date(row[125]),
                dat_penale=self._parse_date(row[126]),
                podpis_prik=row[127],
                prikaz_sum=row[128],
                prikaz_sum_men=row[129],
                juh_sum=row[130],
                juh_sum_men=row[131],
                juh_dat=row[132],
                juh_dat_men=row[133],
                zbyva_uhradit=row[134],
                zbyva_uhradit_men=row[135],
                forma_uhrady_cis=row[136],
                stav_uhr_k=row[137],
                juh_sum_pp=row[138],
                juh_sum_pp_men=row[139],
                sum_prepl=row[140],
                sum_prepl_men=row[141],
                sum_zalohy=row[142],
                sum_zalohy_men=row[143],
                stav_odpocet_k=row[144],
                generovat_skl=row[145],
                zaokrouhlit_po_odpoctu=row[146],
                hrom_fakt=row[147],
                zdroj_pro_skl=row[148],
                prodejka=row[149],
                stav_mail_k=row[150],
                dobropisovano=row[151],
                sum_celkem_bez_zaloh=row[152],
                sum_celkem_bez_zaloh_men=row[153],
                odpoc_auto=row[154],
                polozky_faktury=polozky_faktury)
            )
        self.invoices = a.Invoices(invoices=invoices)
        log.debug("Invoices loaded successfully.")
        return self.invoices.invoices

    def migrate_invoices(self) -> "InvoiceHandler":
        _invoices = list()
        
        for invoice in self.load_invoices():
            log.debug(f"Migrating invoice {invoice.kod} / {invoice.cis_obj}")

            i_payment_type = p.PaymentType(paymentType=invoice.forma_uhrady_cis)
            
            i_my_identity = IDENTITY_NEVEN
            i_partner_identity = p.Identity(
                address=p.Address(
                    company=invoice.naz_firmy,
                    city=invoice.mesto,
                    street=invoice.ulice,
                    zip=invoice.psc,
                    ico=invoice.ic,
                    dic=invoice.dic,
                    name=invoice.kontakt_jmeno,
                    phone=invoice.kontakt_tel,
                    email=invoice.kontakt_email
                )
            )

            i_type = invoice.typ_dokl
            i_number = invoice.kod
            i_number_order = invoice.cis_obj
            i_sym_par = invoice.cis_obj
            i_sym_var = invoice.var_sym
            i_sym_const = invoice.kon_sym
            i_date = invoice.dat_vyst
            i_date_tax = invoice.duzp_puv
            i_date_due = invoice.dat_splat
            i_date_act = invoice.dat_ucto
            i_date_order = invoice.dat_vyst

            invoice_header = p.InvoiceHeader(
                invoiceType=i_type,
                number=i_number,
                numberOrder=i_number_order,
                symVar=i_sym_var,
                symPar=i_sym_par,
                symConst=i_sym_const,
                date=i_date,
                dateOrder=i_date_order,
                dateTax=i_date_tax,
                dateDue=i_date_due,
                dateAccounting=i_date_act,
                paymentType=i_payment_type,
                myIdentity=i_my_identity,
                partnerIdentity=i_partner_identity
            )

            invoice_items = [
                p.InvoiceItem(
                    text=item.nazev,
                    note=item.poznam,
                    code=item.kod,
                    quantity=item.mnoz_mj,
                    unit=item.mj,
                    payVAT=bool(item.szb_dph),
                    rateVAT=str(item.szb_dph),
                    homeCurrency=p.HomeCurrency(unitPrice=item.cena_mj),
                    stockItem=p.StockItem(ids=item.kod)
                ) for item in invoice.polozky_faktury
            ]

            invoice_detail = p.InvoiceDetail(invoiceItems=invoice_items)

            invoice_summary_currency = p.InvoiceSummaryCurrency(
                priceHigh=invoice.sum_zkl_zakl,
                priceHighVAT=invoice.sum_dph_zakl,
                priceHighSum=invoice.sum_celkem,
                priceNone=invoice.sum_osv
            )

            invoice_summary = p.InvoiceSummary(
                roundingDocument=None,
                homeCurrency=invoice_summary_currency
            )

            invoice = p.Invoice(
                version="2.0",
                invoiceHeader=invoice_header,
                invoiceDetail=invoice_detail,
                invoiceSummary=invoice_summary
            )

            _invoices.append(invoice)

        self.migrated = p.Invoices(invoices=_invoices)
        return self
    
    def save_migrated_invoices(self, filename: Path = None, encoding: str = 'cp1250') -> "InvoiceHandler":
        if not filename:
            dt = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"pohoda-{encoding}-{dt}.xml"
        path = config.output_path / filename
        log.info(f"Saving migrated invoices to [{path}]")
        model_data = self.migrated.model_dump()
        pohoda_xml = build_data_pack(model_data)
        #import ipdb; ipdb.set_trace()
        with open(path, "w", encoding=encoding) as f:
            f.write(pohoda_xml)
        return self