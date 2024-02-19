ArtD Order
==========
Art Order is a package that makes it possible to manage orders.
---------------------------------------------------------------
1. Add to your INSTALLED_APPS setting like this::
``INSTALLED_APPS = [
        ...
        'django_json_widget',
        'artd_location',
        'artd_partner',
        'artd_customer',
        'artd_product',
        'artd_price_list',
        'artd_stock',
        'artd_order',
    ]
``
3. Run the seeder data:
``python manage.py create_countries``
``python manage.py create_colombian_regions``
``python manage.py create_colombian_cities``
``python manage.py create_taxes``
``python manage.py create_order_statuses``