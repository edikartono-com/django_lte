from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

#---- ManyToMany | Channel & Category ------------------------------------
class Channel(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(upload_to='images/channel', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
         return self.name or ''

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(upload_to='images/category', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
         return self.name or ''

# --------- unit ---------------------
class Unit(models.Model):
    name = models.CharField(max_length=200, null=True, default='None')

    def __str__(self):
         return self.name or ''

# --------- brand---------------------
class Brand(models.Model):
    name = models.CharField(max_length=200, null=True, default='None')

    def __str__(self):
         return self.name or ''

class Material(models.Model):
    name = models.CharField(max_length=200, null=True, default='None')

    def __str__(self):
         return self.name or ''

# Create your models here.
class Product(models.Model):
    class Prefix_code(models.TextChoices):
        LOUNGE_CHAIR = 'LC', 'Lounge Chair'
        LOVE_SEAT = 'LS', 'Love Seat'
        SOFA = 'SO', 'Sofa'
        LOUNGE_STOOL = 'LO', 'Lounge Stool'
        COFFE_TABLE = 'CT', 'Coffe Table'
        SIDE_TABLE = 'ST', 'Side Table'
        OTTOMAN = 'OT', 'Ottoman'
        DINNING_CHAIR = 'DC', 'Dining Chair'
        SIDE_CHAIR = 'SC', 'Side Chair'
        LOUNGER = 'LG', 'Lounger'
        DINNING_TABLE = 'DT', 'Dining Table'
        BENCH = 'BN', 'Bench'
        PANEL = 'PN', 'Panel'
        BAR_TABLE = 'BT', 'Bar Table'
        BAR_STOOL = 'BS', 'Bar Stool'
        BAR_CHAIR = 'BC', 'Bar Chair'
        MODULAR_RIGHT = 'MR', 'Modular Right'
        MODULAR_LEFT = 'ML', 'Modular Left'
        MODULAR_MIDDLE = 'MM', 'Modular Middle'
        MODULAR_CORNER = 'MC', 'Modular Corner'
        CONSOLE_TABLE = 'NT', 'Console Table'
        BATHROOM_STOOL = 'BO', 'Bathroom Stool'
        BATHROOM_BENCH = 'BB', 'Bathroom Bench'
        SHAVING_STOOL = 'SS', 'Shaving Stool'
        SHELF = 'SF', 'Shelf'
        BASKET = 'BK', 'Basket'
        TRAY = 'TY', 'Tray'
        TOWEL_STAND = 'TS', 'Towel Stand'
        MAT = 'MT', 'Mat'
        CABANA = 'CB', 'Cabana'
        PARASOL = 'PR', 'Parasol'
        BASE_STAND = 'SD', 'Base Stand'
        PLANTER = 'PL', 'Planter'
        LANTERN = 'LT', 'Lantern'
        THROW_PILLOW = 'TP', 'Throw Pillow'
        PUF = 'PF', 'Pouf'
        NONE = 'NO', 'None'
    class Status(models.TextChoices):
        DISABLE = 'DI', 'Disable'
        ENABLE = 'EN', 'Enable'
    # General Information ---------------------------
    prefix_code = models.CharField(max_length=2, choices=Prefix_code.choices, default=Prefix_code.NONE, null=True, blank=True)
    sku = models.CharField(max_length=200, null=True, unique=True)
    name = models.CharField(max_length=200, null=True)
    featured_image = models.ImageField(upload_to="featured_image_path", null=True, blank=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE, related_name='brands_product', blank=True, null=True )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_product', blank=True, null=True)
    channel = models.ManyToManyField(Channel, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    material = models.ManyToManyField(Material, blank=True)
    cbm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    moq = models.PositiveIntegerField(default=0, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Product Specifications -----------
    ps_overal_dimension = models.CharField(max_length=200, null=True, blank=True)
    ps_arm_height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ps_seat_height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ps_seat_depth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ps_nett_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ps_gross_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ps_product_type = models.CharField(max_length=200, null=True, blank=True)
    ps_seat_construction = models.CharField(max_length=200, null=True, blank=True)
    # Shipping Details
    ps_box_dimension = models.CharField(max_length=200, help_text='74,48,20', blank=True)
    ps_box_weight = models.CharField(max_length=200, null=True, blank=True)
    ps_pax = models.CharField(max_length=200, null=True, blank=True)
    ps_20ft_container = models.CharField(max_length=200, null=True, blank=True)
    ps_40gp_container = models.CharField(max_length=200, null=True, blank=True)
    ps_40hq_container = models.CharField(max_length=200, null=True, blank=True)
    # Factory Drawing ---------------
    production_drawing_pdf = models.FileField(upload_to='production_drawing_pdf_path', null=True, blank=True)
    production_drawing_archive = models.FileField(upload_to='production_drawing_archive_path', null=True, blank=True)
    assembly_pdf = models.FileField(upload_to='assembly_pdf_path', null=True, blank=True)
    assembly_archive = models.FileField(upload_to='assembly_archive_path', null=True, blank=True)
    bom_file = models.FileField(upload_to='bom_file_path', null=True, blank=True)
    # Dezign Studio
    drawing_3d_dwg = models.FileField(upload_to='drawing_3d_dwg_path',null=True, blank=True)
    drawing_3d_obj = models.FileField(upload_to='drawing_3d_obj_path',null=True, blank=True)
    drawing_3d_3dmax = models.FileField(upload_to='drawing_3d_3dmax_path',null=True, blank=True)
    drawing_3d_sketchup = models.FileField(upload_to='drawing_3d_sketchup_path', null=True, blank=True)
    # SEO ----------------------
    seo_meta_title = models.CharField(max_length=200, null=True, blank=True)
    seo_meta_description = models.CharField(max_length=200, null=True, blank=True)
    seo_meta_keyword = models.CharField(max_length=200, null=True, blank=True)
    seo_content_overview = RichTextField(blank=True)
    # Time ---------------
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                choices=Status.choices,
                                default=Status.ENABLE)

    class Meta:
        ordering = ['-created_at']
        indexes = [
        models.Index(fields=['-created_at']),
        ]
        # unique_together = ('sku',)

    def __str__(self):
        return self.name or ''
    
    @property
    def pim_code(self):
        id_zfill =('%s'% (self.id)).zfill(5)
        return '%s-%s' % (self.prefix_code,id_zfill)

class AmbienceImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ambience_image')
    image = models.ImageField(upload_to = 'ambience_image', null=True)

class SpecificationImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='spec_image')
    image = models.ImageField(upload_to = 'specification_image', null=True)

class TechnicalImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='technical_image')
    image = models.ImageField(upload_to = 'technical_image', null=True)