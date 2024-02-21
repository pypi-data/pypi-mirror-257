import os
import time
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger
from typing import List, Literal, Optional, Union

import docker
import docker.errors
import docker.types
from huggingface_hub import InferenceClient
from huggingface_hub.inference._text_generation import TextGenerationResponse

from .utils import get_nvidia_gpu_devices, timeout

LOGGER = getLogger("tgi")
HF_CACHE_DIR = f"{os.path.expanduser('~')}/.cache/huggingface/hub"

Quantization_Literal = Literal["bitsandbytes-nf4", "bitsandbytes-fp4", "gptq"]
Torch_Dtype_Literal = Literal["float32", "float16", "bfloat16"]


class TGI:
    def __init__(
        self,
        # model options
        model: str,
        revision: str = "main",
        # image options
        image: str = "ghcr.io/huggingface/text-generation-inference",
        version: str = "latest",
        # docker options
        volume: str = HF_CACHE_DIR,
        shm_size: str = "1g",
        address: str = "127.0.0.1",
        port: int = 1111,
        # tgi launcher options
        sharded: Optional[bool] = None,
        num_shard: Optional[int] = None,
        torch_dtype: Optional[Torch_Dtype_Literal] = None,
        quantize: Optional[Quantization_Literal] = None,
        trust_remote_code: Optional[bool] = False,
        disable_custom_kernels: Optional[bool] = False,
    ) -> None:
        # model options
        self.model = model
        self.revision = revision
        # image options
        self.image = image
        self.version = version
        # docker options
        self.port = port
        self.volume = volume
        self.address = address
        self.shm_size = shm_size
        # tgi launcher options
        self.sharded = sharded
        self.num_shard = num_shard
        self.torch_dtype = torch_dtype
        self.quantize = quantize
        self.trust_remote_code = trust_remote_code
        self.disable_custom_kernels = disable_custom_kernels

        LOGGER.info("\t+ Starting Docker client")
        self.docker_client = docker.from_env()

        try:
            LOGGER.info("\t+ Checking if TGI image exists")
            self.docker_client.images.get(f"{self.image}:{self.version}")
        except docker.errors.ImageNotFound:
            LOGGER.info("\t+ TGI image not found, downloading it (this may take a while)")
            self.docker_client.images.pull(f"{self.image}:{self.version}")

        env = {}
        if os.environ.get("HUGGING_FACE_HUB_TOKEN", None) is not None:
            env["HUGGING_FACE_HUB_TOKEN"] = os.environ["HUGGING_FACE_HUB_TOKEN"]

        LOGGER.info("\t+ Building TGI command")
        self.command = ["--model-id", self.model, "--revision", self.revision]

        if self.sharded is not None:
            self.command.extend(["--sharded", str(self.sharded).lower()])
        if self.num_shard is not None:
            self.command.extend(["--num-shard", str(self.num_shard)])
        if self.quantize is not None:
            self.command.extend(["--quantize", self.quantize])
        if self.torch_dtype is not None:
            self.command.extend(["--dtype", self.torch_dtype])

        if self.trust_remote_code:
            self.command.append("--trust-remote-code")
        if self.disable_custom_kernels:
            self.command.append("--disable-custom-kernels")

        try:
            LOGGER.info("\t+ Checking if GPU is available")
            if os.environ.get("CUDA_VISIBLE_DEVICES") is not None:
                LOGGER.info("\t+ Using specified `CUDA_VISIBLE_DEVICES` to set GPU(s)")
                device_ids = os.environ.get("CUDA_VISIBLE_DEVICES")
            else:
                LOGGER.info("\t+ Using nvidia-smi to get available GPU(s) (if any)")
                device_ids = get_nvidia_gpu_devices()

            LOGGER.info(f"\t+ Using GPU(s): {device_ids}")
            self.device_requests = [docker.types.DeviceRequest(device_ids=[device_ids], capabilities=[["gpu"]])]
        except Exception:
            LOGGER.info("\t+ No GPU detected")
            self.device_requests = None

        self.tgi_container = self.docker_client.containers.run(
            command=self.command,
            image=f"{self.image}:{self.version}",
            volumes={self.volume: {"bind": "/data", "mode": "rw"}},
            ports={"80/tcp": (self.address, self.port)},
            device_requests=self.device_requests,
            shm_size=self.shm_size,
            environment=env,
            detach=True,
        )

        LOGGER.info("\t+ Waiting for TGI server to be ready")
        with timeout(60):
            for line in self.tgi_container.logs(stream=True):
                tgi_log = line.decode("utf-8").strip()
                if "Connected" in tgi_log:
                    break
                elif "Error" in tgi_log:
                    raise Exception(f"\t {tgi_log}")

                LOGGER.info(f"\t {tgi_log}")

        LOGGER.info("\t+ Conecting to TGI server")
        self.url = f"http://{self.address}:{self.port}"
        with timeout(60):
            while True:
                try:
                    self.tgi_client = InferenceClient(model=self.url)
                    self.tgi_client.text_generation("Hello world!")
                    LOGGER.info(f"\t+ Connected to TGI server at {self.url}")
                    break
                except Exception:
                    LOGGER.info("\t+ TGI server not ready, retrying in 1 second")
                    time.sleep(1)

    def close(self) -> None:
        if hasattr(self, "tgi_container"):
            LOGGER.info("\t+ Stoping TGI container")
            self.tgi_container.stop()
            LOGGER.info("\t+ Waiting for TGI container to stop")
            self.tgi_container.wait()

        if hasattr(self, "docker_client"):
            LOGGER.info("\t+ Closing docker client")
            self.docker_client.close()

    def __call__(
        self, prompt: Union[str, List[str]], **kwargs
    ) -> Union[TextGenerationResponse, List[TextGenerationResponse]]:
        return self.generate(prompt, **kwargs)

    def generate(
        self, prompt: Union[str, List[str]], **kwargs
    ) -> Union[TextGenerationResponse, List[TextGenerationResponse]]:
        if isinstance(prompt, str):
            return self.tgi_client.text_generation(prompt=prompt, **kwargs)

        elif isinstance(prompt, list):
            with ThreadPoolExecutor(max_workers=len(prompt)) as executor:
                futures = [
                    executor.submit(self.tgi_client.text_generation, prompt=prompt[i], **kwargs)
                    for i in range(len(prompt))
                ]

            output = []
            for i in range(len(prompt)):
                output.append(futures[i].result())
            return output
