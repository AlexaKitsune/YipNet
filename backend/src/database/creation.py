# The code on this file creates a database if not exists.
import mysql.connector, json

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


def create_database_and_tables():
    try:
        # Conecta a MySQL (ajusta los parámetros según sea necesario)
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASS
        )

        # Crea un cursor para ejecutar consultas SQL
        cursor = connection.cursor()

        # Nombre de la base de datos que deseas crear
        database_name = "yip_net"

        # Consulta SQL para crear la base de datos si no existe
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
        cursor.execute(create_database_query)

        # Selecciona la base de datos recién creada
        cursor.execute(f"USE {database_name}")

        # Consultas SQL para crear las tablas
        create_posts_table_query = """
        CREATE TABLE IF NOT EXISTS posts (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            ownerId BIGINT(20) NOT NULL,
            postDate DATETIME NOT NULL,
            content MEDIUMTEXT NOT NULL,
            sharedByList JSON DEFAULT '[]',
            shareId BIGINT(20) DEFAULT 0,
            media MEDIUMTEXT,
            apiOrigin VARCHAR(255),
            privatePost TINYINT(1) NOT NULL,
            nsfwPost TINYINT(1) NOT NULL,
            commentCount BIGINT(20) DEFAULT 0,
            voteHeart JSON DEFAULT '[]',
            voteUp JSON DEFAULT '[]',
            voteDown JSON DEFAULT '[]',
            origin VARCHAR(255)
        );
        """

        create_comments_table_query = """
        CREATE TABLE IF NOT EXISTS comments (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            postId BIGINT(20) NOT NULL,
            ownerId BIGINT(20) NOT NULL,
            content MEDIUMTEXT NOT NULL,
            media MEDIUMTEXT,
            commentDate DATETIME NOT NULL,
            voteHeart JSON DEFAULT '[]',
            voteUp JSON DEFAULT '[]',
            voteDown JSON DEFAULT '[]',
            origin VARCHAR(255)
        );
        """

        create_users_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT(20) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(63) NOT NULL,
            surname VARCHAR(63) NOT NULL,
            birthday DATE NOT NULL,
            gender VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            email VARCHAR(255) NOT NULL,
            password VARCHAR(64) NOT NULL,
            currentProfilePic VARCHAR(255) NOT NULL,
            currentCoverPic VARCHAR(255) NOT NULL,
            apiCode VARCHAR(63),
            positiveList JSON DEFAULT '[]',
            externalPositiveList JSON DEFAULT '[]',
            negativeList JSON DEFAULT '[]',
            externalNegativeList JSON DEFAULT '[]',
            userSettings JSON NOT NULL,
            theme VARCHAR(63),
            registrationDate DATETIME NOT NULL,
            origin VARCHAR(255)
        );
        """

        # Ejecuta las consultas para crear las tablas
        cursor.execute(create_posts_table_query)
        cursor.execute(create_comments_table_query)
        cursor.execute(create_users_table_query)

        # Confirma la transacción
        connection.commit()

        print("Database creation check executed successfully.")

    except Exception as e:
        # Maneja cualquier error que pueda ocurrir
        print(f"Error: {str(e)}")

    finally:
        # Cierra el cursor y la conexión a la base de datos
        cursor.close()
        connection.close()
