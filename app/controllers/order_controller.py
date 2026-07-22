from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.repositories.product_repository import ProductRepository

router = APIRouter(prefix="/orders", tags=["Orders"])

# Schema Validasi Request Body
class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

class CreateOrderSchema(BaseModel):
    user_id: int
    items: List[OrderItemSchema]

@router.post("/")
def create_order(payload: CreateOrderSchema):
    try:
        # Convert schema items ke list of dict
        items_dict = [item.dict() for item in payload.items]
        
        result = ProductRepository.create_order_transaction(
            user_id=payload.user_id,
            items=items_dict
        )
        
        return {
            "status": "success",
            "message": "Order berhasil dibuat!",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{order_id}")
def get_order_detail(order_id: int):
    try:
        order = ProductRepository.get_order_detail(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order tidak ditemukan")
        
        return {
            "status": "success",
            "data": order
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))