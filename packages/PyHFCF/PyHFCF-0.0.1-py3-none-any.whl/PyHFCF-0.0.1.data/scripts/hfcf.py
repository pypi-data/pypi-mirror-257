class HFCF:
    def __init__(self, filename_nofileextension: str, pythoninitclassid: float = 0) -> None:
        self.file = None
        if '.hfcf' in filename_nofileextension:
            self.file = filename_nofileextension.strip('.hfcf')
        else:
            self.file = filename_nofileextension
        self.id = pythoninitclassid

    def get(self, attrib: str):
        try:
            path = attrib.split(";")
            key = str(path[0])
            index = int(path[1]) - 1

            with open(f"{self.file}.hfcf", 'r') as f:
                data = f.readlines()

            filtered_data = [line.strip() for line in data if not line.strip().startswith(";;")]

            if 0 <= index < len(filtered_data):
                value = filtered_data[index].split(f'{key}=')[1].strip()

                if value.isalpha():
                    return str(value)
                elif value.isalnum():
                    return str(value)
                elif value.replace('.', '', 1).isdigit():
                    try:
                        return float(value)
                    except ValueError:
                        return str(value)
                elif ',' in value:
                    return value.split(',')
                else:
                    return str(value)
            else:
                print(f"Error: Index {index} is out of range.")
        except (IndexError, FileNotFoundError) as e:
            print(f"Error: {e}")

    def set(self, attrib: str, new_value):
        try:
            path = attrib.split(";")
            key = str(path[0])
            index = int(path[1]) - 1

            with open(f"{self.file}.hfcf", 'r') as f:
                data = f.readlines()

            if 0 <= index < len(data):
                data[index] = data[index].replace(f'{key}={data[index].split(f"{key}=")[1].strip()}', f'{key}={new_value}')

                with open(f"{self.file}.hfcf", 'w') as f:
                    f.writelines(data)
            else:
                print(f"Error: Index {index} is out of range.")
        except (IndexError, FileNotFoundError) as e:
            print(f"Error: {e}")