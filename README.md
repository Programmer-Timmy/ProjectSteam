# ProjectSteam

[//]: # (This file provides all necessary details on working on the project)

Welcome to ProjectSteam! This guide provides a complete overview of installation, setup, and guidelines for developing new features and contributing to the project.

---

## Table of Contents (dev documentation, for the project documentation go [here](#project-steam)) 
- [Installation](#installation)
- [How the Project Works](#how-the-project-works)
- [Creating a New App](#creating-a-new-app)
- [Adding a New Web Page](#adding-a-new-web-page)
- [Working on the Project](#working-on-the-project)
- [Using the Authentication System](#using-the-authentication-system)
- [Frequently Used Commands](#frequently-used-commands)
- [Team Notes](#team-notes)

---

## Installation

1. **Clone the Repository**  
   First, clone the repository to your local machine:
   ```bash
   git clone <repository_url>
   ```

2. **Install Required Packages**  
   Install all necessary Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup for PyCharm Users**  
   For PyCharm users who encounter missing HTTP links:
   - Go to `/templates/base.html`
   - Hover over the yellow-marked links
   - Click on `Download library` to resolve missing dependencies

4. **Run the Server**  
   Start the Django web server with:
   ```bash
   python manage.py runserver
   ```
   Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the site locally.

---

## How the Project Works

This project is structured with Django applications ("apps"), each responsible for specific functionalities. Below is an overview of the main apps and their purposes:

### Existing Apps

- **`Account`**: Handles user profiles, settings, and game libraries.
- **`Ajax`**: Manages AJAX requests for dynamic and seamless user interactions.
- **`AuthManager`**: Controls user authentication, including Steam login.
- **`Controllers`**: Contains reusable logic and controllers shared across the project.
- **`Daily_Checks`**: Includes scripts that update data daily by syncing with the Steam API.
- **`Dashboard`**: Provides the main user dashboard with statistics, friends, and achievements.
- **`Games`**: Allows users to view, play, and interact with their games.
- **`Steam`**: Serves as the homepage, where users land after logging in.
- **`Raspberry`**: Handles integration with Raspberry Pi for external hardware interactions.
- **`DjangoProject`**: Hosts project-wide settings, static files, and base templates.
- **`/media`**: Stores uploaded files, including user profile pictures and other media assets.
- **`Templates`**: Contains HTML templates organized into subfolders matching the app structure.

---

## Creating a New App

To create a new app within the project:

1. **Run the Start Command**  
   Use this command to create a new app:
   ```bash
   python manage.py startapp <app_name>
   ```

2. **Set Up URL Configuration**  
   In your new app's directory, create a file named `urls.py` and add the following code:
   ```python
   from django.urls import path
   from . import views

   urlpatterns = [
       # Define paths and views here
   ]
   ```

3. **Register the App in `settings.py`**  
   Add the new app to the `INSTALLED_APPS` list in the main `settings.py`:
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       '<app_name>.apps.AppNameConfig',  # Add your app here
   ]
   ```

---

## Adding a New Web Page

To add a new page within an app, follow these steps:

1. **Define a New View**  
   In your app's `views.py`, define a view function:
   ```python
   def new_page(request):
       return render(request, 'app_name/new_page.html', {'page_title': 'New Page'})
   ```

2. **Create an HTML Template**  
   In the `templates/app_name/` directory, create an HTML file (e.g., `new_page.html`):
   ```html
   {% extends 'base.html' %}
   {% block page_title %}{{ page_title }}{% endblock %}

   {% block content %}
   <div class="container">
       <h1>New Page</h1>
       <p>This is a new page.</p>
   </div>
   {% endblock %}
   ```

3. **Add a Route to the `urls.py` of the App**  
   In `urls.py`, add a path to your new view:
   ```python
   path('new_page/', views.new_page, name='new_page'),
   ```

4. **Optional: Add Link to Navbar**  
   To add a link to the navbar, open `base.html` in the main `templates` folder and add:
   ```html
   <li class="nav-item">
       <a class="nav-link" href="{% url 'new_page' %}">New Page</a>
   </li>
   ```

---

## Using the Authentication System

To protect views requiring authentication, use the `@login_required` decorator. This ensures that only logged-in users can access certain pages:

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    # your view code here
```

To log in a user, use the `login` function from `django.contrib.auth` or direct them to the login page provided.

---

## Working on the Project

### Git Workflow

1. **Create a New Branch**  
   For each task or feature, start by creating a new branch:
   ```bash
   git checkout -b <branch_name>
   ```

2. **Make Changes**  
   Implement your updates, fix issues, or add new features.

3. **Stage Changes**  
   Add your changes to the staging area:
   ```bash
   git add .
   ```

4. **Commit Changes**  
   Commit with a clear message describing the update:
   ```bash
   git commit -m "Your commit message"
   ```

5. **Push Changes**  
   Push your branch to the remote repository:
   ```bash
   git push origin <branch_name>
   ```

6. **Create a Pull Request (PR)**  
   Open GitHub, create a PR, and wait for it to be reviewed.

7. **Merge and Cleanup**  
   After your PR is merged, delete your branch:
   ```bash
   git branch -d <branch_name>
   ```

8. **Update Local Repository**  
   Sync your local repo with the latest changes:
   ```bash
   git pull
   ```

9. **Repeat for New Issues/Tasks**

---

## Frequently Used Commands

To start the web server:
```bash
python manage.py runserver
```

To create a new app:
```bash
python manage.py startapp <app_name>
```

To create a new superuser:
```bash
python manage.py createsuperuser
```

To make and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

To run tests:
```bash
python manage.py test
```

---

## Team Notes

- "Ik weet niet hoe Django werkt." – Programmer Timmy
- "Welkom bij ons Steam project!" – Chris van Veen
- "Zullen we onze store de ... store noemen?" – Jerome de Vaal
- "peepeepoopoo" – Oscar Gruijs (peepeepoopoo@collector.org)

# Project Steam

### Documentatie
De Dumdums (groep 4)  
Geschreven door:  
Jerome de Vaal 1879373  
Tim van der Kloet 1887188  
Chris van Veen 1885709  

---

## Contents
- [Inleiding](#inleiding)  
- [Minimum Viable Product](#minimum-viable-product)  
- [Cyber Security & Cloud](#cyber-security--cloud)  
- [Server](#server)  
- [Toegang verlenen tot de Database](#toegang-verlenen-tot-de-database)  
- [Software Development](#software-development)  
- [Gebruikte Subsystemen](#gebruikte-subsystemen)  
- [Development: Structuur en Functie van de Django Apps](#development-structuur-en-functie-van-de-django-apps)  
- [Technische Informatica](#technische-informatica)  
- [Hardware](#hardware)  
- [Handleiding voor het aansluiten van de Raspberry Pico](#handleiding-voor-het-aansluiten-van-de-raspberry-pico)

---

## Inleiding
Project Steam is een fictief project bedacht en geschreven door de Hogeschool van Utrecht voor de opleiding HBO-ICT 1e jaar. Dit project is bedoeld zodat studenten hun voorkeur van studierichting kunnen bepalen en ervaring opdoen binnen samenwerkingverband en de AGILE werkmethode.  
Daarbij is dit project de grote afsluiting van het 1e semester, waarbij alle vakken zoals Cybersecurity & Cloud, Software Development, Artificial Intelligence, Technische Informatica en Business IT & Management samen komen.  
Daarnaast is dit ook het eerste project waarbij wij kennis maken met Sustainable Development Goals, wat gaat over de meerwaarde van het project tot de samenleving en invloed op het milieu.

---

## Minimum Viable Product
In dit project zijn wij benaderd door Valve om een visueel dashboard te maken, waar gebruikers van het gameplatform Steam, hun gamegedrag en statistieken kunnen inzien. Het is een vrij project waarbij je als projectteam zelf mag bepalen hoe je tot het eindresultaat komt en welke frameworks en toepassingen je gebruikt.

Het is belangrijk om als projectteam ons bezig te houden met de impact van de samenleving. Om te achterhalen wat wij belangrijk vinden, gingen wij onderzoeken welke Sustainable Development Goal ons het meest aansprak.  
Wij hebben gekozen voor Sustainable Development Goal 16 – Vrede, Justitie en sterke publieke diensten. Afgelopen decennia is er grotere bewustwording over de impact van data verzameling. Wij willen hier bewuster mee bezig zijn en de gebruiker een kans geven om zichzelf minder bloot te stellen aan het verzamelen van data.  
Wij kunnen dit toepassen door een Opt-in/out systeem te implementeren. De gebruiker krijgt dan de keuze om wel of niet mee te doen aan dit systeem. In het geval van niet meedoen, heeft de applicatie toch een functie. De applicatie geeft dan algemene cijfers weer, waardoor de gebruiker statistieken omtrent beoordelingen van games kunnen zien en een korte omschrijving over de game kunnen lezen.

---

## Cyber Security & Cloud
**Geschreven door Jerome de Vaal**

Voor Cyber Security & Cloud is er gekozen voor een lokaal beheerde server. De voornamelijkste redenen hiervoor zijn: beschikking tot een lokaal gehoste server die 24/7 aanstaat. Omdat de server continu draait, kunnen alle projectgenoten te allen tijde bij de database. Daarnaast wil ik meer leren over externe toegang verlenen buiten het lokale netwerk van deze server.  
Deze server draait op een Linux variant genaamd UNRAID, voor meer informatie nodig ik jullie uit om een kijk te nemen op [UNRAID](https://unraid.net/).  

---

## Server
Mijn server wordt voornamelijk gebruikt voor media consumptie binnen mijn woning op de TV, PC’s en mobiele platformen, maar ook extern naar bijvoorbeeld mijn ouders hun TV of onderweg op mijn telefoon en laptop. Dit project is voor mij een mooie kans om op een andere manier gebruik te maken van deze server.

**Screenshot van het UNRAID dashboard**

Voor het Steam project gebruiken wij PostgreSQL en pgAdmin4 docker containers. PostgreSQL17 zorgt voor de opbouw van de Database, waarin wij het meegeleverde .JSON bestand hebben geïmporteerd en uiteindelijk hebben uitgebreid met het Steam API (Software Development) en Raspberry Pico (Technische Informatica).

---

## Toegang verlenen tot de Database
Om toegang te verlenen tot de database dienen wij gebruikers aan te maken en eventuele machtigingen te geven zodat gebruikers de database kunnen benaderen en wijzigingen kunnen toepassen.  
Hieronder leg ik in stappen uit hoe dit wordt gerealiseerd.

1. Login met een Administrator account op de web GUI van pgAdmin 4 via het volgende URL: `http://85.144.230.126:8792/`
2. Klik vervolgens rechtsbovenin op jouw e-mailadres en klik vervolgens op ‘Users’ zoals hieronder vertoond.
3. Je ziet vervolgens het User Management panel. Hier worden alle gebruikers getoond die toegang hebben tot de Steam Dashboard database.  
   Om een nieuwe gebruiker aan te maken klik je rechts boven op het + teken zoals onderstaand aangegeven.
4. Wanneer hierop is geklikt, zie je dat er een nieuwe regel is toegevoegd om gegevens in te vullen. Je vult dan het volgende in:  
   • E-mailadres (username)  
   • Rol  
   • Wachtwoord  
   De gebruiker kan achteraf zelf een nieuw wachtwoord kiezen zoals te zien is bij stap 2.
5. Als laatste stap is het noodzakelijk dat de gebruiker gekoppeld wordt aan de database.  
   Login op de zojuist aangemaakte user.  
   Klik in het midden op de knop ‘Add New Server’ of rechterklik op Server > Register > Server, in het linker kolom zoals op de onderstaande afbeelding wordt afgebeeld.

---

## Software Development
**Geschreven door Tim van der Kloet**

Het softwaregedeelte van het Steam Dashboard voor SD richt zich op het ontwikkelen van een platform waarmee gebruikers hun Steam-account kunnen koppelen en hun game-activiteiten kunnen volgen en analyseren. Het project maakt gebruik van verschillende technologieën en subsystemen om een gebruiksvriendelijke, stabiele en schaalbare oplossing te bieden.  

---

## Gebruikte Subsystemen
### Algemeen:
1. [Django](https://www.djangoproject.com/)  
   Django is gekozen als webframework vanwege zijn uitgebreide functionaliteiten, zoals automatische admin-pagina's, formulierverwerking en ingebouwde beveiliging.
2. [Bootstrap](https://getbootstrap.com/)  
   Bootstrap is gebruikt om de webapplicatie visueel aantrekkelijk en responsief te maken.
3. [jQuery / JS](https://jquery.com/)  
   jQuery werd gekozen om de interactie met de gebruiker te verbeteren.
4. [Django-social-auth](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html)  
   De integratie van de Steam-login via django-social-auth stelde ons in staat om gebruikers eenvoudig toegang te geven tot hun Steam-account.

### Dashboard:
1. [Steam API](https://developer.valvesoftware.com/wiki/Steam_Web_API)  
   De Steam API is een belangrijke bron voor het verkrijgen van gebruikers- en game-informatie.
2. [Steam Spy API](https://steamspy.com/api.php)  
   De Steam Spy API werd geïmplementeerd om het aantal verzoeken naar de Steam API te minimaliseren.
   
### Gebruikbare App: Satisfactory API
1. [satisfactory-dedicated-server-api-SDK](https://github.com/Programmer-Timmy/satisfactory-dedicated-server-api-SDK)  
   Voor de integratie van een Satisfactory Dedicated Server werd de Satisfactory Dedicated Server API SDK gebruikt.

### Overige Technologieën en Tools
1. PostgreSQL Database  
2. Docker

---

## Development: Structuur en Functie van de Django Apps
Het Steam Dashboard project is opgebouwd met een logische structuur waarin elke app of map een specifieke rol heeft.

1. **Account**: Beheert alles wat met gebruikersaccounts te maken heeft.
2. **Ajax**: Behandelt alle AJAX-verzoeken.
3. **AuthManager**: Beheert het gebruikersmodel en het inlogsysteem.
4. **Controllers**: Bevat herbruikbare logica.
5. **Daily_Checks**: Voert dagelijkse scripts uit.
6. **Dashboard**: De kernfunctionaliteit van de applicatie.
7. **DjangoProject**: Bevat algemene configuratiebestanden.
8. **Games**: Bevat functionaliteit voor het bekijken van games.
9. **/media**: Slaat geüploade bestanden en afbeeldingen op.
10. **Raspberry**: Bevat de integratie met Raspberry Pi-hardware.
11. **Steam**: Functies als de hoofdpagina van het project.
12. **Templates**: Bevat alle HTML-bestanden.

---

## Technische Informatica
**Geschreven door Chris van Veen**

De Pico wordt in samenwerking met de Neopixel en een afstandssensor gebruikt om een beeld te geven hoe dicht je op je scherm zit. De neopixel kleurt groen, oranje of rood aan de hand van de afstand. Wanneer je te dicht bij zit wordt er een melding verstuurd naar het dashboard.

---

## Hardware
1. [Raspberry Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)
2. [Neopixel](https://store.arduino.cc/en-nl/products/neopixel-stick-with-8-rgb-ws2812-leds-and-integrated-driver)
3. [Afstandsensor](https://www.otronic.nl/nl/hc-sr04-ultrasonische-afstandssensor.html)

---

## Handleiding voor het aansluiten van de Raspberry Pico
1. Maak de constructie op de afbeelding na. Sluit daarna de Raspberry Pico aan op de computer via een USB-kabel.
2. Open PyCharm en ga naar plugins. Download en installeer de MicroPython plugin.
3. Zoek MicroPython op in de instellingen. Zet **Enable MicroPython support** aan.
4. Flash daarna het bestand `main.py` naar de Pico.
5. Open een terminal en run het bestand `TI/PC/pcmain.py` door het commando `python TI/PC/pcmain.py` te gebruiken.


