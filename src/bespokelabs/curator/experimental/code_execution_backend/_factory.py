from typing import Optional

from bespokelabs.curator.experimental.types import CodeExecutionBackendConfig


class _CodeExecutionBackendFactory:
    @classmethod
    def create(cls, backend: str, backend_params: Optional[CodeExecutionBackendConfig] = None):
        if backend_params is None:
            backend_params = {}

        if backend == "multiprocessing":
            from bespokelabs.curator.experimental.code_execution_backend.multiprocessing_backend import MultiprocessingCodeExecutionBackend

            _code_executor = MultiprocessingCodeExecutionBackend(CodeExecutionBackendConfig(**backend_params))
        elif backend == "docker":
            from bespokelabs.curator.experimental.code_execution_backend.docker_backend import DockerCodeExecutionBackend

            _code_executor = DockerCodeExecutionBackend(CodeExecutionBackendConfig(**backend_params))
        elif backend == "ray":
            from bespokelabs.curator.experimental.code_execution_backend.ray_backend import RayCodeExecutionBackend

            _code_executor = RayCodeExecutionBackend(CodeExecutionBackendConfig(**backend_params))
        else:
            raise ValueError(f"Unsupported backend: {backend}")

        return _code_executor
