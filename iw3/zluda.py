# hide rocm and hip
import os
os.environ.pop("ROCM_HOME",None)
os.environ.pop("HIP_HOME",None)
os.environ.pop("ROCM_VERSION",None)
paths=os.environ["PATH"].split(";")
paths_no_rocm=[]
for path_ in paths:
    if "rocm" not in path_.lower():
        paths_no_rocm.append(path_)
os.environ["PATH"]=";".join(paths_no_rocm)

import torch
import torch._dynamo 
	

# audio patch
if torch.cuda.is_available() and torch.cuda.get_device_name().endswith("[ZLUDA]"):
    _torch_stft = torch.stft
    _torch_istft = torch.istft

    def z_stft(input: torch.Tensor, window: torch.Tensor, *args, **kwargs):
        return _torch_stft(input=input.cpu(), window=window.cpu(), *args, **kwargs).to(input.device)

    def z_istft(input: torch.Tensor, window: torch.Tensor, *args, **kwargs):
        return _torch_istft(input=input.cpu(), window=window.cpu(), *args, **kwargs).to(input.device)

    def z_jit(f, *_, **__):
        f.graph = torch._C.Graph()
        return f

    torch.stft = z_stft
    torch.istft = z_istft
    torch.jit.script = z_jit 
# audio patch end  

# disable non-supported functions  
    print(" ")
    print("  ::  ZLUDA is found.")
    torch._dynamo.config.suppress_errors = True
    torch.backends.cudnn.enabled = False
    torch.backends.cuda.enable_flash_sdp(False)
    torch.backends.cuda.enable_math_sdp(True)
    torch.backends.cuda.enable_mem_efficient_sdp(False)
    print("  ::  Used device:", torch.cuda.get_device_name())
    print(" ")
