import re, os, uuid, random, string, yagmail
from dotenv import load_dotenv
#char_alphanumeric = string.ascii_letters + string.digits
char_greek = 'αβγδεζηθικλμνξοπρστυφχψω'
char_cyrilic = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
char_katakana = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
permissible_characters = char_greek + char_cyrilic + char_katakana # + char_alphanumeric

load_dotenv()


def validateString(type_, string_):
    if(type_ == "email"):
        return bool(re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", string_))
    if(type_ == "date"):
        return bool(re.match(r"^\d{4}\-[0-1][0-9]\-[0-2][0-9]$", string_))
    if(type_ == "username"):
        if(string_ != "" and not bool(re.match(r"^\s+$", string_))):
            return bool(re.match(r"[A-Za-z_一-龠ぁ-ゔァ-ヴー]*[A-Za-z0-9_\s一-龠ぁ-ゔァ-ヴー\-]+$", string_))
        else:
            return False
    if(type_ == "password"): #>8 characters, at least 1 number, 1 uppercase, 1 lowercase, 1 special character
        return bool(re.match(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*\W)(?!.* ).{8,128}$", string_))
    if(type_ == "string"): # Valida que la cadena no esté vacía
        return bool(string_ != "")
    if(type_ == "alphabet"): # Valida que la cadena no esté vacía y solo contenga letras del alfabeto y espacios
        return bool(re.match(r"^[A-Za-z\s]*$", string_))
    return False


def json_status(success_, status_, message_):
    if status_ == 1:
        status_ = "ok"
    elif status_ == 0:
        status_ = "error"
    return {
        "success": success_,
        "json": {
            "status": status_,
            "message": message_
        }
    }


def create_folder(id_, get_=False):
    static_users_folder = './src/static/users/'
    user_folder_path = os.path.join(static_users_folder, str(id_))

    if(get_):
        return user_folder_path

    if not os.path.exists(user_folder_path):
        os.mkdir(user_folder_path)


def generate_api_key(id_):
    random_uuid = uuid.uuid4()
    random_uuid = str(random_uuid).replace("-", str(id_))
    random_str = ''.join(random.choice(permissible_characters) for _ in range(len(random_uuid)-1))

    result = "".join(c1 + c2 for c1, c2 in zip(random_uuid, random_str))
    if len(random_uuid) > len(random_str):
        result += random_uuid[len(random_str):]
    else:
        result += random_str[len(random_uuid):]
    return result


def send_mail(subject, body, to_email):
    email_user = os.getenv("SMTP_USERNAME")
    email_pass = os.getenv("SMTP_PASSWORD")

    yag = yagmail.SMTP(email_user, email_pass)

    try:
        yag.send(
            to=to_email,
            subject=subject,
            contents=body
        )
        print("Correo enviado exitosamente a", to_email)
    except Exception as e:
        print("Error al enviar el correo:", e)

#send_mail("Asunto del correo", "Cuerpo del correo", "example@gmail.com")