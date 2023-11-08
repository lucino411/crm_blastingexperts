from django.db import models
from django.utils.translation import gettext_lazy as _


'''
OneToOneField es un tipo de campo en Django que se utiliza para establecer una relación uno a uno entre dos modelos. Este campo se utiliza para indicar que cada instancia del modelo que lo contiene está relacionada con exactamente una instancia de otro modelo especificado.
En el contexto de tu situación, estás utilizando OneToOneField en el modelo DefaultCreatedBy para establecer una relación uno a uno entre esta instancia y una instancia específica del modelo CustomUser de la aplicación userprofile. Esto significa que cada instancia de DefaultCreatedBy se relaciona con exactamente una instancia de CustomUser.
En términos más generales, OneToOneField se utiliza para mantener una relación que es simétrica en ambos sentidos. A diferencia de un campo ForeignKey, que permite una relación de uno a muchos, OneToOneField impone restricciones adicionales para garantizar que cada objeto esté asociado con exactamente un objeto en el otro extremo de la relación.
'''

class Title(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True, null=False, blank=False)
    is_selected = models.BooleanField(default=False)  # Nuevo campo

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['name']
        constraints = [
            models.CheckConstraint(check=models.Q(code__regex=r'^CO[A-Z]{3}$'), name='El código debe empezar con CO seguido de tres mayúsculas'),
            models.UniqueConstraint(fields=['code'], name='Ese código de país ya existe.'),
        ]

'''
En Django, models.Q es una herramienta que te permite construir consultas más complejas y flexibles para las bases de datos. Proporciona una forma de definir condiciones de consulta más avanzadas que van más allá de las consultas simples de igualdad o comparaciones estándar.
models.Q se puede utilizar para agrupar condiciones de consulta utilizando operadores lógicos como AND y OR, lo que te permite crear consultas más elaboradas y precisas. Esto es especialmente útil cuando necesitas realizar consultas que involucran múltiples condiciones y combinarlas de formas más complejas.
Por ejemplo, puedes usar models.Q para crear consultas que contienen varias condiciones de filtro, como consultas con múltiples filtros OR. Esto te permite realizar consultas más avanzadas y sofisticadas en tu base de datos con una mayor flexibilidad y control sobre los resultados que obtienes.
'''

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name