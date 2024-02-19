ArtD Customer
=============
Art Customer is a package that makes it possible to manage customers, tags, addresses and additional fields.
------------------------------------------------------------------------------------------------------------
1. Add to your INSTALLED_APPS setting like this:
``INSTALLED_APPS = [
        ...
        'artd_location',
        'artd_partner',
        'django-json-widget'
        'artd_customer'
    ]
``
2. Run `python manage.py migrate` to create the models.

3. Run the seeder data:
``python manage.py create_countries``
``python manage.py create_colombian_regions``
``python manage.py create_colombian_cities``
