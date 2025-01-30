@echo off
cls
echo --- IW3 Installer for AMD GPU's on Windows (With ZLUDA)---
echo.
echo - Setting up the virtual enviroment
Set "VIRTUAL_ENV=venv"
If Not Exist "%VIRTUAL_ENV%\Scripts\activate.bat" (
    python.exe -m venv %VIRTUAL_ENV%
)
If Not Exist "%VIRTUAL_ENV%\Scripts\activate.bat" Exit /B 1
echo - Virtual enviroment activation
Call "%VIRTUAL_ENV%\Scripts\activate.bat"
echo - Updating the pip package 
python.exe -m pip install --upgrade pip --quiet
echo - Installing torch for AMD GPUs (Using torch 2.3.0 if you want you can change it but this works well with zluda)
pip install torch==2.3.0 torchvision==0.18.0 --index-url https://download.pytorch.org/whl/cu118
echo.
echo - Installing necessary packages
pip install tqdm wand >= 0.6.10 --quiet
pip install fonttools scipy waitress bottle diskcache flake8 psutil pyyaml onnx onnxconverter_common lpips packaging dctorch timm rembg pywin32 --quiet
pip install "av>=12.2.0,<14.0.0" --quiet
pip install truststore; python_version >= '3.10' --quiet
pip install wxpython >= 4.0.0 --quiet
echo.
echo - Downloading models
:: python -m waifu2x.download_models
:: python -m waifu2x.web.webgen
:: python -m iw3.download_models
echo.
echo - Patching ZLUDA (Zluda 3.8.4 for HIP SDK 5.7.1)
curl -s -L https://github.com/lshqqytiger/ZLUDA/releases/download/rel.c0804ca624963aab420cb418412b1c7fbae3454b/ZLUDA-windows-rocm5-amd64.zip > zluda.zip
tar -xf zluda.zip
del zluda.zip
copy zluda\cublas.dll venv\Lib\site-packages\torch\lib\cublas64_11.dll /y >NUL
copy zluda\cusparse.dll venv\Lib\site-packages\torch\lib\cusparse64_11.dll /y >NUL
copy zluda\nvrtc.dll venv\Lib\site-packages\torch\lib\nvrtc64_112_0.dll /y >NUL
echo - ZLUDA is patched. (Zluda 3.8.4 for HIP 5.7.1)
echo. 
echo *** IMPORTANT PLEASE READ CAREFULLY***
echo *** Under iw3 folder, First make a copy of gui.py for backup. Open gui.py with a text editor , even notepad works.
echo *** At the beginning of the file find the line "import torch" after that copy and paste these four lines under it :
echo.
echo torch.backends.cudnn.enabled = False
echo torch.backends.cuda.enable_flash_sdp(False)
echo torch.backends.cuda.enable_math_sdp(True)
echo torch.backends.cuda.enable_mem_efficient_sdp(False)
echo.
echo *** After it would be like this :
echo.
echo ...
echo ...
echo import torch
echo torch.backends.cudnn.enabled = False
echo torch.backends.cuda.enable_flash_sdp(False)
echo torch.backends.cuda.enable_math_sdp(True)
echo torch.backends.cuda.enable_mem_efficient_sdp(False)
echo. 
echo IMAGE_EXTENSIONS = extension_list_to_wildcard(LOADER_SUPPORTED_EXTENSIONS)
echo ...
echo ...
echo.
echo *** Now save the file. 
echo You can now use the iw3 gui with gpu acceleration with amd gpu's. 
echo Run iw3z.bat to start iw3 with amd gpu support. 
echo ******** The first time you select a model (only a new type of model) it would seem like your computer is doing nothing, 
echo ******** that's normal , zluda is creating a database for future use.
pause
