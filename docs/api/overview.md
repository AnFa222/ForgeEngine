# API Reference Overview

This is the complete API reference for ForgeEngine. Use this when you need detailed information about classes, methods, and functions.

## Quick Links

- [Engine API](engine.md) - Core engine class and main API
- [Objects & Components](objects-and-components.md) - Object, transform, and all component classes
- [Input System](input.md) - Keyboard and mouse input
- [Physics & Collision](physics.md) - Kinematic and collision system
- [Rendering](rendering.md) - Renderer, camera, and rendering system
- [Scene Management](scenes.md) - Scene class and scene management
- [Utilities](utilities.md) - Math, file I/O, and helper functions
- [Audio](audio.md) - Audio component and playback

## Common Patterns

### Creating a Game Object

```python
import ForgeEngine

# Create engine
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 800
engine.window.height = 600
engine.window.title = "My Game"
engine.window.initialize()

# Create object
player = ForgeEngine.Object(engine)

# Add components
player.transform = ForgeEngine.Transform(x=100, y=200)
player.renderer = ForgeEngine.Renderer(image_id=my_image, layer=1)
player.kinematic = ForgeEngine.Kinematic()
player.script = MyPlayerScript()

# Add to scene
scene = ForgeEngine.Scene("main")
scene.add_object(player)
engine.add_scene(scene)
engine.load_scene("main")

# Run game
engine.main_loop()
```

### Writing a Script

```python
from ForgeEngine import Key

class PlayerScript:
    def start(self, thisObject, engine):
        """Called once when game starts"""
        print("Player initialized")
    
    def early_update(self, thisObject, engine):
        """Called before physics each frame"""
        if engine.get_key(Key.W):
            thisObject.kinematic.velocity_y = -500
    
    def update(self, thisObject, engine):
        """Called after physics each frame"""
        print(f"Player position: {thisObject.transform.x}, {thisObject.transform.y}")
```

### Detecting Collisions

```python
# Option 1: Use on_ground property (for gravity-based games)
if player.kinematic.on_ground:
    print("Player is on ground")

# Option 2: Check collision manually
others = [o for o in engine.objects if o != thisObject]
collisions = engine.check_collision(thisObject, others)
if collisions:
    print(f"Collided with: {collisions}")
```

### Loading Assets

```python
# Load image
player_image = engine.import_image(r"assets\player.png")
background = engine.import_image(r"assets\background.jpg")

# Load audio
jump_sound = engine.import_audio(r"assets\jump.wav")
background_music = engine.import_audio(r"assets\music.mp3")

# Use in components
renderer = ForgeEngine.Renderer(image_id=player_image, layer=1)
audio = ForgeEngine.Audio(audio_id=jump_sound)
```

## API Index

### Classes

#### Core Engine
- [Engine](engine.md#engine) - Main game engine class
- [Scene](scenes.md#scene) - Container for game objects
- [Object](objects-and-components.md#object) - Game entity

#### Components
- [Transform](objects-and-components.md#transform) - Position, rotation, scale
- [Renderer](rendering.md#renderer) - Sprite rendering
- [TextRenderer](rendering.md#textrenderer) - Text rendering
- [Animation](objects-and-components.md#animation) - Sprite animation
- [Collider](physics.md#collider) - Collision shape
- [Kinematic](physics.md#kinematic) - Physics simulation
- [Camera](rendering.md#camera) - Viewport control
- [Audio](audio.md#audio) - Audio playback

#### Collision Shapes
- [Rectangle](physics.md#rectangle) - Rectangular collision shape
- [Polygon](physics.md#polygon) - Polygonal collision shape

#### Utilities
- [fMath](utilities.md#fmath) - Math utilities and Vector2
- [Key](input.md#key) - Keyboard and mouse constants
- [Event](input.md#event) - Engine events

#### Build
- [Build](utilities.md#build) - Build system for executables

### Enums

- [Key](input.md#key) - Keyboard and mouse button constants
- [Event](input.md#event) - Engine event constants
- Pipelines: `pygamePipeline`, `modernGlPipeline`

### Functions

#### Engine Methods
- `engine.add_scene(scene)` - Register a scene
- `engine.load_scene(scene_id)` - Load a scene
- `engine.import_image(path)` - Load an image
- `engine.import_audio(path)` - Load audio
- `engine.main_loop()` - Start the game loop
- `engine.get_key(key)` - Check if key is held
- `engine.get_key_down(key)` - Check if key was pressed this frame
- `engine.get_key_up(key)` - Check if key was released this frame
- `engine.get_mouse_button(button)` - Check mouse button state
- `engine.set_mouse_position(position)` - Move mouse cursor
- `engine.show_mouse()` - Show mouse cursor
- `engine.hide_mouse()` - Hide mouse cursor

#### File I/O
- `ForgeEngine.save_json(obj, path)` - Save JSON file
- `ForgeEngine.load_json(path, default)` - Load JSON file
- `ForgeEngine.save_text(path, data)` - Save text file
- `ForgeEngine.load_text(path, default)` - Load text file
- `ForgeEngine.save_binary(path, data)` - Save binary file
- `ForgeEngine.load_binary(path, default)` - Load binary file

#### Math Functions
- `fMath.lerp(a, b, t)` - Linear interpolation
- `fMath.distance(p1, p2)` - Distance between points
- `fMath.clamp(value, min, max)` - Clamp value
- `fMath.remap(value, in_min, in_max, out_min, out_max)` - Remap range
- `fMath.wrap(value, min, max)` - Wrap value

## Properties vs Methods

In ForgeEngine, components use properties for state and methods for actions:

### Properties (Read/Write)
```python
player.transform.x = 100          # Set position
player.transform.rotation = 45    # Set rotation
player.renderer.alpha = 128       # Set opacity
player.kinematic.gravity = 2000   # Set gravity

# Read
current_x = player.transform.x
is_on_ground = player.kinematic.on_ground
```

### Methods (Call to Perform Action)
```python
player.animation.play()           # Start animation
player.animation.pause()          # Pause animation
player.animation.stop()           # Stop animation
player.audio.play_sound()         # Play sound
player.audio.stop_sound()         # Stop sound
```

## Coordinate System

ForgeEngine uses a **screen coordinate system**:

```
(0, 0) ----------> X increases
  |
  |
  v
Y increases
(right, down)
```

- **X axis:** Increases to the right
- **Y axis:** Increases downward
- **Rotation:** 0° points right, increases counter-clockwise (standard math convention in some places, check implementation for specifics)
- **Units:** Pixels

## Color Format

Colors are specified as RGB tuples:

```python
# Black
(0, 0, 0)

# White
(255, 255, 255)

# Red
(255, 0, 0)

# Green
(0, 255, 0)

# Blue
(0, 0, 255)

# Semi-transparent via alpha parameter (separate from RGB tuple)
renderer = ForgeEngine.Renderer(image_id=img, layer=1, alpha=128)
```

## Delta Time

Delta time (time between frames) is available via:

```python
dt = engine.time.deltaTime  # Time since last frame in seconds
fps = 1.0 / dt              # Frames per second

# Use in calculations
player.transform.x += player.kinematic.velocity_x * dt
```

## Tags

Objects can be tagged for organization:

```python
# Add tag
player.add_tag("player")
obj.add_tag("enemy")

# Check tag
if obj.has_tag("enemy"):
    print("This is an enemy!")

# Remove tag
player.remove_tag("player")
```

## Event System

ForgeEngine handles events like window close:

```python
# Check for quit event
if ForgeEngine.Event.QUIT in engine.window.get_events():
    engine.running = False
```

## Error Handling

ForgeEngine logs errors to console and `error.log` file:

```python
from ForgeEngine import error

error("Something went wrong!")  # Logs error message
```

## Performance Notes

- Component caching improves performance for large scenes
- Layer sorting is efficient for reasonable layer counts
- SAT collision detection is fast for typical object counts
- Consider spatial partitioning for 1000+ objects with colliders

## Thread Safety

**ForgeEngine is NOT thread-safe.** All code must run on the main thread. Do not create threads that access engine objects or components.

## Version

To check ForgeEngine version:

```python
import ForgeEngine
print(ForgeEngine.__version__)  # If available
```

## Minimal Working Example

```python
import ForgeEngine

# Create and setup engine
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 800
engine.window.height = 600
engine.window.initialize()

# Create scene with camera
scene = ForgeEngine.Scene("main")
camera = ForgeEngine.Object(engine)
camera.transform = ForgeEngine.Transform()
camera.camera = ForgeEngine.Camera(1)
camera.camera.render_zone_width = 800
camera.camera.render_zone_height = 600
scene.add_object(camera)

# Create player
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)
# Note: Renderer needs an image_id - in real code, load an image first
scene.add_object(player)

# Run
engine.add_scene(scene)
engine.load_scene("main")
engine.main_loop()
```

See individual API pages for complete documentation of each class and method.
