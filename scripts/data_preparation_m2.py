import os
import re
import urllib.request
from urllib.parse import urljoin


def download_answer_files(cloud_url: str, path_to_data_folder: str, respondent_index: int) -> None:
    if not isinstance(cloud_url, str) or not cloud_url.strip():
        raise ValueError("cloud_url must be a non-empty string.")
    if not isinstance(path_to_data_folder, str) or not path_to_data_folder.strip():
        raise ValueError("path_to_data_folder must be a non-empty string.")
    if not isinstance(respondent_index, int) or respondent_index <= 0:
        raise ValueError("respondent_index must be a positive integer.")

    os.makedirs(path_to_data_folder, exist_ok=True)

    if not cloud_url.endswith("/"):
        cloud_url += "/"

    for i in range(1, respondent_index + 1):
        source_name = f"a{i}.txt"
        destination_name = f"answers_respondent_{i}.txt"
        source_url = urljoin(cloud_url, source_name)
        destination_path = os.path.join(path_to_data_folder, destination_name)

        try:
            urllib.request.urlretrieve(source_url, destination_path)
        except Exception as e:
            raise OSError(f"Could not download file from {source_url}") from e


def collate_answer_files(data_folder_path: str) -> None:
    if not os.path.isdir(data_folder_path):
        raise FileNotFoundError(f"Data folder does not exist: {data_folder_path}")
    
    repository_root = os.path.dirname(data_folder_path)
    output_folder = os.path.join(repository_root, "output")
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, "collated_answers.txt")

    pattern = re.compile(r"^answers_respondent_(\d+)\.txt$")

    files_with_index = []
    for file_name in os.listdir(data_folder_path):
        match = pattern.match(file_name)
        if match:
            try:
                files_with_index.append((int(match.group(1)), file_name))
            except ValueError:
                pass

    if not files_with_index:
        raise ValueError("No respondent answer files found in the data folder.")

    files_with_index.sort()

    with open(output_path, "w", encoding="utf-8") as out_file:
        for idx, (_, file_name) in enumerate(files_with_index):
            file_path = os.path.join(data_folder_path, file_name)

            with open(file_path, "r", encoding="utf-8") as in_file:
                out_file.write(in_file.read().rstrip())
            out_file.write("\n")

            if idx != len(files_with_index) - 1:
                out_file.write("*\n")
