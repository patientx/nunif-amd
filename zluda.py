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
else:
    print(f"  ::  CUDA device detected: {zluda_device_name or 'None'}")
# ------------------- End Zluda detection -------------------
