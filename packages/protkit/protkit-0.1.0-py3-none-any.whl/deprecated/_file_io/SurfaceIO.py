from src.util.surface import Surface

class SurfaceIO():
    @staticmethod
    def read(file_path: str) -> Surface:
        return Surface()

    @staticmethod
    def write(file_path: str, surface: Surface):
        with open(file_path, "wt") as file:
            file.write("")
