import mysql.connector, json
from functions import validateString, json_status, create_folder, send_mail_formatted
import datetime
import bcrypt
import random
import string

json_file = "./src/config.json"
try:
    with open(json_file, "r") as file:
        datos = json.load(file)
        HOST = datos[0]["database"]["host"]
        USER = datos[0]["database"]["user"]
        PASS = datos[0]["database"]["password"]
except FileNotFoundError:
    print(f"El archivo {json_file} no se encontró.")
except json.JSONDecodeError:
    print(f"El archivo {json_file} no es un JSON válido.")
except Exception as e:
    print(f"Error: {str(e)}")

# Functions:


def user_exists(check_by, data_):
    print("email:")
    print(data_)

    if(check_by == "email"):
        if "email" not in data_ or not validateString("email", data_["email"]):
            return json_status(True, 1, "Incorrect email.")
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor()
        if check_by == "id":
            cursor.execute("SELECT * FROM users WHERE id = %s", (data_["id"],))
        elif check_by == "email":
            cursor.execute("SELECT * FROM users WHERE email = %s", (data_["email"],))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user is not None:
            return json_status(True, 1, "User exists.")
        else:
            return json_status(True, 1, "Not exists.")
    
    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")


def generate_random_key(length=64):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def add_user(data_):
    print(data_)

    if "email" not in data_ or not validateString("email", data_["email"]):
        return json_status(True, 1, "Incorrect email.")
    if "password" not in data_ or not validateString("password", data_["password"]):
        return json_status(True, 1, "Incorrect password.")
    if "name" not in data_ or not validateString("username", data_["name"]):
        return json_status(True, 1, "Incorrect name.")
    if "surname" not in data_ or not validateString("username", data_["surname"]):
        return json_status(True, 1, "Incorrect surname.")
    if "birthday" not in data_ or not validateString("date", data_["birthday"]):
        return json_status(True, 1, "Incorrect birthday.")
    if "gender" not in data_ or not validateString("alphabet", data_["gender"]):
        return json_status(True, 1, "Incorrect gender.")
    
    name = data_["name"]
    surname = data_["surname"]
    birthday = data_["birthday"]
    gender = data_["gender"]
    email = data_["email"]
    password = data_["password"]
    currentCoverPic = ""
    currentProfilePic = ""
    positiveList = json.dumps([])
    externalPositiveList = json.dumps([])
    negativeList = json.dumps([])
    externalNegativeList = json.dumps([])
    userSettings = json.dumps({"key": "value"})

    # Encriptar la contraseña usando bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Generar la clave aleatoria para verifyKey
    verify_key = generate_random_key()

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO users (name, surname, birthday, gender, email, password, currentCoverPic, currentProfilePic, registrationDate, positiveList, externalPositiveList, negativeList, externalNegativeList, userSettings, verifyKey, verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, 0)
        """
        values = (name, surname, birthday, gender, email, hashed_password, currentCoverPic, currentProfilePic, positiveList, externalPositiveList, negativeList, externalNegativeList, userSettings, verify_key)
        cursor.execute(insert_query, values)
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        connection.close()

        create_folder(user_id)
        send_mail_formatted("YipNet Verification Account", [user_id, verify_key, name], email)
        return json_status(True, 1, {"response": "User added."})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")
    

def login(data_):
    if "email" not in data_ or "password" not in data_:
        return json_status(True, 0, "Empty email or password.")

    email = data_["email"]
    password = data_["password"]

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
    
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cursor.fetchone()

        if user_data is None:
            cursor.close()
            connection.close()
            return json_status(True, 0, "User does not exist.")
        
        password_database = user_data[7]
        if bcrypt.checkpw(password.encode('utf-8'), password_database.encode('utf-8')):
            return json_status(True, 1, "Correct login.")
        else:
            return json_status(True, 0, "Incorrect email or password.")

    except mysql.connector.Error as error:
        print(f"Error connecting to the database: {error}")
        return json_status(False, 0, "Database connection error.")


def get_user_data(get_by, data_):
    print(">>>", get_by, ">>>", data_)
    if(get_by == "email"):
        data_ = data_["email"]

    print(">>>", get_by, ">>>", data_)

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )

        cursor = connection.cursor()
        if(get_by == "email"):
            cursor.execute("SELECT * FROM users WHERE email = %s", (data_,))
        else:
            cursor.execute("SELECT * FROM users WHERE id = %s", (data_,))
        user_data = cursor.fetchone()

        if user_data is None:
            cursor.close()
            connection.close()
            return json_status(True, 0, "Not exists.")

        # Mapear los datos a la estructura JSON deseada
        user_json = {
            "id": user_data[0],
            "name": user_data[1],
            "surname": user_data[2],
            "birthday": str(user_data[3]), # Arreglar
            "gender": user_data[4],
            "description": user_data[5],
            "currentProfilePic": user_data[8],
            "currentCoverPic": user_data[9],
            "apiCode": 0 if user_data[10] in (None, "") else 1,
            "positiveList": json.loads(user_data[11]),
            "externalPositiveList": json.loads(user_data[12]),
            "negativeList": json.loads(user_data[13]),
            "externalNegativeList": json.loads(user_data[14]),
            "userSettings": json.loads(user_data[15]),
            "theme": user_data[16],
            "registrationDate": str(user_data[17]), # Arreglar
            "verified": str(user_data[18]),
            #"verifyKey": str(user_data[19]),
        }

        cursor.close()
        connection.close()

        return json_status(True, 1, user_json)

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")


def create_post(owner_id, data_):
    print("CREACION DE POST:")
    print(owner_id, data_)

    privatePost = data_["privatePost"]
    nsfwPost = data_["nsfwPost"]
    shareId = data_["shareId"]

    if "content" not in data_:
        return json_status(True, 0, "Empty content.")
    
    content = data_["content"]
    media = data_["media"]

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor(dictionary=True)  # Cambiado a cursor de diccionario

        # Verificar y actualizar sharedByList si shareId es diferente de 0
        if shareId != 0:
            select_query = "SELECT sharedByList FROM posts WHERE id = %s"
            cursor.execute(select_query, (shareId,))
            result = cursor.fetchone()

            if result:
                shared_by_list = json.loads(result['sharedByList'])
                if owner_id not in shared_by_list:
                    shared_by_list.append(owner_id)
                    update_query = "UPDATE posts SET sharedByList = %s WHERE id = %s"
                    cursor.execute(update_query, (json.dumps(shared_by_list), shareId))
                    connection.commit()

        # Insertar el nuevo post
        insert_query = """
            INSERT INTO posts (ownerId, postDate, content, media, privatePost, nsfwPost, shareId)
            VALUES (%s, NOW(), %s, %s, %s, %s, %s)
        """
        values = (owner_id, content, media, privatePost, nsfwPost, shareId)
        cursor.execute(insert_query, values)
        connection.commit()
        post_id = cursor.lastrowid

        cursor.close()
        connection.close()

        return json_status(True, 1, {"response": "Post added.", "post_created_id": post_id})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")


def list_posts(target_owner_id, my_id):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor(dictionary=True)  # Configura el cursor para devolver resultados como diccionarios

        if target_owner_id == my_id:
            query = """
                SELECT p.*, u.name, u.surname, u.currentProfilePic 
                FROM posts p
                JOIN users u ON p.ownerId = u.id
                WHERE p.ownerId = %s
                ORDER BY p.postDate DESC  -- Ordenar en orden descendente por fecha
            """
        else:
            query = """
                SELECT p.*, u.name, u.surname, u.currentProfilePic 
                FROM posts p
                JOIN users u ON p.ownerId = u.id
                WHERE p.ownerId = %s AND p.privatePost = 0
                ORDER BY p.postDate DESC  -- Ordenar en orden descendente por fecha
            """
        cursor.execute(query, (target_owner_id,))
        result = cursor.fetchall()

        # Convertir los campos potencialmente problemáticos a tipos JSON serializables
        for row in result:
            if 'content' in row and isinstance(row['content'], bytes):
                row['content'] = row['content'].decode('utf-8')
            if 'media' in row and isinstance(row['media'], bytes):
                row['media'] = row['media'].decode('utf-8')
            if 'sharedByList' in row and isinstance(row['sharedByList'], bytes):
                row['sharedByList'] = row['sharedByList'].decode('utf-8')
            if 'postDate' in row and isinstance(row['postDate'], datetime.datetime):
                row['postDate'] = row['postDate'].isoformat()

            if 'voteHeart' in row and isinstance(row['voteHeart'], bytes):
                row['voteHeart'] = row['voteHeart'].decode('utf-8')
            if 'voteUp' in row and isinstance(row['voteUp'], bytes):
                row['voteUp'] = row['voteUp'].decode('utf-8')
            if 'voteDown' in row and isinstance(row['voteDown'], bytes):
                row['voteDown'] = row['voteDown'].decode('utf-8')

        cursor.close()
        connection.close()

        return json_status(True, 1, {"post_list": result})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")


def get_single_post(id_):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor()
        
        # Ejecuta la consulta SQL para obtener el post y los datos del usuario
        query = """
        SELECT 
            posts.*, 
            users.name, 
            users.surname, 
            users.currentProfilePic 
        FROM posts
        LEFT JOIN users ON posts.ownerId = users.id
        WHERE posts.id = %s
        """
        cursor.execute(query, (id_,))

        # Recupera el resultado de la consulta
        post_data = cursor.fetchone()

        if post_data:
            # Convierte los resultados en un diccionario
            post = {
                'id': post_data[0],
                'ownerId': post_data[1],
                'postDate': post_data[2].isoformat() if isinstance(post_data[2], datetime.datetime) else post_data[2],
                'content': post_data[3].decode('utf-8') if isinstance(post_data[3], bytes) else post_data[3],
                'sharedByList': post_data[4].decode('utf-8') if isinstance(post_data[4], bytes) else post_data[4],
                'shareId': post_data[5],
                'media': post_data[6].decode('utf-8') if isinstance(post_data[6], bytes) else post_data[6],
                'apiOrigin': post_data[7],
                'privatePost': post_data[8],
                'nsfwPost': post_data[9],
                'commentCount': post_data[10],
                #'origin': post_data[11],
                'voteHeart': post_data[11].decode('utf-8') if isinstance(post_data[11], bytes) else post_data[11],
                'voteUp': post_data[12].decode('utf-8') if isinstance(post_data[12], bytes) else post_data[12],
                'voteDown': post_data[13].decode('utf-8') if isinstance(post_data[13], bytes) else post_data[13],
                'name': post_data[15],
                'surname': post_data[16],
                'currentProfilePic': post_data[17]
            }
            return json_status(True, 1, post)
        else:
            return json_status(False, 0, "Post not found")

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error")

    finally:
        cursor.close()
        connection.close()


def update_pics(id_, pic_type, pic_name):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor()

        # Verifica el tipo de imagen
        if pic_type == 'profile':
            column_to_update = 'currentProfilePic'
        elif pic_type == 'cover':
            column_to_update = 'currentCoverPic'
        else:
            # Tipo de imagen no válido, maneja el error apropiadamente
            return json_status(False, 1, "Invalid pic_type")

        # Realiza la actualización en la base de datos
        update_query = f"UPDATE users SET {column_to_update} = %s WHERE id = %s"
        cursor.execute(update_query, (pic_name, id_))
        connection.commit()

        return json_status(True, 1, {"response": "Image updated successfully", "image_added": pic_name})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error")
    finally:
        cursor.close()
        connection.close()


def api_code(id_, action_, key_=False):
    if(action_ == "revoke"):
        pass

    if(action_ == "generate"):
        try:
            connection = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASS,
                database="yip_net"
            )
            cursor = connection.cursor()

            update_query = f"UPDATE users SET apiCode = %s WHERE id = %s"
            cursor.execute(update_query, (key_, id_))
            connection.commit()

            return json_status(True, 1, {"response": "API key generated successfully", "key": key_})
        
        except mysql.connector.Error as error:
            print(f"Error al conectarse a la base de datos: {error}")
            return json_status(False, 0, "Database connection error")
        finally:
            cursor.close()
            connection.close()

    if action_ == "get":
        try:
            connection = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASS,
                database="yip_net"
            )
            cursor = connection.cursor()

            # Consulta para obtener el valor actual de 'apiCode'
            select_query = "SELECT apiCode FROM users WHERE id = %s"
            cursor.execute(select_query, (id_,))
            result = cursor.fetchone()

            if result:
                current_api_code = result[0]
            else:
                current_api_code = None

            if not current_api_code:
                return json_status(True, 0, "API key does not exist for this user")

            # Actualiza la API key en la base de datos (esto no es necesario si no se genera una nueva API key)
            # update_query = "UPDATE users SET apiCode = %s WHERE id = %s"
            # cursor.execute(update_query, (key_, id_))
            # connection.commit()

            return json_status(True, 1, {"response": "API key retrieved successfully", "key": current_api_code})

        except mysql.connector.Error as error:
            print(f"Error al conectarse a la base de datos: {error}")
            return json_status(False, 0, "Database connection error")
        finally:
            cursor.close()
            connection.close()


def update_profile(id_, data_):
    if "name" not in data_ or not validateString("username", data_["name"]):
        return json_status(True, 1, "Incorrect name.")
    if "surname" not in data_ or not validateString("username", data_["surname"]):
        return json_status(True, 1, "Incorrect surname.")
    if "birthday" not in data_ or not validateString("date", data_["birthday"]):
        return json_status(True, 1, "Incorrect birthday.")
    if "gender" not in data_ or not validateString("alphabet", data_["gender"]):
        return json_status(True, 1, "Incorrect gender.")

    new_name = data_["name"]
    new_surname = data_["surname"]
    new_birthday = data_["birthday"]
    new_gender = data_["gender"]
    new_negative_list =  json.dumps(data_["negativeList"])
    new_description = data_["description"]

    print(">>>DESC>>>", new_description)

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor()

        update_query = (
            "UPDATE users "
            "SET name = %s, surname = %s, birthday = %s, gender = %s, negativeList = %s, description = %s "
            "WHERE id = %s"
        )

        cursor.execute(update_query, (new_name, new_surname, new_birthday, new_gender, new_negative_list, new_description, id_))
        connection.commit()

        return json_status(True, 1, {
            "response": "User profile updated successfully",
            "new_data": {
                    "name": new_name,
                    "surname": new_surname,
                    "birthday": new_birthday,
                    "gender": new_gender,
                    "negativeList": new_negative_list,
                    "description": new_description
                }
            })

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error")
    finally:
        cursor.close()
        connection.close()


def update_pass(my_id, old_pass, new_pass):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor(dictionary=True)

        # Verificar si el usuario existe
        cursor.execute("SELECT password FROM users WHERE id = %s", (my_id,))
        user = cursor.fetchone()

        if not user:
            return {"status": "error", "message": "User not found"}

        # Verificar la contraseña antigua
        if not bcrypt.checkpw(old_pass.encode('utf-8'), user['password'].encode('utf-8')):
            return {"status": "error", "message": "Incorrect old password"}

        # Validar la nueva contraseña
        if not validateString("password", new_pass):
            return {"status": "error", "message": "New password does not meet the required criteria"}

        # Encriptar la nueva contraseña
        hashed_new_pass = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())

        # Actualizar la contraseña en la base de datos
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_new_pass, my_id))
        connection.commit()

        return {"status": "success", "message": "Password updated successfully"}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        connection.close()


def create_comment(post_id, owner_id, data_, origin):
    if "content" not in data_:
        return json_status(True, 0, "Empty content")

    content = data_["content"]
    media = data_["media"]

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor()

        # Inserción de comentario
        insert_query = """
            INSERT INTO comments (postId, ownerId, content, media, commentDate, origin)
            VALUES (%s, %s, %s, %s, NOW(), %s)
        """
        values = (post_id, owner_id, content, media, origin)
        cursor.execute(insert_query, values)
        comment_id = cursor.lastrowid

        # Recuperar el comentario insertado
        select_query = """
            SELECT comments.id, comments.postId, comments.ownerId, comments.content, comments.media, comments.commentDate, 
                   comments.voteHeart, comments.voteUp, comments.voteDown, users.name, users.surname, users.currentProfilePic
            FROM comments
            LEFT JOIN users ON comments.ownerId = users.id
            WHERE comments.id = %s
        """
        cursor.execute(select_query, (comment_id,))
        comment_data = cursor.fetchone()

        column_names = cursor.column_names  # Obtiene los nombres de las columnas
        inserted_comment = dict(zip(column_names, comment_data))  # Combina los nombres de las columnas con los valores

        # Decodificar los campos JSON desde bytes a cadenas de texto
        if inserted_comment['voteHeart'] is not None:
            inserted_comment['voteHeart'] = json.loads(inserted_comment['voteHeart'].decode('utf-8'))
        if inserted_comment['voteUp'] is not None:
            inserted_comment['voteUp'] = json.loads(inserted_comment['voteUp'].decode('utf-8'))
        if inserted_comment['voteDown'] is not None:
            inserted_comment['voteDown'] = json.loads(inserted_comment['voteDown'].decode('utf-8'))

        # Actualización de commentCount en la tabla "posts"
        update_query = """
            UPDATE posts
            SET commentCount = commentCount + 1
            WHERE id = %s
        """
        cursor.execute(update_query, (post_id,))

        connection.commit()
        cursor.close()
        connection.close()

        return json_status(True, 1, {"response": "Comment added", "comment": inserted_comment})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")


def list_comments(post_id, user_id):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor(dictionary=True)  # Configura el cursor para devolver resultados como diccionarios

        query = """
            SELECT c.id AS comment_id, c.postId, c.ownerId AS comment_owner_id, c.content AS comment_content,
                   c.media AS comment_media, c.commentDate, c.voteHeart, c.voteUp, c.voteDown,
                   u.name AS user_name, u.surname AS user_surname,
                   u.currentProfilePic AS user_profile_pic
            FROM comments c
            LEFT JOIN users u ON c.ownerId = u.id
            WHERE c.postId = %s
            AND (
                (
                    (SELECT privatePost FROM posts WHERE id = %s) = 0)
                OR
                (c.ownerId = %s AND (SELECT privatePost FROM posts WHERE id = %s) = 1)
            )
        """

        cursor.execute(query, (post_id, post_id, user_id, post_id))
        result = cursor.fetchall()
        cursor.close()
        connection.close()

        # Convert bytes to str for JSON serialization
        for row in result:
            if isinstance(row['voteHeart'], bytes):
                row['voteHeart'] = row['voteHeart'].decode('utf-8')
            if isinstance(row['voteUp'], bytes):
                row['voteUp'] = row['voteUp'].decode('utf-8')
            if isinstance(row['voteDown'], bytes):
                row['voteDown'] = row['voteDown'].decode('utf-8')

        return json_status(True, 1, {"comment_list": result})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")


def manage_follow(my_id, target_id, add_):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor()

        my_id = int(my_id)
        target_id = int(target_id)

        print("IDS", my_id, target_id, add_)

        if add_:
            response_text = "Followed"
            # Agregar el 'id' del usuario objetivo a mi 'positiveList', si no existe.
            update_query1 = """
                UPDATE users
                SET positiveList = JSON_ARRAY_APPEND(positiveList, '$', %s)
                WHERE id = %s
                AND NOT JSON_CONTAINS(positiveList, %s)
            """
            cursor.execute(update_query1, (target_id, my_id, target_id))
            # Agregar mi 'id' al 'externalPositiveList' del usuario objetivo, si no existe.
            update_query2 = """
                UPDATE users
                SET externalPositiveList = JSON_ARRAY_APPEND(externalPositiveList, '$', %s)
                WHERE id = %s
                AND NOT JSON_CONTAINS(externalPositiveList, %s)
            """
            cursor.execute(update_query2, (my_id, target_id, my_id))
        else:
            response_text = "Unfollowed"
            # Eliminar "target_id" del array del campo "positiveList" donde el id = my_id.
            # Eliminar "my_id" del array del campo "externalPositiveList" donde el id = target_id.
            select_query_positiveList = "SELECT positiveList FROM users WHERE id = %s"
            cursor.execute(select_query_positiveList, (my_id,))
            positiveList = cursor.fetchone()
            positiveList = json.loads(positiveList[0].decode('utf-8'))
            select_query_externalPositiveList = "SELECT externalPositiveList FROM users WHERE id = %s"
            cursor.execute(select_query_externalPositiveList, (target_id,))
            externalPositiveList = cursor.fetchone()
            externalPositiveList = json.loads(externalPositiveList[0].decode('utf-8'))

            if(target_id in positiveList and my_id in externalPositiveList):
                positiveList.remove(target_id)
                externalPositiveList.remove(my_id)
            
                positiveList = json.dumps(positiveList)
                externalPositiveList = json.dumps(externalPositiveList)

                update_query1 = "UPDATE users SET positiveList = %s WHERE id = %s"
                cursor.execute(update_query1, (positiveList, my_id))
                update_query2 = "UPDATE users SET externalPositiveList = %s WHERE id = %s"
                cursor.execute(update_query2, (externalPositiveList, target_id))

        connection.commit()
        cursor.close()
        connection.close()
        return json_status(True, 1, {"response": response_text, "target_user": target_id})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")
    

def get_follow_list(target_id):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor(dictionary=True)

        target_id = int(target_id)
        
        # Obtener los campos positiveList y externalPositiveList
        cursor.execute("SELECT positiveList, externalPositiveList FROM users WHERE id = %s", (target_id,))
        result = cursor.fetchone()

        if result is None:
            return json_status(False, 1, "User not found.")

        positive_list = json.loads(result['positiveList'])
        external_positive_list = json.loads(result['externalPositiveList'])

        # Crear arrays de objetos
        def get_user_info(user_ids):
            if not user_ids:
                return []
            format_strings = ','.join(['%s'] * len(user_ids))
            cursor.execute(f"""
                SELECT id, name, surname, currentProfilePic, externalPositiveList, positiveList 
                FROM users 
                WHERE id IN ({format_strings})
            """, tuple(user_ids))
            users = cursor.fetchall()
            user_info_list = []
            for user in users:
                external_positive_list = user["externalPositiveList"]
                positive_list = user["positiveList"]
                if isinstance(external_positive_list, bytes):
                    external_positive_list = external_positive_list.decode()  # Decodifica bytes a cadena
                if isinstance(positive_list, bytes):
                    positive_list = positive_list.decode()  # Decodifica bytes a cadena
                user_info_list.append({
                    "id": user["id"],
                    "name": user["name"],
                    "surname": user["surname"],
                    "pfp": user["currentProfilePic"],
                    "externalPositiveList": external_positive_list,
                    "positiveList": positive_list
                })
            return user_info_list

        positive_list_objects = get_user_info(positive_list)
        external_positive_list_objects = get_user_info(external_positive_list)

        data = {
            "positiveList": positive_list_objects,
            "externalPositiveList": external_positive_list_objects
        }

        return json_status(True, 1, {"response": data})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    
def manage_block(my_id, target_id, add_):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor()

        my_id = int(my_id)
        target_id = int(target_id)

        print("IDS", my_id, target_id, add_)

        if add_:
            response_text = "Blocked"
            # Agregar el 'id' del usuario objetivo a mi 'negativeList', si no existe.
            update_query1 = """
                UPDATE users
                SET negativeList = JSON_ARRAY_APPEND(negativeList, '$', %s)
                WHERE id = %s
                AND NOT JSON_CONTAINS(negativeList, %s)
            """
            cursor.execute(update_query1, (target_id, my_id, target_id))
            # Agregar mi 'id' al 'externalNegativeList' del usuario objetivo, si no existe.
            update_query2 = """
                UPDATE users
                SET externalNegativeList = JSON_ARRAY_APPEND(externalNegativeList, '$', %s)
                WHERE id = %s
                AND NOT JSON_CONTAINS(externalNegativeList, %s)
            """
            cursor.execute(update_query2, (my_id, target_id, my_id))
        else:
            response_text = "Unblocked"
            # Eliminar "target_id" del array del campo "negativeList" donde el id = my_id.
            # Eliminar "my_id" del array del campo "externalNegativeList" donde el id = target_id.
            select_query_negativeList = "SELECT negativeList FROM users WHERE id = %s"
            cursor.execute(select_query_negativeList, (my_id,))
            negativeList = cursor.fetchone()
            negativeList = json.loads(negativeList[0].decode('utf-8'))
            select_query_externalNegativeList = "SELECT externalNegativeList FROM users WHERE id = %s"
            cursor.execute(select_query_externalNegativeList, (target_id,))
            externalNegativeList = cursor.fetchone()
            externalNegativeList = json.loads(externalNegativeList[0].decode('utf-8'))

            if target_id in negativeList and my_id in externalNegativeList:
                negativeList.remove(target_id)
                externalNegativeList.remove(my_id)

                negativeList = json.dumps(negativeList)
                externalNegativeList = json.dumps(externalNegativeList)

                update_query1 = "UPDATE users SET negativeList = %s WHERE id = %s"
                cursor.execute(update_query1, (negativeList, my_id))
                update_query2 = "UPDATE users SET externalNegativeList = %s WHERE id = %s"
                cursor.execute(update_query2, (externalNegativeList, target_id))

        connection.commit()
        cursor.close()
        connection.close()
        return json_status(True, 1, {"response": response_text, "target_user": target_id})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")


def manage_vote_db(my_id_, entity_id_, entity_type_, vote_type_):
    my_id_ = int(my_id_)
    entity_id_ = int(entity_id_)

    # Validar los tipos de entidad y voto
    if entity_type_ not in ["posts", "comments"]:
        return json_status(False, 1, {"response": "Invalid entity type."})
    if vote_type_ not in ["Heart", "Up", "Down"]:
        return json_status(False, 1, {"response": "Invalid vote type."})

    # Definir el campo a actualizar basado en el tipo de voto
    vote_field = f"vote{vote_type_}"

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor(dictionary=True)  # Configura el cursor para devolver resultados como diccionarios

        # Obtener el valor actual del campo de votos
        cursor.execute(f"SELECT {vote_field} FROM {entity_type_} WHERE id = %s", (entity_id_,))
        print(f"SELECT {vote_field} FROM {entity_type_} WHERE id = %s", (entity_id_,))
        result = cursor.fetchone()

        if result is None:
            return json_status(False, 2, {"response": "Entity not found."})

        # Parsear el campo JSON
        vote_list = json.loads(result[vote_field])

        # Agregar o eliminar el ID del usuario de la lista
        if my_id_ in vote_list:
            vote_list.remove(my_id_)
            action = "removed"
        else:
            vote_list.append(my_id_)
            action = "added"

        # Actualizar el campo en la base de datos
        updated_vote_list = json.dumps(vote_list)
        cursor.execute(f"UPDATE {entity_type_} SET {vote_field} = %s WHERE id = %s", (updated_vote_list, entity_id_))
        connection.commit()

        return json_status(True, 1, {"response": f"Vote {action} successfully."})
    
    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def get_news_feed(my_id_):
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor(dictionary=True)

        # Obtener el positiveList del usuario actual
        cursor.execute("SELECT positiveList FROM users WHERE id = %s", (my_id_,))
        result = cursor.fetchone()

        if not result:
            return json_status(False, 0, "User not found.")

        # Convertir el positiveList JSON a una lista de IDs
        positive_list = json.loads(result['positiveList'])

        # Agregar my_id_ al array si no se encuentra allí
        if my_id_ not in positive_list:
            positive_list.append(my_id_)

        if not positive_list:
            return json_status(True, 1, {"post_list": []})

        # Obtener todos los posts cuyos ownerId estén en positive_list
        format_strings = ','.join(['%s'] * len(positive_list))
        query = f"""
            SELECT p.*, u.name, u.surname, u.currentProfilePic 
            FROM posts p
            JOIN users u ON p.ownerId = u.id
            WHERE p.ownerId IN ({format_strings})
            ORDER BY p.postDate DESC
        """
        cursor.execute(query, tuple(positive_list))
        posts = cursor.fetchall()

        # Convertir los campos potencialmente problemáticos a tipos JSON serializables
        for post in posts:
            if 'content' in post and isinstance(post['content'], bytes):
                post['content'] = post['content'].decode('utf-8')
            if 'media' in post and isinstance(post['media'], bytes):
                post['media'] = post['media'].decode('utf-8')
            if 'sharedByList' in post and isinstance(post['sharedByList'], bytes):
                post['sharedByList'] = post['sharedByList'].decode('utf-8')
            if 'postDate' in post and isinstance(post['postDate'], datetime.datetime):
                post['postDate'] = post['postDate'].isoformat()

            if 'voteHeart' in post and isinstance(post['voteHeart'], bytes):
                post['voteHeart'] = post['voteHeart'].decode('utf-8')
            if 'voteUp' in post and isinstance(post['voteUp'], bytes):
                post['voteUp'] = post['voteUp'].decode('utf-8')
            if 'voteDown' in post and isinstance(post['voteDown'], bytes):
                post['voteDown'] = post['voteDown'].decode('utf-8')

        return json_status(True, 1, {"response": posts})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def verify_account(id_, verify_key_received):
    try:
        # Conecta a MySQL (ajusta los parámetros según sea necesario)
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS,
            database='yip_net'  # Asegúrate de usar el nombre de la base de datos correcta
        )

        # Crea un cursor para ejecutar consultas SQL
        cursor = connection.cursor()

        # Consulta para verificar el usuario
        query = "SELECT verifyKey FROM users WHERE id = %s"
        cursor.execute(query, (id_,))
        result = cursor.fetchone()

        if result and result[0] == verify_key_received:
            # Si coincide el verifyKey, actualiza el valor de 'verified'
            update_query = "UPDATE users SET verified = 1 WHERE id = %s"
            cursor.execute(update_query, (id_,))
            connection.commit()
            return json_status(True, 1, {"response": "verified"})
        else:
            return json_status(False, 0, {"response": "error on verification"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return False

    finally:
        # Cierra el cursor y la conexión a la base de datos
        cursor.close()
        connection.close()
