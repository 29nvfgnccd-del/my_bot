from flask import Flask, request, jsonify

app = Flask(__name__)

menu = [
    {"id": 1, "name": "Плов",      "category": "main",  "price": 40, "available": True},
    {"id": 2, "name": "Шурпа",     "category": "soup",  "price": 30, "available": True},
    {"id": 3, "name": "Самса",     "category": "snack", "price": 10, "available": True},
    {"id": 4, "name": "Чай",       "category": "drink", "price": 5,  "available": True},
    {"id": 5, "name": "Кофе",      "category": "drink", "price": 15, "available": False},
]

@app.route("/menu", methods=["GET"])
def get_menu():
    return jsonify(menu)

@app.route("/menu/<int:id>", methods=["GET"])
def get_dish(id):
    for dish in menu:
        if dish["id"] == id:
            return jsonify(dish)
    return jsonify({"error": "Блюдо не найдено"}), 404


if __name__ == "__main__":
    app.run(debug=True)