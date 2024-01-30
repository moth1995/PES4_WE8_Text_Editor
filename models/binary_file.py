class BinaryFile():
    def __init__(self, filename:str,):
        self.filename = filename

    @property
    def file_bytes(self):
        try:
            with open(self.filename, "rb") as f: 
                return bytearray(f.read()) 
        except Exception:
            return bytearray()
    
    def set_bytes(self, offset:int, data:bytes):
        with open(self.filename, "r+b") as f:
            f.seek(offset, 0)
            f.write(data)
    
    @property
    def size(self):
        return (len(self.file_bytes))
    