"""Illustrates a mixin which provides a generic association
using a single target table and a single association table,
referred to by all parent tables.  The association table
contains a "discriminator" column which determines what type of
parent object associates to each particular row in the association
table.

SQLAlchemy's single-table-inheritance feature is used
to target different association types.

This configuration attempts to simulate a so-called "generic foreign key"
as closely as possible without actually foregoing the use of real
foreign keys.   Unlike table-per-related and table-per-association,
it uses a fixed number of tables to serve any number of potential parent
objects, but is also slightly more complex.

"""
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Table


    
@as_declarative()
class Base(object):
    """Base class which provides automated table name
    and surrogate primary key column.

    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

address_parent_association = Table('address_parent_association', Base.metadata,
    Column('id',Integer, primary_key=True),
    Column('address_id', Integer, ForeignKey('address.id')),
    Column('parent_association_id', Integer, ForeignKey('parent_association.id'))
    )
    
class ParentAssociation(Base):
    """Associates a collection of Address objects
    with a particular parent.

    """

    __tablename__ = "parent_association"

    discriminator = Column(String)
    """Refers to the type of parent."""

    __mapper_args__ = {"polymorphic_on": discriminator}


class Address(Base):
    """The Address class.

    This represents all address records in a
    single table.

    """

    #association_id = Column(Integer, ForeignKey("parent_association.id"))
    street = Column(String)
    city = Column(String)
    zip = Column(String)
    association = relationship("ParentAssociation",secondary=address_parent_association, backref="addresses")

    parent = association_proxy("association", "parent")

    def __repr__(self):
        return "%s(street=%r, city=%r, zip=%r)" % (
            self.__class__.__name__,
            self.street,
            self.city,
            self.zip,
        )


class HasAddresses(object):
    """HasAddresses mixin, creates a relationship to
    the parent_association table for each parent.

    """

    @declared_attr
    def parent_association_id(cls):
        return Column(Integer, ForeignKey("parent_association.id"))

    @declared_attr
    def parent_association(cls):
        name = cls.__name__
        discriminator = name.lower()

        assoc_cls = type(
            "%sParentAssociation" % name,
            (ParentAssociation,),
            dict(
                __tablename__=None,
                __mapper_args__={"polymorphic_identity": discriminator},
            ),
        )

        cls.addresses = association_proxy(
            "parent_association",
            "addresses",
            creator=lambda addresses: assoc_cls(addresses=addresses),
        )
        return relationship(
            assoc_cls, backref=backref("parent", uselist=True) #多對多: True
        )


class Customer(HasAddresses, Base):
    name = Column(String)


class Supplier(HasAddresses, Base):
    name = Column(String)

def init_db():
    engine = create_engine("sqlite:///address.db", echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = Session(engine)
    add_1 = Address(street="光復路71號", city="新竹", zip="303")
    session.add(add_1)
    session.add_all(
        [
            Customer(
                name="customer 1",
                addresses=[
                    Address(
                        street="123 anywhere street", city="New York", zip="10110"
                    ),
                    Address(
                        street="40 main street", city="San Francisco", zip="95732"
                    ),
                    add_1,
                ],
            ),
            Supplier(
                name="Ace Hammers",
                addresses=[
                    Address(street="2569 west elm", city="Detroit", zip="56785"),
                    add_1,
                ],
            ),
        ]
    )

    session.commit()
    """
    for customer in session.query(Customer):
        for address in customer.addresses:
            print(address)
            print(address.parent)
    """
def add_address():
    engine = create_engine("sqlite:///address.db", echo=False)
    session = Session(engine)
    session.add(
                Customer(
                    name="customer 2",
                    addresses=[
                        session.query(Address).get(1)])
    )
    session.commit()

def query_test():

    engine = create_engine("sqlite:///address.db", echo=False)
    session = Session(engine)
    for add in session.query(Address):
        print(f'{add.id}-{add.street}')
        for item in add.parent:
            for p in item:
                #print(dir(p))
                print('-----'+p.name+','+str(p.id)+','+p.parent_association.discriminator)
        for item in add.association:
            pass
            #print(p.parent_association) #dir(p))
        
                
if __name__ == "__main__":
    add_address()
    query_test()
            