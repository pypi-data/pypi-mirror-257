ArtD Stock
==========
Art Product is a package that makes it possible to manage stock and stock changes.
----------------------------------------------------------------------------------
1. Add to your INSTALLED_APPS setting like this:
``INSTALLED_APPS = [
        ...
        'django-json-widget'
        'artd_location',
        'artd_partner',
        'artd_product',
        'artd_stock',
    ]
``
2. Run `python manage.py migrate` to create the models.

3. Run the seeder data:
``python manage.py create_countries``
``python manage.py create_colombian_regions``
``python manage.py create_colombian_cities``
``python manage.py create_taxes``
