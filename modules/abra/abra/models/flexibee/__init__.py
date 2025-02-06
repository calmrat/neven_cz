from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from dateutil import parser
import pytz



# Define Pydantic model for invoice parsing
class InvoiceItem(BaseModel):
    """Represents an item in the invoice."""
    ext_id: str = Field(..., alias="ext_id", description="External ID of the item.")
    ext_id_k: float = Field(..., alias="ext_id_k", description="External ID item count.")
    id: str = Field(..., alias="id", description="Internal ID of the item.")
    last_update: Optional[datetime] = Field(None, description="Last update timestamp of the item.")
    kod: Optional[str] = Field(None, description="Item identification code.")
    ean_kod: Optional[str] = Field(None, description="EAN code of the item.")
    nazev: Optional[str] = Field(None, description="Name of the item.")
    mnoz_mj: Optional[float] = Field(None, description="Quantity of the item.")
    cena_mj: Optional[float] = Field(None, description="Unit price of the item.")
    sum_zkl: Optional[float] = Field(None, description="Tax base amount for the item.")
    sum_dph: Optional[float] = Field(None, description="VAT amount for the item.")
    sum_celkem: Optional[float] = Field(None, description="Total price of the item including VAT.")
    storno: Optional[bool] = Field(None, description="Indicates whether the item is canceled.")
    storno_pol: Optional[bool] = Field(None, description="Indicates whether the item position is canceled.")
    typ_polozky: Optional[str] = Field(None, description="Type of item (general, catalog, text, etc.).")
    szb_dph: Optional[float] = Field(None, description="VAT rate percentage.")
    sum_zkl_men: Optional[float] = Field(None, description="Tax base amount in foreign currency.")
    sum_dph_men: Optional[float] = Field(None, description="VAT amount in foreign currency.")
    sum_celkem_men: Optional[float] = Field(None, description="Total price including VAT in foreign currency.")
    sazba_dph: Optional[str] = Field(None, description="VAT rate key.")
    mena: Optional[str] = Field(None, description="Currency of the item.")
    sklad: Optional[str] = Field(None, description="Warehouse reference.")
    zakazka: Optional[str] = Field(None, description="Project reference.")
    dodavatel: Optional[str] = Field(None, description="Supplier reference.")
    clen_dph: Optional[str] = Field(None, description="Tax classification code.")


class Invoice(BaseModel):
    """Represents an issued invoice with its details."""
    ext_id: str = Field(..., alias="ext_id", description="External ID of the invoice.")
    id: str = Field(..., alias="id", description="Internal ID of the invoice.")
    last_update: Optional[datetime] = Field(None, description="Last update timestamp of the invoice.")
    kod: Optional[str] = Field(None, description="Invoice identification code.")
    zamek_k: Optional[str] = Field(None, description="Lock status of the invoice (Open, Viewed, Locked, etc.).")
    cis_dosle: Optional[str] = Field(None, description="Incoming invoice number.")
    var_sym: Optional[str] = Field(None, description="Variable symbol of the invoice.")
    cis_sml: Optional[str] = Field(None, description="Agreement number.")
    cis_obj: Optional[str] = Field(None, description="Order number.")
    dat_vyst: Optional[datetime] = Field(None, description="Issue date of the invoice.")
    duzp_puv: Optional[datetime] = Field(None, description="Taxable supply date.")
    duzp_ucto: Optional[datetime] = Field(None, description="Accounting taxable supply date.")
    dat_splat: Optional[datetime] = Field(None, description="Due date of the invoice.")
    dat_uhra: Optional[datetime] = Field(None, description="Settlement date of the invoice.")
    sum_zkl_celkem: Optional[float] = Field(None, description="Total tax base amount.")
    sum_dph_celkem: Optional[float] = Field(None, description="Total VAT amount.")
    sum_celkem: Optional[float] = Field(None, description="Total amount including VAT.")
    sum_celkem_men: Optional[float] = Field(None, description="Total amount including VAT in foreign currency.")
    mena: Optional[str] = Field(None, description="Currency of the invoice.")
    stav_uhr: Optional[str] = Field(None, description="Payment status of the invoice.")
    firma: Optional[str] = Field(None, description="Company associated with the invoice.")
    kontakt_jmeno: Optional[str] = Field(None, description="Contact person name.")
    kontakt_email: Optional[str] = Field(None, description="Contact person email.")
    kontakt_tel: Optional[str] = Field(None, description="Contact person phone number.")
    polozky_faktury: List[InvoiceItem] = Field([], description="List of invoice items.")
    ic: Optional[str] = Field(None, description="Company ID number.")
    dic: Optional[str] = Field(None, description="VAT ID number.")
    bic: Optional[str] = Field(None, description="Bank SWIFT BIC code.")
    iban: Optional[str] = Field(None, description="Bank IBAN number.")
    banka: Optional[str] = Field(None, description="Bank account name.")
    zaokr_jak_sum_k: Optional[str] = Field(None, description="Rounding method for total sum.")
    zaokr_na_sum_k: Optional[str] = Field(None, description="Rounding degree for total sum.")
    stav_mail_k: Optional[str] = Field(None, description="Email status of the invoice.")
    stav_uziv_k: Optional[str] = Field(None, description="User order status of the invoice.")
    zdroj_pro_skl: Optional[bool] = Field(None, description="Indicates if the invoice is a stock source.")
    hrom_fakt: Optional[bool] = Field(None, description="Indicates multiple invoicing.")
    prodejka: Optional[bool] = Field(None, description="Indicates sales draft.")
    storno: Optional[bool] = Field(None, description="Indicates whether the invoice is canceled.")
    fa_stat: Optional[str] = Field(None, description="Billing country code.")
    mist_urc: Optional[str] = Field(None, description="Destination of goods.")
    zaokrouhlit_po_odpoctu: Optional[bool] = Field(None, description="Indicates rounding after deduction.")
    forma_uhrady_cis: Optional[str] = Field(None, description="Payment method.")
    stav_uhr_k: Optional[str] = Field(None, description="Settlement status.")
    typ_dokl: Optional[str] = Field(None, description="Invoice type.")
    uuid: Optional[str] = Field(None, description="Unique identifier of the invoice.")


class Invoices(BaseModel):
    invoices: List[Invoice]