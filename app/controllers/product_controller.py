from fastapi import APIRouter, HTTPException, Request  
from fastapi.encoders import jsonable_encoder
from app.core.limiter import limiter
from app.repositories.product_repository import ProductRepository

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
@limiter.limit("5/minute")  
def get_products(request: Request):  
    try:
        products = ProductRepository.get_all_products()
        return {
            "status": "success",
            "data": jsonable_encoder(products)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}")
@limiter.limit("10/minute")  
def get_product_detail(request: Request, product_id: int):  
    try:
        product = ProductRepository.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
        
        return {
            "status": "success",
            "data": product
        }
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))