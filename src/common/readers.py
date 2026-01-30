from pathlib import Path

import orjson
import pandas as pd
from pydantic._internal._model_construction import ModelMetaclass
import yaml

def _check_file(file_path: Path | str, expected_type: str) -> Path:
    """
    Проверяет, существует ли файл и имеет ли он расширение и правильное ли у него расширение.
    :param file_path: Путь к файлу.
    :return: Путь к файлу.

    :raises FileNotFoundError: Если файл не найден.
    :raises ValueError: Если файл не имеет расширение .yaml.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден")

    if file_path.suffix != f".{expected_type}":
        raise ValueError(f"Файл {file_path} должен иметь расширение .{expected_type}")

    return Path(file_path)

def yaml_read(file_path: Path | str, schema: ModelMetaclass = None):
    """
    Загружает и валидирует данные из YAML-файла согласно указанной схеме.

    :param file_path: Путь к YAML-файлу.
    :param schema: Схема для валидации данных.
    """
    file_path = _check_file(file_path, "yaml")

    with open(file_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        raise ValueError(f"Файл {file_path} пуст или повреждён")

    return schema(**data) if schema else data

def txt_read(file_path: Path | str) -> list[str]:
    """
    Читает данные из текстового файла.

    :param file_path: Путь к файлу.
    """

    file_path = _check_file(file_path, "txt")

    with open(file_path, encoding="utf-8") as f:
        data = f.read()
    return data.splitlines()

def txt_add(file_path: Path | str, data: str):
    """
    Добавляет данные в текстовый файл.

    :param file_path: Путь к файлу.
    :param data: Данные для записи.
    """
    file_path = _check_file(file_path, "txt")

    old_data = txt_read(file_path)
    if len(old_data) > 0:
        data = "\n" + data

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(data)

def save_json(data: dict | list, file_path: str | Path):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(orjson.dumps(data, option=orjson.OPT_INDENT_2))

def read_json(file_path: str | Path) -> dict | list:
    return orjson.loads(Path(file_path).read_bytes())

def save_csv(df: pd.DataFrame, file_path: str | Path) -> None:
    if not str(file_path).endswith('.csv'):
        file_path = str(file_path) + '.csv'
    file_path = Path(file_path) if isinstance(file_path, str) else file_path
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, sep=';', decimal=',', encoding='utf-8-sig', index=False)


def read_csv(file_path: str | Path) -> pd.DataFrame:
    if not str(file_path).endswith('.csv'):
        file_path = str(file_path) + '.csv'
    _df = pd.read_csv(file_path, sep=';', decimal=',', encoding='utf-8-sig', low_memory=False)
    return _df

