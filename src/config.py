from configparser import ConfigParser


def config(
    filename: str = "database.ini",
    section: str = "postgresql",
) -> dict[str, str]:
    """Читает параметры подключения к БД из INI-файла."""

    parser = ConfigParser()

    if not parser.read(filename):
        raise FileNotFoundError(f"Configuration file '{filename}' not found.")

    if not parser.has_section(section):
        raise ValueError(f"Section '{section}' not found in '{filename}'.")

    return dict(parser.items(section))
