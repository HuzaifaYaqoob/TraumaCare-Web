
def getUserImage(user, *args, **kwargs):
    return user.profile_image if user.profile_image else 'https://ionicframework.com/docs/img/demos/avatar.svg'


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Trauma AI Care",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Trauma AI Care",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Trauma AI Care",

    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "assets/Images/small_logo.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle img-responsive",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the TraumaAICare",

    # Copyright on the footer
    "copyright": "TraumaAICare PVT-LTD",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    "search_model": [
        "Authentication.User", 
        # "auth.Group",
        "Doctor.Doctor",
    ],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": getUserImage,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": []},
        {"name": "Users",  "url": "/admin/Authentication/user/", "permissions": ["Authentication.view_user"]},
        {"name": "Hospitals",  "url": "/admin/Hospital/hospital/", "permissions": ["Hospital.view_hospital"]},
        {"name": "Doctors",  "url": "/admin/Doctor/doctor/", "permissions": ["Doctor.view_doctor"]},
        {"name": "Appointments",  "url": "/admin/Appointment/appointment/", "permissions": ["Appointment.view_appointment"]},
        {"name": "Products",  "url": "/admin/Product/product/", "permissions": ["Doctor.view_product"]},
        {"name": "Tasks",  "url": "/admin/Task/task/", "permissions": ["Task.view_task"]},
        {"name": "Organization",  "url": "/admin/organization/", "permissions": []},

        # external url that opens in a new window (Permissions can be added)
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "authentication.user"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        # {"app": "Authentication"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        {"model": "Authentication.User"}
    ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": False,

    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "authentication", 
        "authentication.role", 
        "authentication.user", 
        "authentication.staffrole", 
        "hospital", 
        "doctor", 
        "doctor.doctor", 
        "doctor.doctorwithhospital", 
        "doctor.doctoronlineavailability", 
        "doctor.DoctorTimeSlots", 
        'appointment', 
        'task'
    ],

    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "books": [{
    #         "name": "Hello", 
    #         "url": "make_messages", 
    #         "icon": "fas fa-comments",
    #         "permissions": ["authentication.view_user"]
    #     }]
    # },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "authentication": "fas fa-users",
        "authentication.user": "fas fa-user",
        "hospital": "fas fa-hospital-alt",
        "hospital.hospital": "fas fa-hospital",
        "doctor": "fas fa-users",
        "doctor.doctor": "fas fa-user-tie",
        "doctor.doctorwithhospital": "fas fa-hospital",
        "doctor.doctoronlineavailability": "fas fa-calendar-day",
        "doctor.doctortimeslots": "fas fa-calendar-day",
        "task": "fas fa-tasks",
        "task.task": "fas fa-tasks",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": 'assets/css/django_jazzmin.css',
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,




    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "authentication.user": "horizontal_tabs", 
        "doctor.doctor": "vertical_tabs"
    },
    # Add a language dropdown into the admin
    "language_chooser": False,
}