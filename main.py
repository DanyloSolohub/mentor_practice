from sqlalchemy import Column, Integer, String, func
from sqlalchemy import create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://root:root@127.0.0.1:5432/test_orm')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency

session = SessionLocal()

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)

    @hybrid_property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @full_name.expression
    def full_name(cls):
        return func.concat(cls.first_name, " ", cls.last_name)

    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name}'


if __name__ == '__main__':
    query = session.query(Person).filter(Person.full_name == 'Вадим Бойко')
    print(query.scalar())
