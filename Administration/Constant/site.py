


def get_site_settings():
    from Administration.models import SiteSetting

    site_setting = SiteSetting.objects.first()

    return {
        'PHARMACY_PLATFORM_FEE' : site_setting.pharmacy_platform_fee,
        'APPOINTMENT_PLATFORM_FEE' : site_setting.appointment_platform_fee
    }