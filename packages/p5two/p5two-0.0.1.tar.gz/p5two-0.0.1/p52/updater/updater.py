import json
import shutil
from pathlib import Path
from zipfile import ZipFile
import requests

from generate_definition import generate_definition_file


def get_latest_version_number():
    # get latest version number of p5js from cdnjs api
    version_endpoint = "https://api.cdnjs.com/libraries/p5.js"

    response = requests.get(version_endpoint)
    return response.json()["latest"].split("/")[-2]


def get_data_from_disk():
    # check if reference data json is already downloaded
    data_path = Path("data.js")
    if data_path.is_file():
        with open(data_path) as fp:
            data = fp.read()
            return json.loads(data[16:])
    else:
        return None


def get_latest_reference_data():
    reference_url = "https://p5js.org/offline-reference/p5-reference.zip"
    req = requests.get(reference_url)
    with open("reference.zip", "wb") as fp:
        fp.write(req.content)

    with ZipFile("reference.zip") as zipfile:
        to_extract = "p5-reference/js/data.js"
        extracted_path = zipfile.extract(to_extract)

        shutil.copy(extracted_path, ".")
        shutil.rmtree("p5-reference")
        Path("reference.zip").unlink()

    return get_data_from_disk()


if __name__ == "__main__":
    if data := get_data_from_disk():
        current_version_number = data["project"]["version"]
        if (current_version_number == get_latest_version_number()) and Path("../static/p5Definition.py").is_file():
            print("Definition file is up to date!")
        else:
            generate_definition_file(data)

    else:
        data = get_latest_reference_data()
        generate_definition_file(data)
