MATH1604 Group Project 25/26 - Team Member 2


This module includes two functions that work together to bring data into the Analysis of Python Quiz Response project:

      1. download_answer_files - It acquires the raw response files from a remote GitHub repository 
                                 and achives them locally under a uniform naming structure.

      2. collated_answer_files - It consolidates all locally stored respondent files into a single, 
                                 collated dataset for subsequent processing by Team Member 3 and 4

================================================================================================================================

import os
import re
import urllib.request
from urllib.parse import urljoin


def download_answer_files(cloud_url: str, path_to_data_folder: str, respondent_index: int) -> None:
      """
      Download quiz answer files from GitHub and saves them locally.

      This function goes through each respondent file one by one, from a1.txt up to aN.txt, 
      fetches it from the given URL, and saves it into the data folder with a clear name like 
      answers_respondent_1.txt. If the folder does not exist yet, it gets created automatically.

      If a file cannot be download, for example, because it does not exist on the server, the 
      function stops and raises an OSError telling you which URL failed. It does not silently 
      skip missing files.
      

      Parameters:
      -----------
      cloud_url : str
           The base URL where the files are hosted.
           "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"
      path_to_data_folder : str
           Where to save the downloaded files on your computer.
           e.g. "data"
      respondent_index : int
           How many files to try to download.
           e.g. passing 64 will attempt to download a1.txt through a64.txt.
           

      Returns: 
      --------
      None


      Raises:
      -------
      ValueError - If any of the inputs are empty or invalid.
      OSError - If a file could not be downloaded, with a message showing the URL that failed


      Examples:
      ---------
      Download all 64 respondent files:

         download_answer_files(
               "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main",
               "data",
               64
         )
         
      Test what happens when ask for more files than exist:
      
         download_answer_files(
               "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main",
               "data",
               70
         )
         #Files a65.txt to a70.txt do not exist, so this will raise an OSError when it reaches a65.txt.
      
      """
      if not isinstance(cloud_url, str) or not cloud_url.strip():
            raise ValueError("cloud_url must be a non-empty string.")
      if not isinstance(path_to_data_folder, str) or not path_to_data_folder.strip():
           raise ValueError("path_to_data_folder must be a non-empty string."
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
      """
      Combines all individual respondent files into one single file.

      This function reads every answers_respondent_N.txt files from the data folder,
      sorts them by respondent number and writes them all into a single file called 
      collated_answers.txt inside the output folder. A line containing just an asterisk (*) 
      is placed between each respondent's section so that the file can be split back apart
      later.

      The output folder is placed alongside the data folder, so if your data folder is at 
      "data", the output will go to "output/collated_answers.txt".

      Parameters:
      -----------
      data_folder_path : str
           Path to the folder containing the individual respondent files.
           e.g. "data".


      Returns:
      --------
      None


      Raises:
      -------
      FileNotFoundError - If the data folder path you provided does not exist.
      ValueError - If the data folder exists but contains no respondent files.


      Notes:
      ------
      The * separator appears between sections only, not after the last one. So
      for 64 respondents, there will be 63 aesterisk lines in total.
      """
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
