# Engine API

The Engine class is the main interface for ForgeEngine. It manages scenes, objects, rendering, input, and all game systems.

## Engine Class

### Constructor

```python
engine = ForgeEngine.Engine(render_pipeline)
```

**Parameters:**
- `render_pipeline` - Rendering backend
  - `ForgeEngine.pygamePipeline` - Pygame rendering (recommended)
  - `ForgeEngine.modernGlPipeline` - ModernGL rendering (advanced)

**Example:**
```python
import ForgeEngine

engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
```

### Window Configuration

Before calling `engine.window.initialize()`, set window properties:

#### Properties

```python
engine.window.width = 1280        # Window width in pixels
engine.window.height = 720        # Window height in pixels
engine.window.title = "My Game"   # Window title
```

#### Methods

```python
engine.window.initialize()         # Initialize window (required before main_loop)
engine.set_mouse_position(pos)    # Set mouse cursor position
engine.show_mouse()               # Show mouse cursor
engine.hide_mouse()               # Hide mouse cursor
```

**Example:**
```python
engine.window.width = 800
engine.window.height = 600
engine.window.title = "My Game"
engine.window.initialize()
```

## Scene Management

### Adding Scenes

```python
scene = ForgeEngine.Scene("main_level")
engine.add_scene(scene)
```

### Loading Scenes

```python
engine.load_scene("main_level")
```

When you load a scene:
- It becomes the `current_scene`
- Its objects become `engine.objects`
- Its background color becomes `engine.background_color`

### Scene Properties

```python
engine.current_scene          # Currently loaded scene
engine.scenes                 # Dict of all registered scenes
engine.objects                # Objects in current scene
engine.background_color       # Scene background color
```

## Asset Loading

### Loading Images

```python
image_id = engine.import_image(path)
```

**Parameters:**
- `path` - File path to image (PNG, JPG, etc.)

**Returns:** Unique ID for the image (used in Renderer component)

**Example:**
```python
player_image = engine.import_image(r"assets\player.png")
background = engine.import_image("assets/background.jpg")

# Use in renderer
renderer = ForgeEngine.Renderer(image_id=player_image, layer=1)
```

### Loading Audio

```python
audio_id = engine.import_audio(path)
```

**Parameters:**
- `path` - File path to audio (WAV, MP3, etc.)

**Returns:** Unique ID for the audio (used in Audio component)

**Example:**
```python
jump_sound = engine.import_audio(r"assets\jump.wav")
background_music = engine.import_audio(r"assets\music.mp3")

# Use in audio component
audio = ForgeEngine.Audio(audio_id=jump_sound)
```

## Game Loop

### Main Loop

```python
engine.main_loop()
```

Starts the game loop. This method blocks until the game exits.

The game loop:
1. Processes window events
2. Updates all game systems each frame
3. Renders each frame
4. Continues until `engine.running` is False or window is closed

**Example:**
```python
# Setup scene
engine.add_scene(scene)
engine.load_scene("main")

# Start game
engine.main_loop()
```

### Stopping the Game Loop

```python
engine.running = False
```

Sets `running` to False to exit the main loop on the next frame.

## Input System

### Keyboard Input

#### Check if Key is Held

```python
if engine.get_key(ForgeEngine.Key.W):
    # Key is currently pressed
    player.move_forward()
```

#### Check if Key Was Pressed This Frame

```python
if engine.get_key_down(ForgeEngine.Key.SPACE):
    # Key was just pressed this frame
    player.jump()
```

#### Check if Key Was Released This Frame

```python
if engine.get_key_up(ForgeEngine.Key.ESC):
    # Key was just released this frame
    show_pause_menu()
```

### Mouse Input

#### Check Mouse Button State

```python
if engine.get_mouse_button(ForgeEngine.Key.MOUSE_LEFT):
    # Left mouse button is pressed
    fire_weapon()

if engine.get_mouse_button_down(ForgeEngine.Key.MOUSE_RIGHT):
    # Right mouse button was just pressed
    use_ability()

if engine.get_mouse_button_up(ForgeEngine.Key.MOUSE_MIDDLE):
    # Middle mouse button was just released
    deselect()
```

#### Mouse Position

```python
# Screen position (relative to window)
screen_x, screen_y = engine.screen_mouse_position

# World position (relative to camera/world)
world_x, world_y = engine.world_mouse_position
```

### Input Properties

```python
engine.pressed_keys              # Set of currently held keys
engine.frame_pressed_keys        # Set of keys pressed this frame
engine.frame_released_keys       # Set of keys released this frame
engine.pressed_mouse_buttons     # Set of held mouse buttons
engine.frame_pressed_mouse_buttons  # Set of mouse buttons pressed this frame
engine.frame_released_mouse_buttons # Set of mouse buttons released this frame
```

## Physics & Collision

### Collision Detection

```python
collisions = engine.check_collision(obj, other_objects)
```

**Parameters:**
- `obj` - Object to check collision for
- `other_objects` - List of objects to check against

**Returns:** List of objects that collided with `obj`, or empty list if no collisions

**Example:**
```python
# Get all objects except the one we're checking
others = [o for o in engine.objects if o != player]

# Check collision
collisions = engine.check_collision(player, others)

if collisions:
    print(f"Player collided with: {collisions}")
    # Handle collision
    for obj in collisions:
        if obj.has_tag("enemy"):
            player.take_damage(10)
```

### Physics Properties

```python
engine.deltaTime              # Time since last frame in seconds (float)
```

Use deltaTime for time-dependent calculations:

```python
class PlayerScript:
    def update(self, thisObject, engine):
        # Move at 500 pixels per second
        thisObject.transform.x += 500 * engine.deltaTime
```

## Camera System

### Switching Cameras

```python
engine.use_camera(camera_id)
```

**Parameters:**
- `camera_id` - ID of camera to activate

**Example:**
```python
# Create two cameras
camera1 = ForgeEngine.Object(engine)
camera1.transform = ForgeEngine.Transform()
camera1.camera = ForgeEngine.Camera(camera_id=1)

camera2 = ForgeEngine.Object(engine)
camera2.transform = ForgeEngine.Transform()
camera2.camera = ForgeEngine.Camera(camera_id=2)

# Later, switch cameras
engine.use_camera(1)  # Use camera 1
engine.use_camera(2)  # Switch to camera 2
```

### Camera Properties

```python
engine.camera                 # Currently active camera (Object with Camera component)
engine.cameras                # Dict of all cameras (camera_id -> Object)
```

## Object Management

### Creating Objects

```python
obj = ForgeEngine.Object(engine)
```

See [Objects & Components API](objects-and-components.md) for details.

### Active/Inactive Objects

```python
obj.active = True   # Object is updated and rendered
obj.active = False  # Object is not updated or rendered
```

Inactive objects are not processed by any systems.

## Debugging

### Debug Mode

```python
engine.debug = True
```

When enabled, collision shapes are drawn with colored outlines:
- Rectangle colliders: Red outline
- Polygon colliders: Cyan outline

Useful for debugging collision issues.

## Time Management

### Delta Time

```python
dt = engine.time.deltaTime
```

Time elapsed since last frame in seconds (float). Use this for frame-rate independent calculations.

### Timers

```python
# Create a timer
engine.time.create_timer("my_timer")

# Get elapsed time
elapsed = engine.time.get_timer("my_timer")

# Reset timer
engine.time.reset_timer("my_timer")
```

## Path Resolution

### Get Correct Asset Path

```python
path = engine.get_path(relative_path)
```

This handles path resolution for both development and packaged builds. Use this when you need the correct path to files.

**Example:**
```python
# Works in both development and packaged builds
image_path = engine.get_path(r"assets\player.png")
image_id = engine.import_image(image_path)
```

## Properties Reference

### Engine State

```python
engine.running              # bool - Is game loop running?
engine.render_pipeline      # int - Current render pipeline
engine.debug                # bool - Debug mode enabled?
engine.deltaTime            # float - Time since last frame
```

### Scene & Object Management

```python
engine.current_scene        # Scene - Currently loaded scene
engine.scenes              # dict - All registered scenes
engine.objects             # list - Objects in current scene
engine.background_color    # tuple - Scene background color (R, G, B)
engine.camera              # Object - Current active camera
engine.cameras             # dict - All cameras (id -> Object)
```

### Input

```python
engine.screen_mouse_position        # tuple - Mouse position in screen coords
engine.world_mouse_position         # tuple - Mouse position in world coords
engine.pressed_keys                 # set - Currently held keys
engine.pressed_mouse_buttons        # set - Currently held mouse buttons
```

## Methods Reference

### Scene Management
- `add_scene(scene)` - Register a scene
- `load_scene(scene_id)` - Load and activate a scene

### Asset Loading
- `import_image(path)` - Load image file
- `import_audio(path)` - Load audio file

### Game Loop
- `main_loop()` - Start the game loop

### Input
- `get_key(key)` - Is key currently held?
- `get_key_down(key)` - Was key pressed this frame?
- `get_key_up(key)` - Was key released this frame?
- `get_mouse_button(button)` - Is mouse button held?
- `get_mouse_button_down(button)` - Was mouse button pressed this frame?
- `get_mouse_button_up(button)` - Was mouse button released this frame?
- `set_mouse_position(position)` - Move mouse cursor
- `show_mouse()` - Show mouse cursor
- `hide_mouse()` - Hide mouse cursor

### Physics & Collision
- `check_collision(obj, other_objects)` - Check if obj collides with others

### Camera
- `use_camera(camera_id)` - Switch to different camera

### Other
- `get_path(relative_path)` - Resolve asset path

## Common Patterns

### Complete Game Initialization

```python
import ForgeEngine

# Create engine
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 1280
engine.window.height = 720
engine.window.title = "My Game"
engine.window.initialize()

# Load assets
player_img = engine.import_image(r"assets\player.png")
jump_sound = engine.import_audio(r"assets\jump.wav")

# Create scene
scene = ForgeEngine.Scene("main")
scene.background_color = (135, 206, 235)

# Create camera
camera = ForgeEngine.Object(engine)
camera.transform = ForgeEngine.Transform(x=0, y=0)
camera.camera = ForgeEngine.Camera(1)
camera.camera.render_zone_width = 1280
camera.camera.render_zone_height = 720
scene.add_object(camera)

# Create player
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=640, y=360)
player.renderer = ForgeEngine.Renderer(image_id=player_img, layer=1)
player.kinematic = ForgeEngine.Kinematic()
player.audio = ForgeEngine.Audio(audio_id=jump_sound)
scene.add_object(player)

# Load and run
engine.add_scene(scene)
engine.load_scene("main")
engine.main_loop()
```

### Detecting Input in Script

```python
from ForgeEngine import Key

class PlayerScript:
    def update(self, thisObject, engine):
        # Movement
        if engine.get_key(Key.W):
            thisObject.transform.y -= 100 * engine.deltaTime
        if engine.get_key(Key.S):
            thisObject.transform.y += 100 * engine.deltaTime
        
        # Jump
        if engine.get_key_down(Key.SPACE):
            thisObject.kinematic.velocity_y = -500
        
        # Shoot on click
        if engine.get_mouse_button_down(Key.MOUSE_LEFT):
            world_x, world_y = engine.world_mouse_position
            self.shoot(thisObject, world_x, world_y)
    
    def shoot(self, player, x, y):
        # Shooting logic here
        pass
```

See [Input API](input.md) for complete key constants.
