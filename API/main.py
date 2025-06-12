from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form
from tortoise.contrib.fastapi import register_tortoise
from models import (supplier_pydantic, supplier_pydanticIn, Supplier,
                    product_pydanticIn, product_pydantic, Product)
from starlette.responses import JSONResponse
from starlette.requests import Request
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List
from pydantic import BaseModel, EmailStr
from dotenv import dotenv_values
from fastapi.middleware.cors import  CORSMiddleware


credentials = dotenv_values("../.env")

app = FastAPI()

# Middleware for CORS
origins = [
    "http://localhost:3000",
]

#add CORS middleware to allow requests from specified origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.get("/products")
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
    old_product.quantity_sold += update_info["quantity_sold"]
    old_product.unit_price = update_info["unit_price"]
    old_product.revenue += update_info["unit_price"] * update_info["quantity_sold"]
    await old_product.save()
    response = await product_pydantic.from_tortoise_orm(old_product)
    return {"status": "ok", "data": response}

@app.delete("/product/{product_id}")
async def delete_product(product_id: int):
    product = await Product.get(id=product_id)
    await product.delete()
    return {"status": "ok", "message": "Product deleted successfully."}


class EmailSchema(BaseModel):
    email: List[EmailStr]

class EmailContent(BaseModel):
    subject: str
    body: str

conf = ConnectionConfig(
    MAIL_USERNAME=credentials["EMAIL"],
    MAIL_PASSWORD=credentials["PASSWORD"],
    MAIL_FROM=credentials["EMAIL"],
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
)

@app.post("/email/{product_id}")
async def send_email(product_id: int, content: EmailContent):
    product = await Product.get(id=product_id)
    supplier = await product.supplied_by
    supplier_email = [supplier.email]

    html = """
    <h5>Thanks for using Fastapi-mail</h5> 
    <br> 
    <p>{content.body}</p>
    <br>
    <h3>Best Regards</h3>
    """
    message = MessageSchema(
        subject=content.subject,
        recipients=supplier_email,
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

# Register Tortoise ORM with FastAPI
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)