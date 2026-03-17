# Edit `models.py` in your papers app to create a model for the PDF question papers:

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
