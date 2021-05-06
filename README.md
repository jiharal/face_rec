## Generate source code from protos file.

```cmd
python -m grpc_tools.protoc -I ./protos --python_out=. --grpc_python_out=. cctv_stream.proto
```