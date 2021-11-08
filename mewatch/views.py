# flask routes handling requests
#import necessary flask modules
from flask import Flask, Blueprint, render_template, request, url_for, redirect, session, flash

from .forms import CheckoutForm
from .models import Category, Product, Order
from datetime import datetime
# from .forms import CheckoutForm 
from . import db

# Main code
bp = Blueprint('main', __name__)

# route for home page
@bp.route('/')
def index():
    category = Category.query.order_by(Category.id).all() 
    productlist = Product.query.order_by(Product.name).all()
    return render_template('index.html', productlist=productlist, category=category)

# route for search result
@bp.route('/search')
def SearchView():
    query_string = request.args.get('query')
    print(query_string)
    print('--------------------------------')
    search = '%{}%'.format(query_string)
    final_products = Product.query.filter(Product.description.like(
        search)+Product.name.like(search)+Product.type.like(search)).all()
    if final_products == []:        
        flash('No result related to your searched keywords...')
    category = Category.query.order_by(Category.id).all()

    print(final_products)
    return render_template('search.html', searchResults=final_products, category=category)

# route for individual category page
@bp.route('/categories/<categoryid>/')
def CategoryView(categoryid):
    categoryWatch = Product.query.filter(Product.category_id == categoryid).all()
    selectedItem = Category.query.filter(Category.id == categoryid).first()
    category = Category.query.order_by(Category.id).all()
    
    return render_template('category.html', 
    watches = categoryWatch,
    item = selectedItem,
    category = category)

# route for individual product page
@bp.route('/product/<productid>')
def ProductView(productid):
    selectedWatch = Product.query.filter(Product.id == productid).first()
    selectedItem = Category.query.filter(Category.id == selectedWatch.category_id).first()
    category = Category.query.order_by(Category.name).all()

    return render_template('product.html', 
    product = selectedWatch,
    item = selectedItem,
    category = category)

# route for cart page
@bp.route('/order', methods=['POST', 'GET'])
def order():
    product_id = request.values.get('product_id')

    # check for a new order
    if 'order_id'in session.keys():
        order = Order.query.get(session['order_id'])
    else:
        order = None
    
     # new order
    if order is None:
        order = Order(status=False, 
        firstname='', 
        lastname='', 
        address = '', 
        postcode = '', 
        email = '', 
        phone = '', 
        totalcost=0, 
        date=datetime.now())
        
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print('Cannot create a new order')
            order = None
    
    # calcultate totalprice
    totalprice = 0
    if order is not None:
        for watch in order.watches:
            totalprice = totalprice + watch.price

    # are we adding an item?
    if product_id is not None and order is not None:
        product = Product.query.get(product_id)
        if product not in order.watches:
            try:
                order.watches.append(product)
                db.session.commit()
            except:
                return 'There was an issue adding the item to your cart'
            return redirect(url_for('main.order'))
        else:
            flash('item already in cart')
            return redirect(url_for('main.order'))
    
    category = Category.query.order_by(Category.name).all()
    print('-----------------------------------------------')
    # print( order )
    print('-----------------------------------------------')

    return render_template('order.html', 
    order=order, 
    totalprice=totalprice, 
    category=category)

# Delete a cart item
@bp.route('/deleteorderitem', methods=['POST'])
def deleteorderitem():
    id=request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        product_to_delete = Product.query.get(id)
        try:
            order.watches.remove(product_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except Exception as e:
            print(e)
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

# Scrap basket
@bp.route('/deleteorder')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))


# for adding products to cart after clicking add to cart button
@bp.route('/cart/add/<productId>')
def addToCart(productId):
    cart_items = request.sesion.get("cart_items")
    cart_items.append(productId)
    request.session.set("cart_items", cart_items)
    return redirect('index')


# route for checkout page
@bp.route('/checkout', methods=['POST','GET'])
def checkout():
    category = Category.query.order_by(Category.name).all()
    form = CheckoutForm() 
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.lastname = form.lastname.data
            order.address = form.address.data
            order.postcode = form.postcode.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for product in order.watches:
                totalcost = totalcost + product.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('Thank you for shopping with MeWatch! You will be contacted soon...')
                return redirect(url_for('main.index'))
            except:
                return 'Oops! We had a problem completing your order'
    return render_template('checkout.html', form = form, category = category)
