::: FOR AMD GPU'S ON WINDOWS :::

## Dependencies

If coming from the very start, you need :

1. **Git**: Download from https://git-scm.com/download/win.
   During installation don't forget to check the box for "Use Git from the Windows Command line and also from
   3rd-party-software" to add Git to your system's PATH.
2. **Python** ([3.10.11](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe) 3.11 also works, but 3.10 is used by most popular nodes atm): Install the latest release from python.org. **Don't Use
   Windows Store Version**. If you have that installed, uninstall and please install from python.org. During
   installation remember to check the box for "Add Python to PATH when you are at the "Customize Python" screen.
3. **Visual C++ Runtime**: Download [vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe) and install it.
4. Install **HIP SDK 5.7.1** from [HERE](https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html) the correct version, "Windows 10 & 11 5.7.1 HIP SDK"
5. Add the system variable HIP_PATH, value: `C:\\Program Files\\AMD\\ROCm\\5.7\\` (This is the default folder, if you
   have installed it on another drive, change if necessary)
    1. Check the variables on the lower part (System Variables), there should be a variable called: HIP_PATH.
    2. Also check the variables on the lower part (System Variables), there should be a variable called: "Path".
       Double-click it and click "New" add this: `C:\Program Files\AMD\ROCm\5.7\bin`
7. If you have an AMD GPU below 6800 (6700,6600 etc.), download the recommended library files for your gpu
   from [Brknsoul Repository](https://github.com/brknsoul/ROCmLibs)
    1. Go to folder "C:\Program Files\AMD\ROCm\5.7\bin\rocblas", there would be a "library" folder, backup the files
       inside to somewhere else.
    2. Open your downloaded optimized library archive and put them inside the library folder (overwriting if
       necessary): "C:\\Program Files\\AMD\\ROCm\\5.7\\bin\\rocblas\\library"
8. Reboot your system.

## Setup (Windows-Only)

Open a cmd prompt. (Powershell doesn't work, you have to use command prompt.)

[ You open command prompt via typing "cmd" in start / run OR the easier way going into the drive or directory you want to install nunif/iw3 to on explorer, click on the address bar and type "cmd" press enter, this would open a commandline window on the directory you are in on explorer at the moment. ]

```bash
git clone https://github.com/patientx/nunif-amd
```

```bash
cd nunif-amd
```

```bash
installzludaforamd.bat
```

to start for later use (or create a shortcut to) :

```bash
iw3z.bat
```

NOTES :::: 

- You can now use the iw3 gui & cli with gpu acceleration with amd gpu's. 
- Run iw3z.bat to start iw3 with amd gpu support.
- CLI can also be used, to use it first you have enable venv , go into nunif-amd folder in commandline, "venv\scripts\activate" enter , now you can see the available parameters with "zluda\zluda.exe -- python -m iw3 -h" then use them to generate from the command prompt.

- ** IMPORTANT ** All depth models work. All method's now* work.
- * Thanks to https://github.com/nagadomi , I was able to disable everything incompatible with ZLUDA, they now work.

******** The first time you select a model and generate, (only a new type of model) it would seem like your computer is doing nothing, 
******** that's normal , zluda is creating a database for future use. That only happens once for every new type of model.


-----------------------------------------------------------------
-----------------------------------------------------------------
ORIGINAL README

My playground.

For the time being, I will make incompatible changes.

## waifu2x

[waifu2x/README.md](./waifu2x/README.md)

waifu2x: Image Super-Resolution for Anime-Style Art. Also it supports photo models (GAN based models)

The repository contains waifu2x pytorch implementation and pretrained models, started with porting the original [waifu2x](https://github.com/nagadomi/waifu2x).

The demo application can be found at
- https://waifu2x.udp.jp/ (Cloud version)
- https://unlimited.waifu2x.net/ (In-Browser version).

## iw3

[iw3/README.md](./iw3/README.md)

I want to watch any 2D video as 3D video on my VR device, so I developed this very personal tool.

iw3 provides the ability to convert any 2D image/video into side-by-side 3D image/video.

## cliqa

[cliqa/README.md](./cliqa/README.md)

`cliqa` provides low-vision image quality scores that are more consistent across different images.

It is useful for filtering low-quality images with a threshold value when creating image datasets.

Currently, the following two models are supported.

- JPEGQuality: Predicts JPEG Quality from image content
- GrainNoiseLeve: Predicts Noise Level related to photograph and PSNR degraded by that noise

CLI tools are also available to filter out low quality images using these results.

## Install

### Installer for Windows users

- [nunif windows package](windows_package/docs/README.md)
- [nunif windows package (日本語)](windows_package/docs/README_ja.md)

### For developers

#### Dependencies

- Python 3 (Works with Python 3.10 or later, developed with 3.10)
- [PyTorch](https://pytorch.org/get-started/locally/)
- See requirements.txt

We usually support the latest version. If there are bugs or compatibility issues, we will specify the version.

- [INSTALL-ubuntu](INSTALL-ubuntu.md)
- [INSTALL-windows](INSTALL-windows.md)
- [INSTALL-macos](INSTALL-macos.md)
