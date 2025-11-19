# PyAudio Installation Guide for Apple Silicon Macs

## Issue
On Apple Silicon Macs (M1, M2, etc.), you may encounter architecture compatibility issues when installing PyAudio. The error typically looks like:
```
Could not import the PyAudio C module 'pyaudio._portaudio'
...
(mach-o file, but is an incompatible architecture (have 'x86_64', need 'arm64'))
```

## Status
✅ **PyAudio has been successfully installed and is working correctly on this system.**

## Solution Options

### Option 1: Install portaudio first, then PyAudio
```bash
# Install portaudio (dependency for PyAudio)
brew install portaudio

# Install PyAudio with proper architecture flags
CPPFLAGS=-I/opt/homebrew/include LDFLAGS=-L/opt/homebrew/lib pip install pyaudio
```

### Option 2: Use conda (if you have it installed)
```bash
conda install pyaudio
```

### Option 3: Install pre-compiled wheel
```bash
pip install --no-cache-dir pyaudio
```

### Option 4: Force reinstall with architecture-specific flags
```bash
arch -arm64 pip install pyaudio --no-cache-dir --force-reinstall
```

## Verification
After installation, verify PyAudio is working:
```bash
python -c "import pyaudio; print('PyAudio installed and working correctly')"
```

✅ **Success**: PyAudio has been successfully reinstalled with proper ARM64 architecture support on this system.

## Troubleshooting

### If you still get architecture errors:
1. Make sure you're using the ARM64 version of Python:
   ```bash
   python -c "import platform; print(platform.machine())"
   ```
   Should output: `arm64`

2. Check if you have multiple Python installations:
   ```bash
   which python
   ```

3. Try using python3 explicitly:
   ```bash
   python3 -c "import pyaudio; print('PyAudio working')"
   ```

## Alternative: Use the existing functionality
Even without PyAudio, you can still use the ASR functionality by:
1. Placing audio files in the Data directory
2. Using the GUI "🎙️ GEMINI ASR" button (it will transcribe existing audio files)
3. Calling the ASR functions directly with file paths

The system will automatically use any audio file found in the Data directory for transcription.