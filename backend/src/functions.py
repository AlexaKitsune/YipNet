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


def send_mail_formatted(subject_, data_body_, to_email):
    id = data_body_[0],
    verify_key = data_body_[1]
    name = data_body_[2]

    template_mailing = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title></title>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;900&display=swap" rel="stylesheet">
        </head>
        <body style="margin:0; padding:0; background-color:#F2F2F2;">

        <center>
        <div style="background-color:#F2F2F2; max-width: 640px; margin: auto;">
        <!--[if mso]> <table role="presentation" width="640" cellspacing="0" cellpadding="0" border="0" align="center"> <tr> <td> <![endif]-->

            <table style="width:100%; max-width:640px; background-color:white" cellspacing="0" cellpadding="0">
                <tr>
                    <p style="font-family:'Montserrat',sans-serif; color:#8A2BE2; font-size:58px; font-weight:bolder; margin-top:30px; margin-bottom:10px;">
                        YipNet
                    </p>
                    <p style="font-family:'Montserrat',sans-serif; color:#8A2BE2; font-size:20px; margin-top:0;">
                        Verification Account
                    </p>
                </tr>
            </table>
            <table style="width:100%; max-width:640px; background-color:white;" cellspacing="0" cellpadding="0">
                <tr>
                    <p style="font-family:'Montserrat',sans-serif; color:black; font-weight:bolder; font-size:16px;">
                        Hello, {name}!
                    </p>
                    <p style="font-family:'Montserrat',sans-serif; font-size:16px; text-wrap:balance;">
                        You've succesfully created your YipNet account.<br>Just confirm yor email address and activate it by click the button below.
                    </p>
                    <a href="localhost:8080/#/verify~{id}&{verify_key}">
                        <button style="font-family:'Montserrat',sans-serif; width:200px; height:40px; margin-top:10px; font-size:16px; color:white; background-color:#8A2BE2; border:none;">
                            Verify your email
                        </button>
                    </a>
                    <p style="font-family:'Montserrat',sans-serif; font-size:14px; color:rgb(143, 143, 143); margin-top:24px">
                        Thank you from the YipNet team
                    </p>
                </tr>
            </table>

        <!--[if mso]> </td> </tr> </table> <![endif]-->
        </div>
        </center>

        </body>
        </html>
    """
    send_mail(subject_, template_mailing, to_email)

#send_mail("Asunto del correo", "Cuerpo del correo", "example@gmail.com")