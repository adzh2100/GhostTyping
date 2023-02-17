class FileService():
  def append_to_file(self, file_name, text):
    file = open(file_name, 'a')
    file.write(text)
    file.close()

  def read_from_file(self, file_name):
    file = open(file_name, 'r')
    content = file.readlines()
    file.close()

    return content
