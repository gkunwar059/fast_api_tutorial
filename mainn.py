from fastapi import FastAPI,status,HTTPException,Path
from pydantic import BaseModel
from typing import Optional,List
from database import session,engine
from models import Item
from fastapi.responses import JSONResponse


app=FastAPI()

class ItemSchema(BaseModel):     #serializers
    name:str
    description:str
    price:int
    on_offer:bool

# When orm_mode = True is set in Pydantic's Config class, it allows Pydantic models to:
    # Automatically convert data types: Pydantic will attempt to automatically convert data types when parsing data from an ORM system. For example, if an integer value is passed as a string in the input data, Pydantic will automatically convert it to an integer.
    # Skip validation for missing fields: Pydantic will skip validation for fields that are missing in the input data. This is useful because ORM systems may not always populate all fields in the model when retrieving data from the database.
   
   
    class Config:
        force_mode=True
        
 
       
# api methods here  
@app.get("/items/",response_model=List[ItemSchema],status_code=status.HTTP_200_OK)
def get_all_item():
    items=session.query(Item).all()
    return items


@app.get('/item/{item_id}',response_model=ItemSchema,status_code=status.HTTP_200_OK)
def get_an_item(item_id:int):
    item= session.query(Item).filter_by(id=item_id).first()
    return item


@app.post('/items',status_code=status.HTTP_201_CREATED)
def create_an_item(item:ItemSchema):
    new_item=Item(
        name=item.name,
        description=item.description,
        price=item.price,
        on_offer=item.on_offer
           
           
    )
   
   
#    yesma chai hamle hamro model class ma vayeko name lai chai tyo pydantic class ma rakheko jun naya hunxa milxa vane chai filter lahinxa hai ta ,
# compare garda chai 2 ota lai chai compare garnu parxa name vaneko chai model class ko name bayo ani item.name baneko chai aaile haleko pydontic class ko vaho hai ta 
   
   
    db_item=session.query(Item).filter_by(name=item.name).first()
    if db_item is not None :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Item already exists")
    
    session.add(new_item)
    session.commit()
    return new_item


    
@app.put("/item/{name}")
def update_item(name,item:ItemSchema):
    item_to_update=session.query(Item).filter_by(name=name).first()
    
    # return{item_to_update.name}
    if item_to_update:  #update garda hamle name chai check garnu parxa, if tyo update garnu parne database ma bheteko ko name ma chai hamle pydonticmodel ma vayeko item ko name cHAI RAKHNU PARXA TODO IT MEAN that paxi rakhne ko ne location dinu parxa hai ta 
        item_to_update.name=item.name
        item_to_update.description=item.description   #update garda chai update k garne ani k ma update garne vanne hunxa 
        #so update garda chai location pani dinu parxa hai ta yo (post gareko vanda farak hunxa hai ta ) 
        item_to_update.price=item.price
        item_to_update.on_offer=item.on_offer
        
        session.commit()
        return item_to_update
    
    else:
        return  JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"Item not Found"})
    
# lets use the exception handling to 
@app.delete("/item/{name}")
# yo validation rakhna ekdam important xa when user click url without having the any values 
def delete_item(name:str=Path(...,title="please enter the item name ",min_length=1)):
    try:
        delete_item= session.query(Item).filter_by(name=name).delete()
        session.commit()
        
        if delete_item==0:
            raise HTTPException(status_code=404,detail="Item not Found ") 
        #yesto hunxa if condition right vayo vane chai  loop vitra janxa and if not bahera ko kura chai right hunxa vitra ko condition sangha kei farak mildaina 
        return {"message":"Item deleted successfully "} # yesle chai mathi ko conditon false hunuparyo  ra mathi ko operation haru le kam gareko ho vanna milnu paryo 
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500,detail="Failed to delete item:"+str(e))




    

        