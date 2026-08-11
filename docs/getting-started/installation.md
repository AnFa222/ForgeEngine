# Installation & Setup

## Requirements

Before installing ForgeEngine, ensure you have the following prerequisites:

### Python
- **Python 3.x** (3.8 or higher recommended)

### For Pygame Pipeline (Recommended for Beginners)
- **pygame** - Cross-platform set of Python modules for game development

### For ModernGL Pipeline (Optional, Advanced)
- **glfw** - OpenGL binding library
- **moderngl** - Modern OpenGL wrapper
- **numpy** - Numerical computing library
- **pillow** - Image processing library

### For Building Executables (Optional)
- **pyinstaller** - Create standalone executables from Python scripts

## Step 1: Install Python

### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Click Install

### macOS
```bash
# Using Homebrew (recommended)
brew install python3

# Or download from python.org
```

### Linux
```bash
# Ubuntu/Debian
sudo apt-get install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python
```

Verify installation:
```bash
python --version
# or
python3 --version
```

## Step 2: Install ForgeEngine

### Clone from Git Repository

```bash
# Navigate to your projects directory
cd /path/to/your/projects

# Clone the repository
git clone https://github.com/your-username/ForgeEngine.git
cd ForgeEngine
```

### Install Dependencies

**For Pygame Pipeline (Recommended):**
```bash
pip install pygame
```

**For ModernGL Pipeline:**
```bash
pip install glfw moderngl numpy pillow
```

**For Building Executables:**
```bash
pip install pyinstaller
```

**Install All (Recommended for Full Features):**
```bash
pip install pygame pyinstaller glfw moderngl numpy pillow
```

### Verify Installation

Test that ForgeEngine imports correctly:

```bash
python -c "import ForgeEngine; print('ForgeEngine installed successfully!')"
```

You should see:
```
Forge engine has been initialized.
ForgeEngine installed successfully!
```

## Step 3: Create Your First Project

### Create Project Directory

```bash
# Create a new directory for your game
mkdir my-first-game
cd my-first-game

# Copy the assets directory from ForgeEngine (optional)
cp -r /path/to/ForgeEngine/assets ./
```

### Create a Simple Game File

Create `game.py`:

```python
import ForgeEngine

# Create the engine
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 800
engine.window.height = 600
engine.window.title = "My First Game"
engine.window.initialize()

# Create a scene
scene = ForgeEngine.Scene("main")
scene.background_color = (50, 150, 255)

# Create a camera
camera = ForgeEngine.Object(engine)
camera.transform = ForgeEngine.Transform(x=0, y=0)
camera.camera = ForgeEngine.Camera(1)
camera.camera.render_zone_width = 800
camera.camera.render_zone_height = 600

scene.add_object(camera)

# Load the scene
engine.add_scene(scene)
engine.load_scene("main")

# Run the game
engine.main_loop()
```

### Run Your Game

```bash
python game.py
```

You should see a blue window! Congratulations, you've created your first ForgeEngine game.

## Step 4: Add Assets

### Asset Directory Structure

```
my-first-game/
├── game.py
└── assets/
    ├── images/
    │   ├── player.png
    │   └── background.png
    ├── audio/
    │   ├── jump.wav
    │   └── music.mp3
    └── fonts/
        └── Arial.ttf
```

### Loading Assets

```python
# Load an image
player_image = engine.import_image(r"assets\player.png")

# Load audio
jump_sound = engine.import_audio(r"assets\jump.wav")
```

## Troubleshooting Installation

### "ModuleNotFoundError: No module named 'pygame'"

**Solution:** Install pygame
```bash
pip install pygame
```

### "python: command not found" (macOS/Linux)

**Solution:** Use `python3` instead:
```bash
python3 game.py
```

Or add an alias to your shell profile:
```bash
# Add to ~/.bashrc or ~/.zshrc
alias python=python3
```

### ImportError on ForgeEngine

**Solution:** Make sure you're in the ForgeEngine directory or that ForgeEngine is in your Python path:

```bash
# Add ForgeEngine to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/ForgeEngine"
```

### pygame module not found after installation

**Solution:** You may have multiple Python installations. Ensure you're using the correct one:

```bash
# Find which pip is being used
which pip

# Install for specific Python version
python3 -m pip install pygame
```

## Next Steps

- Read the [Getting Started Guide](first-project.md)
- Check out the [Tutorials](../tutorials/tutorial-01-hello-world.md)
- Learn about [Components](../architecture/systems.md)

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review error messages carefully
3. Search existing GitHub issues
4. Create a new issue with:
   - Your Python version
   - Your OS
   - The complete error message
   - Minimal code that reproduces the issue
