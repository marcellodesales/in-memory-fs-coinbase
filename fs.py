# map[directory] = [[file1]=data, [file2]=data]
class FileSystem:

    def __init__(self):
        # [string] = [string[data]]
        self.tree = dict()
        self.mkdir("/")

    def mkdir(self, path):
        self.tree[path] = []

    def write_file(self, path, data) -> int:
        dir_path, file_name = self.make_file_metadata(path)

        # Check first if the path exists
        if not self.contains_dir(dir_path):
            raise Exception(f"The dir '{path}' does NOT exist")
        if self.contains_file(path):
            raise Exception(f"The file '{path}' already exists!")

        return self._add_file_to_tree(dir_path, file_name, data)

    def _add_file_to_tree(self, dir_path, file_name, data) -> int:
        file = dict()
        file[file_name] = data
        tree_ref = self.tree[dir_path]
        tree_ref.append(file)
        return len(data)

    def read_dir(self, path) -> [dict]:
        if self.contains_dir(path):
            file_names = []
            for file in self.tree[path]:
                # pointer to the keys
                # https://stackoverflow.com/questions/18552001/accessing-dict-keys-element-by-index-in-python3/66109243#66109243
                file_names.append(*file)

            # Add sufix to comprehension https://www.geeksforgeeks.org/python-append-suffix-prefix-to-strings-in-list/
            return [f"{path}/{name}" for name in file_names]

        raise Exception(f"Directory not found '{path}'")

    def read_file(self, path) -> str:
        dir_path, file_name = FileSystem.make_file_metadata(path)
        if self.contains_file(path):
            tree_ref = self.tree[dir_path]
            for file_ref in tree_ref:
                if file_name in file_ref:
                    return file_ref[file_name]

    @staticmethod
    def make_file_metadata(file_path) -> tuple[str, str]:
        paths = file_path.split("/")
        dir_path = "/".join(paths[:-1])
        file_path = paths[-1]
        return "/" if len(dir_path) == 0 else dir_path, file_path

    def contains_dir(self, dir_path) -> bool:
        return dir_path in self.tree

    def contains_file(self, file_path) -> bool:
        dir_path, file_name = FileSystem.make_file_metadata(file_path)
        if not self.contains_dir(dir_path):
            return False

        for file_data in self.tree[dir_path]:
            if file_name in file_data:
                return True
        return False

