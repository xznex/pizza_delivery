from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from fastapi.exceptions import HTTPException
from database import Session, engine
from fastapi.encoders import jsonable_encoder


order_router = APIRouter(
    prefix="/orders",
    tags=['orders']
)

session = Session(bind=engine)


@order_router.get("/")
async def hello(authorize: AuthJWT = Depends()):
    """
        ## A sample hello world route
        This returns hello world
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")
    return {"message": "Hello World"}


@order_router.post("/order", status_code=status.HTTP_201_CREATED, )
async def place_an_order(order: OrderModel, authorize: AuthJWT = Depends()):
    """
        ## Placing an Order
        This requires the following
        - quantity: integer
        - pizza_size: str
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")

    current_user = authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
    )

    new_order.user = user

    session.add(new_order)

    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)


@order_router.get("/orders")
async def list_all_orders(authorize: AuthJWT = Depends()):
    """
        ## List all orders
        This lists all orders made. It can be accessed by superusers
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")

    current_user = authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()

        return jsonable_encoder(orders)

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You are not a superuser")


@order_router.get("/orders/{order_id}")
async def retrieve_an_order(order_id: int, authorize: AuthJWT = Depends()):
    """
        ## Get an order by its ID
        This gets an order by its ID and is only accessed by a superuser
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")

    current_user = authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        order = session.query(Order).filter(Order.id == order_id).first()

        return jsonable_encoder(order)

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You are not a superuser")


@order_router.get("/user/orders")
async def user_orders(authorize: AuthJWT = Depends()):
    """
        ## Get a current user's orders
        This lists the orders made by the currently logged in users
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")

    current_user = authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    return jsonable_encoder(user.orders)


@order_router.get("/user/order/{order_id}")
async def specific_user(order_id: int, authorize: AuthJWT = Depends()):
    """
        ## Get a specific order by the currently logged in user
        This returns an order by ID for the currently logged in user
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")

    current_user = authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    orders = user.orders

    for order in orders:
        if order.id == order_id:
            return jsonable_encoder(order)

    raise HTTPException(status.HTTP_400_BAD_REQUEST, "No order with such id")


@order_router.put("/order/update/{order_id}")
async def update_order(order_id: int, order: OrderModel, authorize: AuthJWT = Depends()):
    """
        ## Updating an order
        This updates an order and requires the following fields
        - quantity : integer
        - pizza_size: str
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")

    order_to_update = session.query(Order).filter(Order.id == order_id).first()

    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size
    order_to_update.flavour = order.flavour

    session.commit()

    response = {
        "id": order_to_update.id,
        "quantity": order_to_update.quantity,
        "pizza_size": order_to_update.pizza_size,
        "order_status": order_to_update.order_status
    }

    return jsonable_encoder(response)


@order_router.patch("/order/status/{order_id}")
async def update_order_status(order_id: int, order: OrderStatusModel, authorize: AuthJWT = Depends()):
    """
        ## Update an order's status
        This is for updating an order's status and requires ` order_status ` in str format
    """
    print(f"\n\n\n{order}\n\n\n")

    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")

    current_user = authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == order_id).first()

        order_to_update.order_status = order.order_status

        session.commit()

        response = {
            "id": order_to_update.id,
            "quantity": order_to_update.quantity,
            "pizza_size": order_to_update.pizza_size,
            "order_status": order_to_update.order_status
        }

        return jsonable_encoder(response)

    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You are not a superuser")


@order_router.delete("/order/delete/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, authorize: AuthJWT = Depends()):
    """
        ## Delete an Order
        This deletes an order by its ID
    """
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Token")

    order_to_delete = session.query(Order).filter(Order.id == order_id).first()

    session.delete(order_to_delete)

    session.commit()

    return order_to_delete
