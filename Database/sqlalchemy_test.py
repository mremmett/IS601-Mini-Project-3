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


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    person = relationship("Customer", backref="addresses")


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a customer
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

# Insert an Address in the address table using a loop

addresses = [
   # Address(post_code='00001', person=new_person1),
   # Address(post_code='00002', person=new_person2),
   # Address(post_code='00003', person=new_person3),
]

# Loop through addresses and commit them to the database
for address in addresses:
    session.add(address)
    session.commit()

# joins Person on Address
all_people = session.query(Person).join(Address).all()

# Accessing a person with their address, You have to loop the addresses property and remember it was added by the
# backref on the addresses class
for person in all_people:
    # use the __dict__ magic method to have the object print it's properties
    pprint(person.__dict__)
    for address in person.addresses:
        pprint(address.__dict__)

# Retrieving the inverse of the relationship.  Notice I reverse the Person and Address to load the Address table
all_addresses = session.query(Address).join(Person).all()
for address in all_addresses:
    # showing how to use the print function with printing text and data at the same time easily
    print(f'{address.person.name} has a postal code of {address.post_code}')
