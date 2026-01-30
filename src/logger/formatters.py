from dataclasses import dataclass

@dataclass(frozen=True)
class TextFormat:
    """Форматы текста логирования"""
    simple = "\r%(levelname)-9s| %(asctime)s.%(msecs)03d | %(lineno)-3d %(module)s | %(message)s"
    detailed = "\r%(levelname)-9s| %(asctime)s.%(msecs)03d | %(lineno)-3d %(pathname)s | %(message)s"

@dataclass(frozen=True)
class DateFormat:
    """Форматы дат логирования"""
    simple = "%H:%M:%S"
    detailed = "%d-%m-%Y %H:%M:%S"
