

import xml.etree.cElementTree as ET
from datetime import datetime
from xml.dom import minidom

from Product.models import Product, ProductStock
from django.conf import settings
import os

def registerProductsSiteMaps():
    if not os.path.exists('static/assets/sitemaps/products'):
        os.makedirs('static/assets/sitemaps/products')
    root = ET.Element('urlset')
    root.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
    root.attrib['xsi:schemaLocation']="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    root.attrib['xmlns']="http://www.sitemaps.org/schemas/sitemap/0.9"

    products = Product.objects.filter(is_deleted = False, is_active = True, is_blocked = False)

    dt = datetime.now().strftime ("%Y-%m-%dT%H:%M:%S+00:00")
    for product in products:
        p_location = ProductStock.custom_objects.filter(product = product, is_active = True, is_deleted = False).first()
        if not p_location:
            continue

        store_name = product.store.name

        product_elmt = ET.SubElement(root, "url")
        product_url = f'{settings.THIS_APPLICATION_URL}/product/view/{product.slug}/?selected_location={p_location.location.id}&available_on={store_name}&price={round(p_location.final_price, 2)} PKR'

        ET.SubElement(product_elmt, "loc").text =  product_url
        ET.SubElement(product_elmt, "lastmod").text = dt
        ET.SubElement(product_elmt, "changefreq").text = "daily"
        ET.SubElement(product_elmt, "priority").text = "1.0"

        print(product_url)

    # Convert the XML tree to a string
    xml_string = ET.tostring(root, encoding='utf-8', method='xml')

    # Prettify the XML string using minidom
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

    # Write the prettified XML to the file
    with open('static/assets/sitemaps/products/products_sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(pretty_xml)