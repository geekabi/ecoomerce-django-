from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='تاریخ ایجاد'
                                      )
    
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='تاریخ آخرین ویرایش'
                                      )
    
    class Meta:
        abstract = True
        verbose_name = 'مدل پایه'
        verbose_name_plural = "مدل‌های پایه"

    def __str__(self):
        return f"{self.pk}"
        
