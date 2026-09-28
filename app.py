from flask import Flask, request, jsonify

app = Flask(__name__)

notes = [
    {
        "id": 1, 
        "title": "Первая заметка",
        "text": "Изучаю Flask"
    }, 
    {
        "id": 2,
        "title":  "Вторая заметка",
        "text": "Учусь создавать API"
    }
]


@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)


@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            return jsonify(note)
    return jsonify({"error": "Заметка не найдена"}), 404

@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Нет данных"}), 400

    title = data.get("title")
    text = data.get("text")

    if not title or not text:
        return jsonify({
            "error": "Поля title и text обязательны"

        }), 400

    new_id = max(note["id"]for note in notes) + 1

    new_note = {
        "id": new_id,
        "title": title,
        "text": text
    }

    notes.append(new_note)
    
    return jsonify(new_note), 201

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return jsonify({"status": "deleted"})
    return jsonify({"error": "Заметка не найдена"}), 404
    


if __name__ == "__main__":
    app.run(debug=True)
