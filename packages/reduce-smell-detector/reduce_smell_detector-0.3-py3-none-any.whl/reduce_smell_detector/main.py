from reduce_smell_detector import detector as dt


def detect_all(input_path, output_path=None):
    dt.main_method(input_path=input_path, output_directory=output_path)
    print("detection process finished.")