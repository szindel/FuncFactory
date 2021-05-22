import yaml


def read_yaml(file):
    with open(file, "r") as stream:
        try:
            file_yaml = yaml.safe_load(stream)
            return file_yaml
        except Exception as ex:
            print(ex)
            print("Error occured reading file: {file}. Excluding file from factory.")
            return None
