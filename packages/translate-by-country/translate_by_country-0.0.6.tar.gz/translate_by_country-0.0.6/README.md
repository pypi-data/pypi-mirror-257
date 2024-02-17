translate-by-country
====================

With this library, you can translate the text without choosing the language and with the characteristics of the countries

installation:
-------------

.. code-block:: text

    pip install translate-by-country

Usage:
------

Translates text based on country alpha2

.. code-block:: python

    from translate_by_country import translate_text_by_alpha2
    print(translate_text_by_alpha2("translate by country","ax")) # Översätt efter land


Translates text based on country alpha3

.. code-block:: python

    from translate_by_country import translate_text_by_alpha3
    print(translate_text_by_alpha3("translate by country","aut")) # nach Land übersetzt

Translates text based on country code

.. code-block:: python

    from translate_by_country import translate_text_by_code
    print(translate_text_by_code("translate by country",98)) # ترجمه توسط کشور

Translates text based on country name

.. code-block:: python

    from translate_by_country import translate_text_by_name
    print(translate_text_by_name("translate by country","albania")) # Përkthejeni sipas vendit

Translates text based on country emoji

.. code-block:: python

    from translate_by_country import translate_text_by_name
    print(translate_text_by_emoji("translate by country","🇹🇼")) # 按国家翻译
