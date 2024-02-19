ArtD Promotion
==============
Art promotion is a package that makes it possible to manage promotions and rules based on customers, categories and products.
-----------------------------------------------------------------------------------------------------------------------------
1. Add to your INSTALLED_APPS setting like this::
``INSTALLED_APPS = [
        ...
        'django-json-widget'
        'artd_location',
        'artd_partner',
        'artd_customer'
        'artd_product',
        'artd_promotion',
    ]
``
2. Run `python manage.py migrate` to create the models.

3. Run the seeder data:
``python manage.py create_countries``
``python manage.py create_colombian_regions``
``python manage.py create_colombian_cities``
``python manage.py create_taxes``
