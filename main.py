import json

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from utils import open_file_json, write_file_json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson.db'
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(20))


class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.NVARCHAR)
    description = db.Column(db.NVARCHAR)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


db.drop_all()
db.create_all()


user_data = open_file_json('User.json')
orders_data = open_file_json('Orders.json')
offer_data = open_file_json('Offers.json')

for i in user_data:
    user = User(id=i['id'], first_name=i['first_name'], last_name=i['last_name'],
                age=i['age'], email=i['email'], role=i['role'], phone=i['phone'])
    db.session.add(user)

for i in orders_data:
    order = Order(id=i['id'], name=i['name'], description=i['description'],
                  start_date=i['start_date'], end_date=i['end_date'], address=i['address'],
                  price=i['price'], customer_id=i['customer_id'], executor_id=i['executor_id'])
    db.session.add(order)

for i in offer_data:
    offer = Offer(id=i['id'], order_id=i['order_id'], executor_id=i['executor_id'])
    db.session.add(offer)

db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def get_all_users():
    result_request = request.values
    if result_request:
        user = User(id=int(result_request['id']), first_name=result_request['first_name'],
                    last_name=result_request['last_name'],
                    age=int(result_request['age']), email=result_request['email'],
                    role=result_request['role'], phone=result_request['phone'])
        db.session.add(user)
        db.session.commit()
    users_list = User.query.all()
    users = []
    for user in users_list:
        users.append({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "role": user.role,
            "email": user.email,
            "phone": user.phone
        })
    data_json_for_write = json.dumps(users)
    write_file_json('User.json', data_json_for_write)
    result = render_template('add_users.html', users=users)
    return f'{result}'


@app.route('/users/<int:id>', methods=['GET', 'POST'])
def get_users_id(id: int):
    result_request = request.values
    if result_request:
        updated_data = db.session.query(User).get(id)
        new_first_name = updated_data.first_name = result_request['first_name']
        new_last_name = updated_data.last_name = result_request['last_name']
        new_age = updated_data.age = int(result_request['age'])
        new_email = updated_data.email = result_request['email']
        new_role = updated_data.role = result_request['role']
        new_phone = updated_data.phone = result_request['phone']
        db.session.add(updated_data)
        db.session.commit()

    user = User.query.get(id)
    user_id = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "age": user.age,
        "role": user.role,
        "email": user.email,
        "phone": user.phone
    }

    result = render_template('change_user.html', id=id, user_id=user_id, )
    return f'{result}'


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    x = db.session.query(User).get(id)
    db.session.delete(x)
    db.session.commit()
    result = render_template('add_users.html')
    return f' {result}  Пользователь удален'


@app.route('/orders', methods=['GET', 'POST'])
def get_all_orders():
    result_request = request.values
    if result_request:
        order = Order(id=int(result_request['id']), name=result_request['name'], description=result_request['description'],
                      start_date=int(result_request['start_date']), end_date=result_request['end_date'],address=result_request['address'],
                      price=result_request['price'], customer_id=result_request['customer_id'], executor_id=result_request['executor_id'])
        db.session.add(order)
        db.session.commit()
    order_list = Order.query.all()
    orders = []
    for order in order_list:
        orders.append({
            'id': order.id,
            'name': order.name,
            'description': order.description,
            'start_date': order.start_date,
            'end_date': order.end_date,
            'address': order.address,
            'price': order.price,
            'customer_id': order.customer_id,
            'executor_id': order.executor_id,
        })
    data_json_for_write = json.dumps(orders)
    write_file_json('Orders.json', data_json_for_write)
    result = render_template('add_orders.html', orders=orders)
    return f'{result}'




@app.route('/orders/<int:id>', methods=['GET', 'POST'])
def get_orders_id(id: int):
    result_request = request.values
    if result_request:
        updated_data = db.session.query(Order).get(id)
        new_name = updated_data.name = result_request['name']
        new_description = updated_data.description = result_request['description']
        new_start_date = updated_data.start_date = result_request['start_date']
        new_end_date = updated_data.end_date = result_request['end_date']
        new_address = updated_data.address = result_request['address']
        new_price = updated_data.price = result_request['price']
        new_customer_id = updated_data.customer_id = result_request['customer_id']
        new_executor_id = updated_data.executor_id = result_request['executor_id']
        db.session.add(updated_data)
        db.session.commit()

    order = Order.query.get(id)
    order_id = {
        'id': order.id,
        'name': order.name,
        'description': order.description,
        'start_date': order.start_date,
        'end_date': order.end_date,
        'address': order.address,
        'price': order.price,
        'customer_id': order.customer_id,
        'executor_id': order.executor_id,
    }

    result = render_template('change_order.html', id=id, order_id=order_id, )
    return f'{result}'


@app.route('/delete_order/<int:id>', methods=['GET', 'POST'])
def delete_order(id):
    x = db.session.query(Order).get(id)
    db.session.delete(x)
    db.session.commit()
    result = render_template('add_orders.html')
    return f' {result}  Order удален'


@app.route('/offers', methods=['GET', 'POST'])
def get_all_offers():
    result_request = request.values
    if result_request:
        offer = Offer(id=int(result_request['id']), order_id=result_request['order_id'],
                      executor_id=result_request['executor_id'])
        db.session.add(offer)
        db.session.commit()
    offer_list = Offer.query.all()
    offers = []
    for offer in offer_list:
        offers.append({
            'id': offer.id,
            'order_id': offer.order_id,
            'executor_id': offer.executor_id
        })
    data_json_for_write = json.dumps(offers)
    write_file_json('offers.json', data_json_for_write)
    result = render_template('add_offers.html', offers=offers)
    return f'{result}'




@app.route('/offers/<int:id>', methods=['GET', 'POST'])
def get_offer_id(id: int):
    result_request = request.values
    if result_request:
        updated_data = db.session.query(Offer).get(id)
        new_order_id = updated_data.order_id = result_request['order_id']
        new_executor_id = updated_data.executor_id = result_request['executor_id']
        db.session.add(updated_data)
        db.session.commit()

    offer = Offer.query.get(id)
    offer_id = {
        'id': offer.id,
        'order_id': offer.order_id,
        'executor_id': offer.executor_id
    }

    result = render_template('change_offer.html', id=id, offer_id=offer_id, )
    return f'{result}'

@app.route('/delete_offer/<int:id>', methods=['GET', 'POST'])
def delete_offer(id):
    x = db.session.query(Offer).get(id)
    db.session.delete(x)
    db.session.commit()
    result = render_template('add_offers.html')
    return f' {result}  Offer удален'

if __name__ == '__main__':
    app.run()