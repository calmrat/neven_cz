# -*- coding: utf-8 -*-
"""
Upgates Client Module

This module provides an asynchronous API client for Upgates.cz, enabling data synchronization,
logging, and translation functionalities. The client supports syncing products, customers, and
orders from the Upgates API and storing the data in a DuckDB database. Additionally, it includes
methods for translating product descriptions using AI and saving the translations back to the API.

Usage:

    client = UpgatesClient()
    asyncio.run(client.sync_all())

File: upgates/client.py
"""

import asyncio
from typing import Any, Dict, List, Optional

import aiohttp

# from flask.cli import F
import logfire
import pandas as pd
from pydantic import BaseModel, Field

from upgates import config
from upgates.ai import TranslationDeps, translate_text
from upgates.db.duckdb_api import UpgatesDuckDBAPI


def log_sync_statistics(sync_results: Dict[str, List]) -> None:
    """Log the number of each object type saved during sync."""
    stats: Dict[str, int] = {key: len(value) for key, value in sync_results.items()}
    logfire.info(f"Sync completed: {stats}")


# FIXME: MOVE TO MODELS
class ParameterDescription(BaseModel):
    language: str
    name: str


class ParameterValueDescription(BaseModel):
    language: str
    value: str


class Image(BaseModel):
    id: int
    url: str


class ParameterValue(BaseModel):
    id: int
    descriptions: List[ParameterValueDescription]
    position: int
    image: Optional[Image] = None


class Parameter(BaseModel):
    id: int
    descriptions: List[ParameterDescription]
    # values: List[str] = Field(default_factory=list)
    # Added v0.1.3
    values: List[ParameterValue] = Field(default_factory=list)
    position: int
    image: Optional[Dict[str, str]] = None
    display_type: str
    display_in_product_list_yn: bool
    display_in_product_detail_yn: bool
    display_in_filters_as_slider_yn: bool


class Parameters(BaseModel):
    parameters: List[Parameter]


class UpgatesClient:
    """Async API Client for Upgates with proper syncing, logging, and translations."""

    PARALLEL_BATCH_SIZE = config.paralell_batch_size

    DATA_PATH = config.data_path
    DB_FILE = config.db_file
    API_URL = config.UPGATES_API_URL
    LOGIN = config.UPGATES_LOGIN
    API_KEY = config.UPGATES_API_KEY
    VERIFY_SSL = True if config.UPGATES_VERIFY_SSL else False

    def __init__(self):
        """Ensure DuckDB database is initialized before starting."""
        logfire.debug("🌉 UpgatesClient initialized.")
        self.db_api = (
            UpgatesDuckDBAPI()
        )  # Initializes only once due to lazy table creation

    async def sync_all(self):
        """Sync all data: products, customers, orders."""
        logfire.info("ℹ️ Starting full API sync...")
        await asyncio.gather(
            self.sync_products(), self.sync_customers(), self.sync_orders()
        )

    async def sync_products(self, page_count=None):
        """Sync products from the Upgates.cz API."""
        logfire.info("Fetching product data...")
        products_response = await self.fetch_data("products", page_count=page_count)

        if products_response:
            products = products_response.get("products", [])
            logfire.info(
                f"Fetched product data: {products[:1]}..."
            )  # Log the first product as a sample

            if products:
                for product in products:
                    # print ("Product: ", product['product_id'], product['code'])
                    # import pdb; pdb.set_trace()
                    product_id = product.get("product_id")
                    code = product.get("code")
                    ean = product.get("ean", "")
                    manufacturer = product.get("manufacturer", "")
                    stock = product.get("stock", 0)
                    weight = product.get("weight", 0)
                    availability = product.get("availability", "")
                    availability_type = product.get("availability_type", "")
                    unit = product.get("unit", "ks")

                    # Convert _yn fields to 1 (True) or 0 (False)
                    action_currently_yn = (
                        1 if product.get("action_currently_yn", False) else 0
                    )
                    active_yn = 1 if product.get("active_yn", False) else 0
                    archived_yn = 1 if product.get("archived_yn", False) else 0
                    can_add_to_basket_yn = (
                        1 if product.get("can_add_to_basket_yn", False) else 0
                    )
                    adult_yn = 1 if product.get("adult_yn", False) else 0
                    set_yn = 1 if product.get("set_yn", False) else 0
                    in_set_yn = 1 if product.get("in_set_yn", False) else 0
                    exclude_from_search_yn = (
                        1 if product.get("exclude_from_search_yn", False) else 0
                    )

                    # Inserting product data into the database
                    self.db_api.insert_product(
                        product_id,
                        code,
                        ean,
                        manufacturer,
                        stock,
                        weight,
                        availability,
                        availability_type,
                        unit,
                        action_currently_yn,
                        active_yn,
                        archived_yn,
                        can_add_to_basket_yn,
                        adult_yn,
                        set_yn,
                        in_set_yn,
                        exclude_from_search_yn,
                    )

                    # Insert descriptions
                    for desc in product.get("descriptions", []):
                        language = desc.get("language", "unknown")
                        title = desc.get("title", "")
                        short_description = desc.get("short_description", "")
                        long_description = desc.get("long_description", "")
                        url = desc.get("url", "")
                        seo_title = desc.get("seo_title", "")
                        seo_description = desc.get("seo_description", "")
                        seo_url = desc.get("seo_url", "")
                        seo_keywords = desc.get("seo_keywords", "")
                        unit = desc.get("unit", "ks")
                        self.db_api.insert_product_description(
                            product_id,
                            language,
                            title,
                            short_description,
                            long_description,
                            url,
                            seo_title,
                            seo_description,
                            seo_url,
                            seo_keywords,
                            unit,
                        )

                    # Insert prices
                    for price in product.get("prices", []):
                        currency = price.get("currency", "unknown")
                        price_with_vat = next(
                            (
                                pl.get("price_with_vat", 0)
                                for pl in price.get("pricelists", [])
                            ),
                            0.0,
                        )
                        self.db_api.insert_product_price(
                            product_id, currency, price_with_vat
                        )

                    # Insert images
                    for image in product.get("images", []):
                        file_id = image.get("file_id", None)
                        url = image.get("url", "")
                        main_yn = 1 if image.get("main_yn", False) else 0
                        position = image.get("position", 0)
                        self.db_api.insert_product_image(
                            product_id, file_id, url, main_yn, position
                        )

                    # Insert categories
                    for category in product.get("categories", []):
                        category_id = category.get("category_id")
                        category_code = category.get("code", "")
                        category_name = category.get("name", "")
                        main_yn = 1 if category.get("main_yn", 0) else 0
                        position = category.get("position", 0)
                        self.db_api.insert_product_category(
                            product_id,
                            category_id,
                            category_code,
                            category_name,
                            main_yn,
                            position,
                        )

                    # Insert metadata
                    for meta in product.get("metas", []):
                        meta_key = meta.get("key", "")
                        meta_type = meta.get("type", "")
                        meta_value = meta.get("value", "")
                        self.db_api.insert_product_meta(
                            product_id, meta_key, meta_type, meta_value
                        )

                    # Insert VAT details
                    for vat_country, vat_percentage in product.get("vats", {}).items():
                        self.db_api.insert_product_vat(
                            product_id, vat_country, vat_percentage
                        )

                logfire.info(
                    f"Product sync complete. {len(products)} products fetched and inserted."
                )
            else:
                logfire.warning("No product data found to sync.")
        else:
            logfire.warning("Failed to fetch product data.")

    async def sync_customers(self, page_count=None):
        """Sync customer data from the API."""
        logfire.info("ℹ️ Fetching customer data...")
        all_customers = []
        page = 1

        while True:
            customers_response = await self.fetch_data("customers", page, page_count)
            if (
                isinstance(customers_response, dict)
                and "customers" in customers_response
            ):
                customers = customers_response["customers"]
                if customers:
                    all_customers.extend(customers)
                    logfire.info(f"Fetched {len(customers)} items from page {page}")

                    total_pages = customers_response.get("number_of_pages", 0)
                    if page >= total_pages:
                        logfire.debug(
                            f"✅ All pages fetched. Total pages: {total_pages}"
                        )
                        break
                    page += 1
                else:
                    logfire.warning(f"⚠️ No customers found on page {page}.")
                    break
            else:
                logfire.error(
                    f"❌ Customers data is missing in response for page {page}."
                )
                break

        # FIXME
        # We need to come back to this later

        # if all_customers:
        #    self.db_api.insert_customers(all_customers)
        #    logfire.info(
        #        f"✅ Customer sync complete. {len(all_customers)} customers fetched and inserted."
        #    )

    async def sync_orders(self):
        """Sync order data from the API."""
        logfire.info("ℹ️ Fetching order data...")
        all_orders = []
        page = 1

        while True:
            orders_response = await self.fetch_data("orders", page)
            if isinstance(orders_response, dict) and "orders" in orders_response:
                orders = orders_response["orders"]
                if orders:
                    all_orders.extend(orders)
                    logfire.info(f"Fetched {len(orders)} items from page {page}")

                    total_pages = orders_response.get("number_of_pages", 0)
                    if page >= total_pages:
                        logfire.debug(
                            f"✅ All pages fetched. Total pages: {total_pages}"
                        )
                        break
                    page += 1
                else:
                    logfire.warning(f"⚠️ No orders found on page {page}.")
                    break
            else:
                logfire.error(f"❌ Orders data is missing in response for page {page}.")
                break

        # if all_orders:
        #     self.db_api.insert_orders(all_orders)
        #     logfire.info(
        #         f"✅ Order sync complete. {len(all_orders)} orders fetched and inserted."
        #     )

    async def sync_parameters(self):
        """Sync parameter data from the API."""
        logfire.info("ℹ️ Fetching parameter data...")
        page = 1

        while True:
            parameters_response = await self.fetch_data("parameters", page)
            if (
                isinstance(parameters_response, dict)
                and "parameters" in parameters_response
            ):
                parameters = parameters_response["parameters"]
                if parameters:
                    logfire.info(f"Fetched {len(parameters)} items from page {page}")
                    logfire.debug(
                        f"Inserting {len(parameters)} parameters into the database."
                    )

                    parameters = Parameters(
                        parameters=[Parameter(**parameter) for parameter in parameters]
                    )

                    import ipdb

                    ipdb.set_trace()
                    # self.db_api.insert_parameters(parameters)

                    total_pages = parameters_response.get("number_of_pages", 0)
                    if page >= total_pages:
                        logfire.debug(
                            f"✅ All pages fetched. Total pages: {total_pages}"
                        )
                        break
                    page += 1
                else:
                    logfire.warning(f"⚠️ No parameters found on page {page}.")
                    break
            else:
                logfire.error(
                    f"❌ Parameters data is missing in response for page {page}."
                )
                break

    async def fetch_data(self, endpoint, page=1, page_count=None) -> dict[str, Any]:
        """Fetch data from the API with retries and handle pagination with rate-limiting."""
        all_data = []

        async def fetch_page(page_number: int):
            """Fetch a single page of data."""
            try:
                logfire.debug(f"🔄 Fetching page {page_number} of {endpoint}")
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.API_URL}/{endpoint}?page={page_number}",
                        auth=aiohttp.BasicAuth(self.LOGIN, self.API_KEY),
                        ssl=self.VERIFY_SSL,
                    ) as response:
                        logfire.debug(
                            f"✅ Received response status: {response.status} for page {page_number}"
                        )

                        if response.status == 429:
                            raise RuntimeError("Rate limit exceeded. Retry later.")
                            # If rate limit exceeded, extract Retry-After header and wait
                            # retry_after = response.headers.get(
                            #    "Retry-After", 60
                            # )  # Default to 60 seconds if not provided
                            # await asyncio.sleep(int(retry_after))  # Wait for retry time
                            # return await fetch_page(page_number)  # Retry the same page

                        # Parse the response
                        data = await response.json()
                        logfire.debug(f"📊 Response data: {data}")

                        # Handle the response depending on the endpoint
                        match endpoint:
                            case "products":
                                items = data.get("products", [])
                            case "customers":
                                items = data.get("customers", [])
                            case "orders":
                                items = data.get("orders", [])
                            case "parameters":
                                items = data.get("parameters", [])
                            case _:
                                logfire.error(
                                    f"❌ Unexpected endpoint {endpoint}. Aborting."
                                )
                                import ipdb

                                ipdb.set_trace()
                                return [], 0

                        return items, data.get("number_of_pages", 1)

            except Exception as e:
                logfire.warning(
                    f"⚠️ Failed to fetch page {page_number} of {endpoint}: {e}"
                )
                raise

        # Fetch pages sequentially or up to the specified `page_count`
        page = 1
        while True:
            items, total_pages = await fetch_page(page)
            all_data.extend(items)

            # If page_count is provided, stop after reaching the specified number of pages
            if page_count and page >= page_count:
                logfire.debug(
                    f"✅ Reached the requested page count of {page_count}. Stopping."
                )
                break

            # If all pages are fetched, stop
            match page >= total_pages:
                case True:
                    logfire.debug(f"✅ All pages fetched. Total pages: {total_pages}")
                    break
                case False:
                    page += 1  # Go to the next page

        logfire.info(f"✅ All pages fetched. Total items: {len(all_data)}")
        return {endpoint: all_data}

    async def translate_product(
        self, product_code: str, target_lang: str, prompt: str
    ) -> dict:
        """Translate product descriptions using AI."""
        target_lang = target_lang.lower()
        prompt = (prompt or "").strip()

        logfire.info(
            f"Starting translation for product '{product_code}' to '{target_lang}'"
        )
        logfire.debug(f"Prompt Injected: {prompt or 'None'}")

        # Retrieve the product details from DuckDB (assumes a DataFrame is returned)
        product_details = await self.db_api.get_product_details(code=product_code)

        if product_details is None:
            raise ValueError(f"Product '{product_code}' not found in local database.")

        if isinstance(product_details, pd.DataFrame) and product_details.empty:
            raise ValueError(
                f"No product details found for '{product_code}' in local database."
            )

        # Assume the first record represents the product.
        product = product_details.iloc[0]

        descriptions = product.get("descriptions", [])
        cz_desc = None
        for desc in descriptions:
            if desc.get("language").lower() in ("cz", "cs"):
                cz_desc = desc
                break

        if not cz_desc:
            msg = "No Czech description available for product."
            # logfire.error(msg)
            raise ValueError(msg)

        source_title = (cz_desc.get("title") or "").strip()
        source_long = (cz_desc.get("long_description") or "").strip()

        # if not source_title or not source_long:
        if not source_title:
            raise ValueError("Missing required field: CZ-{Title}")

        user_prompt = f"""
        Translate requested fields to {target_lang} language based on:
        
         Product code: {product_code}
         Title: {source_title}
        """
        user_prompt += f"Long Description: {source_long}" if source_long else ""

        if prompt and prompt != "None":
            logfire.debug(f"Injecting additional user prompt text: {prompt}")
            user_prompt += f"\n\nAdditionally, {prompt}"

        # Call the AI translation function using pydantic AI run()
        try:
            deps = TranslationDeps()
            ai_result = await translate_text(user_prompt, deps=deps)
        except RuntimeError as e:
            logfire.error(f"AI translation failed: {e}")
            raise

        if not ai_result:
            logfire.error("AI translation returned an empty result.")
            raise SystemExit

        logfire.info(f"Translation result: {ai_result}")

        ai_dump = ai_result.model_dump()

        # Update the DuckDB instance with the new translation fields.
        self.db_api.update_product_translation(product_code, ai_dump)

        logfire.info("DuckDB instance updated with new translation fields.")
        return ai_dump

    async def save_translation(self, product_code: str, target_lang: str = "cz"):
        """Save the translated product back to Upgates API."""
        target_lang = target_lang.lower().strip()
        logfire.info(
            f"Saving '{target_lang}' translations for product '{product_code}' back to Upgates.cz API"
        )

        product_details = await self.db_api.get_product_details(product_code)
        if product_details.empty:
            logfire.error(f"Product '{product_code}' not found in local database.")
            return

        product = product_details.iloc[0]
        descriptions = product.get("descriptions", [])
        if not descriptions:
            logfire.error("No descriptions found for the product.")
            return
        desc_matched = [
            d
            for d in descriptions
            if d.get("language").lower().strip() == target_lang.lower().strip()
        ]
        translations = desc_matched[0] if desc_matched else None

        if not translations:
            logfire.error("No translation found to save for the product.")
            return

        # Corrected payload structure
        payload = {
            "products": [
                {
                    "code": product_code,
                    "descriptions": [
                        {
                            "language": translations.get("language"),
                            "active_yn": True,  # optional, default is TRUE
                            "title": translations.get("title")
                            or translations.get("seo_title"),
                            "short_description": translations.get("short_description"),
                            "long_description": translations.get("long_description"),
                            "seo_description": translations.get("seo_description"),
                            "seo_keywords": translations.get("seo_keywords"),
                            "seo_title": translations.get("seo_title"),
                            "seo_url": translations.get(
                                "seo_url"
                            ),  # optional if needed
                        }
                    ],
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            url = f"{self.API_URL}/products/{product_code}"
            auth = aiohttp.BasicAuth(self.LOGIN, self.API_KEY)
            async with session.put(
                url, json=payload, auth=auth, ssl=self.VERIFY_SSL
            ) as resp:
                if resp.status == 200:
                    logfire.info(
                        "Product translations saved to Upgates.cz API successfully."
                    )
                    return await resp.json()
                else:
                    error_text = await resp.text()
                    raise RuntimeError(
                        f"🔥 [{product_code}] Failed to save translation. Status: {resp.status} - {error_text}"
                    )


# EOF
