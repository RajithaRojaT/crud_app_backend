from fastapi import Depends, FastAPI
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Item
from sqlalchemy.orm import Session
from database import get_db
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
# The line `app.mount("/uploads", staticfiles.StaticFiles(directory="uploads"))` is mounting a
# directory named "uploads" to the "/uploads" path in the FastAPI application. This allows the FastAPI
# application to serve static files from the specified directory. In this case, any files stored in
# the "uploads" directory will be accessible via the "/uploads" URL path in the application.
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

class ItemBase(BaseModel):
    name: str
    description: str
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
@app.post("/items_create")
def create_item(item : ItemBase, db:Session=Depends(get_db)):
    create_item = Item(name=item.name, description=item.description)
    db.add(create_item)
    db.commit()
    return {"success": True, "message": "Items Created Successfully"}

@app.get("/")
def get_all_items(db:Session=Depends(get_db)):
    all_items = db.query(Item).all()
    return all_items

@app.put("/update_item/{id}")
def update_items(id: int, item: ItemBase, db: Session = Depends(get_db)):
    filter_item = db.query(Item).filter(Item.id == id).first()
    
    if filter_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    filter_item.name = item.name
    filter_item.description = item.description
    
    db.commit()
    db.refresh(filter_item)
    
    return {"success": True, "message": "Updated successfully"}

@app.delete("/delete/{id}")
def delete_items(id:int, db:Session=Depends(get_db)):
    deleted_item= db.query(Item).filter(Item.id==id).first()
    if deleted_item is None: 
        raise HTTPException(status_code=404, detail= "Item does not exist")
        
    db.delete(deleted_item)
    db.commit()
    
    return {"success": True, "message": "Item deleted successfully"}

    
