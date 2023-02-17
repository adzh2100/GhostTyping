class FileService:
    def __init__(self):
        pass

    def append_to_file(self, file_name, text):
        file = open(file_name, "a", encoding="UTF-8")
        file.write(text)
        file.close()

    def read_from_file(self, file_name):
        file = open(file_name, "r", encoding="UTF-8")
        content = file.readlines()
        file.close()

        return content
