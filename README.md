# APIS RSE Assignment Directory

This repository contains a minimal web application built with Django (v6.0.4) that pulls data from the <a href="https://discworld.acdh-dev.oeaw.ac.at/" target="_blank">Discworld APIS instance</a> and displays it in HTML templates.

Two views are implemented: 

1) Person List View: a list view that displays all persons. Every entry links to the detail view for that person. The list view also has filters for name, profession, and gender.

2) Person Detail View: a detail view that displays all available information for a single person.

The data (https://discworld.acdh-dev.oeaw.ac.at/api/sample_project.person/) contains fictional characters in JSON-format with the following fields: 
- url in format <i>api/sample_project.person/id/</i>
- forename (all entries have a value for this field)
- surname (may be empty for some entries)
- gender (all but one entry has a value for this field)
- date and of birth and death (no entry has a value for these fields)
- profession (http://discworld.acdh-dev.oeaw.ac.at/api/sample_project.profession/ with label field).

Missing values are treated as empty strings for surname and gender, as <i>null</i> for date of birth and death, and as an empty list for profession.


Tools used: Python 3.14.4, Django 6.0.4, Docker 29.4.1.

AI assistance: Github Copilot.

---

## Setup

### 1. Git clone
```bash
git clone https://github.com/NKCZ/python_assignment_rse_acdh_2026.git
cd python_assignment_rse_acdh_2026
```

Alternatively, you can manually download the repository as a ZIP file and extract it in the directory of your choice.

### 2a. Install dependencies
```bash
pip install django requests
```

### 2b. Create and activate a virtual environment
```bash
# Create venv (Windows)
python -m venv .venv
# Activate (Windows PowerShell)
.\\.venv\\Scripts\\Activate.ps1
# Or activate (Windows Command Prompt)
.\\.venv\\Scripts\\activate.bat
# On macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# After activation, install dependencies
pip install django requests
```

### 3. Run
```bash
python manage.py runserver
```
Then visit http://127.0.0.1:8000/

### Docker 
Alternatively, you can run the application using <a href="https://www.docker.com/" target="_blank">Docker</a>:

```bash
git clone https://github.com/NKCZ/python_assignment_rse_acdh_2026.git
cd python_assignment_rse_acdh_2026
docker build -t apis_docker_app .
docker run -p 8000:8000 apis_docker_app
```
Then visit http://localhost:8000

---

## URLs

| Path | View | Description |
|------|------|-------------|
| `/` | `person_list` | Filterable table of all persons |
| `/persons/<id>/` | `person_detail` | Full detail for one person |

---

## Filters available on the list view

| Filter | Behaviour |
|--------|-----------|
| Name | Case-insensitive substring match on forename + surname |
| Profession | Case-insensitive substring match on profession labels |
| Gender | Exact match; dropdown is built from values present in the data |

---

## File structure

- apis_project (root directory)
    - manage.py (Django management script)
    - apis_project (Django project configuration)
        - settings.py (Django settings)
        - urls.py (Project-level URL configuration)
    - apis_app (Django application)
        - api_client.py (Module for API interactions)
        - views.py (Django views for handling requests)
        - urls.py (Application-level URL configuration)
        - templates/persons/ (HTML templates for rendering views)
            - base.html (Base template for consistent layout)
            - person_list.html (Template for the list view)
            - person_detail.html (Template for the detail view)

There are some additional files generated through the Django setup process, but these are irrelevant for the assignment and have not been modified.

---
## AI Assistance
I used Visual Studio Code with the <a href="https://github.com/features/copilot" target="_blank">Github Copilot</a> auto-completion function. 

Github Copilot is an AI pair programming tool that provides code suggestions and completions based on the context. 

I usually start writing a one-line comment describing the functionality I want to implement, and then Copilot generates the next lines of code. 

I find that this approach allows to quickly generate code that is often quite close to what I want to achieve, while still giving me the flexibility to make adjustments as needed.

When it does not go in the direction I wish, I simply write the next lines myself, which usually leads to suggestions that are more in line with what I want to achieve.

The same approach was used for this assignment.







