from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import (supplier_pydantic, supplier_pydanticIn, Supplier,
                    product_pydanticIn, product_pydantic, Product)


app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello, World!"}

@app.post("/supplier")
async def add_supplier(supplier_info: supplier_pydanticIn):
    supplier_object = await Supplier.create(**supplier_info.dict(exclude_unset=True))
    response = await supplier_pydantic.from_tortoise_orm(supplier_object)
    return {"status": "ok", "data": response}


@app.get("/supplier")
async def get_all_suppliers():
    response = await supplier_pydantic.from_queryset(Supplier.all())
    return {"status": "ok", "data": response}

@app.get("/supplier/{supplier_id}")
async def get_specific_supplier(supplier_id: int):
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
    return {"status": "ok", "data": response}

@app.put("/supplier/{supplier_id}")
async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn):
    supplier = await Supplier.get(id=supplier_id)
    update_info = update_info.dict(exclude_unset=True)
    supplier.name = update_info["name"]
    supplier.company = update_info["company_name"]
    supplier.phone = update_info["phone"]
    supplier.email = update_info["email"]
    await supplier.save()
    response = await supplier_pydantic.from_tortoise_orm(supplier)
    return {"status": "ok", "data": response}

@app.delete("/supplier/{supplier_id}")
async def delete_supplier(supplier_id: int):
    supplier = await Supplier.get(id=supplier_id)
    await supplier.delete()
    return {"status": "ok", "message": "Supplier deleted successfully."}

@app.post("/product/{supplier_id}")
async def add_product(supplier_id: int, product_details: product_pydanticIn):
    supplier = await Supplier.get(id=supplier_id)
    product = product_details.dict(exclude_none=True)
    product["revenue"] += product["unit_price"] * product["quantity_sold"]
    product_obj = await Product.create(**product, supplied_by=supplier)
    response = await product_pydantic.from_tortoise_orm(product_obj)
    return {"status": "ok", "data": response}

@app.get("/product")
async def get_all_products():
    response =  await product_pydantic.from_queryset(Product.all())
    return {"status": "ok", "data": response}

@app.get("/product/{product_id}")
async def get_specific_product(product_id: int):
    response = await product_pydantic.from_queryset_single(Product.get(id=product_id))
    return {"status": "ok", "data": response}

@app.put("/product/{product_id}")
async def update_product(product_id: int, update_info: product_pydanticIn):
    old_product = await Product.get(id=product_id)
    update_info = update_info.dict(exclude_unset=True)
    old_product.name = update_info["name"]
    old_product.quantity_in_stock = update_info["quantity_in_stock"]
    old_product.quantity_sold = update_info["quantity_sold"]
    old_product.unit_price = update_info["unit_price"]
    old_product.revenue += update_info["unit_price"] * update_info["quantity_sold"]
    await old_product.save()
    response = await product_pydantic.from_tortoise_orm(old_product)
    return {"status": "ok", "data": response}

# Register Tortoise ORM with FastAPI
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)