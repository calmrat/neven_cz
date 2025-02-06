from pathlib import Path
from typing import List, Optional

from xml.etree import ElementTree as ET

import duckdb

from .models.flexibee import Invoice, Invoices, InvoiceItem
from .models.pohoda import InvoiceHeader, PaymentType, Address, Identity

import logging
from datetime import datetime

log = logging.getLogger(__name__)

class DefaultHandler:
    conn = None
    invoices: Invoices | None = None

    def __init__(self, db_path : Path):
        # DuckDB connection
        self.conn = duckdb.connect(str(db_path))

    def __get_float(self, tag: str, element) -> Optional[float]:
        text = element.findtext(tag)
        try:
            return float(text) if text not in (None, "") else None
        except ValueError:
            return None

    def __get_text(self, tag: str, element) -> Optional[str]:
        text = element.findtext(tag)
        return text.strip() if text else None
    
    def __get_date(self, tag: str, element) -> Optional[str]:
        text = element.findtext(tag).strip()
        if not text:
            log.debug(f"Missing date in the tag {tag}.")
            return None
        
        dt = None
        try:
            dt = datetime.strptime(text, "%Y-%m-%dT%z")
        except ValueError:
            try:
                dt = datetime.fromisoformat(text)
            except ValueError:
                import ipdb; ipdb.set_trace()
                raise ValueError(f"Missing or invalid date in the tag {tag}.")    

        dt_str = dt.isoformat()    
        return dt_str

    def __extract_invoice_items(self, element: ET.Element) -> List[InvoiceItem]:
        items = []
        all_elements = element.findall(".//polozkyFaktury")
        ext_id, ext_id_k, _id = "", "", ""
        for item_elements in all_elements:
            for _element in item_elements:
                _ids = _element.findall("id")
                for _id in _ids:
                    if _id.text.startswith("ext:"):
                        ext_id = _id.text.split(":")[-1]
                        ext_id, ext_id_k = ext_id.split("-")
                        ext_id_k = float(ext_id_k) # Convert to float
                    else:
                        _id = _id.text
                #import ipdb; ipdb.set_trace()

                # We will have always extracted the IDs by now
                if ext_id == "" or ext_id_k == "" or _id == "":
                    raise ValueError("Missing ID in the invoice item.")
                
                items.append(InvoiceItem(
                    id=_id,
                    ext_id=ext_id,
                    ext_id_k=ext_id_k,
                    last_update=self.__get_date("lastUpdate", _element),
                    kod=self.__get_text("kod", _element),
                    ean_kod=self.__get_text("eanKod", _element),
                    nazev=self.__get_text("nazev", _element),
                    mnoz_mj=self.__get_float("mnozMj", _element),
                    cena_mj=self.__get_float("cenaMj", _element),
                    sum_zkl=self.__get_float("sumZkl", _element),
                    sum_dph=self.__get_float("sumDph", _element),
                    sum_celkem=self.__get_float("sumCelkem", _element),
                    storno=self.__get_text("storno", _element),
                    storno_pol=self.__get_text("stornoPol", _element),
                    typ_polozky=self.__get_text("typPolozky", _element),
                    szb_dph=self.__get_float("szbDph", _element),
                    sum_zkl_men=self.__get_float("sumZklMen", _element),
                    sum_dph_men=self.__get_float("sumDphMen", _element),
                    sum_celkem_men=self.__get_float("sumCelkemMen", _element),
                    sazba_dph=self.__get_text("sazbaDph", _element),
                    mena=self.__get_text("mena", _element),
                    sklad=self.__get_text("sklad", _element),
                    zakazka=self.__get_text("zakazka", _element),
                    dodavatel=self.__get_text("dodavatel", _element),
                    clen_dph=self.__get_text("clenDph", _element)
                ))
        return items
    
    def from_xml(self, element: ET.Element) -> "Invoice":
        # Helper to clean text and convert to float

        # Handling duplicate <id> elements: first for ext_id, second for id
        ids = element.findall("id")
        ext_id = None
        _id = None
        for i in ids:
            text = i.text.strip() if i.text else ""
            if text.startswith("ext:"):
                ext_id = text.split("ext:")[-1]
            elif text.startswith("key:"):
                _id = text.split("key:")[-1]
            #import ipdb; ipdb.set_trace()

        polozky_faktury = self.__extract_invoice_items(element)

        return Invoice(
            ext_id=ext_id,
            id=_id,
            kod=self.__get_text("kod", element),
            last_update=self.__get_date("lastUpdate", element),
            dat_vyst=self.__get_date("datVyst", element),
            duzp_puv=self.__get_date("duzpPuv", element),
            duzp_ucto=self.__get_date("duzpUcto", element),
            dat_splat=self.__get_date("datSplat", element),
            dat_uhra=self.__get_date("datUhr", element),
            sum_zkl_celkem=self.__get_float("sumZklCelkem", element),
            sum_dph_celkem=self.__get_float("sumDphCelkem", element),
            sum_celkem=self.__get_float("sumCelkem", element),
            mena=self.__get_text("mena", element),
            var_sym=self.__get_text("varSym", element),
            firma=self.__get_text("nazFirmy", element),
            kontakt_jmeno=self.__get_text("kontaktJmeno", element),
            kontakt_email=self.__get_text("kontaktEmail", element),
            kontakt_tel=self.__get_text("kontaktTel", element),
            ic=self.__get_text("ic", element),
            dic=self.__get_text("dic", element),
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
            dat_uhra TEXT,
            sum_zkl_celkem FLOAT,
            sum_dph_celkem FLOAT,
            sum_celkem FLOAT,
            sum_celkem_men FLOAT,
            mena TEXT,
            stav_uhr TEXT,
            firma TEXT,
            kontakt_jmeno TEXT,
            kontakt_email TEXT,
            kontakt_tel TEXT,
            ic TEXT,
            dic TEXT,
            bic TEXT,
            iban TEXT,
            banka TEXT,
            zaokr_jak_sum_k TEXT,
            zaokr_na_sum_k TEXT,
            stav_mail_k TEXT,
            stav_uziv_k TEXT,
            zdroj_pro_skl BOOLEAN,
            hrom_fakt BOOLEAN,
            prodejka BOOLEAN,
            storno BOOLEAN,
            fa_stat TEXT,
            mist_urc TEXT,
            zaokrouhlit_po_odpoctu BOOLEAN,
            forma_uhrady_cis TEXT,
            stav_uhr_k TEXT,
            typ_dokl TEXT,
            uuid TEXT
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS invoice_items (
                ext_id TEXT,
                ext_id_k FLOAT,
                id TEXT,
                last_update TEXT,
                kod TEXT,
                ean_kod TEXT,
                nazev TEXT,
                mnoz_mj FLOAT,
                cena_mj FLOAT,
                sum_zkl FLOAT,
                sum_dph FLOAT,
                sum_celkem FLOAT,
                storno BOOLEAN,
                storno_pol BOOLEAN,
                typ_polozky TEXT,
                szb_dph FLOAT,
                sum_zkl_men FLOAT,
                sum_dph_men FLOAT,
                sum_celkem_men FLOAT,
                sazba_dph TEXT,
                mena TEXT,
                sklad TEXT,
                zakazka TEXT,
                dodavatel TEXT,
                clen_dph TEXT
            )
        """)

        

class InvoiceHandler(DefaultHandler):
    # Function to parse XML invoices
    def parse_invoices(self, xml_file: Path) -> List[Invoice]:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        invoices = []
        
        # Now matching the faktura-vydana elements as invoice sources
        for invoice in root.findall(".//faktura-vydana"):
            invoices.append(self.from_xml(invoice))

        self.invoices = Invoices(invoices=invoices)
        return self

    def sync_invoices(self):
        if not self.invoices:
            log.info("[bold red]No invoices to sync.[/bold red]")
            return

        log.info("[bold green]Syncing invoices to database...[/bold green]")
        for invoice in self.invoices.invoices:
            self.conn.execute("""
                INSERT INTO invoices (
                    ext_id, id, last_update, kod, zamek_k, cis_dosle, var_sym, cis_sml, cis_obj, dat_vyst, duzp_puv, duzp_ucto, dat_splat, dat_uhra,
                    sum_zkl_celkem, sum_dph_celkem, sum_celkem, sum_celkem_men, mena, stav_uhr, firma, kontakt_jmeno, kontakt_email, kontakt_tel,
                    ic, dic, bic, iban, banka, zaokr_jak_sum_k, zaokr_na_sum_k, stav_mail_k, stav_uziv_k, zdroj_pro_skl, hrom_fakt, prodejka,
                    storno, fa_stat, mist_urc, zaokrouhlit_po_odpoctu, forma_uhrady_cis, stav_uhr_k, typ_dokl, uuid
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                invoice.ext_id, invoice.id, invoice.last_update, invoice.kod, invoice.zamek_k, invoice.cis_dosle, invoice.var_sym, invoice.cis_sml,
                invoice.cis_obj, invoice.dat_vyst, invoice.duzp_puv, invoice.duzp_ucto, invoice.dat_splat, invoice.dat_uhra, invoice.sum_zkl_celkem,
                invoice.sum_dph_celkem, invoice.sum_celkem, invoice.sum_celkem_men, invoice.mena, invoice.stav_uhr, invoice.firma, invoice.kontakt_jmeno,
                invoice.kontakt_email, invoice.kontakt_tel, invoice.ic, invoice.dic, invoice.bic, invoice.iban, invoice.banka, invoice.zaokr_jak_sum_k,
                invoice.zaokr_na_sum_k, invoice.stav_mail_k, invoice.stav_uziv_k, invoice.zdroj_pro_skl, invoice.hrom_fakt, invoice.prodejka, invoice.storno,
                invoice.fa_stat, invoice.mist_urc, invoice.zaokrouhlit_po_odpoctu, invoice.forma_uhrady_cis, invoice.stav_uhr_k, invoice.typ_dokl, invoice.uuid
            ))

            for item in invoice.polozky_faktury:
                self.conn.execute("""
                    INSERT INTO invoice_items (
                        ext_id, ext_id_k, id, last_update, kod, ean_kod, nazev, mnoz_mj, cena_mj, sum_zkl, sum_dph, sum_celkem, storno, storno_pol,
                        typ_polozky, szb_dph, sum_zkl_men, sum_dph_men, sum_celkem_men, sazba_dph, mena, sklad, zakazka, dodavatel, clen_dph
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.ext_id, item.ext_id_k, item.id, item.last_update, item.kod, item.ean_kod, item.nazev, item.mnoz_mj, item.cena_mj, item.sum_zkl,
                    item.sum_dph, item.sum_celkem, item.storno, item.storno_pol, item.typ_polozky, item.szb_dph, item.sum_zkl_men, item.sum_dph_men,
                    item.sum_celkem_men, item.sazba_dph, item.mena, item.sklad, item.zakazka, item.dodavatel, item.clen_dph
                ))

        log.info("[green]Invoices synced successfully.[/green]")
    
    def load_invoices(self) -> List[Invoice]:
        log.info("[bold green]Loading invoices from database...[/bold green]")
        rows = self.conn.execute("SELECT * FROM invoices").fetchall()
        invoices = []
        
        for row in rows:
            invoices.append(Invoice(
                ext_id=row[0],
                id=row[1],
                last_update=row[2],
                kod=row[3],
                zamek_k=row[4],
                cis_dosle=row[5],
                var_sym=row[6],
                cis_sml=row[7],
                cis_obj=row[8],
                dat_vyst=row[9],
                duzp_puv=row[10],
                duzp_ucto=row[11],
                dat_splat=row[12],
                dat_uhra=row[13],
                sum_zkl_celkem=row[14],
                sum_dph_celkem=row[15],
                sum_celkem=row[16],
                sum_celkem_men=row[17],
                mena=row[18],
                stav_uhr=row[19],
                firma=row[20],
                kontakt_jmeno=row[21],
                kontakt_email=row[22],
                kontakt_tel=row[23],
                ic=row[24],
                dic=row[25],
                bic=row[26],
                iban=row[27],
                banka=row[28],
                zaokr_jak_sum_k=row[29],
                zaokr_na_sum_k=row[30],
                stav_mail_k=row[31],
                stav_uziv_k=row[32],
                zdroj_pro_skl=row[33],
                hrom_fakt=row[34],
                prodejka=row[35],
                storno=row[36],
                fa_stat=row[37],
                mist_urc=row[38],
                zaokrouhlit_po_odpoctu=row[39],
                forma_uhrady_cis=row[40],
                stav_uhr_k=row[41],
                typ_dokl=row[42],
                uuid=row[43],
                polozky_faktury=self.__extract_invoice_items(row[1])  # Assuming row[1] is the invoice ID
            ))
        self.invoices = Invoices(invoices=invoices)
        log.info("[green]Invoices loaded successfully.[/green]")
        return self.invoices.invoices

    def migrate_invoices(self) -> "InvoiceHandler":
        for invoice in self.load_invoices():
            log.info(f"[bold]Migrating invoice {invoice.id}[/bold]")

            i_payment_type = PaymentType(name="Bank transfer")
            i_my_identity = Identity(
                address=Address(
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
            i_partner_identity = Identity(
                address=Address(
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

            i_type = "issued"
            i_number = invoice.kod
            i_number_order = invoice.var_sym
            i_sym_var = invoice.var_sym
            i_date = invoice.dat_vyst
            i_date_tax = invoice.duzp_puv
            i_date_due = invoice.dat_splat
            i_payment_type = i_payment_type

            invoice_header = InvoiceHeader(
                invoiceType=i_type,
                number=i_number,
                numberOrder=i_number_order,
                symVar=i_sym_var,
                date=i_date,
                dateTax=i_date_tax,
                dateDue=i_date_due,
                paymentType=i_payment_type,
                myIdentity=i_my_identity,
                partnerIdentity=i_partner_identity
            )

            invoice = Invoice(
                version="2.0",
                header=invoice_header,
                detail=None,
                summary=None
            )



        import ipdb; ipdb.set_trace()