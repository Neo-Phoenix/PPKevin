# PPKevin
Naam project: EhB Uitleensysteem webapp.

## Beschrijving:
Dit is een klein Django webapplicatie project dat een beheer/uitleen systeem voor het medialab van EhB zal kunnen dienen.

## Kenmerken:
- Beheer/Uitleen systeem voor het medialab van EhB.
- Verbinding met een databank voor permanente opslag van gegevens.
- Beveiliging wachtwoorden met hashing.
- Mogelijkheid om het systeem aan te passen studenten aan te maken.
- Searchfunctie (bijvoorbeeld op ID, naam, enzovoort) voor gebruik in andere functies.
- Overzicht van gegevens via console of grafische gebruikersinterface.

## Optioneel:
- Controleren van de voorraad van producten.
- Verlengen van uitleenperiodes
- Toepassen van boetes op laattijdig terugbrengen

## Installatie:
1. Installeer de laatste versie van Python 3
2. Installeer Django 5.0.4
   Linux / macOS:
      python -m pip install Django==5.0.4

   Windows:
      python -m pip install Django==5.0.4
      
3. Installeer Django tailwind (css framework)
pip install django-tailwind

4. Installeer Django Browser Reload
pip install django-browser-reload

5. Clone de repository met git clone naar target folder
      https://github.com/Neo-Phoenix/PPKevin

6. Run Django app in terminal
python .\PPKevin\UitleensysteemApp\manage.py runserver

7. Optioneel: voor development start tailwind service op voor updated css
python .\PPKevin\UitleensysteemApp\manage.py tailwind start