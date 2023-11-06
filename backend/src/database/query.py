import mysql.connector, json
from functions import validateString, json_status, create_folder
import datetime

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

    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            # password=PASS,
            database="yip_net"
        )
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO users (name, surname, birthday, gender, email, password, currentCoverPic, currentProfilePic, registrationDate, positiveList, externalPositiveList, negativeList, externalNegativeList, userSettings)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s)
        """
        values = (name, surname, birthday, gender, email, password, currentCoverPic, currentProfilePic, positiveList, externalPositiveList, negativeList, externalNegativeList, userSettings)
        cursor.execute(insert_query, values)
        connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        connection.close()

        create_folder(user_id)
        return json_status(True, 1, {"response": "User added."})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")


def login(data_):
    if("email" not in data_ or "password" not in data_):
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
            return json_status(True, 0, "Not exists.")
        
        password_database = user_data[7]
        if(password_database == password):
            return json_status(True, 1, "Correct login.")
        else:
            return json_status(True, 0, "Incorrect login.")

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")
    

def get_user_data(get_by, data_):
    if(get_by == "email"):
        data_ = data_["email"]

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

            "negativeList": json.loads(user_data[13]),

            "userSettings": json.loads(user_data[15]),
            "theme": user_data[16],
            "registrationDate": str(user_data[17]), # Arreglar
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

    if("content" not in data_):
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
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO posts (ownerId, postDate, content, media, privatePost, nsfwPost)
            VALUES (%s, NOW(), %s, %s, %s, %s)
        """
        values = (owner_id, content, media, privatePost, nsfwPost)
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
                'postDate': post_data[2],
                'content': post_data[3],
                'media': post_data[4],
                'apiOrigin': post_data[5],
                'privatePost': post_data[6],
                'nsfwPost': post_data[7],
                'origin': post_data[8],
                'name': post_data[9],
                'surname': post_data[10],
                'currentProfilePic': post_data[11]
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
            SELECT comments.id, comments.postId, comments.ownerId, comments.content, comments.media, comments.commentDate, users.name, users.surname, users.currentProfilePic
            FROM comments
            LEFT JOIN users ON comments.ownerId = users.id
            WHERE comments.id = %s
        """
        cursor.execute(select_query, (comment_id,))
        comment_data = cursor.fetchone()

        column_names = cursor.column_names  # Obtiene los nombres de las columnas
        inserted_comment = dict(zip(column_names, comment_data))  # Combina los nombres de las columnas con los valores

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
                   c.media AS comment_media, c.commentDate, u.name AS user_name, u.surname AS user_surname,
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

        return json_status(True, 1, {"comment_list": result})

    except mysql.connector.Error as error:
        print(f"Error al conectarse a la base de datos: {error}")
        return json_status(False, 0, "Database connection error.")
