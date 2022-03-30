from fs import FileSystem


# map[directory] = [[file1]=data, [file2]=data]
def test_initial_state(fs: FileSystem):
    try:
        assert fs.contains_dir("/") is True, "The file-system has no root dir path"
        print(f"(v) Test initial state passed!")

    except Exception as error:
        print(f"(x) Test initial state failed failed: {error}")
        raise error


def test_write_read_file(fs: FileSystem, file_path: str, data: str):
    try:
        data_size = fs.write_file(file_path, data)
        assert data_size == len(data)

        assert fs.contains_file(file_path)

        file_contents = fs.read_file(file_path)
        assert file_contents == data
        print(f"(v) Test write file passed! path={file_path}")

    except Exception as err:
        print(f"(x) Test write file failed!: {err}")
        raise err


def test_delete_file(fs: FileSystem, path: str):
    try:
        fs.rm(path)
        print(f"(v) Test delete path passed! path={path}")

    except Exception as errorDeleting:
        print(f"(x) Test delete path failed!: {errorDeleting}")
        raise errorDeleting


def test_read_root(fs: FileSystem, expected):
    try:
        path = "/"
        names = fs.read_dir(path)
        for file in expected:
            if file not in names:
                print(f"(x) Test read root dir path failed!: {file} not in {names}")

        print(f"(v) Test read root path passed!")

    except Exception as errorDeleting:
        print(f"(x) Test delete path fialed!: {errorDeleting}")
        raise errorDeleting


if __name__ == '__main__':
    fs_instance = FileSystem()
    test_initial_state(fs_instance)
    test_write_read_file(fs_instance, "/marcello.txt", "My name is Marcello")
    test_write_read_file(fs_instance, "/leandro.txt", "My name is Leandro")
    test_write_read_file(fs_instance, "/thiago.txt", "My name is Thiago")
    test_delete_file(fs_instance, "/thiago.txt")

    fs_instance.mkdir("/users")
    fs_instance.mkdir("/users/awesome")
    test_write_read_file(fs_instance, "/users/awesome/nft.txt", "My nft is in ipfs")
    test_read_root(fs_instance, ["/leandro.txt", "/marcello.txt", "/users"])

