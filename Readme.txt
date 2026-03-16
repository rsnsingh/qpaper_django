## Step 1: Set Up Your Django Project

### 1. Create a Django Project

```bash
# Activate your virtual environment if you have one
source myenv/bin/activate  # For Linux
# myenv\Scripts\activate    # For Windows

# Create a new Django project
django-admin startproject qpapers
cd qpapers
```

### 2. Install Required Packages

Install necessary packages:
```bash
pip install psycopg2-binary django-elasticsearch-dsl
```

### 3. Configure PostgreSQL Database

1. Open PostgreSQL prompt:
   ```bash
   sudo -u postgres psql  # Linux
   psql -U postgres       # Windows
   ```

2. Create a new database and user:
   ```sql
   CREATE DATABASE qpapers_db;
   CREATE USER qpapers_user WITH PASSWORD 'your_password';
   ALTER ROLE qpapers_user SET client_encoding TO 'utf8';
   ALTER ROLE qpapers_user SET timezone TO 'UTC';
   ALTER ROLE qpapers_user LOGIN;
   GRANT ALL PRIVILEGES ON DATABASE qpapers_db TO qpapers_user;
   ```

3. Exit the PostgreSQL prompt:
   ```sql
   \q
   ```

### 4. Configure Django Database Settings

Edit `settings.py` in your Django project:

```python
# qpapers/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'qpapers_db',
        'USER': 'qpapers_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

### 5. Create a Django App

```bash
python manage.py startapp papers
```

### 6. Define Models

Edit `models.py` in your papers app to create a model for the PDF question papers:

```python
# papers/models.py
from django.db import models

class Paper(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=50)
    file = models.FileField(upload_to='papers/')
    
    def __str__(self):
        return self.title
```

### 7. Configure Media Storage

Edit `settings.py` to configure media storage:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 8. Update URLs

Edit `urls.py` to include your app’s URLs:

```python
# qpapers/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('papers.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 9. Create Forms for Uploading PDFs

Create a form in `forms.py`:

```python
# papers/forms.py
from django import forms
from .models import Paper

class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'subject', 'subject_code', 'file']
```

### 10. Create Views for Handling Uploads and Searches

Edit `views.py`:

```python
# papers/views.py
from django.shortcuts import render
from .forms import PaperForm
from .models import Paper

def upload(request):
    if request.method == 'POST':
        form = PaperForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = PaperForm()
    return render(request, 'upload.html', {'form': form})

def paper_list(request):
    papers = Paper.objects.all()
    return render(request, 'papers.html', {'papers': papers})
```

### 11. Define URLs for Your App

Create `urls.py` in your papers app:

```python
# papers/urls.py
from django.urls import path
from .views import upload, paper_list

urlpatterns = [
    path('upload/', upload, name='upload'),
    path('papers/', paper_list, name='papers'),
]
```

### 12. Create Templates

Create `upload.html` and `papers.html` in a `templates` folder within the `papers` app.

#### upload.html
```html
<h1>Upload Paper</h1>
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>
```

#### papers.html
```html
<h1>Uploaded Papers</h1>
<ul>
    {% for paper in papers %}
        <li>
            <strong>{{ paper.title }}</strong> - 
            <a href="{{ paper.file.url }}">Download</a>
        </li>
    {% endfor %}
</ul>
```

### 13. Run Migrations

Run the following commands to create the database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 14. Create a Superuser

Create a superuser to access the admin panel:
```bash
python manage.py createsuperuser
```

### 15. Run the Development Server

```bash
python manage.py runserver
```

You can now go to `http://127.0.0.1:8000/upload/` to upload your PDFs and `http://127.0.0.1:8000/papers/` to list them.

## Step 2: Set Up Elasticsearch (Optional)

If you want to enhance search functionality:

1. **Install Elasticsearch** and run it as previously described.
2. **Integrate Elasticsearch with Django** using `django-elasticsearch-dsl`.

### In `settings.py`, configure Elasticsearch:

```python
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}
```

### Create a Document for the Paper:

```python
# papers/documents.py
from papers.models import Paper
from elasticsearch_dsl import Document, Text, File

class PaperDocument(Document):
    class Index:
        name = 'papers'

    title = Text()
    subject = Text()
    file = File()

    class Django:
        model = Paper
        fields = ['id']
```

### 1. Create a search view and update your URLs accordingly.

## Step 3: Set Up React Front-End (Optional)

To create a front-end in React, you can follow these steps:

1. **Create a New React App**:
   ```bash
   npx create-react-app frontend
   cd frontend
   ```

2. **Install Axios** for API requests:
   ```bash
   npm install axios
   ```

3. **Create Components to Handle Uploads and Fetch Data**.

4. **Connect to Django API** to upload and list the papers.
