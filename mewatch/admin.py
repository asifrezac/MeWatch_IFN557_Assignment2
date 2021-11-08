from flask import Blueprint
from . import db
from .models import Category, Product, Order
import datetime


bp = Blueprint('admin', __name__, url_prefix='/admin/')

# function to put some seed data in the database
@bp.route('/dbseed/')
def dbseed():
    category1 = Category(name='Leather Strap Watch', image='carousel_2.png')
    category2 = Category(name='Stainless Steel Watch', image='carousel_1.png')
    category3 = Category(name='Smart Watch', image='carousel_3.png')
      
    try:
        db.session.add(category1)
        db.session.add(category2)
        db.session.add(category3)
        db.session.commit()
    except:
        return 'There was an issue adding the categories in dbseed function'

    w1 = Product(
        name='Leather Strap Blue Watch',
        type = category1.name,
        description= 'Minimalistic watch with leather strap and magnificent blue dial',
        material = 'Leather',
        size = '40 mm',
        price= 79,
        image='watch_leather_1.jpeg',
        category_id=category1.id) 
    w2 = Product(
        name='Silver Smart Watch',
        type = category3.name,
        description= 'Smart Watch with silver stainless steel band',
        material = 'Aluminium',
        size = '40 mm',
        price= 199,
        image='watch_smart_1.jpeg',
        category_id=category3.id)
    w3 = Product(
        name='Stainless Steel Strap Silver Watch',
        type = category2.name,
        description= 'Chronograph watch with stainless steel band and elegant black dial',
        material = 'Stainless Steel',
        size = '40 mm',
        price= 119,
        image='watch_ss_1.jpeg',
        category_id=category2.id)
    w4 = Product(
        name='Leather Strap White Watch',
        type = category1.name,
        description= 'Chronograph watch with leather strap and beautiful white dial',
        material = 'Leather',
        size = '40 mm',
        price= 79,
        image='watch_leather_2.jpeg',
        category_id=category1.id)                
    w5 = Product(
        name='Gold Smart Watch',
        type = category3.name,
        description= 'Smart Watch with golden stainless steel band',
        material = 'Aluminium',
        size = '40 mm',
        price= 199,
        image='watch_smart_2.jpeg',
        category_id=category3.id)
    w6 = Product(
        name='Stainless Steel Strap Black Watch',
        type = category2.name,
        description= 'Chronograph watch with gorgius black stainless steel band',
        material = 'Stainless Steel',
        size = '40 mm',
        price= 119,
        image='watch_ss_2.jpeg',
        category_id=category2.id)

    try:
        db.session.add(w1)
        db.session.add(w2)
        db.session.add(w3)
        db.session.add(w4)
        db.session.add(w5)
        db.session.add(w6)
        db.session.commit()
    except:
        return 'There was an issue adding a watch in dbseed function'

    return 'DATA LOADED'