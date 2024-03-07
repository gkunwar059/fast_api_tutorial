from database import Base,engine
from sqlalchemy import String,Boolean,Integer,Column,Text
from sqlalchemy.orm import Mapped,MappedColumn,mapped_column

Base.metadata.create_all(engine)

class Item(Base):
        __tablename__='items'
        
        id:Mapped[int]=mapped_column(primary_key=True,autoincrement=True)
        name:Mapped[str]=mapped_column(nullable=False,unique=True)
        description:Mapped[str]=mapped_column(Text,nullable=False)
        price:Mapped[int]=mapped_column(nullable=False)
        on_offer:Mapped[bool]=mapped_column(default=False)
        
        
        # def __repr__(self):
        #     return f"<Item name={self.name} price={self.price}>"

        
        
        
    