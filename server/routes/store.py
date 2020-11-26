import json

from flask import Blueprint, session, request
from sqlalchemy.sql import func
from server.models import Store, Transaction, Item
from server import db

store_bp = Blueprint("store_bp", __name__, url_prefix="/api/store")

def valid_funds(user_id, item_id):
    total_tickets = (
        db.session.query(func.sum(Transaction.ticket_amount))\
        .filter(Transaction.user_id == user_id)
        .scalar()
    )
    item_price = Store.query.filter_by(id=item_id).first().price
    if total_tickets is None or item_price is None:
        return False
    return total_tickets >= item_price

def item_available(user_id, item_id):
    item_info = Store.query.filter_by(id=item_id).first()
    item_query = Item.query.filter_by(user_id=user_id, item_type=item_id).first()
    if item_query is not None and item_query.count >= item_info.limit:
        return False
    return True

def make_purchase(user_id, item_id):
    item_info = Store.query.filter_by(id=item_id).first()
    transaction = Transaction(
        user_id=user_id,
        ticket_amount=item_info.price,
        activity="ticketstore",
    )
    db.session.add(transaction)
    item_query = Item.query.filter_by(user_id=user_id, item_type=item_id).first()
    if item_query is None:
        item = Item(
            item_type = item_id,
            item_group = item_info.item_group,
            user_id = user_id,
        )
        db.session.add(item)
    else:
        item_query.count = item.query.count + 1
    db.session.commit()

@store_bp.route("/list", methods=["GET"])
def store_list():
    store_items = []
    for item in Store.query.all():
        item_obj = {
            "id": item.id,
            "name": item.name,
            "group": item.item_group,
            "limit": item.limit,
            "price": item.price,
        }
        store_items.append(item_obj)

    return {"items": store_items}

@store_bp.route("/buy", methods=["POST"])
def buy_item():
    try:
        data = json.loads(request.data)
        item_id = data["item_id"]
        user_id = session["user_id"]
        if not valid_funds(user_id, item_id):
            return {"success": False, "message": "Insufficient funds"}
        if not item_available(user_id, item_id):
            return {"success": False, "message": "Reached purchase limit"}
        make_purchase(user_id, item_id)
        return {"success": True}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400
