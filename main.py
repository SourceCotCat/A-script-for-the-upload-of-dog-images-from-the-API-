from utils.user_input import get_user_input_cnt, get_users_breed_subreed, clear_f
from utils.yadisk_integration import check_token
from utils.image_processing import proc_image
from utils.logger import setup_log, get_log
from yadisk import YaDisk
import os


setup_log()
logger = get_log(__name__)

json_file = os.path.join(os.path.dirname(__file__), "results.json")

def preparation() -> None:
    """
    Очищает json файл перед началом сессии.
    Returns: None
    """
    clear_f(json_file) 

def get_user_input() -> tuple[None | int, None | str, None | list[str], None | str]:
    """
    Получает данные от пользователя через консоль.
    -Запрашивает кол-во изображений.
    -Получает информацию о породе(подпороде).

    Returns: tuple[...]
        - cnt: количество изображений (int или None, если 'all').
        - breed: порода (str или None).
        - subbreeds: список подпород (list[str] или None).
        - subbreed: подпорода (str или None).  
    """
    cnt = get_user_input_cnt()
    breed, subbreeds, subbreed = get_users_breed_subreed()
    return cnt, breed, subbreeds, subbreed

def run(
    cnt: None | int,
    breed: None | str,
    subbreeds: None | list[str],
    subbreed: None | str,
    y_disk: None | YaDisk
) -> None:
    """
    Основная часть программы.
    Выполняет проверку данных и запускает обработку изображений.
    
    Args:
        cnt (int): Количество изображений для загрузки.
        breed (str): Название породы.
        subbreeds (list[str]): Список подпород.
        subbreed (str): Конкретная подпорода.
        y_disk ("YaDisk"): YaDisk.

    Returns:
        None
    """
    if not breed and not subbreed:
        logger.warning("Порода или подпорода не выбраны.")
        return
    if not y_disk:
        logger.error("Не удалось авторизоваться в Яндекс.Диске.")
        return

    logger.info("Начинаем обработку изображений...")
    proc_image(breed, subbreeds, subbreed, cnt, y_disk)
    logger.info("Обработка завершена.")


if __name__ == "__main__":
    try:
        logger.info("Запуск приложения")
        preparation()
        cnt, breed, subbreeds, subbreed = get_user_input()
        y_disk = check_token()
        run(cnt, breed, subbreeds, subbreed, y_disk)
    except KeyboardInterrupt:
        logger.warning("Операция прервана пользователем.")
        exit(1) # возникла ошибка и она была аварийно завершена
    except Exception as e:
        logger.error(f"Ошибка выполнения: {e}", exc_info=True)
        exit(1) # возникла ошибка и она была аварийно завершена


