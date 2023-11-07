import os
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use('Agg')

SAMPLE = "sample"
TOTAL_COUNT = "total_count"
CELL_TYPES = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
PERCENTAGE_SUFFIX = "_percentage"


def calculate_percentages(df: pd.DataFrame) -> pd.DataFrame:
    df[TOTAL_COUNT] = df[CELL_TYPES].sum(axis=1)
    for cell_type in CELL_TYPES:
        percentage_col_name = f"{cell_type}{PERCENTAGE_SUFFIX}"
        df[percentage_col_name] = (df[cell_type] / df[TOTAL_COUNT]) * 100
    return df


def load_data(file_path: str) -> pd.DataFrame:
    input_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', file_path))
    try:
        return pd.read_csv(input_file)
    except FileNotFoundError as e:
        print(f"file not found at path: {input_file}")
        raise e


def save_data(df: str, output_file: str) -> None:
    try:
        df.to_csv(output_file, index=False)
    except Exception as e:
        print(f"Failed to save the file at path: {output_file}.")
        raise e


def create_output_folders(input_file: str) -> str:
    base_output_folder = "output"
    os.makedirs(base_output_folder, exist_ok=True)

    input_file_name = os.path.splitext(os.path.basename(input_file))[0]

    input_file_folder = os.path.join(base_output_folder, input_file_name)
    os.makedirs(input_file_folder, exist_ok=True)

    images_folder = os.path.join(input_file_folder, "images")
    os.makedirs(images_folder, exist_ok=True)

    return input_file_folder, images_folder


def CellAnalyzer(input_file: str, output_file: str) -> None:
    cell_data = load_data(input_file)
    cell_data_with_percentages = calculate_percentages(cell_data)

    input_file_folder, images_folder = create_output_folders(input_file)

    responders = cell_data_with_percentages[cell_data_with_percentages['response'] == 'y']
    non_responders = cell_data_with_percentages[cell_data_with_percentages['response'] == 'n']

    image_urls = []

    for cell_type in CELL_TYPES:
        plt.figure(figsize=(8, 6))
        plt.boxplot([responders[f"{cell_type}{PERCENTAGE_SUFFIX}"], non_responders[f"{cell_type}{PERCENTAGE_SUFFIX}"]],
                    labels=['Responders', 'Non-Responders'])
        plt.title(f'Boxplot of {cell_type} Relative Frequencies')
        plt.ylabel('Percentage (%)')
        plt.xlabel('Response')
        image_file_path = os.path.join(
            images_folder, f'{cell_type}_boxplot.png')
        plt.savefig(image_file_path)
        image_urls.append(f'{input_file_folder}/images/{cell_type}_boxplot.png')
    

    analysis = []
    for cell_type in CELL_TYPES:
        responders_mean = responders[f"{cell_type}{PERCENTAGE_SUFFIX}"].mean()
        non_responders_mean = non_responders[f"{cell_type}{PERCENTAGE_SUFFIX}"].mean(
        )
        analysis.append(f'{cell_type} - Responders Mean: {responders_mean:.2f}%, Non-Responders Mean: {non_responders_mean:.2f}%')

    output_file_path = os.path.join(input_file_folder, output_file.split(".")[0])
    save_data(cell_data_with_percentages, output_file_path)
    return analysis, image_urls
