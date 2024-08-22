from pathlib import Path
from typing import List
from phyphox.raw_data_parser import PhyPhoxData


# Maybe add a sort: bool parameter here
def get_phyphox_data(data_folder_name: str) -> List[PhyPhoxData]:
    # Get the current working directory
    current_dir = Path.cwd()

    # Get the parent directory
    parent_dir = current_dir.parent

    # Get the path to the data directory
    data_dir = parent_dir / "data" / "phyphox_data" / data_folder_name

    # Get the filenames in the specified directory
    files_in_current_dir = [file.name for file in data_dir.iterdir()]

    # Return a list of PhyPhoxData for each file name in the directory
    return [PhyPhoxData(data_dir / file_name) for file_name in files_in_current_dir]
