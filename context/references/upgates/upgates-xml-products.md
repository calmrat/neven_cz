<div class="row gx-4 gy-6 section pt-0">
					<div class="col-lg-18 col-main col-main-left">	<article class="col-main-in text content-text">
		<!-- Search input -->
		<div class="w-100 mb-4"><div class="d-flex input-group-md position-relative frmsearchForm-wrap" role="search" aria-expanded="false">
	<div class="twitter-typeahead w-100 position-static" style="position: relative; display: inline-block;"><input type="search" name="phrase" class="form-control w-100 frmsearchForm-phrase tt-input" placeholder="Co chcete najít?" aria-label="Co chcete najít?" data-products-header="Produkty" data-categories-header="Kategorie" data-articles-header="Články" data-products-url="/search/suggest?type=products&amp;phrase=%QUERY" data-categories-url="/search/suggest?type=categories&amp;phrase=%QUERY" data-articles-url="/search/suggest?type=articles&amp;phrase=%QUERY" data-no_item="Žádná položka" data-loading="Nahrávám" data-show_all="Zobrazit všechny" autocomplete="off" spellcheck="false" dir="auto" style="position: relative; vertical-align: top;"><pre aria-hidden="true" style="position: absolute; visibility: hidden; white-space: pre; font-family: CircularXXWeb-Book, sans-serif, system-ui, -apple-system, &quot;Segoe UI&quot;, Roboto, &quot;Helvetica Neue&quot;, Arial, &quot;Noto Sans&quot;, &quot;Liberation Sans&quot;, sans-serif, &quot;Apple Color Emoji&quot;, &quot;Segoe UI Emoji&quot;, &quot;Segoe UI Symbol&quot;, &quot;Noto Color Emoji&quot;; font-size: 18px; font-style: normal; font-variant: normal; font-weight: 400; word-spacing: 0px; letter-spacing: 0px; text-indent: 0px; text-rendering: auto; text-transform: none;"></pre><div class="dropdown-menu dopdown-menu-white-sm text-start py-0 tt-menu" style="position: absolute; top: 100%; left: 0px; z-index: 100; display: none;"><div class="tt-dataset tt-dataset-articles"></div><div class="tt-dataset tt-dataset-products"></div><div class="tt-dataset tt-dataset-categories"></div></div></div>
	<button class="btn position-absolute frmsearchForm-search" style="right: 5px; font-size: 1.5rem; padding-top: .625rem; padding-bottom: .625rem;" aria-label="Vyhledat" type="submit" name="search" data-url="/search?phrase=placeholder"><i class="bi bi-search"></i></button>
</div></div>
		<!-- Img, Header, Text -->
<div class="text content-text">
	<header>
		<div class="d-flex align-items-center pb-4 border-bottom text-muted fs-6 article-detail-meta">			<div class="my-2 me-4 text-nowrap d-none d-sm-block"><time class="creation">03. 02. 2025</time></div>
			<div class="my-2 w-100 d-flex align-items-center">	<ol class="m-0 breadcrumb me-auto text-muted" itemscope="" itemtype="http://schema.org/BreadcrumbList">
				<li class="breadcrumb-item pl-1" itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a href="https://www.upgates.cz/pruvodce" class="text-muted text-decoration-underline" itemprop="item"><span itemprop="name">Nápověda</span></a><meta itemprop="position" content="2"></li>
				<li class="breadcrumb-item pl-1" itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a href="https://www.upgates.cz/propojeni-napoveda" class="text-muted text-decoration-underline" itemprop="item"><span itemprop="name">Propojení</span></a><meta itemprop="position" content="3"></li>
				<li class="breadcrumb-item pl-1" itemprop="itemListElement" itemscope="" itemtype="http://schema.org/ListItem"><a href="https://www.upgates.cz/dokumentace-xml" class="text-muted text-decoration-underline" itemprop="item"><span itemprop="name">Dokumentace XML</span></a><meta itemprop="position" content="4"></li>
	</ol>
			<div class="a-d-m-icons text-nowrap"><a href="javascript:upC.openNewWindow('https://www.facebook.com/sharer/sharer.php?u=' + document.location,'',661,338)" class="p-2" role="button"><i class="bi-facebook"></i></a>
<!--<a href="javascript:upC.openNewWindow('https://twitter.com/intent/tweet?original_referer=' + document.location + '&amp;tw_p=tweetbutton&amp;url='+ document.location,'',695,300)" class="p-2" role="button"><i class="bi-twitter"></i></a>--></div>
</div> <!-- BREADCRUMBS - components/breadcrumbs.phtml -->
		</div>		<h1 class="text-center text-sm-start h1-smaller-xs" itemprop="name">Dokumentace XML - produkty</h1>
	</header>
<!-- Internal info part -->
</div>		<!-- GRAPHICS -->
		<div class="help-text HelpSection">
			<!-- Long description -->
					<h2 id="zakladni-pravidla-scroll">Základní pravidla</h2>
<ul>
<li>XML produktů se používá pro import i export z Upgates.</li>
<li>Zde je k náhledu <a href="https://files.upgates.com/examples/products.xml" target="_blank" rel="noopener"> prázdne vzorové XML</a>.</li>
<li><strong>K testování struktury XML je možno použít naše XSD <a href="https://files.upgates.com/schema/products.xsd" target="_blank" rel="noopener">verze 1.0</a>, <a href="https://files.upgates.com/schema/products_v2.xsd" target="_blank" rel="noopener">verze 2.0</a></strong>.</li>
<li>Tagy končící na <code>_YN&gt;</code> jsou typu boolean a mohou nabývat hodnoty <em>0, 1, true, false</em>.</li>
<li>Datum je zapsané jako řeťezec znaků ve formátu YYYY-MM-DD dle <a href="https://en.wikipedia.org/wiki/ISO_8601" class="blank" target="_blank" rel="noopener">ISO 8601</a>. Y je rok, M je měsíc a D je den. Příklad: 2020-12-30.</li>
<li>Atributy <em><code>language</code></em> označující jazykovou mutaci používají kódy podle <a href="https://cs.wikipedia.org/wiki/Seznam_k%C3%B3d%C5%AF_ISO_639-1" target="_blank" class="blank" rel="noopener">ISO 639-1</a> a jsou povinné.</li>
</ul>
<h2 id="import-scroll">Import</h2>
<ul>
<li>Neuvádějte prázdné obalové tagy (např. tag <code>&lt;IMAGES&gt;</code>, pokud neobsahuje žádné obrázky).</li>
<li>V případě editace (při importu) se prázdný tag chápe jako vymazání původní hodnoty v databázi kromě všech typů cen, souvisejících produktů včetně dárků. Smazání cen v e-shopu nelze provést importem, je potřeba využít např. hromadné úpravy produktů.</li>
<li>Produkty, varianty a kategorie se při importu párují podle kódu (tag <code>&lt;CODE&gt;</code>). Pokud chcete produkty a varianty importem aktualizovat, musí být tagy <code>&lt;CODE&gt;</code> vyplněny, jinak se budou zakládat při každém importu nové produkty a varianty.</li>
<li>Všechny tagy jsou nepovinné, kromě kořenových tagů <code>&lt;PRODUCTS&gt;</code> a <code>&lt;PRODUCT&gt;</code>. Při importu nových produktů (nebo při založení další jazykové mutace produktu) je povinný tag <code>&lt;TITLE&gt;</code> (s celou nadřezenou strukturou), protože z názvu produktu se tvoří URL adresa. Tento název je potřeba zadat v aktivním jazyku e-shopu. Ve variantách jsou pak povinné parametry, opět pouze při importu nových variant. Pro aktualizaci existujících variant je potřeba zadat všechny jejich parametry nebo v nastavení importu zvolit, aby se parametry variant nezpracovávaly. Dále je všude povinný atribut <em><code>language</code></em>.</li>
<li>U produktu je potřeba v XML uvést <code>&lt;DESCRIPTION&gt;</code> pro všechny jazykové mutace. Pokud některý z jazyků nebude uveden, systém produkt v této jazykové mutaci deaktivuje. Tomu se lze vyhnout uvedením tagu <code>&lt;ACTIVE_YN&gt;</code> s hodnotou <code>1</code> u všech jazykových mutací, pro které nezasíláte data. Ale produkt má zůstat v těchto jazycích aktivní.</li>
<li>Tagy, které mohou obsahovat HTML formátování je možno zapsat buď jako převedeno do HTML entit nebo pomocí CDATA (<code>&lt;![CDATA[ ]]&gt;</code>).</li>
<li>Číselné hodnoty se uvádí nezformátované bez znaku jednotky (např. ceny, hmotnost nebo DPH). Pro zápis desetinného místa můžete použít buď desetinnou tečku nebo čárku.</li>
<li>Pokud má systém nově vytvořeným produktům automaticky přiřadit štítek novinka, pak je potřeba v nastavení importu povolit zpracování položky <strong>Štítky -&gt; Novinka (do)</strong>. To je potřeba provést i když tento štítek nenastavujete přes importní soubor.</li>
<li>Další chování importu můžete ovlivnit nastavením v administraci (<a href="/a/uprava-nastaveni-importu">viz. nápověda</a>).</li>
</ul>
<h3>Malý import</h3>
<ul>
<li>V malém importu se zpracovávají pouze následující tagy (včetně všech vnořených):
<ul>
<li><code>&lt;CODE&gt;</code></li>
<li><code>&lt;PRODUCT_ID&gt;</code></li>
<li><code>&lt;ACTIVE_YN&gt;</code></li>
<li><code>&lt;ARCHIVED_YN&gt;</code></li>
<li><code>&lt;REPLACEMENT_PRODUCT_CODE&gt;</code></li>
<li><code>&lt;CAN_ADD_TO_BASKET_YN&gt;</code></li>
<li><code>&lt;LABELS&gt;</code></li>
<li><code>&lt;AVAILABILITY&gt;</code></li>
<li><code>&lt;STOCK&gt;</code></li>
<li><code>&lt;PRICES&gt;</code></li>
<li><code>&lt;METAS&gt;</code></li>
<li>Ve variantách:
<ul>
<li><code>&lt;CODE&gt;</code></li>
<li><code>&lt;MAIN_YN&gt;</code></li>
<li><code>&lt;ACTIVE_YN&gt;</code></li>
<li><code>&lt;CAN_ADD_TO_BASKET_YN&gt;</code></li>
<li><code>&lt;LABELS&gt;</code></li>
<li><code>&lt;AVAILABILITY&gt;</code></li>
<li><code>&lt;STOCK&gt;</code></li>
<li><code>&lt;PRICES&gt;</code></li>
</ul>
</li>
</ul>
</li>
</ul>
<h2 id="export-scroll">Export</h2>
<ul>
<li>Exportují se všechny tagy s výjimkou tagů s prázdnou hodnotou. Ty mohou v exportu chybět. U některých je uvedeno, že jsou pouze pro import nebo export.</li>
<li>Export z jednoho e-shopu Upgates je možno použít pro import do jiného e-shopu Upgates.</li>
</ul>
<h3>Malý export</h3>
<ul>
<li>Do malého exportu se dávají pouze následující tagy (včetně všech vnořených):
<ul>
<li><code>&lt;CODE&gt;</code></li>
<li><code>&lt;PRODUCT_ID&gt;</code></li>
<li><code>&lt;ACTIVE_YN&gt;</code></li>
<li><code>&lt;ARCHIVED_YN&gt;</code></li>
<li><code>&lt;REPLACEMENT_PRODUCT_CODE&gt;</code></li>
<li><code>&lt;CAN_ADD_TO_BASKET_YN&gt;</code></li>
<li><code>&lt;AVAILABILITY&gt;</code></li>
<li><code>&lt;STOCK&gt;</code></li>
<li><code>&lt;PRICES&gt;</code></li>
<li>Ve variantách:
<ul>
<li><code>&lt;CODE&gt;</code></li>
<li><code>&lt;MAIN_YN&gt;</code></li>
<li><code>&lt;ACTIVE_YN&gt;</code></li>
<li><code>&lt;CAN_ADD_TO_BASKET_YN&gt;</code></li>
<li><code>&lt;AVAILABILITY&gt;</code></li>
<li><code>&lt;STOCK&gt;</code></li>
<li><code>&lt;PRICES&gt;</code></li>
</ul>
</li>
</ul>
</li>
</ul>
<h2 id="struktura-xml-scroll">Struktura XML</h2>
<ul>
<li><code>&lt;PRODUCTS&gt;</code>
<ul>
<li><em><code>version</code></em> - verze formátu XML <strong>1.0</strong></li>
<li><code>&lt;PRODUCT&gt;</code>
<ul>
<li><em><code>last_update_time</code></em> - datum poslední aktualizace produktu <strong>(pouze import)</strong> ve formátu <a href="http://php.net/manual/en/function.date.php" target="_blank" class="blank" rel="noopener">Y-m-dTH:i:s</a> (např. 2017-03-07T13:35:08). Pokud bude při importu toto datum starší než datum poslední aktualizace produktu v databázi, produkt se přeskočí.</li>
<li><code>&lt;CODE&gt;</code> - kód produktu, páruje se podle existující hodnoty v databázi, nebo vytvoří nový produkt</li>
<li><code>&lt;PRODUCT_ID&gt;</code> - interní ID produktu <strong>(pouze export)</strong></li>
<li><code>&lt;ACTIVE_YN&gt;</code> - zobrazit produkt na webu</li>
<li><code>&lt;ARCHIVED_YN&gt;</code> - archivovaný produkt</li>
<li><code>&lt;REPLACEMENT_PRODUCT_CODE&gt;</code> - kód náhradního produktu, pouze pokud je produkt archivovaný</li>
<li><code>&lt;CAN_ADD_TO_BASKET_YN&gt;</code> - lze vložit do košíku</li>
<li><code>&lt;ADULT_YN&gt;</code> - pouze pro dospělé</li>
<li><code>&lt;NEW_YN&gt;</code> <strong>(pouze verze 1.0)</strong> - zobrazení příznaku <em>Novinka</em></li>
<li><code>&lt;NEW_FROM&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, od kterého se zobrazí příznak <em>Novinka</em></li>
<li><code>&lt;NEW_TO&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, do kterého je zobrazen příznak <em>Novinka</em></li>
<li><code>&lt;SPECIAL_YN&gt;</code> <strong>(pouze verze 1.0)</strong> - zobrazení příznaku <em>Akce</em></li>
<li><code>&lt;SPECIAL_FROM&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, od kterého se zobrazí příznak <em>Akce</em></li>
<li><code>&lt;SPECIAL_TO&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, do kterého je zobrazen příznak <em>Akce</em></li>
<li><code>&lt;SELLOUT_YN&gt;</code> <strong>(pouze verze 1.0)</strong> - zobrazení příznaku <em>Výprodej</em></li>
<li><code>&lt;SELLOUT_FROM&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, od kterého se zobrazí příznak <em>Výprodej</em></li>
<li><code>&lt;SELLOUT_TO&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, do kterého je zobrazen příznak <em>Výprodej</em></li>
<li><code>&lt;LABELS&gt;</code> - štítky
<ul>
<li><code>&lt;LABEL&gt;</code>
<ul>
<li><code>&lt;NAME&gt;</code> - název štítku, páruje se podle existující hodnoty v databázi, nebo vytvoří novou</li>
<li><code>&lt;ACTIVE_YN&gt;</code> - aktivní</li>
<li><code>&lt;ACTIVE_FROM&gt;</code> - datum, od kterého bude štítek aktivní</li>
<li><code>&lt;ACTIVE_TO&gt;</code> - datum, do kterého bude štítek aktivní</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;DESCRIPTIONS&gt;</code> - texty
<ul>
<li><code>&lt;DESCRIPTION&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
<li><code>&lt;ACTIVE_YN&gt;</code> - aktivní v jazykové mutaci, pokud se neuvede tak se bere jako aktivní. Použitelné pouze pro deaktivaci jazykové mutace (skrytí produktu v jazykove mutaci)</li>
<li><code>&lt;URL&gt;</code> - URL produktu</li>
<li><code>&lt;TITLE&gt;</code> - název (POVINNÝ v případě vytváření nového produktu). Pokud není definovaný, nezaloží se ani jazyková mutace produktu (související data se přeskočí)</li>
<li><code>&lt;SHORT_DESCRIPTION&gt;</code> - krátký popis, bez HTML formátování</li>
<li><code>&lt;LONG_DESCRIPTION&gt;</code> - dlouhý popis, může obsahovat formátování pouze pomocí HTML značek</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;SEO_OPTIMALIZATION&gt;</code> - SEO
<ul>
<li><code>&lt;SEO&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
<li><code>&lt;SEO_URL&gt;</code> - vlastní koncovka URL adresy</li>
<li><code>&lt;SEO_TITLE&gt;</code> - SEO titulek produktu</li>
<li><code>&lt;SEO_META_DESCRIPTION&gt;</code> - META popisek stránky produktu</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;MANUFACTURER&gt;</code> - název výrobce, páruje se podle existující hodnoty v databázi, nebo vytvoří novou</li>
<li><code>&lt;MANUFACTURER_IMAGE_URL&gt;</code> - URL na obrázek výrobce <strong>(pouze import)</strong></li>
<li><code>&lt;MANUFACTURER_DESCRIPTIONS&gt;</code> - popisy výrobce <strong>(pouze import)</strong>
<ul>
<li><code>&lt;DESCRIPTION&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;SUPPLIER_CODE&gt;</code> - kód dodavatele</li>
<li><code>&lt;EAN&gt;</code> - čárkový kód</li>
<li><code>&lt;AVAILABILITY&gt;</code> - název dostupnosti, páruje se podle existující hodnoty v databázi, nebo vytvoří novou. Neimportuje se u položek s nastavením <a href="/a/nastaveni-dostupnosti-dle-stavu-zasob" target="_blank" rel="noopener">dostupnosti dle stavu zásob</a>. Pokud však v tomto případě stav zásob není definován (tag <code>&lt;STOCK&gt;</code> musí být prázdný nebo úplně chybět), dostupnost se importuje</li>
<li><code>&lt;STOCK&gt;</code> - počet jednotek na skladě</li>
<li><code>&lt;STOCK_POSITION&gt;</code> - pozice na skladě</li>
<li><code>&lt;LIMIT_ORDERS&gt;</code> - Omezení objednání
<ul>
<li><em>1</em> - Omezení je zapnuté</li>
<li><em>0</em> - Omezení je vypnuté</li>
<li><em>sale </em>- Když je produkt ve výprodeji</li>
<li>*Pokud je pole prázdné dědí hodnotu z nastavení e-shopu</li>
</ul>
</li>
<li><code>&lt;WEIGHT&gt;</code> - hmotnost v gramech</li>
<li><code>&lt;UNIT&gt;</code> - název měrné jednotky, páruje se podle stejné hodnoty, nebo založí novou</li>
<li><code>&lt;SHIPMENT_GROUP&gt;</code> - skupina doprav, páruje se podle stejné hodnoty, nebo založí novou</li>
<li><code>&lt;VATS&gt;</code> - DPH
<ul>
<li><code>&lt;VAT&gt;</code> - páruje se podle existující hodnoty v databázi, nebo vytvoří novou. Pokud není vyplněno bere se výchozí DPH
<ul>
<li><em><code>country</code></em> - země</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;LENGTH&gt;</code> - množtví
<ul>
<li><code>&lt;ACTIVE_YN&gt;</code> - aktivní</li>
<li><code>&lt;LABELS&gt;</code> - popisky
<ul>
<li><code>&lt;LABEL&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;LENGTH_FROM&gt;</code> - minimální množství</li>
<li><code>&lt;LENGTH_TO&gt;</code> - maximální množství</li>
<li><code>&lt;UNIT&gt;</code> - název měrné jednotky, páruje se podle stejné hodnoty, nebo založí novou</li>
<li><code>&lt;STEPS_TYPE&gt;</code> - typ krokování metráže, možné hodnoty:
<ul>
<li><em>neither</em> - žádné krokování, výchozí</li>
<li><em>multiples</em> - násobky</li>
<li><em>select</em> - výběr z možností</li>
</ul>
</li>
<li><code>&lt;STEPS&gt;</code> - hodnota podle typu krokování:
<ul>
<li><em>neither</em> - může být prázdné</li>
<li><em>multiples</em> - hodnota násobku</li>
<li><em>select</em> - každá hodnota na nový řádek</li>
</ul>
</li>
<li><code>&lt;NOTE&gt;</code> - poznámka</li>
</ul>
</li>
<li><code>&lt;PRIVATE_YN&gt;</code> - zobrazit produkt pouze přihlášeným uživatelům</li>
<li><code>&lt;PRIVATE_CUSTOMERS_ONLY_YN&gt;</code> - zobrazit pouze uživatelům, kteří mohou vidět skryté stránky</li>
<li><code>&lt;EXCLUDE_FROM_SEARCH_YN&gt;</code> - vyřazeno z vyhledávání <strong>(pouze export verze 2.0)</strong></li>
<li><code>&lt;GROUPS&gt;</code> - skupiny zákazníků
<ul>
<li><code>&lt;GROUP&gt;</code> - název skupiny</li>
</ul>
</li>
<li><code>&lt;CATEGORIES&gt;</code> - kategorie
<ul>
<li><code>&lt;CATEGORY&gt;</code>
<ul>
<li><code>&lt;CODE&gt;</code> - kód kategorie, do které bude produkt zařazen. V případě, že se vyskytne více stejných kódů kategorie v jednom produktu, zpracuje se první v pořadí. Páruje se podle existujícího kódu kategorie</li>
<li><code>&lt;NAME&gt;</code> - název kategorie, do které je produkt zařazen (export)</li>
<li><code>&lt;PRIMARY_YN&gt;</code> - informace, zda je kategorie primární. V případě, že se vyskytne více primárních kategorií v jednom produktu, bere se první v pořadí</li>
<li><code>&lt;POSITION&gt;</code> - pozice produktu v kategorii</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;PRICES_FORMULAS&gt;</code> - cenové vzorce
<ul>
<li><code>&lt;NAME&gt;</code> - název vzorce, páruje se podle existující hodnoty v databázi, vzorec musí být vytvořen</li>
</ul>
</li>
<li><code>&lt;RECYCLING_FEE&gt;</code> <strong>(pouze verze 2.0)</strong> - recyklační poplatek
<ul>
<li><code>&lt;NAME&gt;</code> - interní název, páruje se podle existující hodnoty v databázi</li>
<li><code>&lt;VALUE&gt;</code> - hodnota poplatku pro jazykovou mutaci
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;PRICES&gt;</code> - ceny
<ul>
<li><code>&lt;PRICE&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
<li><code>&lt;PRICELISTS&gt;</code> - ceníky
<ul>
<li><code>&lt;PRICELIST&gt;</code>
<ul>
<li><code>&lt;NAME&gt;</code> - název ceníku, pokud je při importu prázdné, chápe se jako výchozí ceník</li>
<li><code>&lt;PRICE_ORIGINAL&gt;</code> - základní ceníková cena, od které se odvozují další (cena před slevou) <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;PRODUCT_DISCOUNT&gt;</code> - sleva na produkt v procentech <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;PRODUCT_DISCOUNT_REAL&gt;</code> - reálná sleva na produkt použitá pro výpočet výsledné ceny <strong>(pouze export, neexportuje se do odběratelského feedu)</strong>, vypočítává se takto:
<ul>
<li>hodnota slevy na produkt (<code>&lt;PRODUCT_DISCOUNT&gt;</code>) + sleva na výrobce + sleva na kategorii (bere se sleva z hlavní kategorie ve které je produkt zařazen). Výsledná hodnota slevy se omezí na hodnotu z nastavení <em>Maximální procento slevy</em>.</li>
</ul>
</li>
<li><code>&lt;PRICE_SALE&gt;</code> - akční cena, exportuje se pouze tehdy, pokud je produkt v akci (štítek akce) <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;PRICE_WITH_VAT&gt;</code> - výsledná cena po slevách s DPH <strong>(pouze export, exportuje se pouze do odběratelského feedu)</strong></li>
<li><code>&lt;PRICE_WITHOUT_VAT&gt;</code> - výsledná cena po slevách bez DPH <strong>(pouze export, exportuje se pouze do odběratelského feedu)</strong></li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;PRICE_PURCHASE&gt;</code> - nákupní cena, interní údaj pro orientaci administrátora <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;PRICE_COMMON&gt;</code> - běžná cena, pro orientaci při nákupu. Může to být např. cena v kamenných obchodech <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;CURRENCY&gt;</code> - měna <strong>(pouze export)</strong></li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;IMAGES&gt;</code> - obrázky
<ul>
<li><code>&lt;IMAGE&gt;</code>
<ul>
<li><code>&lt;URL&gt;</code> - URL adresa obrázku</li>
<li><code>&lt;TITLES&gt;</code> - popisky obrázku
<ul>
<li><code>&lt;TITLE&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;MAIN_YN&gt;</code> - obrázek je hlavní, v případě, že se vyskytne více hlavních obrázků v jednom produktu, zpracovává se první v pořadí</li>
<li><code>&lt;LIST_YN&gt;</code> - obrázek je seznamový, v případě, že se vyskytne více seznamových obrázků v jednom produktu, zpracovává se první v pořadí</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;FILES&gt;</code> - soubory
<ul>
<li><code>&lt;FILE&gt;</code>
<ul>
<li><code>&lt;URL&gt;</code> - URL adresa souboru</li>
<li><code>&lt;TITLES&gt;</code> - popisky souboru
<ul>
<li><code>&lt;TITLE&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;BENEFITS&gt;</code> - benefity
<ul>
<li><code>&lt;BENEFIT&gt;</code>
<ul>
<li><code>&lt;NAME&gt;</code> - název benefitu, páruje se podle existující hodnoty v databázi (v hlavním jazyku), nebo vytvoří novou</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;PARAMETERS&gt;</code> - parametry
<ul>
<li><code>&lt;PARAMETER&gt;</code>
<ul>
<li><code>&lt;NAME&gt;</code> - název parametru, páruje se podle existující hodnoty v databázi, nebo vytvoří novou
<ul>
<li><em><code>language</code></em> <strong>(pouze verze 2.0)</strong> - specifikace jazykové mutace</li>
</ul>
</li>
<li><code>&lt;VALUE&gt;</code> - hodnota parametru, v případě, že se vyskytne více stejných hodnot parametru v jednom produktu, zpracovává se první v pořadí. Páruje se podle existující hodnoty v databázi, nebo vytvoří novou
<ul>
<li><em><code>language</code></em> <strong>(pouze verze 2.0)</strong> - specifikace jazykové mutace</li>
</ul>
</li>
<li><code>&lt;IMAGE_URL&gt;</code> - URL obrázku. V případě že bude uveden, nastaví se parametr jako obrázkový</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;CONFIGURATIONS&gt;</code> - konfigurace
<ul>
<li><code>&lt;CONFIGURATION&gt;</code>
<ul>
<li><em><code>type</code></em> - typ konfigurace:
<ul>
<li><em>one_value</em> - možno vybrat pouze jednu hodnotu (select)</li>
<li><em>more_values</em> - možno vybrat více hodnot (checkboxy)</li>
<li><em>group</em> - skupina konfigurací, v tagu <code>&lt;NAME&gt;</code> musí být název skupiny který je uveden v administraci. Pokud je typ konfigurace <em>group</em> neuvádí se hodnota <code>&lt;VALUE&gt;</code></li>
<li><em>text</em> - jako hodnota je použito textové pole (textarea), nemá hodnotu <code>&lt;VALUE&gt;</code></li>
<li><em>separator</em> - oddělovač, nemá hodnotu <code>&lt;VALUE&gt;</code></li>
</ul>
</li>
<li><code>&lt;NAME&gt;</code> - název parametru konfigurace, páruje se podle existující hodnoty v databázi, nebo vytvoří novou (neplatí pokud je typ konfigurace <em>group</em>)
<ul>
<li><em><code>language</code></em> <strong>(pouze verze 2.0)</strong> - specifikace jazykové mutace</li>
</ul>
</li>
<li><code>&lt;VALUE&gt;</code> - hodnota parametru konfigurace, páruje se podle existující hodnoty v databázi, nebo vytvoří novou (může být uvedeno vícekrát)
<ul>
<li><code>&lt;NAME&gt;</code> - název hodnoty
<ul>
<li><em><code>language</code></em> <strong>(pouze verze 2.0)</strong> - specifikace jazykové mutace</li>
</ul>
</li>
<li><code>&lt;IMAGE_URL&gt;</code> - URL obrázku. V případě, že bude uveden, nastaví se parametr jako obrázkový</li>
<li><code>&lt;DEFAULT_YN&gt;</code> - výchozí hodnota parametru konfigurace</li>
<li><code>&lt;PRICE&gt;</code> - cena (nepovinné)
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
<li><em><code>operation</code></em> - operace, která se provede s cenou poduktu při vybrání hodnoty. Povolené hodnoty jsou:
<ul>
<li><em>+</em> sčítání (výchozí)</li>
<li><em>-</em> odčítání</li>
<li><em>*</em> násobení</li>
<li><em>/</em> dělení</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;VARIANTS&gt;</code> - varianty
<ul>
<li><code>&lt;VARIANT</code>
<ul>
<li><code>&lt;CODE&gt;</code> - kód varianty, páruje se podle existující hodnoty v databázi, nebo vytvoří novou</li>
<li><code>&lt;VARIANT_ID&gt;</code> - interní ID varianty <strong>(pouze export)</strong></li>
<li><code>&lt;MAIN_YN&gt;</code> - hlavní varianta. V případě, že se vyskytne více hlavních variant v jednom produktu, bere se první v pořadí</li>
<li><code>&lt;ACTIVE_YN&gt;</code> - zobrazit variantu na webu</li>
<li><code>&lt;CAN_ADD_TO_BASKET_YN&gt;</code> - lze vložit do košíku</li>
<li><code>&lt;SUPPLIER_CODE&gt;</code> - kód dodavatele</li>
<li><code>&lt;EAN&gt;</code> - čárkový kód</li>
<li><code>&lt;NEW_YN&gt;</code> <strong>(pouze verze 1.0)</strong> - zobrazení příznaku <em>Novinka</em></li>
<li><code>&lt;NEW_FROM&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, od kterého se zobrazí příznak <em>Novinka</em></li>
<li><code>&lt;NEW_TO&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, do kterého je zobrazen příznak <em>Novinka</em></li>
<li><code>&lt;SPECIAL_YN&gt;</code> <strong>(pouze verze 1.0)</strong> - zobrazení příznaku <em>Akce</em></li>
<li><code>&lt;SPECIAL_FROM&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, od kterého se zobrazí příznak <em>Akce</em></li>
<li><code>&lt;SPECIAL_TO&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, do kterého je zobrazen příznak <em>Akce</em></li>
<li><code>&lt;SELLOUT_YN&gt;</code> <strong>(pouze verze 1.0)</strong> - zobrazení příznaku <em>Výprodej</em></li>
<li><code>&lt;SELLOUT_FROM&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, od kterého se zobrazí příznak <em>Výprodej</em></li>
<li><code>&lt;SELLOUT_TO&gt;</code> <strong>(pouze verze 1.0)</strong> - datum, do kterého je zobrazen příznak <em>Výprodej</em></li>
<li><code>&lt;LABELS&gt;</code> - štítky variant
<ul>
<li><code>&lt;LABEL&gt;</code>
<ul>
<li><code>&lt;NAME&gt;</code> - název štítku. Páruje se podle existující hodnoty v databázi, nebo vytvoří novou.</li>
<li><code>&lt;ACTIVE_YN&gt;</code> - aktivní</li>
<li><code>&lt;ACTIVE_FROM&gt;</code> - datum od kterého bude štítek aktivní</li>
<li><code>&lt;ACTIVE_TO&gt;</code> - datum do kterého bude štítek aktivní</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;AVAILABILITY_NOTES&gt;</code> - poznámky k dostupnosti
<ul>
<li><code>&lt;AVAILABILITY_NOTE&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;AVAILABILITY&gt;</code> - název dostupnosti, páruje se podle existující hodnoty v databázi, nebo vytvoří novou. Neimportuje se u položek s nastavením <a href="/a/nastaveni-dostupnosti-dle-stavu-zasob" target="_blank" rel="noopener">dostupnosti dle stavu zásob</a>. Pokud však v tomto případě stav zásob není definován (tag <code>&lt;STOCK&gt;</code> musí být prázdný nebo úplně chybět), dostupnost se importuje</li>
<li><code>&lt;STOCK&gt;</code> - počet jednotek na skladě</li>
<li><code>&lt;STOCK_POSITION&gt;</code> - pozice na skladě</li>
<li><code>&lt;WEIGHT&gt;</code> - hmotnost v gramech (pro výběr dopravy)</li>
<li><code>&lt;IMAGE_URL&gt;</code> - URL adresa obrázku</li>
<li><code>&lt;PARAMETERS&gt;</code> - parametry variant
<ul>
<li><code>&lt;PARAMETER&gt;</code>
<ul>
<li><code>&lt;NAME&gt;</code> - název parametru. V případě, že se vyskytne více stejných názvů parametru v jednom produktu, bere se první v pořadí. Páruje se podle existující hodnoty v databázi, nebo vytvoří novou
<ul>
<li><em><code>language</code></em> <strong>(pouze verze 2.0)</strong> - specifikace jazykové mutace</li>
</ul>
</li>
<li><code>&lt;VALUE&gt;</code> - hodnota parametru. V případě, že se vyskytne více stejných hodnot parametru v jednom produktu, zpracovává se první v pořadí. Páruje se podle existující hodnoty v databázi, nebo vytvoří novou
<ul>
<li><em><code>language</code></em> <strong>(pouze verze 2.0)</strong> - specifikace jazykové mutace</li>
</ul>
</li>
<li><code>&lt;IMAGE_URL&gt;</code> - URL obrázku. V případě, že bude uveden, nastaví se parametr jako obrázkový</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;PRICES&gt;</code> - ceny
<ul>
<li><code>&lt;PRICE&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
<li><code>&lt;PRICELISTS&gt;</code> - ceníky
<ul>
<li><code>&lt;PRICELIST&gt;</code>
<ul>
<li><code>&lt;NAME&gt;</code> - název ceníku. Pokud je při importu prázdné, chápe se jako výchozí ceník</li>
<li><code>&lt;PRICE_ORIGINAL&gt;</code> - základní ceníková cena, od které se odvozují další (cena před slevou) <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;PRODUCT_DISCOUNT&gt;</code> - sleva na variantu v procentech <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;PRODUCT_DISCOUNT_REAL&gt;</code> - reálná sleva na variantu použitá pro výpočet výsledné ceny <strong>(pouze export, neexportuje se do odběratelského feedu)</strong>, vypočítává se takto:
<ul>
<li>hodnota slevy na variantu (<code>&lt;PRODUCT_DISCOUNT&gt;</code>) + sleva na výrobce + sleva na kategorii (bere se sleva z hlavní kategorie ve které je produkt zařazen). Výsledná hodnota slevy se omezí na hodnotu z nastavení <em>Maximální procento slevy</em>.</li>
</ul>
</li>
<li><code>&lt;PRICE_SALE&gt;</code> - akční cena. Exportuje se pouze tehdy, pokud je varianta v akci (štítek akce) <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;PRICE_WITH_VAT&gt;</code> - výsledná cena po slevách s DPH <strong>(pouze export, exportuje se pouze do odběratelského feedu)</strong></li>
<li><code>&lt;PRICE_WITHOUT_VAT&gt;</code> - výsledná cena po slevách bez DPH <strong>(pouze export, exportuje se pouze do odběratelského feedu)</strong></li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;PRICE_PURCHASE&gt;</code> - nákupní cena, interní údaj pro orientaci administrátora <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;PRICE_COMMON&gt;</code> - běžná cena, pro orientaci při nákupu. Může to být např. cena v kamenných obchodech <strong>(neexportuje se do odběratelského feedu)</strong></li>
<li><code>&lt;CURRENCY&gt;</code> - měna <strong>(pouze export)</strong></li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;METAS&gt;</code> - vlastní pole variant
<ul>
<li><code>&lt;META&gt;</code>
<ul>
<li><em><code>type</code></em> - typ vlastního pole, možné hodnoty:
<ul>
<li><em>radio</em> - přepínač</li>
<li><em>checkbox</em> - zaškrtávací políčko</li>
<li><em>input</em> - textové pole</li>
<li><em>date</em> - datum</li>
<li><em>email</em> - email</li>
<li><em>number</em> - číslo</li>
<li><em>select</em> - rozbalovací nabídka</li>
<li><em>multiselect</em> - multi rozbalovací nabídka</li>
<li><em>textarea</em> - víceřádkové textové pole</li>
<li><em>formatted</em> - víceřádkové textové pole formátované (WYSIWYG)</li>
</ul>
</li>
<li><code>&lt;META_KEY&gt;</code> - Klíč vlastního pole - povolené znaky jsou malá písmena, čísla (nesmí být na první pozici) a podtržítko</li>
<li><code>&lt;META_VALUE&gt;</code> - hodnota vlastního pole. Uvádí se, pokud je stejná pro všechny jazykové mutace</li>
<li><code>&lt;META_VALUES&gt;</code> - hodnoty vlastního pole pro jednotlivé jazykové mutace
<ul>
<li><code>&lt;META_VALUE&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;RELATED_PRODUCTS&gt;</code> - související produkty
<ul>
<li><code>&lt;CODE&gt;</code> - kód souvisejícího produktu, páruje se podle existující hodnoty v databázi</li>
</ul>
</li>
<li><code>&lt;ALTERNATIVE_PRODUCTS&gt;</code> - alternativní produkty
<ul>
<li><code>&lt;CODE&gt;</code> - kód alternativního produktu, páruje se podle existující hodnoty v databázi</li>
</ul>
</li>
<li><code>&lt;ACCESSORIES&gt;</code> - příslušenství
<ul>
<li><code>&lt;CODE&gt;</code> - kód produktu příslušenství, páruje se podle existující hodnoty v databázi</li>
</ul>
</li>
<li><code>&lt;GIFTS&gt;</code> - dárky
<ul>
<li><code>&lt;CODE&gt;</code> - kód varianty nebo produktu dárku, páruje se podle existující hodnoty v databázi. Pokud&nbsp;je vyplněna vymyšlená hodnota, dárky&nbsp;se od daného produktu&nbsp; promažou.
<ul>
<li><em><code>type</code></em> - typ varianty
<ul>
<li><em>highest_stock_variant</em> - varianta s nejvyšším skladem (při importu, pokud atribut chybí je toto výchozí hodnota)</li>
<li><em>random_stock_variant</em> - náhodná varianta</li>
<li><em>variant</em> - vybraná varianta</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;SETS&gt;</code> - sada
<ul>
<li><code>&lt;CODE&gt;</code> - kód varianty nebo produktu, páruje se podle existující hodnoty v databázi
<ul>
<li><em><code>quantity</code></em> - počet jednotek produktu v sadě (při importu. Pokud atribut chybí, je výchozí hodnota 1)</li>
</ul>
</li>
</ul>
</li>
<li><code>&lt;METAS&gt;</code> - vlastní pole
<ul>
<li><code>&lt;META</code>
<ul>
<li><em><code>type</code></em> - typ vlastního pole, možné hodnoty:
<ul>
<li><em>radio</em> - přepínač</li>
<li><em>checkbox</em> - zaškrtávací políčko</li>
<li><em>input</em> - textové pole</li>
<li><em>date</em> - datum</li>
<li><em>email</em> - email</li>
<li><em>number</em> - číslo</li>
<li><em>select</em> - rozbalovací nabídka</li>
<li><em>multiselect</em> - multi rozbalovací nabídka</li>
<li><em>textarea</em> - víceřádkové textové pole</li>
<li><em>formatted</em> - víceřádkové textové pole formátované (WYSIWYG)</li>
</ul>
</li>
<li><code>&lt;META_KEY&gt;</code> - klíč vlastního pole - povolené znaky jsou malá písmena, čísla (nesmí být na první pozici) a podtržítko</li>
<li><code>&lt;META_VALUE&gt;</code> - hodnota vlastního pole. Uvádí se, pokud je stejná pro všechny jazykové mutace</li>
<li><code>&lt;META_VALUES&gt;</code> - hodnoty vlastního pole pro jednotlivé jazykové mutace
<ul>
<li><code>&lt;META_VALUE&gt;</code>
<ul>
<li><em><code>language</code></em> - specifikace jazykové mutace</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
		<aside class="list-group list-group-flush list-group-sm">
			<h2 class="w-100 border-top ms-0 first" id="dalsi-clanky-v-teto-kategorii-scroll">Další články v této kategorii</h2>
		<div class="SNIcontainer" data-next-items="10">
	<a href="/a/dokumentace-xml-objednavek" class="list-group-item SNIitem">
	Dokumentace XML - objednávky
</a>	<a href="/a/dokumentace-xml-kategorii" class="list-group-item SNIitem">
	Dokumentace XML - kategorie
</a>	<a href="/a/dokumentace-xml-zakazniku" class="list-group-item SNIitem">
	Dokumentace XML - zákazníci
</a>	<a href="/a/dokumentace-xml-produktu" class="list-group-item active SNIitem">
	Dokumentace XML - produkty
</a>	<a href="/a/dokumentace-xml-textu" class="list-group-item SNIitem">
	Dokumentace XML - články a aktuality
</a>					</div>
	</aside>
		</div>
		<!-- Old text -->
	</article>
</div>
					<div class="col-lg-6 col-sider-right"><div class="position-sticky col-sider-in">		<div class="list-group list-group-flush list-group-sm HelpColumnList">
			<header class="fw-bold list-group-item pt-0">Na této stránce</header>
			<div id="H2Menu"><a class="list-group-item" href="#zakladni-pravidla-scroll">Základní pravidla</a><a class="list-group-item active" href="#import-scroll">Import</a><a class="list-group-item" href="#export-scroll">Export</a><a class="list-group-item" href="#struktura-xml-scroll">Struktura XML</a><a class="list-group-item" href="#dalsi-clanky-v-teto-kategorii-scroll">Další články v této kategorii</a></div>
					</div>
</div></div>
				</div>