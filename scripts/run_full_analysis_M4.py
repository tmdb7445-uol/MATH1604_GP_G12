

from data_preparation_M2 import download_answer_files, collate_answer_files

from data_extraction_M1 import extract_answers_sequence

from data_analysis_M3 import generate_means_sequence, visualize_data

import matplotlib.pyplot as plt


def main():
    cloud_url = "https://raw.githubusercontent.com/fc-leeds/MATH1604_2025_2026_data/main"
    data_folder = "data"
    collated_file = "output/collated_answers.txt"
    num_respondents = 64 #total respondents Based on the data

    # 1. Download data (uses M2s)
    download_answer_files(cloud_url , data_folder, num_respondents)

    # 2. Extract sequences ( using M1s)

    for i in range(1, num_respondents + 1):
        file_path = f"{data_folder}/answers_respondent_{i}.txt"
        extract_answers_sequence(file_path)

    # 3. Collate files into one (using M2)
    #Takes the folder of 70 files and makes 1 file
    collate_answer_files(data_folder)

    # 4. Compute summaries (uses M3) - uses the 1 collated file
    means_list = generate_means_sequence(collated_file)

    # 5. Visualise results (using M3) -using the 1 collated file
    visualize_data(collated_file, 1) 
    plt.savefig("output/plot_scatter.png") #saves a scatterplot
    plt.close()

    visualize_data(collated_file, 2) 
    plt.savefig("output/plot_line.png") # saves a line plot
    plt.close()


if __name__ == "__main__":
    main()




