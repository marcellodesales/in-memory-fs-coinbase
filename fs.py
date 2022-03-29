# map[directory] = [[file1]=data, [file2]=data]
class FileSystem:

    def __init__(self):
        # [string] = [string[data]]
        self.tree = dict()
        self.mkdir("/")

    def mkdir(self, path):
        self.tree[path] = []

    def write_file(self, path, data):
        dir_path, file_name = self._make_file_metadata(path)

        # Check first if the path exists
        if not self.contains_dir(dir_path):
            raise Exception(f"The dir '{path}' does NOT exist")
        if self.contains_file(dir_path, file_name):
            raise Exception(f"The file '{path}' already exists!")

        return self._add_file_to_tree(dir_path, file_name, data)

    def _add_file_to_tree(self, dir_path, file_name, data):
        file = dict()
        file[file_name] = data
        tree_ref = self.tree[dir_path]
        tree_ref.append(file)
        return len(data)

    def read_file(self, path):
        dir_path, file_name = FileSystem._make_file_metadata(path)
        if self.contains_file(dir_path, file_name):
            tree_ref = self.tree[dir_path]
            for file_ref in tree_ref:
                if file_name in file_ref:
                    return file_ref[file_name]

    @staticmethod
    def _make_file_metadata(file_path):
        paths = file_path.split("/")
        dir_path = "/".join(paths[:-1])
        file_path = paths[-1]
        return "/" if len(dir_path) == 0 else dir_path, file_path

    def contains_dir(self, dir_path):
        return dir_path in self.tree

    def contains_file(self, dir_path, file_name):
        if not self.contains_dir(dir_path):
            return False

        for file_data in self.tree[dir_path]:
            if file_name in file_data:
                return True
        return False

