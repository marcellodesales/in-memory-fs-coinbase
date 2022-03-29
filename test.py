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

        dir_path, file_name = FileSystem._make_file_metadata(file_path)
        assert fs.contains_file(dir_path, file_name)

        file_contents = fs.read_file(file_path)
        assert file_contents == data
        print(f"(v) Test write file passed!")

    except Exception as err:
        print(f"(x) Test write file failed!: {err}")
        raise err


if __name__ == '__main__':
    fs_instance = FileSystem()
    test_initial_state(fs_instance)
    test_write_read_file(fs_instance, "/marcello", "My name is Marcello")
