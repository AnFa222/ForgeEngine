# Troubleshooting

This guide covers common problems you might encounter when using ForgeEngine and how to solve them.

## Installation Issues

### "ModuleNotFoundError: No module named 'pygame'"

**Problem:** ForgeEngine tries to import pygame but it's not installed.

**Solutions:**
1. Install pygame:
   ```bash
   pip install pygame
   ```

2. If you have multiple Python versions, ensure pygame is installed for the correct one:
   ```bash
   python3 -m pip install pygame
   ```

3. Verify installation:
   ```bash
   python -c "import pygame; print(pygame.__version__)"
   ```

### "No module named 'ForgeEngine'"

**Problem:** Python can't find the ForgeEngine module.

**Solutions:**
1. Make sure you're in the correct directory or that ForgeEngine is in your Python path:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:/path/to/ForgeEngine"
   ```

2. Or run your game from the ForgeEngine directory

3. Or install ForgeEngine in development mode:
   ```bash
   cd /path/to/ForgeEngine
   pip install -e .
   ```

### "python: command not found" (macOS/Linux)

**Problem:** Python is installed but the command isn't recognized.

**Solutions:**
1. Use `python3` instead:
   ```bash
   python3 game.py
   ```

2. Create an alias:
   ```bash
   alias python=python3
   echo "alias python=python3" >> ~/.bashrc  # or ~/.zshrc
   ```

## Runtime Issues

### Black Window Appears Then Game Closes

**Problem:** The game starts but crashes immediately.

**Possible causes and solutions:**

1. **No scene loaded:**
   ```python
   # Make sure you have:
   engine.add_scene(scene)
   engine.load_scene("scene_id")
   engine.main_loop()
   ```

2. **No camera in scene:**
   ```python
   # Add a camera to your scene
   camera = ForgeEngine.Object(engine)
   camera.transform = ForgeEngine.Transform(x=0, y=0)
   camera.camera = ForgeEngine.Camera(1)
   scene.add_object(camera)
   ```

3. **Import errors:** Check the console output for error messages (the window might close too fast to see them). Run from terminal to see output:
   ```bash
   python game.py
   ```

### Assets Not Loading

**Problem:** "FileNotFoundError" when trying to load images or audio.

**Solutions:**

1. **Check file paths exist:**
   ```bash
   # Verify file exists
   ls assets/images/player.png  # macOS/Linux
   dir assets\images\player.png  # Windows
   ```

2. **Use correct path separator:**
   ```python
   # Windows
   image = engine.import_image(r"assets\player.png")
   
   # macOS/Linux
   image = engine.import_image("assets/player.png")
   
   # Platform-independent
   from pathlib import Path
   path = str(Path("assets") / "player.png")
   image = engine.import_image(path)
   ```

3. **Check relative paths:**
   - Are you running the script from the correct directory?
   - Does the path work from your current directory?

4. **Use absolute paths for testing:**
   ```python
   import os
   abs_path = os.path.abspath("assets/player.png")
   image = engine.import_image(abs_path)
   ```

### Objects Not Rendering

**Problem:** Objects don't appear on screen.

**Solutions:**

1. **Missing renderer component:**
   ```python
   # Objects need a renderer to be visible
   renderer = ForgeEngine.Renderer(image_id=my_image, layer=1)
   obj.renderer = renderer
   ```

2. **Image not loaded:**
   ```python
   # Load image before using it
   my_image = engine.import_image("path/to/image.png")
   renderer = ForgeEngine.Renderer(image_id=my_image, layer=1)
   ```

3. **Object not added to scene:**
   ```python
   scene.add_object(obj)
   ```

4. **Layer ordering issues:**
   - Higher layer numbers render on top
   - Make sure your object's layer isn't behind other objects:
   ```python
   # Render on top
   renderer = ForgeEngine.Renderer(image_id=my_image, layer=100)
   
   # Render behind
   renderer = ForgeEngine.Renderer(image_id=my_image, layer=1)
   ```

5. **Off-screen positioning:**
   - Check that your object's position is within the render zone:
   ```python
   print(obj.transform.x, obj.transform.y)
   print(camera.camera.render_zone_width, camera.camera.render_zone_height)
   ```

### Input Not Working

**Problem:** Keyboard or mouse input isn't being detected.

**Solutions:**

1. **Check key enum:**
   ```python
   # Use ForgeEngine.Key constants
   if engine.get_key(ForgeEngine.Key.W):
       print("W pressed")
   ```

2. **Use correct timing:**
   ```python
   # get_key checks if key is currently held
   if engine.get_key(ForgeEngine.Key.SPACE):
       pass  # Currently pressed
   
   # get_key_down checks if key was pressed this frame
   if engine.get_key_down(ForgeEngine.Key.SPACE):
       pass  # Just pressed
   
   # get_key_up checks if key was released this frame
   if engine.get_key_up(ForgeEngine.Key.SPACE):
       pass  # Just released
   ```

3. **Check mouse position:**
   ```python
   screen_pos = engine.screen_mouse_position
   world_pos = engine.world_mouse_position
   print(f"Screen: {screen_pos}, World: {world_pos}")
   ```

## Performance Issues

### Game Running Slowly (Low FPS)

**Problem:** Frame rate is low.

**Solutions:**

1. **Too many objects:**
   - Reduce the number of active objects
   - Use pooling to reuse objects instead of creating new ones

2. **Complex colliders:**
   - Use rectangle colliders when possible (faster than polygons)
   - Disable collider visualization in production (engine.debug = False)

3. **Large images:**
   - Use appropriately sized textures
   - Pre-scale images instead of scaling at runtime

4. **Check FPS:**
   ```python
   fps = 1.0 / engine.time.deltaTime
   print(f"FPS: {fps}")
   ```

### Memory Usage Growing

**Problem:** Memory usage increases over time.

**Solutions:**

1. **Clean up destroyed objects:**
   ```python
   scene.destroy_object(obj)  # Queue for deletion
   ```

2. **Unload unused assets:**
   - Don't keep references to unused images/audio

3. **Profile your code:**
   - Use Python profiling tools to find leaks

## Build Issues

### "PyInstaller not installed"

**Problem:** Can't build executable.

**Solution:**
```bash
pip install pyinstaller
```

### Executable Can't Find Assets

**Problem:** Game runs fine in development but assets are missing in packaged build.

**Solution:**
```python
# Use engine.get_path() for correct asset resolution
path = engine.get_path(r"assets\image.png")
image = engine.import_image(path)
```

Or when building:
```python
build = ForgeEngine.Build(
    main_script='game.py',
    output_name='MyGame',
    extra_data=['assets/']  # Include assets directory
)
```

## Getting More Help

1. **Check error messages:** Read the full error output carefully
2. **Enable debug mode:** `engine.debug = True`
3. **Add print statements:** Debug by printing values
4. **Simplify:** Create a minimal example that reproduces the issue

## Reporting Issues

When reporting a bug, include:

1. Your OS and Python version:
   ```bash
   python --version
   uname -a  # macOS/Linux
   systeminfo  # Windows
   ```

2. Your ForgeEngine version

3. Minimal code that reproduces the issue

4. Complete error message and traceback

5. What you expected to happen vs. what actually happened
