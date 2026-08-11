# Configuration & Setup

## Engine Configuration

### Creating the Engine

The first step in any ForgeEngine game is creating an Engine instance:

```python
import ForgeEngine

# Create engine with Pygame pipeline (recommended)
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)

# Or create engine with ModernGL pipeline
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.modernGlPipeline)
```

### Window Configuration

Before initializing the window, configure its properties:

```python
# Set window dimensions
engine.window.width = 1920
engine.window.height = 1080

# Set window title
engine.window.title = "My Awesome Game"

# Initialize the window
engine.window.initialize()
```

### Background Color

Set the scene background color:

```python
scene = ForgeEngine.Scene("main")
scene.background_color = (50, 150, 255)  # RGB tuple: light blue
```

### Debug Mode

Enable debug visualization:

```python
# Show collision shapes and other debug info
engine.debug = True
```

When debug mode is enabled:
- Collider shapes are drawn with colored outlines
- Rectangle colliders show as red polygons
- Polygon colliders show as cyan polygons

## Loading Assets

### Loading Images

```python
# Load a single image
player_image = engine.import_image(r"assets\player.png")

# Load multiple images
background = engine.import_image(r"assets\background.jpg")
enemy = engine.import_image(r"assets\enemy.png")
```

The returned ID is used when creating Renderer components:

```python
renderer = ForgeEngine.Renderer(image_id=player_image, layer=1)
```

### Loading Audio

```python
# Load audio files
jump_sound = engine.import_audio(r"assets\jump.wav")
background_music = engine.import_audio(r"assets\music.mp3")
```

### Asset Paths

On Windows:
```python
image = engine.import_image(r"assets\character.png")
```

On macOS/Linux:
```python
image = engine.import_image("assets/character.png")
```

Or use platform-independent approach:
```python
from pathlib import Path
asset_dir = Path("assets")
image_path = str(asset_dir / "character.png")
image = engine.import_image(image_path)
```

## Rendering Pipeline Selection

### Pygame Pipeline

**Recommended for:** Most games, beginners, maximum compatibility

```python
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
```

**Pros:**
- Easy to use
- Cross-platform
- Good performance
- Well-supported

**Cons:**
- Less efficient for very large scenes
- Limited advanced graphics

### ModernGL Pipeline

**Recommended for:** Advanced users, graphics-heavy games

```python
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.modernGlPipeline)
```

**Pros:**
- Higher performance
- Modern graphics API
- More control

**Cons:**
- Requires OpenGL drivers
- More complex
- Basic support (fewer features than Pygame)

## Scene Setup

### Creating a Scene

```python
scene = ForgeEngine.Scene("scene_id")
scene.background_color = (0, 0, 0)  # Black background
```

### Adding Objects to Scene

```python
# Create an object
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)
player.renderer = ForgeEngine.Renderer(image_id=my_image, layer=1)

# Add to scene
scene.add_object(player)
```

### Loading Scenes

```python
# Register scene with engine
engine.add_scene(scene)

# Load the scene
engine.load_scene("scene_id")
```

## Input Configuration

### Keyboard Input

By default, ForgeEngine maps standard keyboard keys through the `Key` enum:

```python
# Check if key is currently pressed
if engine.get_key(ForgeEngine.Key.SPACE):
    print("Space is pressed")

# Check if key was pressed this frame
if engine.get_key_down(ForgeEngine.Key.W):
    print("W was just pressed")

# Check if key was released this frame
if engine.get_key_up(ForgeEngine.Key.ESC):
    print("Escape was just released")
```

### Mouse Input

```python
# Check if mouse button is pressed
if engine.get_mouse_button(ForgeEngine.Key.MOUSE_LEFT):
    print("Left mouse button is pressed")

# Check if mouse button was pressed this frame
if engine.get_mouse_button_down(ForgeEngine.Key.MOUSE_RIGHT):
    print("Right mouse button was just pressed")

# Get mouse position
mouse_x, mouse_y = engine.screen_mouse_position
world_x, world_y = engine.world_mouse_position
```

## Camera Configuration

### Basic Camera Setup

```python
# Create a camera object
camera = ForgeEngine.Object(engine)
camera.transform = ForgeEngine.Transform(x=0, y=0)

# Add camera component
camera.camera = ForgeEngine.Camera(camera_id=1)
camera.camera.render_zone_width = 1920
camera.camera.render_zone_height = 1080

scene.add_object(camera)
```

### Multiple Cameras

```python
# Create two cameras
camera1 = ForgeEngine.Object(engine)
camera1.camera = ForgeEngine.Camera(camera_id=1)
camera1.camera.render_zone_width = 800
camera1.camera.render_zone_height = 600

camera2 = ForgeEngine.Object(engine)
camera2.camera = ForgeEngine.Camera(camera_id=2)
camera2.camera.render_zone_width = 800
camera2.camera.render_zone_height = 600

# Switch cameras
engine.use_camera(1)  # Use camera 1
engine.use_camera(2)  # Switch to camera 2
```

## Basic Game Template

Here's a complete template to get started:

```python
import ForgeEngine

# Initialize
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 800
engine.window.height = 600
engine.window.title = "My Game"
engine.window.initialize()

# Load assets
player_image = engine.import_image(r"assets\player.png")

# Create scene
scene = ForgeEngine.Scene("main")
scene.background_color = (200, 200, 200)

# Create camera
camera = ForgeEngine.Object(engine)
camera.transform = ForgeEngine.Transform(x=0, y=0)
camera.camera = ForgeEngine.Camera(1)
camera.camera.render_zone_width = 800
camera.camera.render_zone_height = 600
scene.add_object(camera)

# Create player
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)
player.renderer = ForgeEngine.Renderer(image_id=player_image, layer=1)
player.kinematic = ForgeEngine.Kinematic()
scene.add_object(player)

# Setup engine
engine.add_scene(scene)
engine.load_scene("main")

# Run
engine.main_loop()
```

## Environment Variables

### Asset Path Resolution

ForgeEngine automatically handles asset path resolution. When running a packaged executable, paths are adjusted automatically. No environment variables are required for normal use.

### For Advanced Users

```python
# Get the correct path (works in both development and packaged builds)
actual_path = engine.get_path(r"assets\image.png")
```

## Next Steps

- Create your first scene (see [First Project](first-project.md))
- Learn about components (see [Architecture](../architecture/systems.md))
- Check out [Tutorials](../tutorials/)
