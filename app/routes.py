from app import app
import os
from flask import request, render_template
from .agent import get_agent


@app.route("/")
def home():
    media_files = os.listdir(app.config["OUTPUT_DIR"])
    return render_template('Index.html', media_files=media_files)


@app.route("/query", methods=["GET"])
def chat():
    query_text = request.args.get("text", None)
    if query_text is None:
        return (
            "No text found, please include a ?text=blah parameter in the URL",
            400,
        )

    agent = get_agent()

    response = agent.chat(query_text)
    return str(response), 200

    # chat_engine = get_chat_engine()
    # response = chat_engine.chat(query_text)
    # response = chat_engine.chat(query_text)
    # agent = create_react_agent()
    # return jsonify({"response": response}), 200
    # query_engine = index.as_query_engine()
    # response = query_engine.query(query_text)


@app.route("/get_file_content", methods=["GET"])
def get_file_content():
    file = request.args.get('file')
    file_path = os.path.join(app.config["OUTPUT_DIR"], file)
    with open(file_path, 'r') as f:
        content = f.read()
    return content
