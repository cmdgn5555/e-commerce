from django.shortcuts import render
from .models import Product, Category
from django.db.models import Q
# Create your views here.


def store(request):
    all_products = (Product.objects
                    .values('title', 'price', 'image', 'slug')
                    .filter(Q(status='Active') | Q(status='Modified'))
                    .order_by('title'))

    """
    Yukarıdaki Django sorgusunun SQL karşılığı
    select title, price, image, slug 
    from store_products 
    where status = Active or status = Modified
    order by title asc
    """

    return render(
        request=request,
        template_name='store.html',
        context={
            'all_products': all_products
        }
    )


def categories(request):
    model = ((Category.objects
             .filter(Q(status='Active') | Q(status='Modified'))
             .values('name', 'slug'))
             .order_by('name'))

    # Dikkat!!!
    # bu data template altında herhangi bir html sayfasına her zamanki gibi basılmayacak. Farkındaysanız render fonksiyonunu kullanmadım.
    # ecommerce => settings.py => TEMPLATE[] listesine "categories()" register et.
    return {
        'model': model
    }


def list_category(request, category_slug=None):
    # 1. adım: Fonksiyona gelen category_slug bilgisi ile category tablsonuna sorgu attım
    # ilgili slug ait categorinin id'sini ve name'ni allalım
    category = (Category.objects
                .filter(Q(status='Active') | Q(status='Modified'), Q(slug=category_slug))
                .values('id', 'name')
                .first())

    # 2. adım: Yukarıda bulduğumuz categorini id bilgisine göre products tablosundan ürünleri çekelim
    model = (Product.objects
                    .values('title', 'price', 'image', 'slug')
                    .filter(Q(status='Active') | Q(status='Modified'), Q(category_id=category['id']))
                    .order_by('title'))

    return render(
        request=request,
        template_name='list-category.html',
        context={
            'category_name': category['name'],
            'products': model
        }
    )


def product_info(request, product_slug=None):
    # ana sayfada ürün adı resmi ve fiyatı var.
    # detay sayfasına gitiğmizde bütün bilgileri ve bağlı olduğu category'de ekrana yazdırıcaz. bağlı olduğu category categories tablosunda bu yüzden burada join yapmamız gerekmetedir. Django sorgularında join select_related() fonksiyonu ile yapılmaktadır.

    # data = (Product.objects
    #         .select_related('category')
    #         .filter(Q(status='Active') | Q(status='Modified'), Q(slug=product_slug))
    #         .values('title', 'description', 'price', 'image', 'brand', 'category__name')
    #         .first())

    data = (Product.objects
            .select_related('category')
            .filter(Q(status='Active') | Q(status='Modified'), Q(slug=product_slug))
            .first())

    return render(
        request=request,
        template_name='product-info.html',
        context={
            'product_info': data
        }
    )