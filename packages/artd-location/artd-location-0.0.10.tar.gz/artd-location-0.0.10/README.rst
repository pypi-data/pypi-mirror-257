ArtD Location
=============
ArtD location is a package that makes it possible to have countries, regions and cities with their respective coding, by default we have all the regions and cities of Colombia.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
1. Add "artD_ocation" to your INSTALLED_APPS setting like this:
``INSTALLED_APPS = [
        ...
        'artd_location',
    ]
``

2. Run `python manage.py migrate` to create the models.

3. Run the seeder data:
``python manage.py create_countries``
``python manage.py create_colombian_regions``
``python manage.py create_colombian_cities``
