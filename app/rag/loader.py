from pathlib import Path
import yaml


DATA_SOURCE_PATH = Path("data/source")


def load_documents():
    documents = []

    for file_path in DATA_SOURCE_PATH.glob("*"):
        if file_path.suffix in [".yaml", ".yml"]:
            documents.extend(load_yaml(file_path))
        elif file_path.suffix == ".md":
            documents.append(load_markdown(file_path))

    return documents


def load_yaml(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)

    return [{
        "content": str(content),
        "metadata": {
            "section": file_path.stem,
            "filetype": "yaml",
            "filename": file_path.name
        }
    }]


def load_markdown(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "content": content,
        "metadata": {
            "section": file_path.stem,
            "filetype": "markdown",
            "filename": file_path.name
        }
    }
