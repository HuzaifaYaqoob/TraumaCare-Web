

import xml.etree.cElementTree as ET
from datetime import datetime
from xml.dom import minidom

from Product.models import Product, ProductStock
from Doctor.models import Doctor, DoctorWithHospital
from Hospital.models import Hospital
from django.conf import settings
from Trauma.models import Speciality, Disease

import os


siteMapBaseUrl = 'static/assets/sitemaps'

def registerProductsSiteMaps():
    if not os.path.exists(f'{siteMapBaseUrl}/products'):
        os.makedirs(f'{siteMapBaseUrl}/products')
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
    with open(f'{siteMapBaseUrl}/products/products_sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

def registerDoctorsSiteMaps():
    if not os.path.exists(f'{siteMapBaseUrl}/doctors'):
        os.makedirs(f'{siteMapBaseUrl}/doctors')
    root = ET.Element('urlset')
    root.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
    root.attrib['xsi:schemaLocation']="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    root.attrib['xmlns']="http://www.sitemaps.org/schemas/sitemap/0.9"

    doctors = Doctor.objects.filter(is_deleted = False, is_active = True, is_blocked = False)

    dt = datetime.now().strftime ("%Y-%m-%dT%H:%M:%S+00:00")
    for doct in doctors:
        doct_hospitsl = DoctorWithHospital.objects.filter(doctor = doct, is_active = True, is_deleted = False)
        for hosp in doct_hospitsl:

            doct_elmt = ET.SubElement(root, "url")
            docotr_url = f'{settings.THIS_APPLICATION_URL}/doctor/profile/view/{doct.slug}/?name=Dr. {doct.name}hospital={hosp.hospital.name}&hospital_location={hosp.location.name}'

            ET.SubElement(doct_elmt, "loc").text =  docotr_url
            ET.SubElement(doct_elmt, "lastmod").text = dt
            ET.SubElement(doct_elmt, "changefreq").text = "daily"
            ET.SubElement(doct_elmt, "priority").text = "1.0"

            print(docotr_url)

    # Convert the XML tree to a string
    xml_string = ET.tostring(root, encoding='utf-8', method='xml')

    # Prettify the XML string using minidom
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")

    # Write the prettified XML to the file
    with open(f'{siteMapBaseUrl}/doctors/doctors_sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

def registerSearchPageDoctorsSiteMaps():
    if not os.path.exists(f'{siteMapBaseUrl}/doctors'):
        os.makedirs(f'{siteMapBaseUrl}/doctors')
    root = ET.Element('urlset')
    root.attrib['xmlns:xsi']="http://www.w3.org/2001/XMLSchema-instance"
    root.attrib['xsi:schemaLocation']="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    root.attrib['xmlns']="http://www.sitemaps.org/schemas/sitemap/0.9"

    search_queries = []
    search_queries.extend([f'speciality={speciality.slug}&availableDoctors={speciality.speciality_doctorspecialities.all().count()}&title=Best {speciality.name} available Doctors in Lahore' for speciality in Speciality.objects.filter(is_deleted = False, is_active = True).exclude(name='')])
    search_queries.extend([f'disease={disease.slug}&availableDoctors={disease.disease_doctor_disease_specialities.all().count()}&title=Best {disease.name} available Doctors in Lahore' for disease in Disease.objects.filter(is_deleted = False, is_active = True).exclude(name='')])
    search_queries.extend([f'hospital={hospital.slug}&availableDoctors={hospital.hospital_timeslots.all().count()}&name={hospital.name}' for hospital in Hospital.objects.filter(is_deleted = False, is_active = True).exclude(name='')])
    print(search_queries)

    dt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    for query in search_queries:
        sp_url = f'{settings.THIS_APPLICATION_URL}/search/?{query}'
        print(sp_url)
        doct_elmt = ET.SubElement(root, "url")
        ET.SubElement(doct_elmt, "loc").text =  sp_url
        ET.SubElement(doct_elmt, "lastmod").text = dt
        ET.SubElement(doct_elmt, "changefreq").text = "daily"
        ET.SubElement(doct_elmt, "priority").text = "1.0"

    xml_string = ET.tostring(root, encoding='utf-8', method='xml')
    pretty_xml = minidom.parseString(xml_string).toprettyxml(indent="  ")
    with open(f'{siteMapBaseUrl}/doctors/doctors_searchpage_sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(pretty_xml)