from fs import FileSystem

from typing import Optional
# https://github.com/tiangolo/fastapi/blob/master/tests/test_modules_same_name_body/app/b.py
from fastapi import FastAPI, Body, HTTPException, Response, status
from pydantic import BaseModel
import json

# https://fastapi.tiangolo.com/tutorial/debugging/
import uvicorn

# Already creates an API docs
# https://fastapi.tiangolo.com/tutorial/security/first-steps/
app = FastAPI()

# The in-memory filesystem instance
fsys = FileSystem()


# https://fastapi.tiangolo.com/tutorial/response-model/#response-model
class FsResponse(BaseModel):
    op: str
    path: str
    type: str
    error: Optional[str] = None
    meta: Optional[object] = None


def _resolve_path(path: str) -> str:
    return path if path[0] == "/" else f"/{path}"


def make_metadata_response(operation: str, path: str, dir_type=True, additional_data=dict()) -> FsResponse:
    response = FsResponse(op=operation, path=path, type="dir" if dir_type else "file")
    # https://www.geeksforgeeks.org/python-merging-two-dictionaries/
    response.meta = additional_data
    return response


# make dir or file
# POST /fs/{path}?file=true  / dir = true | data == null
# https://fastapi.tiangolo.com/tutorial/security/first-steps/ (REST API DOC)
# For path converter: https://fastapi.tiangolo.com/tutorial/path-params/#path-convertor
# For body: https://fastapi.tiangolo.com/tutorial/body/
@app.post("/fs/{path:path}", operation_id="/fs/path", summary="Create a directory or a file", response_model=FsResponse)
def create_dir_or_file(path: str, file: Optional[bool] = False, data=Body(...)):
    path = _resolve_path(path)
    if not file:
        op = "mkdir"
        resp = make_metadata_response(op, path)
        try:
            fsys.mkdir(path)

        except Exception as errorCreatingDir:
            resp.error = errorCreatingDir

            # https://fastapi.tiangolo.com/advanced/additional-status-codes/
            # Avoid errors
            # https://www.w3schools.com/python/gloss_python_json_parse.asp
            # https://stackoverflow.com/questions/65230997/when-i-use-fastapi-and-pydantic-to-build-post-api-appear-a-typeerror-object-of/69537682#69537682
            raise HTTPException(status_code=400, detail=json.loads(resp.json()))

        return resp

    else:
        op = "write_file"
        resp = make_metadata_response(op, path, False)
        try:
            fsys.write_file(path, data)
            resp.meta = {"len": len(data)}

        except Exception as errorCreatingFile:
            resp.error = errorCreatingFile

            # https://fastapi.tiangolo.com/advanced/additional-status-codes/
            # Avoid errors
            # https://www.w3schools.com/python/gloss_python_json_parse.asp
            # https://stackoverflow.com/questions/65230997/when-i-use-fastapi-and-pydantic-to-build-post-api-appear-a-typeerror-object-of/69537682#69537682
            raise HTTPException(status_code=400, detail=json.loads(resp.json()))

        return resp


# get dir or file (metadata)
# GET /fs/{path}?metadata=true
# https://fastapi.tiangolo.com/tutorial/path-params/#path-convertor
@app.get("/fs/{path:path}", operation_id="/fs/path", summary="Retrieves a directory or a file metadata and data", response_model=FsResponse)
def get_path(path: str, metadata: Optional[bool] = True):
    path = _resolve_path(path)

    if fsys.contains_dir(path):
        op = "read_dir"

        if metadata:
            resp = make_metadata_response(op, path)
            resp.meta = fsys.read_dir(path)
            return resp

    elif fsys.contains_file(path):
        data = fsys.read_file(path)
        op = "read_file"

        if metadata:
            resp = make_metadata_response(op, path, False, {"data": data, "len": len(data)})
            return resp

    path = _resolve_path(path)
    op = "read_path"
    # temporary assumption
    is_dir = "." not in path
    resp = make_metadata_response(op, path, is_dir)
    resp.error = f"Provided path '{path}' does not exist!"
    # https://fastapi.tiangolo.com/advanced/additional-status-codes/
    # Avoid errors
    # https://www.w3schools.com/python/gloss_python_json_parse.asp
    # https://stackoverflow.com/questions/65230997/when-i-use-fastapi-and-pydantic-to-build-post-api-appear-a-typeerror-object-of/69537682#69537682
    raise HTTPException(status_code=404, detail=json.loads(resp.json()))


# HEAD /fs/{path}
# https://fastapi.tiangolo.com/tutorial/security/first-steps/ (REST API DOC)
# For path converter: https://fastapi.tiangolo.com/tutorial/path-params/#path-convertor
# For body: https://fastapi.tiangolo.com/tutorial/body/
@app.head("/fs/{path:path}", operation_id="/fs/path", summary="Verifies if a path exist")
def check_path_exists(path: str):
    path = _resolve_path(path)
    if fsys.contains_file(path):
        return Response(status_code=200, headers={"X-type": "file"})

    elif fsys.contains_dir(path):
        return Response(status_code=200, headers={"X-type": "dir"})

    else:
        raise HTTPException(status_code=404, detail="Not found!")


# DELETE /fs/{path}
# delete an empty dir or file
# https://fastapi.tiangolo.com/tutorial/security/first-steps/ (REST API DOC)
# For path converter: https://fastapi.tiangolo.com/tutorial/path-params/#path-convertor
# For body: https://fastapi.tiangolo.com/tutorial/body/
@app.delete("/fs/{path:path}", operation_id="/fs/path", summary="Deletes a dir or a file if it exists")
def check_path_exists(path: str):
    path = _resolve_path(path)
    try:
        type_deleted = fsys.rm(path)
        return Response(status_code=200, headers={"X-type": type_deleted})

    except Exception as error_deleting:
        raise HTTPException(status_code=404, detail=error_deleting)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)