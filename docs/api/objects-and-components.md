# Objects & Components API

## Object Class

Objects are the basic entities in ForgeEngine. They hold components that define their appearance and behavior.

### Constructor

```python
obj = ForgeEngine.Object(engine)
```

**Parameters:**
- `engine` - The Engine instance

**Example:**
```python
player = ForgeEngine.Object(engine)
enemy = ForgeEngine.Object(engine)
```

### Properties

```python
obj.engine              # Reference to engine
obj.active              # bool - Is this object active?
obj.tags               # list - Tags attached to this object

# Components
obj.transform          # Transform component (position, rotation, scale)
obj.renderer           # Renderer component (sprite drawing)
obj.textRenderer       # TextRenderer component (text drawing)
obj.animation          # Animation component (sprite animation)
obj.script             # Script component (custom behavior)
obj.collider           # Collider component (collision shape)
obj.camera             # Camera component (viewport)
obj.audio              # Audio component (sound)
obj.kinematic          # Kinematic component (physics)
```

### Methods

#### Lifecycle

```python
obj.start()            # Called at scene start (via script)
obj.update()           # Called each frame (calls script.update())
obj.early_update()     # Called before physics (calls script.early_update())
```

#### Tags

```python
obj.add_tag(tag)       # Add a tag
obj.remove_tag(tag)    # Remove a tag
obj.has_tag(tag)       # Check if object has tag
```

**Example:**
```python
player.add_tag("player")
enemy.add_tag("enemy")

if obj.has_tag("enemy"):
    print("This is an enemy")

player.remove_tag("player")
```

### Object Lifecycle

1. **Creation** - `obj = ForgeEngine.Object(engine)`
2. **Component Setup** - Attach components to object
3. **Scene Addition** - `scene.add_object(obj)`
4. **Initialization** - `obj.start()` called when scene loads
5. **Update Loop** - Each frame: `early_update()` → physics → `update()`
6. **Rendering** - Rendered each frame if visible
7. **Destruction** - `scene.destroy_object(obj)` queues for deletion

---

## Transform Component

The Transform component defines an object's position, rotation, and scale in the world.

### Constructor

```python
transform = ForgeEngine.Transform(x=0, y=0, rotation=0, scale_x=1, scale_y=1)
```

**Parameters:**
- `x` (float) - X position in pixels (default: 0)
- `y` (float) - Y position in pixels (default: 0)
- `rotation` (float) - Rotation in degrees (default: 0)
- `scale_x` (float) - X scale factor (default: 1)
- `scale_y` (float) - Y scale factor (default: 1)

### Properties

```python
transform.x            # float - X position
transform.y            # float - Y position
transform.rotation     # float - Rotation in degrees
transform.scale_x      # float - X scale (1 = normal, 2 = 2x larger)
transform.scale_y      # float - Y scale
```

### Example

```python
# Create player at position (400, 300), slightly rotated
player.transform = ForgeEngine.Transform(
    x=400,
    y=300,
    rotation=45,
    scale_x=1,
    scale_y=1
)

# Move player
player.transform.x += 10
player.transform.y += 5

# Rotate
player.transform.rotation += 90

# Scale
player.transform.scale_x = 2  # Double width
```

---

## Renderer Component

The Renderer component displays a sprite on screen.

### Constructor

```python
renderer = ForgeEngine.Renderer(image_id, layer, alpha=255)
```

**Parameters:**
- `image_id` - ID returned from `engine.import_image()`
- `layer` (int) - Rendering layer (higher = rendered on top)
- `alpha` (int) - Opacity 0-255 (default: 255, fully opaque)

### Properties

```python
renderer.image_id           # Image to render
renderer.layer              # int - Render layer (higher on top)
renderer.alpha              # int - Opacity (0-255)
renderer.visible            # bool - Should render?
renderer.always_render      # bool - Render even if off-screen?
renderer.is_overlay         # bool - Render on top of everything?
```

### Methods

```python
renderer.update_properties()  # Mark renderer as dirty (needs re-rendering)
```

### Example

```python
# Create renderer
image_id = engine.import_image(r"assets\player.png")
renderer = ForgeEngine.Renderer(image_id=image_id, layer=10, alpha=255)
obj.renderer = renderer

# Change opacity (fade effect)
renderer.alpha = 128  # 50% transparent

# Always render (useful for UI)
renderer.always_render = True

# Overlay rendering (UI on top)
renderer.is_overlay = True
```

### Layer System

Objects are rendered in layer order:

```python
# Background (rendered first)
bg_renderer = ForgeEngine.Renderer(image_id=bg_img, layer=0)

# Characters
player_renderer = ForgeEngine.Renderer(image_id=player_img, layer=10)
enemy_renderer = ForgeEngine.Renderer(image_id=enemy_img, layer=10)

# Foreground
fg_renderer = ForgeEngine.Renderer(image_id=fg_img, layer=20)

# UI (on top)
ui_renderer = ForgeEngine.Renderer(image_id=ui_img, layer=100)
```

---

## TextRenderer Component

The TextRenderer component displays text on screen.

### Constructor

```python
text_renderer = ForgeEngine.TextRenderer(
    text,
    font_path,
    font_size,
    color,
    layer,
    alpha=255
)
```

**Parameters:**
- `text` (str) - Text to display
- `font_path` (str) - Path to .ttf font file
- `font_size` (int) - Font size in pixels
- `color` (tuple) - Color as (R, G, B)
- `layer` (int) - Rendering layer
- `alpha` (int) - Opacity 0-255 (default: 255)

### Properties

```python
text_renderer.text              # str - Text to display
text_renderer.font_path         # str - Path to font file
text_renderer.font_size         # int - Font size
text_renderer.color             # tuple - (R, G, B) color
text_renderer.layer             # int - Render layer
text_renderer.alpha             # int - Opacity
text_renderer.is_overlay        # bool - Overlay rendering?
text_renderer.always_render     # bool - Render even if off-screen?
```

### Example

```python
# Create text renderer
text_renderer = ForgeEngine.TextRenderer(
    text="Score: 0",
    font_path=r"assets\fonts\Arial.ttf",
    font_size=32,
    color=(255, 255, 255),  # White
    layer=100,
    alpha=255
)
obj.textRenderer = text_renderer

# Update text
text_renderer.text = "Score: 100"

# Make it an overlay (always on top)
text_renderer.is_overlay = True
```

---

## Animation Component

The Animation component handles frame-based sprite animation.

### Constructor

```python
animation = ForgeEngine.Animation(
    frame_ids,
    frame_duration=0.1,
    loop=True,
    playing=True
)
```

**Parameters:**
- `frame_ids` (list) - List of image IDs (from `engine.import_image()`)
- `frame_duration` (float) - Duration per frame in seconds (default: 0.1)
- `loop` (bool) - Loop when finished? (default: True)
- `playing` (bool) - Start playing? (default: True)

### Properties

```python
animation.frame_ids           # list - Animation frame images
animation.frame_duration      # float - Seconds per frame
animation.loop                # bool - Should loop?
animation.playing             # bool - Is currently playing?
animation.current_frame       # int - Current frame index
animation.elapsed_time        # float - Time in current frame
```

### Methods

```python
animation.play()              # Start/resume animation
animation.pause()             # Pause animation
animation.stop()              # Stop and reset to frame 0
animation.reset()             # Reset to frame 0
animation.get_current_frame() # Get current frame image ID
```

### Example

```python
# Create animation
frame1 = engine.import_image(r"assets\walk1.png")
frame2 = engine.import_image(r"assets\walk2.png")
frame3 = engine.import_image(r"assets\walk3.png")

animation = ForgeEngine.Animation(
    frame_ids=[frame1, frame2, frame3],
    frame_duration=0.1,  # 100ms per frame
    loop=True
)
player.animation = animation

# Control animation
animation.play()    # Start walking
animation.pause()   # Stop walking animation
animation.stop()    # Stop and reset

# One-shot animation
idle_anim = ForgeEngine.Animation(
    frame_ids=[stand_frame],
    loop=False
)
```

---

## Component Requirements

Some components require others to function:

| Component | Requires | Reason |
|-----------|----------|--------|
| Renderer | Transform | Needs position to render |
| Collider | Transform | Needs position for collision |
| Camera | Transform | Needs position for viewport |
| TextRenderer | Transform | Needs position to render |
| Kinematic | Transform | Needs position for physics |

ForgeEngine logs warnings if these requirements aren't met.

---

## Object Creation Best Practices

### Complete Example

```python
import ForgeEngine

class PlayerScript:
    def update(self, thisObject, engine):
        if engine.get_key(ForgeEngine.Key.W):
            thisObject.transform.y -= 500 * engine.deltaTime

# Create engine
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 800
engine.window.height = 600
engine.window.initialize()

# Load assets
player_img = engine.import_image(r"assets\player.png")
walk_frame1 = engine.import_image(r"assets\walk1.png")
walk_frame2 = engine.import_image(r"assets\walk2.png")
jump_sound = engine.import_audio(r"assets\jump.wav")

# Create player object
player = ForgeEngine.Object(engine)

# Transform (required for rendering/collision)
player.transform = ForgeEngine.Transform(
    x=400,
    y=300,
    rotation=0,
    scale_x=1,
    scale_y=1
)

# Rendering
player.renderer = ForgeEngine.Renderer(
    image_id=player_img,
    layer=10,
    alpha=255
)

# Animation
player.animation = ForgeEngine.Animation(
    frame_ids=[walk_frame1, walk_frame2],
    frame_duration=0.1,
    loop=True
)

# Physics
player.kinematic = ForgeEngine.Kinematic()
player.kinematic.gravity = 2000

# Collision
player.collider = ForgeEngine.Collider(
    shape=ForgeEngine.Rectangle(width=64, height=64),
    x_offset=0,
    y_offset=0
)

# Audio
player.audio = ForgeEngine.Audio(audio_id=jump_sound)

# Behavior
player.script = PlayerScript()

# Tags
player.add_tag("player")

# Add to scene
scene = ForgeEngine.Scene("main")
scene.add_object(player)

# Run
engine.add_scene(scene)
engine.load_scene("main")
engine.main_loop()
```

---

## Common Patterns

### Creating Multiple Objects

```python
# Create 10 enemies
enemies = []
for i in range(10):
    enemy = ForgeEngine.Object(engine)
    enemy.transform = ForgeEngine.Transform(x=i*100, y=500)
    enemy.renderer = ForgeEngine.Renderer(image_id=enemy_img, layer=5)
    enemy.collider = ForgeEngine.Collider(
        shape=ForgeEngine.Rectangle(width=50, height=50),
        x_offset=0,
        y_offset=0
    )
    enemy.add_tag("enemy")
    scene.add_object(enemy)
    enemies.append(enemy)
```

### Finding Tagged Objects

```python
# Find all enemies in scene
enemies = [obj for obj in engine.objects if obj.has_tag("enemy")]

# Find first player
player = next((obj for obj in engine.objects if obj.has_tag("player")), None)
```

### Cloning Objects

```python
# Create a new object with same properties as existing one
def clone_object(obj):
    copy = ForgeEngine.Object(obj.engine)
    
    if obj.transform:
        copy.transform = ForgeEngine.Transform(
            x=obj.transform.x,
            y=obj.transform.y,
            rotation=obj.transform.rotation,
            scale_x=obj.transform.scale_x,
            scale_y=obj.transform.scale_y
        )
    
    if obj.renderer:
        copy.renderer = ForgeEngine.Renderer(
            image_id=obj.renderer.image_id,
            layer=obj.renderer.layer,
            alpha=obj.renderer.alpha
        )
    
    # Copy other components as needed...
    
    return copy
```

See also:
- [Input API](input.md) for keyboard/mouse constants
- [Physics API](physics.md) for physics/collision
- [Rendering API](rendering.md) for advanced rendering
- [Scenes API](scenes.md) for scene management
