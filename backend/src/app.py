from flask import Flask, jsonify, request, send_from_directory
from flask_session import Session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from database.creation import create_database_and_tables
import database.query as query
#from example_data import get_example
import os
import functions
import json
from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Cambia esto a una clave secreta segura
jwt = JWTManager(app)
create_database_and_tables()


#@app.route('/posts', methods=['GET'])
#def obtener_json(): 
#    return jsonify(get_example("post"))


@app.route('/login', methods=['POST'])
def login_user(): 
    data = request.json
    user_email = data.get('email')
    response = query.login(data)

    if(response["json"]["status"] == "ok"):
        expires = timedelta(hours=24)
        access_token = create_access_token(identity=user_email, expires_delta=expires)
        user_data = query.get_user_data("email", data)
        user_data = user_data["json"]["message"]
        print("DATA TO SEND")
        print(user_data)
        return jsonify({"status": "ok", "message": {"access_token": access_token, "user_data": user_data}})
    else:
        return jsonify(response["json"])


@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    user_exists = query.user_exists("email", data)
    if(user_exists["json"]["message"] == "User exists."):
        return jsonify(user_exists["json"])
    else:
        register_user = query.add_user(data)
        return jsonify(register_user["json"])
    

@app.route('/profile/<int:id>', methods=['GET'])
def get_profile(id):
    user_data = query.get_user_data("id", id)
    return jsonify(user_data["json"])


@app.route('/post', methods=['POST'])
@jwt_required()
def publish_post():
    try:
        current_user_email = get_jwt_identity()
        user_id = query.get_user_data("email", {"email": current_user_email})
        user_id = user_id["json"]["message"]["id"]

        if 'content' in request.form: # Se está enviando contenido JSON
            data = {
                "content": request.form.get('content'),
                "media": "",
                "nsfwPost": request.form.get('nsfwPost'),
                "privatePost": request.form.get('privatePost'),
                "shareId": request.form.get('shareId')
            }

        if 'media' in request.files: # Se están enviando archivos
            functions.create_folder(user_id)
            media_files = request.files.getlist('media')
            media_file_names = []

            for media_file in media_files:
                print("MEDIA FILES: ")
                file_name = secure_filename(media_file.filename)
                media_file_names.append(file_name)
                media_file.save(os.path.join("./src/static/users/", str(user_id), file_name))
            data["media"] = json.dumps(media_file_names)

        response = query.create_post(user_id, data)
        return jsonify(response["json"])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/post_list/<int:target_id>', methods=['GET'])
@jwt_required()
def get_post_list(target_id):
    try:
        current_user_email = get_jwt_identity()
        user_id = query.get_user_data("email", {"email": current_user_email})
        user_id = user_id["json"]["message"]["id"]

        response = query.list_posts(target_id, user_id)
        
        if response["json"]["status"] == "ok":
            return jsonify(response["json"])
        else:
            return jsonify({"status": "error", "message": response["json"]["message"]})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/single_post/<int:target_id>', methods=['GET'])
@jwt_required()
def single_post(target_id):
    try:
        current_user_email = get_jwt_identity()
        user_id = query.get_user_data("email", {"email": current_user_email})
        user_id = user_id["json"]["message"]["id"]

        response = query.get_single_post(target_id)
        
        # Asegurarse de que response["json"]["message"] sea JSON serializable
        return jsonify(response["json"])
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/update_pic/<string:pic_type>', methods={'POST'})
@jwt_required()
def update_pics(pic_type):
    try:
        current_user_email = get_jwt_identity()
        user_id = query.get_user_data("email", {"email": current_user_email})
        user_id = user_id["json"]["message"]["id"]
        pic_name = ""

        if 'media' in request.files:  # Se está enviando un archivo
            print("MEDIA IN REQUEST")
            functions.create_folder(user_id)
            media_file = request.files['media']  # Obtén el archivo de la solicitud
            if media_file:
                file_name = secure_filename(media_file.filename)
                current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M")
                new_file_name = f"{file_name.split('.')[0]}_{current_datetime}.{file_name.split('.')[-1]}"
                media_file.save(os.path.join("./src/static/users/", str(user_id), new_file_name))
                pic_name = new_file_name  # Ahora contiene el nombre del archivo con la fecha y hora
                print("FILENAME", new_file_name)
            response = query.update_pics(user_id, pic_type, pic_name)["json"]
        else:
            response = {"status": "error", "message": "no image"}
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/update_profile', methods={'POST'})
@jwt_required()
def update_profile():
    try: 
        current_user_email = get_jwt_identity()
        user_id = query.get_user_data("email", {"email": current_user_email})
        user_id = user_id["json"]["message"]["id"]

        data = request.json
        print(data)
        response =  query.update_profile(user_id, data)["json"]

        print(response)
                
        return jsonify(response)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.route('/api/<string:action>', methods={'GET'})
@jwt_required()
def api_key(action):
    try:
        current_user_email = get_jwt_identity()
        user_id = query.get_user_data("email", {"email": current_user_email})
        user_id = user_id["json"]["message"]["id"]

        if(action == "generate"):
            generated_api_key = functions.generate_api_key(user_id)
            response = query.api_code(user_id, "generate", generated_api_key)
            return jsonify(response["json"])
        if(action == "get"):
            response = query.api_code(user_id, "get")
            return jsonify(response["json"])
        if(action == "revoke"):
            return jsonify({"message": "api-key revoked"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/comment/<int:post_id>', methods=['POST'])
@jwt_required()
def publish_comment(post_id):
    try:
        current_user_email = get_jwt_identity()
        user_id = query.get_user_data("email", {"email": current_user_email})
        user_id = user_id["json"]["message"]["id"]

        if 'content' in request.form: # Se está enviando contenido JSON
            data = {
                "content": request.form.get('content'),
                "media": "",
            }

        if 'media' in request.files: # Se están enviando archivos
            functions.create_folder(user_id)
            media_files = request.files.getlist('media')
            media_file_names = []

            for media_file in media_files:
                print("MEDIA FILES: ")
                file_name = secure_filename(media_file.filename)
                media_file_names.append(file_name)
                media_file.save(os.path.join("./src/static/users/", str(user_id), file_name))
            data["media"] = json.dumps(media_file_names)

        response = query.create_comment(post_id, user_id, data, 'orig 0.0.0.0')
        return jsonify(response["json"])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/comment_list/<int:post_id>', methods=['GET'])
@jwt_required()
def get_comment_list(post_id):
    try:
        current_user_email = get_jwt_identity()
        user_id = query.get_user_data("email", {"email": current_user_email})
        user_id = user_id["json"]["message"]["id"]

        response = query.list_comments(post_id, user_id)
        return jsonify(response["json"])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/manage_follow/<int:target_id>', methods=['POST'])
@jwt_required()
def manage_follow(target_id):
    try:
        current_user_email = get_jwt_identity()
        user_data = query.get_user_data("email", {"email": current_user_email})
        user_id = user_data["json"]["message"]["id"]

        # Verificar si target_id es igual a user_id
        if target_id == user_id:
            return jsonify({"status": "error", "message": "You can't follow or unfollow yourself."})

        follow_or_unfollow = request.json.get('followOrUnfollow')
        action = True if follow_or_unfollow == 1 else False

        response = query.manage_follow(user_id, target_id, action)

        return jsonify(response["json"])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.route('/manage_block/<int:target_id>', methods=['POST'])
@jwt_required()
def manage_block(target_id):
    try:
        current_user_email = get_jwt_identity()
        user_data = query.get_user_data("email", {"email": current_user_email})
        user_id = user_data["json"]["message"]["id"]

        # Verificar si target_id es igual a user_id
        if target_id == user_id:
            return jsonify({"status": "error", "message": "You can't block or unblock yourself."})

        block_or_unblock = request.json.get('blockOrUnblock')
        action = True if block_or_unblock == 1 else False

        response = query.manage_block(user_id, target_id, action)

        return jsonify(response["json"])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})




@app.route('/follow_list/<int:target_id>', methods=['GET'])
def follow_list(target_id):
    try:
        response = query.get_follow_list(target_id)
        return jsonify(response["json"])
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)