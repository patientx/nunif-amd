import torch

# ------------------- Hide ROCm/HIP -------------------
import os

os.environ.pop("ROCM_HOME", None)
os.environ.pop("HIP_HOME", None)
os.environ.pop("ROCM_VERSION", None)

paths = os.environ["PATH"].split(";")
paths_no_rocm = [p for p in paths if "rocm" not in p.lower()]
os.environ["PATH"] = ";".join(paths_no_rocm)
# ------------------- End ROCm/HIP Hiding -------------

# Fix for cublasLt errors on newer ZLUDA (if no hipblaslt)
os.environ['DISABLE_ADDMM_CUDA_LT'] = '1'

import torch

# ------------------- ZLUDA Detection -------------------
zluda_device_name = torch.cuda.get_device_name() if torch.cuda.is_available() else ""
is_zluda = zluda_device_name.endswith("[ZLUDA]")
# ------------------- End Detection --------------------

# ------------------- Audio Ops Patch -------------------
if is_zluda:
    _torch_stft = torch.stft
    _torch_istft = torch.istft

    def z_stft(input: torch.Tensor, window: torch.Tensor, *args, **kwargs):
        return _torch_stft(input=input.cpu(), window=window.cpu(), *args, **kwargs).to(input.device)

    def z_istft(input: torch.Tensor, window: torch.Tensor, *args, **kwargs):
        return _torch_istft(input=input.cpu(), window=window.cpu(), *args, **kwargs).to(input.device)

    def z_jit(f, *_, **__):
        f.graph = torch._C.Graph()
        return f

    torch._dynamo.config.suppress_errors = True
    torch.stft = z_stft
    torch.istft = z_istft
    torch.jit.script = z_jit
# ------------------- End Audio Patch -------------------

# ------------------- Top-K Fallback Patch -------------------
if is_zluda:
    _topk = torch.topk

    def safe_topk(input: torch.Tensor, *args, **kwargs):
        device = input.device
        values, indices = _topk(input.cpu(), *args, **kwargs)
        return torch.return_types.topk((values.to(device), indices.to(device),))

    torch.topk = safe_topk
# ------------------- End Top-K Patch -------------------

# ------------------- ONNX Runtime Patch -------------------
try:
    import onnxruntime as ort

    if is_zluda:
        print("\n***----------------------ZLUDA-----------------------------***")
        print("  ::  Patching ONNX Runtime for ZLUDA — disabling CUDA EP.")

        # Store original get_available_providers
        original_get_available_providers = ort.get_available_providers

        def filtered_providers():
            return [ep for ep in original_get_available_providers() if ep != "CUDAExecutionProvider"]

        # Patch ONLY the _pybind_state version (used during session creation)
        ort.capi._pybind_state.get_available_providers = filtered_providers

        # Wrap InferenceSession to force CPU provider when CUDA is explicitly requested
        OriginalSession = ort.InferenceSession

        class SafeInferenceSession(OriginalSession):
            def __init__(self, *args, providers=None, **kwargs):
                if providers and "CUDAExecutionProvider" in providers:
                    print("  ::  Forcing ONNX to use CPUExecutionProvider instead of CUDA.")
                    providers = ["CPUExecutionProvider"]
                super().__init__(*args, providers=providers, **kwargs)

        ort.InferenceSession = SafeInferenceSession
except ImportError:
    print("  ::  ONNX Runtime not installed — skipping patch.")
except Exception as e:
    print("  ::  Failed to patch ONNX Runtime:", e)
# ------------------- End ONNX Patch -------------------

# ------------------- ZLUDA Backend Patch -------------------
if is_zluda:
    print("  ::  ZLUDA detected, disabling non-supported functions.      ")
    torch.backends.cudnn.enabled = False

    if hasattr(torch.backends.cuda, "enable_flash_sdp"):
        torch.backends.cuda.enable_flash_sdp(False)
    if hasattr(torch.backends.cuda, "enable_math_sdp"):
        torch.backends.cuda.enable_math_sdp(True)
    if hasattr(torch.backends.cuda, "enable_mem_efficient_sdp"):
        torch.backends.cuda.enable_mem_efficient_sdp(False)
    print("  ::  CuDNN, flash_sdp, mem_efficient_sdp disabled.           ")
 
if is_zluda:
    print(f"  ::  Using ZLUDA with device: {zluda_device_name}")
    print("***--------------------------------------------------------***\n")
else:
    print(f"  ::  CUDA device detected: {zluda_device_name or 'None'}")
    print("***--------------------------------------------------------***\n")
# ------------------- End Zluda detection -------------------
# ------------------- Check/Install Required Modules -------------------
import subprocess
import pkg_resources

def check_install(package, min_version=None):
    try:
        if min_version:
            pkg_resources.require(f"{package}>={min_version}")
        else:
            __import__(package)
    except (ImportError, pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", f"{package}>={min_version}" if min_version else package],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass  # Silent fail

check_install("safetensors")
check_install("pillow_heif")
check_install("av", "14.2.0")
# ------------------- End Module Check -------------------

from .utils import create_parser, set_state_args, iw3_main
from . import models # noqa
from nunif.logger import logger
from nunif.device import device_is_cuda


def main():
    parser = create_parser()
    args = parser.parse_args()
    set_state_args(args)
    iw3_main(args)

    if device_is_cuda(args.state["device"]):
        max_vram_mb = int(torch.cuda.max_memory_allocated(args.state["device"]) / (1024 * 1024))
        logger.debug(f"GPU Max Memory Allocated {max_vram_mb}MB")


if __name__ == "__main__":
    main()
