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
echo.
echo - Installing torch for AMD GPUs (Using torch 2.3.0 if you want you can change it but this works well with zluda)
pip install torch==2.3.0 torchvision==0.18.0 --index-url https://download.pytorch.org/whl/cu118 --quiet
echo.
echo - Installing necessary packages
pip install tqdm wand >= 0.6.10 --quiet
pip install fonttools scipy waitress bottle diskcache flake8 psutil pyyaml onnx onnxconverter_common lpips packaging dctorch timm rembg pywin32 --quiet
pip install "av>=12.2.0,<14.0.0" --quiet
pip install truststore; python_version >= '3.10' --quiet
pip install wxpython >= 4.0.0 --quiet
echo.
echo - Downloading models
echo.
python -m iw3.download_models
echo.
echo - Patching ZLUDA (Zluda 3.8.4 for HIP SDK 5.7.1)
curl -sL --ssl-no-revoke https://github.com/lshqqytiger/ZLUDA/releases/download/rel.c0804ca624963aab420cb418412b1c7fbae3454b/ZLUDA-windows-rocm5-amd64.zip > zluda.zip
tar -xf zluda.zip
del zluda.zip
copy zluda\cublas.dll venv\Lib\site-packages\torch\lib\cublas64_11.dll /y >NUL
copy zluda\cusparse.dll venv\Lib\site-packages\torch\lib\cusparse64_11.dll /y >NUL
copy zluda\nvrtc.dll venv\Lib\site-packages\torch\lib\nvrtc64_112_0.dll /y >NUL
echo - ZLUDA is patched. (Zluda 3.8.4 for HIP 5.7.1)
echo. 
echo  - Patching ZOED models.
copy patch\attractor.py iw3\pretrained_models\hub\nagadomi_ZoeDepth_iw3_main\zoedepth\models\layers\ /y >NUL
copy patch\attractor.py iw3\pretrained_models\hub\nagadomi_Depth-Anything_iw3_main\metric_depth\zoedepth_depth_anything\models\layers\ /y >NUL
echo.
echo You can now use the iw3 gui & cli with gpu acceleration with amd gpu's. 
echo Run iw3z.bat to start iw3 with amd gpu support. 
echo.
echo ** IMPORTANT ** All depth models work. (zoed models are higher quality but slower) BUT for METHOD only "forward_fill" work.
echo ******** The first time you select a model and generate, (only a new type of model) it would seem like your computer is doing nothing, 
echo ******** that's normal , zluda is creating a database for future use. That only happens once for every new type of model.
pause
