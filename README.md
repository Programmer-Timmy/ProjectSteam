# ProjectSteam

[//]: # (This file provides all necessary details on working on the project)

Welcome to ProjectSteam! This guide provides a complete overview of installation, setup, and guidelines for developing new features and contributing to the project.

---

## Table of Contents
- [Installation](#installation)
- [How the Project Works](#how-the-project-works)
- [Creating a New App](#creating-a-new-app)
- [Adding a New Web Page](#adding-a-new-web-page)
- [Working on the Project](#working-on-the-project)

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

This project is structured with Django applications (or "apps"). Each app contains its own views, models, and templates.

### Existing Apps
- **`steam`** – The main app that serves the core pages
- **`dashboard`** – Handles dashboard-related functionality

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

## using the authentication system

You can specify what view requires a user to be logged in by using the `@login_required` decorator. This decorator will redirect the user to the login page if they are not logged in.

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    # your view code here
```

To log a user in, you can use the `login` function from `django.contrib.auth` or just use the login page. 

---

```python

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

- "Idk how Django works." – Programmer Timmy
- "Welkom bij ons Steam project!" – Chris van Veen
- "Zullen we onze store de ... store noemen?" – Jerome de Vaal
- "peepeepoopoo" – Oscar Gruijs (peepeepoopoo@collector.org)
