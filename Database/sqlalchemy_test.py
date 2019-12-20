from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pprint import pprint

engine = create_engine('sqlite:////web/Sqlite-Data/example.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

session = Session()


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    town = Column(String(250), nullable=False)


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    cost_price = Column(Integer, nullable=False)
    selling_price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    line_items = relationship("OrderLine", backref='order')

class OrderLine(Base):
    __tablename__ = 'orderline'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    quantity = Column(Integer)


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


c1 = Customer(first_name='Toby',
              last_name='Miller',
              username='tmiller',
              email='tmiller@example.com',
              address='1662 Kinney Street',
              town='Wolfden'
              )

c2 = Customer(first_name='Scott',
              last_name='Harvey',
              username='scottharvey',
              email='scottharvey@example.com',
              address='424 Patterson Street',
              town='Beckinsdale'
              )
c1, c2

session.add(c1)
session.add(c2)

c1.id, c2.id

session.commit()

c3 = Customer(
    first_name="John",
    last_name="Lara",
    username="johnlara",
    email="johnlara@mail.com",
    address="3073 Derek Drive",
    town="Norfolk"
)

c4 = Customer(
    first_name="Sarah",
    last_name="Tomlin",
    username="sarahtomlin",
    email="sarahtomlin@mail.com",
    address="3572 Poplar Avenue",
    town="Norfolk"
)

c5 = Customer(first_name='Toby',
              last_name='Miller',
              username='tmiller',
              email='tmiller@example.com',
              address='1662 Kinney Street',
              town='Wolfden'
              )

c6 = Customer(first_name='Scott',
              last_name='Harvey',
              username='scottharvey',
              email='scottharvey@example.com',
              address='424 Patterson Street',
              town='Beckinsdale'
              )

session.add_all([c3, c4, c5, c6])
session.commit()

i1 = Item(name='Chair', cost_price=9.21, selling_price=10.81, quantity=5)
i2 = Item(name='Pen', cost_price=3.45, selling_price=4.51, quantity=3)
i3 = Item(name='Headphone', cost_price=15.52, selling_price=16.81, quantity=50)
i4 = Item(name='Travel Bag', cost_price=20.1, selling_price=24.21, quantity=50)
i5 = Item(name='Keyboard', cost_price=20.1, selling_price=22.11, quantity=50)
i6 = Item(name='Monitor', cost_price=200.14, selling_price=212.89, quantity=50)
i7 = Item(name='Watch', cost_price=100.58, selling_price=104.41, quantity=50)
i8 = Item(name='Water Bottle', cost_price=20.89, selling_price=25, quantity=50)

session.add_all([i1, i2, i3, i4, i5, i6, i7, i8])
session.commit()

o1 = Order(customer=c1)
o2 = Order(customer=c1)

line_item1 = OrderLine(order=o1, item=i1, quantity=3)
line_item2 = OrderLine(order=o1, item=i2, quantity=2)
line_item3 = OrderLine(order=o2, item=i1, quantity=1)
line_item3 = OrderLine(order=o2, item=i2, quantity=4)

session.add_all([o1, o2])

session.new
session.commit()

o3 = Order(customer=c1)
orderline1 = OrderLine(item=i1, quantity=5)
orderline2 = OrderLine(item=i2, quantity=10)

o3.order_lines.append(orderline1)
o3.order_lines.append(orderline2)

session.add_all([o3])

session.commit()

session.query(Customer).all()

pprint(session.query(Customer))

q = session.query(Customer).all()

for c in q:
    pprint(c.id, c.first_name)


session.query(Customer.id, Customer.first_name).all()

session.query(Customer).count()
session.query(Item).count()
session.query(Order).count()

session.query(Customer).first()
session.query(Item).first()
session.query(Order).first()

session.query(Customer).get(1)
session.query(Item).get(1)
session.query(Order).get(100)

session.query(Order).filter(Order.date_shipped == None).all()

session.query(Order).filter(Order.date_shipped != None).all()

session.query(Customer).filter(Customer.first_name.in_(['Toby', 'Sarah'])).all()

session.query(Customer).filter(Customer.first_name.notin_(['Toby', 'Sarah'])).all()

session.query(Item).filter(Item.cost_price.between(10, 50)).all()

# session.query(Item).filter(not_(Item.cost_price.between(10, 50))).all()

session.query(Item).filter(Item.name.like("%r")).all()
session.query(Item).filter(Item.name.ilike("w%")).all()

# session.query(Item).filter(not_(Item.name.like("W%"))).all()

session.query(Customer).limit(2).all()
session.query(Customer).filter(Customer.address.ilike("%avenue")).limit(2).all()

session.query(Customer).limit(2).offset(2).all()

pprint(session.query(Customer).limit(2).offset(2))

session.query(Item).filter(Item.name.ilike("wa%")).all()
session.query(Item).filter(Item.name.ilike("wa%")).order_by(Item.cost_price).all()

# session.query(Item).filter(Item.name.ilike("wa%")).order_by(desc(Item.cost_price)).all()

session.query(Customer).join(Order).all()

pprint(session.query(Customer).join(Order))

session.query(Customer.id, Customer.username, Order.id).join(Order).all()

session.query(Customer).join(Item).join(Order).join(OrderLine).all()

session.query(
    Customer.first_name,
    Item.name,
    Item.selling_price,
    OrderLine.quantity
).join(Order).join(OrderLine).join(Item).filter(
    Customer.first_name == 'John',
    Customer.last_name == 'Green',
    Order.id == 1,
).all()

session.query(
    Customer.first_name,
    Order.id,
).outerjoin(Order).all()
session.query(
    Customer.first_name,
    Order.id,
).outerjoin(Order, full=True).all()

from sqlalchemy import func

session.query(func.count(Customer.id)).join(Order).filter(
    Customer.first_name == 'John',
    Customer.last_name == 'Green',
).group_by(Customer.id).scalar()

session.query(
    func.count("*").label('town_count'),
    Customer.town
).group_by(Customer.town).having(func.count("*") > 2).all()

from sqlalchemy import distinct

session.query(Customer.town).filter(Customer.id < 10).all()
session.query(Customer.town).filter(Customer.id < 10).distinct().all()

session.query(
    func.count(distinct(Customer.town)),
    func.count(Customer.town)
).all()

from sqlalchemy import cast, Date, distinct, union

session.query(
    cast(func.pi(), Integer),
    cast(func.pi(), Numeric(10, 2)),
    cast("2010-12-01", DateTime),
    cast("2010-12-01", Date),
).all()

s1 = session.query(Item.id, Item.name).filter(Item.name.like("Wa%"))
s2 = session.query(Item.id, Item.name).filter(Item.name.like("%e%"))
s1.union(s2).all()

s1.union_all(s2).all()

session.query(Item).filter(
    Item.name.ilike("W%")
).update({"quantity": 60}, synchronize_session='fetch')
session.commit()

session.query(Item).filter(
    Item.name.ilike("W%")
).delete(synchronize_session='fetch')
session.commit()

from sqlalchemy import text

session.query(Customer).filter(text("first_name = 'John'")).all()

session.query(Customer).filter(text("town like 'Nor%'")).all()

session.query(Customer).filter(text("town like 'Nor%'")).order_by(text("first_name, id desc")).all()

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def dispatch_order(order_id):
    # check whether order_id is valid or not
    order = session.query(Order).get(order_id)

    if not order:
        raise ValueError("Invalid order id: {}.".format(order_id))

    if order.date_shipped:
        pprint("Order already shipped.")
        return

    try:
        for i in order.order_lines:
            i.item.quantity = i.item.quantity - i.quantity

        order.date_shipped = datetime.now()
        session.commit()
        pprint("Transaction completed.")

    except IntegrityError as e:
        pprint(e)
        pprint("Rolling back ...")
        session.rollback()
        pprint("Transaction failed.")

dispatch_order(1)
dispatch_order(2)

session.query(Customer).filter(and_(
    Customer.first_name == 'John',
    not_(
        Customer.town == 'Peterbrugh',
    )
)).all()


