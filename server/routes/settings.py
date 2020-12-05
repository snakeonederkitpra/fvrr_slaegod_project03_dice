import json
import os

from flask import request, session, Blueprint
from werkzeug.utils import secure_filename
from server.routes.decorators import login_required
from server.utils.item_helper import (
    item_group_by_user_id,
    handle_text_color,
    handle_username_change
)


settings_bp = Blueprint("settings_bp", __name__)

@settings_bp.route("/api/settings/get", methods=["GET"])
@login_required
def update_settings():
    user_id = session["user_id"]
    colors = []
    change_username_bool = False
    change_profile_pic_bool = False
    text_colors = item_group_by_user_id(user_id, 101)
    if text_colors is not None:
        for text_color in text_colors:
            colors.append({
                "item_type": text_color.item_type,
                "name": text_color.name,
                "active": text_color.active
            })
    if item_group_by_user_id(user_id, 102) is not None:
        change_username_bool = True
    if item_group_by_user_id(user_id, 107) is not None:
        change_profile_pic_bool = True
    return {
        "success": True,
        "text_color": colors,
        "change_username": change_username_bool,
        "change_profile_pic": change_profile_pic_bool
    }

@settings_bp.route("/api/settings/textcolor", methods=["POST"])
@login_required
def change_text_color():
    try:
        data = json.loads(request.data)
        item_type = data["item_type"]
        user_id = session["user_id"]
        handle_text_color(user_id, item_type)
        return {"success": True}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

@settings_bp.route("/api/settings/username", methods=["POST"])
@login_required
def change_username():
    try:
        data = json.loads(request.data)
        username = data["username"]
        user_id = session["user_id"]
        if handle_username_change(user_id, username):
            return {"success": True}
        return {"success": False, "message": "username already taken"}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400

@settings_bp.route("/api/settings/profilepic", methods=["POST"])
@login_required
def chnage_profile_pic():
    try:
        data = request.files
        image_data = data["file"]
        user_id = session["user_id"]
        image_data.filename = "profile" + str(user_id) + ".png"
        filename = secure_filename(image_data.filename)
        current_path = os.path.dirname(os.path.realpath(__file__))
        root_path = os.path.sep.join(current_path.split(os.path.sep)[:-2])
        static_folder = "/public/static/"
        path = root_path + static_folder + filename
        image_data.save(path)
        return {"success": True}
    except json.decoder.JSONDecodeError:
        return {"error": "Malformed request"}, 400
