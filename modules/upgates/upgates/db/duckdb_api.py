#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DuckDB API for Upgates Data Management

This module provides a class `UpgatesDuckDBAPI` to manage interactions with DuckDB for Upgates data.
It includes methods to initialize the database, create tables, insert data, and retrieve data.

Usage:

    db_api = UpgatesDuckDBAPI()
    db_api.insert_product(...)
    product_details = db_api.get_product_details(product_id=123)

File: /Users/cward/Repos/neven_cz/modules/upgates/upgates/db/duckdb_api.py
"""

import os

import duckdb
import logfire
import pandas as pd

from upgates import config


class UpgatesDuckDBAPI:
    """Class to manage interactions with DuckDB for Upgates data."""

    _initialized = False  # Class-level flag to track initialization

    def __init__(self):
        """Initialize the DuckDB API client."""
        self.cache_path = config.cache_path
        self.db_file = config.default_db_path
        self._ensure_cache_directory_exists()
        existed_already = os.path.exists(self.db_file)
        self.conn = duckdb.connect(self.db_file)

        # Initialize DB only if not already done
        if not (UpgatesDuckDBAPI._initialized and existed_already):
            logfire.debug(f"Initializing DuckDB API @ {self.db_file}")
            self._initialize_db()
            UpgatesDuckDBAPI._initialized = True
        else:
            logfire.debug("DuckDB tables already exist. Skipping initialization.")

        logfire.debug("UpgatesDuckDBAPI initialized.")

    def _initialize_db(self):
        """Create tables if they don't exist."""
        logfire.debug("Initializing DuckDB tables...")

        # Create sequences for primary key auto-generation
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_product_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_description_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_prices_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_image_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_meta_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_vat_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_category_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_customer_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_order_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_parameter_id START 1;")
        self.conn.execute(
            "CREATE SEQUENCE IF NOT EXISTS seq_parameter_description_id START 1;"
        )
        self.conn.execute(
            "CREATE SEQUENCE IF NOT EXISTS seq_parameter_value_id START 1;"
        )
        self.conn.execute(
            "CREATE SEQUENCE IF NOT EXISTS seq_parameter_value_description_id START 1;"
        )
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_image_id START 1;")

        # Check if the database and tables exist before creating
        if not self._check_table_exists("products"):
            self._create_products_table()
        if not self._check_table_exists("customers"):
            self._create_customers_table()
        if not self._check_table_exists("orders"):
            self._create_orders_table()
        if not self._check_table_exists("descriptions"):
            self._create_descriptions_table()
        if not self._check_table_exists("prices"):
            self._create_prices_table()
        if not self._check_table_exists("images"):
            self._create_images_table()
        if not self._check_table_exists("categories"):
            self._create_categories_table()
        if not self._check_table_exists("metas"):
            self._create_metas_table()
        if not self._check_table_exists("vats"):
            self._create_vats_table()
        if not self._check_table_exists("parameters"):
            self._create_parameters_table()

        logfire.debug("DuckDB tables initialized.")

    def _check_table_exists(self, table_name):
        """Check if the table exists in DuckDB."""
        query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
        result = self.conn.execute(query).fetchone()
        return result[0] > 0

    def _ensure_cache_directory_exists(self):
        """Ensure the cache directory exists."""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)

    def _create_products_table(self):
        """Create products table if it doesn't exist."""
        logfire.debug("Creating products table...")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_product_id'),
                product_id INTEGER UNIQUE,
                code TEXT,
                ean TEXT,
                manufacturer TEXT,
                stock INTEGER,
                weight INTEGER,
                availability TEXT,
                availability_type TEXT,
                unit TEXT,
                action_currently_yn BOOLEAN,
                active_yn BOOLEAN,
                archived_yn BOOLEAN,
                can_add_to_basket_yn BOOLEAN,
                adult_yn BOOLEAN,
                set_yn BOOLEAN,
                in_set_yn BOOLEAN,
                exclude_from_search_yn BOOLEAN
            );
        """)
        logfire.debug(
            f"Product table created: {self.conn.execute('DESCRIBE products').fetchall()}"
        )

    def _create_customers_table(self):
        """Create customers table if it doesn't exist."""
        logfire.debug("Creating customers table...")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_customer_id'),
                customer_id INTEGER UNIQUE,
                type TEXT,
                firstname TEXT,
                surname TEXT,
                email TEXT,
                phone TEXT,
                company_name TEXT
            );
        """)

    def _create_orders_table(self):
        """Create orders table if it doesn't exist."""
        logfire.debug("Creating orders table...")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_order_id'),
                order_id INTEGER,
                order_number TEXT,
                customer_id INTEGER,
                total_price FLOAT,
                total_weight FLOAT,
                status TEXT
            );
        """)

    def _create_descriptions_table(self):
        """Create descriptions table if it doesn't exist."""
        logfire.debug("Creating descriptions table...")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS descriptions (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_description_id'),
                -- description_id INTEGER,
                product_id INTEGER,
                language TEXT,
                title TEXT,
                short_description TEXT,
                long_description TEXT,
                url TEXT,
                seo_title TEXT,
                seo_description TEXT,
                seo_url TEXT,
                seo_keywords TEXT,
                unit TEXT,
                UNIQUE (product_id, language),
                FOREIGN KEY (product_id) REFERENCES products(product_id) 
            );
        """)

    def _create_prices_table(self):
        """Create prices table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_prices_id'),
                price_id INTEGER,
                product_id INTEGER,
                currency TEXT,
                price_with_vat FLOAT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def _create_images_table(self):
        """Create images table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_image_id'),
                image_id INTEGER,
                product_id INTEGER,
                file_id INTEGER,
                url TEXT,
                main_yn BOOLEAN,
                position INTEGER,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def _create_categories_table(self):
        """Create categories table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_category_id'),
                category_id INTEGER,
                product_id INTEGER,
                category_code TEXT,
                category_name TEXT,
                main_yn BOOLEAN,
                position INTEGER,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def _create_metas_table(self):
        """Create metas table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS metas (
                meta_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_meta_id'),
                product_id INTEGER,
                meta_key TEXT,
                meta_type TEXT,
                meta_value TEXT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def _create_vats_table(self):
        """Create VAT details table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vats (
                vat_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_vat_id'),
                product_id INTEGER,
                country_code TEXT,
                vat_percentage FLOAT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def _create_parameter_descriptions_table(self):
        """Create parameter descriptions table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS parameter_descriptions (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_parameter_description_id'),
                parameter_id INTEGER,
                language TEXT,
                name TEXT,
                FOREIGN KEY (parameter_id) REFERENCES parameters(id)
            );
        """)

    def _create_parameter_value_descriptions_table(self):
        """Create parameter value descriptions table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS parameter_value_descriptions (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_parameter_value_description_id'),
                parameter_value_id INTEGER,
                language TEXT,
                value TEXT,
                FOREIGN KEY (parameter_value_id) REFERENCES parameter_values(id)
            );
        """)

    def _create_parameter_values_table(self):
        """Create parameter values table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS parameter_values (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_parameter_value_id'),
                position INTEGER,
                image_id INTEGER,
                FOREIGN KEY (image_id) REFERENCES images(id)
            );
        """)

    def _create_parameters_table(self):
        """Create parameters table if it doesn't exist."""
        if self._check_table_exists("parameter_values"):
            return

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS parameters (
                id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_parameter_id'),
                position INTEGER,
                display_type TEXT,
                display_in_product_list_yn BOOLEAN,
                display_in_product_detail_yn BOOLEAN,
                display_in_filters_as_slider_yn BOOLEAN,
                image_id INTEGER,
                FOREIGN KEY (image_id) REFERENCES images(id)
            );
        """)

        self._create_parameter_values_table()
        self._create_parameter_descriptions_table()
        self._create_parameter_value_descriptions_table()
        self._create_images_table()
        self._create_parameters_table()

    def insert_product(
        self,
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
    ):
        """Insert product data into the products table."""
        self.conn.execute(
            """
            INSERT INTO products (product_id, code, ean, manufacturer, stock, weight, availability, availability_type, unit,
                                action_currently_yn, active_yn, archived_yn, can_add_to_basket_yn, adult_yn, set_yn, in_set_yn, exclude_from_search_yn)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(product_id) DO UPDATE
            SET code = excluded.code, ean = excluded.ean, manufacturer = excluded.manufacturer, 
                stock = excluded.stock, weight = excluded.weight, availability = excluded.availability,
                availability_type = excluded.availability_type, unit = excluded.unit,
                action_currently_yn = excluded.action_currently_yn, active_yn = excluded.active_yn,
                archived_yn = excluded.archived_yn, can_add_to_basket_yn = excluded.can_add_to_basket_yn,
                adult_yn = excluded.adult_yn, set_yn = excluded.set_yn, in_set_yn = excluded.in_set_yn,
                exclude_from_search_yn = excluded.exclude_from_search_yn
        """,
            (
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
            ),
        )
        # Debug output the count of products
        # product_count = self.conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        # logfire.debug(f"Added Product ID {product_id}\nTotal number of products: {product_count}")

    def insert_product_description(
        self,
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
    ):
        """Insert product descriptions into the descriptions table."""
        # Czech language code is 'cz' in the database
        language = language.lower()
        language = "cz" if language == "cs" else language

        seo_keywords = ", ".join(seo_keywords) if seo_keywords else ""

        try:
            self.conn.execute(
                """
                INSERT INTO descriptions (product_id, language, title, short_description, long_description, url, seo_title, seo_description, seo_url, seo_keywords, unit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
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
                ),
            )
        except duckdb.duckdb.ConstraintException as e:
            logfire.debug(
                f"❌ Failed to insert description for product {product_id}: {e}"
            )
            # import ipdb; ipdb.set_trace()

    def insert_product_price(self, product_id, currency, price_with_vat):
        """Insert price data into the prices table."""
        self.conn.execute(
            """
            INSERT INTO prices (product_id, currency, price_with_vat)
            VALUES (?, ?, ?)
        """,
            (product_id, currency, price_with_vat),
        )

    def insert_product_image(self, product_id, file_id, url, main_yn, position):
        """Insert image data into the images table."""
        self.conn.execute(
            """
            INSERT INTO images (product_id, file_id, url, main_yn, position)
            VALUES (?, ?, ?, ?, ?)
        """,
            (product_id, file_id, url, main_yn, position),
        )

    def insert_product_category(
        self, product_id, category_id, category_code, category_name, main_yn, position
    ):
        """Insert category data into the categories table, skipping duplicates."""
        try:
            # Check if the category_id already exists
            existing_category = self.conn.execute(
                """
                SELECT 1 FROM categories WHERE category_id = ? and product_id = ?
            """,
                (category_id, product_id),
            ).fetchone()
            # print (f"Existing category: {existing_category}; category_id: {category_id}; product_id: {product_id}")

            import ipdb

            ipdb.set_trace()

            # something here is wrong
            # we inserting duplicates

            if existing_category:
                logfire.debug(
                    f"⚠️ Category with ID {category_id} already exists. Skipping insert."
                )
                return
            else:
                # Insert category if it doesn't exist
                self.conn.execute(
                    """
                    INSERT INTO categories (product_id, category_id, category_code, category_name, main_yn, position)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        product_id,
                        category_id,
                        category_code,
                        category_name,
                        main_yn,
                        position,
                    ),
                )
                logfire.debug(
                    f"✅ Category with ID {category_id} inserted successfully."
                )

        except Exception as e:
            logfire.error(f"❌ Failed to insert category {category_id}: {e}")

    def insert_product_meta(self, product_id, meta_key, meta_type, meta_value):
        """Insert metadata into the metas table."""
        self.conn.execute(
            """
            INSERT INTO metas (product_id, meta_key, meta_type, meta_value)
            VALUES (?, ?, ?, ?)
        """,
            (product_id, meta_key, meta_type, meta_value),
        )

    def insert_product_vat(self, product_id, country_code, vat_percentage):
        """Insert VAT details into the vats table."""
        self.conn.execute(
            """
            INSERT INTO vats (product_id, country_code, vat_percentage)
            VALUES (?, ?, ?)
        """,
            (product_id, country_code, vat_percentage),
        )

    def insert_parameter(self, key, value):
        """Insert parameter into the parameters table."""
        self.conn.execute(
            """
            INSERT INTO parameters (key, value)
            VALUES (?, ?)
        """,
            (key, value),
        )

    def insert_parameters(self, parameters: list):
        """Insert multiple parameters into the parameters table."""
        for parameter in parameters:
            pass

    def insert_parameter_value(self, parameter_id, value):
        """Insert parameter value into the parameter_values table."""
        self.conn.execute(
            """
            INSERT INTO parameter_values (parameter_id, value)
            VALUES (?, ?)
        """,
            (parameter_id, value),
        )

    def insert_parameter_description(self, parameter_id, language, name):
        """Insert parameter description into the parameter_descriptions table."""
        self.conn.execute(
            """
            INSERT INTO parameter_descriptions (parameter_id, language, name)
            VALUES (?, ?, ?)
        """,
            (parameter_id, language, name),
        )

    def insert_parameter_value_description(self, parameter_value_id, language, value):
        """Insert parameter value description into the parameter_value_descriptions table."""
        self.conn.execute(
            """
            INSERT INTO parameter_value_descriptions (parameter_value_id, language, value)
            VALUES (?, ?, ?)
        """,
            (parameter_value_id, language, value),
        )

    def insert_image(self, url):
        """Insert image URL into the images table."""
        self.conn.execute(
            """
            INSERT INTO images (url)
            VALUES (?)
        """,
            (url,),
        )

    def get_product_fields(self):
        """Show all product fields."""
        query = "PRAGMA table_info(products)"
        results = self.conn.execute(query).fetchdf()
        fields = ", ".join(results["name"].tolist())
        return fields

    def get_product_code_by_id(self, product_id: str) -> int:
        """
        Retrieves the product_code for the given product id.
        Returns the product_code if found, otherwise returns None.
        """
        query = "SELECT code FROM products WHERE product_id = ?"
        result = self.conn.execute(query, (product_id,)).fetchone()
        return result[0] if result else None

    def get_product_id_by_code(self, code: str) -> int:
        """
        Retrieves the product_id for the given product code.
        Returns the product_id if found, otherwise returns None.
        """
        query = "SELECT product_id FROM products WHERE code = ?"
        result = self.conn.execute(query, (code,)).fetchone()
        return result[0] if result else None

    def get_product_core(self, product_id=None):
        """SQL Query to get product core details."""
        logfire.debug(f"Fetching product core details for product_id: {product_id}")
        query = """
        SELECT 
            p.product_id, 
            p.code AS code, 
            p.ean AS ean, 
            p.manufacturer AS manufacturer, 
            p.stock AS stock, 
            p.weight AS weight, 
            p.availability AS availability, 
            p.availability_type AS availability_type, 
            p.unit AS unit
        FROM products p
        """.strip()
        parameters = []
        if product_id:
            query += " WHERE p.product_id = ? "
            parameters.append(product_id)
        else:
            raise ValueError("Product ID is required.")

        result = self.conn.execute(query, parameters).fetchdf()
        return result

    def get_product_images(self, product_id=None):
        """SQL Query to get product images"""
        query = """
        SELECT 
            i.product_id,
            i.file_id as file_id,
            i.url as url,
            i.main_yn as main_yn,
            i.position as position
        FROM images i
        """
        parameters = []
        if product_id:
            query += " WHERE i.product_id = ? "
            parameters.append(product_id)

        result = self.conn.execute(query, parameters).fetchdf()
        return result

    def get_product_prices(self, product_id=None):
        """SQL Query to product prices"""
        query = """
        SELECT 
            pr.product_id,
            pr.currency as currency,
            pr.price_with_vat as price_with_vat
        FROM prices pr
        """
        parameters = []
        if product_id:
            query += " WHERE pr.product_id = ? "
            parameters.append(product_id)

        result = self.conn.execute(query, parameters).fetchdf()
        return result

    def get_product_categories(self, product_id=None):
        """SQL Query to get product categories."""
        query = """
        SELECT 
            c.product_id,
            c.category_id as category_id,
            c.category_code as category_code,
            c.category_name as category_name,
            c.main_yn as main_yn,
            c.position as position
        FROM categories c
        """
        parameters = []
        if product_id:
            query += " WHERE c.product_id = ? "
            parameters.append(product_id)

        result = self.conn.execute(query, parameters).fetchdf()

        # import ipdb; ipdb.set_trace()

        return result

    def get_product_vat(self, product_id=None):
        """SQL Query to product vat"""
        query = """
        SELECT 
            v.product_id,
            v.country_code as country_code,
            v.vat_percentage as vat_percentage
        FROM vats v
        """
        parameters = []
        if product_id:
            query += " WHERE v.product_id = ? "
            parameters.append(product_id)

        result = self.conn.execute(query, parameters).fetchdf()
        return result

    def get_product_descriptions(self, product_id=None):
        """SQL Query to get product descriptiong"""
        query = """
        SELECT 
            d.product_id,
            d.language as language,
            d.title as title,
            d.short_description as short_description,
            d.long_description as long_description,
            d.url as url,
            d.seo_keywords as seo_keywords,
            d.seo_title as seo_title,
            d.seo_description as seo_description,
            d.seo_url as seo_url,
            d.unit as unit
        FROM descriptions d
        """
        parameters = []
        if product_id:
            query += " WHERE d.product_id = ? "
            parameters.append(product_id)

        result = self.conn.execute(query, parameters).fetchdf()
        return result

    async def get_all_products(self) -> list[tuple]:
        """Show all products."""
        logfire.info("Fetching all products.")
        query = "SELECT product_id FROM products"
        pids = self.conn.execute(query).fetchall()

        if not pids:
            logfire.info("No product ids found.")
            return list()

        products = [
            (
                self.get_product_core(pid[0]),
                self.get_product_images(pid[0]),
                self.get_product_prices(pid[0]),
                self.get_product_categories(pid[0]),
                self.get_product_vat(pid[0]),
                self.get_product_descriptions(pid[0]),
            )
            for pid in pids
        ]

        logfire.info(f"Found {len(products)} products.")
        return products

    async def get_product_details(
        self, code=None, product_id=None
    ) -> pd.DataFrame | None:
        """Show all products with aggregated details from separate queries."""
        logfire.info(
            f"Fetching product details for code, product_id: {code}, {product_id}"
        )

        if (code and product_id) or (not (code or product_id)):
            raise ValueError(
                "Provide either code or product_id, never neither nor both."
            )

        if code and not product_id:
            query = "SELECT product_id FROM products WHERE code = ?"
            params = [code]
            product_id = self.conn.execute(query, params).fetchone()
            if product_id:
                product_id = product_id[0]
            else:
                logfire.debug(f"Product with code '{code}' not found.")
                return None

        core = self.get_product_core(product_id)
        images = self.get_product_images(product_id)
        prices = self.get_product_prices(product_id)
        categories = self.get_product_categories(product_id)
        vat = self.get_product_vat(product_id)
        descriptions = self.get_product_descriptions(product_id)

        combined = core.copy()

        combined["images"] = (
            images.groupby("product_id")
            .apply(lambda x: x.to_dict(orient="records"))
            .reset_index(drop=True)
        )
        combined["prices"] = (
            prices.groupby("product_id")
            .apply(lambda x: x.to_dict(orient="records"))
            .reset_index(drop=True)
        )
        combined["categories"] = (
            categories.groupby("product_id")
            .apply(lambda x: x.to_dict(orient="records"))
            .reset_index(drop=True)
        )
        combined["vat"] = (
            vat.groupby("product_id")
            .apply(lambda x: x.to_dict(orient="records"))
            .reset_index(drop=True)
        )
        combined["descriptions"] = (
            descriptions.groupby("product_id")
            .apply(lambda x: x.to_dict(orient="records"))
            .reset_index(drop=True)
        )
        return combined

    def get_customer_details(self) -> pd.DataFrame:
        """Show all customers."""
        query = "SELECT * FROM customers"
        results = self.conn.execute(query).fetchdf()
        return results

    def get_order_details(self):
        """Show all orders."""
        query = "SELECT * FROM orders"
        results = self.conn.execute(query).fetchdf()
        return results

    def update_product_translation(self, product_code: str, translations: dict):
        """
        Update the product translation fields in DuckDB for the product
        identified by its code.
        """

        try:
            query = """
                INSERT INTO descriptions (
                    product_id,
                    language,
                    title,
                    long_description,
                    short_description,
                    url,
                    seo_keywords,
                    seo_description,
                    seo_title,
                    seo_url,
                    unit
                )
                VALUES (
                    (SELECT product_id FROM products WHERE code = ?),
                    LOWER(?),
                    ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                ON CONFLICT (product_id, language) DO UPDATE SET
                    title = EXCLUDED.title,
                    long_description = EXCLUDED.long_description,
                    short_description = EXCLUDED.short_description,
                    url = EXCLUDED.url,
                    seo_keywords = EXCLUDED.seo_keywords,
                    seo_description = EXCLUDED.seo_description,
                    seo_title = EXCLUDED.seo_title,
                    seo_url = EXCLUDED.seo_url,
                    unit = EXCLUDED.unit;
            """

            self.conn.execute(
                query,
                (
                    product_code,  # for SELECT product_id
                    translations.get("target_language"),  # for LOWER(?)
                    translations.get("title"),
                    translations.get("long_description"),
                    translations.get("short_description"),
                    translations.get("url"),
                    translations.get("seo_keywords"),
                    translations.get("seo_description"),
                    translations.get("seo_title"),
                    translations.get("seo_url"),
                    translations.get("unit"),
                ),
            )
        except Exception as e:
            logfire.error(
                f"Failed to update translation for product '{product_code}' in DuckDB: \nERROR: {e}"
            )
            raise


# EOF
