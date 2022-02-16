from pyexpat import model
from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel
from typing import Optional,List
from database import SessionLocal
import models

app=FastAPI()

# Model
class Item(BaseModel):
    id:int
    name:str
    description:str
    price:int
    on_offer:bool

    class Config:
        orm_mode=True

# Déclarer la session
db=SessionLocal()

# Endpoint GET: obtenir toutes les items
@app.get('/items', response_model=List[Item],status_code=200)
async def get_all_items():
    items=db.query(models.Item).all()

    return items

# Endpoint GET: obtenir un item via son id
@app.get('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
async def get_an_item(item_id:int):
    item=db.query(models.Item).filter(models.Item.id==item_id).first()
    return item

# Endpoint POST: créer un item
@app.post('/items',response_model=Item,status_code=status.HTTP_201_CREATED)
async def create_an_item(item:Item):

    # Vérification sur le nom existe dans la BD
    db_item= db.query(models.Item).filter(models.Item.name==item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400,detail="Cet item existe déjà !")

    new_item=models.Item(
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer
    )

    db.add(new_item)
    db.commit()
    
    return new_item


# Endpoint PUT: modifier un item
@app.put('/item/{item_id}',response_model=Item,status_code=status.HTTP_200_OK)
async def update_an_item(item_id:int,item:Item):
    item_to_update=db.query(models.Item).filter(models.Item.id==item_id).first()
    item_to_update.name=item.name
    item_to_update.price=item.price
    item_to_update.description=item.description
    item_to_update.on_offer=item.on_offer

    db.commit()

    return {"OK"}

# Endpoint  DELETE: Supprimer un item
@app.delete('/item/{item_id}')
async def update_an_item(item_id:int):
    item_to_delete=db.query(models.Item).filter(models.Item.id==item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cet item n'existe pas !")

    db.delete(item_to_delete)
    db.commit()
    return {"Suppression réussite !"}


