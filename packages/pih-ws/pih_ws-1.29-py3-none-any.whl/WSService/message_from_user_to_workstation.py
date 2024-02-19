import importlib.util
import sys

pih_exists = importlib.util.find_spec("pih") is not None
if not pih_exists:
    sys.path.append("//pih/facade")
from pih import A, NotFound
from pih.collections import User
from pih.tools import FullNameTool

if __name__ == '__main__':
    sender_user_login: str = A.SE.arg(0)
    host: str = A.SE.arg(1)
    input_message: str = A.SE.arg(2)
    sender_user: User = A.R_U.by_login(sender_user_login).data
    recipient_user_name: str = ""
    try:
        recipient_user_name = f"{FullNameTool.to_given_name(A.R_U.by_workstation_name(host).data)}, "
    except NotFound:
        pass
    message_result: str = f"Сообщение от {FullNameTool.to_given_name(sender_user)}({A.D_F.description(sender_user.description)}): "
    if input_message == "__ask_confirmation__":
        message_result += f"День добрый, {FullNameTool.to_given_name(sender_user)}, хочу подключиться к вашему компьютеру! Для разрешения - подвигайте курсором мыши вверх-вниз. Для отмены - вправо-влево."
    else:
        message_result += f"{recipient_user_name}{input_message}"
    A.ME_WS.by_workstation_name(host, message_result)
  
   