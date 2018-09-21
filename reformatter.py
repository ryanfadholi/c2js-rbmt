import constants

class Reformatter:
    def write(self, target_path):
        """Copies temporary file contents to the given target path."""
        with open(constants.OUTPUT_TEMPFILE_PATH, "r") as result_temp:
            with open(target_path, "w") as target:
                target.write(result_temp.read())