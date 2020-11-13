from flask import session
from sqlalchemy.orm.exc import NoResultFound
from server import app, db
from server.models.transaction import Transaction


@app.route("/api/tickethistory/", defaults={"user_id": None})
@app.route("/api/tickethistory/<user_id>")
def get_transaction_history(user_id):
    # session['user_id'] = '1' # delete in future (off for unittest) (on for webpage)
    if user_id is None and "user_id" in session:
        user_id = session["user_id"]

    if "user_id" in session:
        if user_id == session["user_id"]:
            try:
                ticket_history = (
                    db.session.query(Transaction)
                    .filter(Transaction.user_id == user_id)
                    .all()
                )
                ticket_rows = []
                for row in ticket_history:
                    ticket_rows.append(
                        {
                            "id": row.id,
                            "datetime": row.datetime,
                            "activity": row.activity,
                            "amount": row.ticket_amount,
                        }
                    )
                return {"ticketTransaction": ticket_rows}
            except NoResultFound:
                no_history = []
                return {"ticketTransaction": no_history}
        else:
            invalid_history = []
            return {"ticketTransaction": invalid_history}
    else:
        return {"error": "client not suppose to be here"}, 404
