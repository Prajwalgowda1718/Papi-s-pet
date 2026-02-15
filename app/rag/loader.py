from pathlib import Path
import yaml
import re



DATA_SOURCE_PATH = Path("data/source")


def load_documents():
    documents = []

    for file_path in DATA_SOURCE_PATH.glob("*"):
        if file_path.suffix in [".yaml", ".yml"]:
            documents.extend(load_yaml(file_path))
        elif file_path.suffix == ".md":
            documents.extend(load_markdown(file_path))

    return documents


def load_yaml(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)

    documents = []

    for key, value in content.items():

        # Convert list values into readable string
        if isinstance(value, list):
            formatted_value = ", ".join(value)
        else:
            formatted_value = str(value)

        # Convert snake_case keys into readable form
        readable_key = key.replace("_", " ").title()

        documents.append({
            "content": f"{readable_key}: {formatted_value}",
            "metadata": {
                "section": file_path.stem,
                "subsection": key,
                "filetype": "yaml",
                "filename": file_path.name,
                "access_level": "public"
            }
        })

    return documents



    return documents


def load_markdown(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = re.split(r"(?=^#{1,3} )", content, flags=re.MULTILINE)

    documents = []

    for section in sections:
        if section.strip():
            documents.append({
                 "content": section.strip(),
                 "metadata": {
                    "section": file_path.stem,
                    "filetype": "markdown",
                    "filename": file_path.name,
                    "access_level": "public"
                    }
})



    return documents
