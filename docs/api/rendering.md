# Rendering API

The rendering system handles all visual output in ForgeEngine, including sprites, text, and cameras.

## Camera Component

The Camera component defines a viewport into the game world. Objects are rendered based on the active camera.

### Constructor

```python
camera = ForgeEngine.Camera(camera_id)
```

**Parameters:**
- `camera_id` (int) - Unique identifier for this camera

### Properties

```python
camera.camera_id                 # int - Camera ID
camera.render_zone_width         # int - Width of viewport
camera.render_zone_height        # int - Height of viewport
camera.render_zone_offset_x      # int - X offset (default: 0)
camera.render_zone_offset_y      # int - Y offset (default: 0)
```

### Example

```python
# Create camera object
camera = ForgeEngine.Object(engine)
camera.transform = ForgeEngine.Transform(x=0, y=0)

# Add camera component
camera.camera = ForgeEngine.Camera(camera_id=1)
camera.camera.render_zone_width = 1280
camera.camera.render_zone_height = 720

# Add to scene
scene.add_object(camera)

# Use this camera for rendering
engine.use_camera(1)
```

### Multiple Cameras

```python
# Create camera 1
cam1 = ForgeEngine.Object(engine)
cam1.transform = ForgeEngine.Transform(x=0, y=0)
cam1.camera = ForgeEngine.Camera(1)
cam1.camera.render_zone_width = 800
cam1.camera.render_zone_height = 600

# Create camera 2
cam2 = ForgeEngine.Object(engine)
cam2.transform = ForgeEngine.Transform(x=500, y=500)
cam2.camera = ForgeEngine.Camera(2)
cam2.camera.render_zone_width = 800
cam2.camera.render_zone_height = 600

scene.add_object(cam1)
scene.add_object(cam2)

# Switch cameras
engine.use_camera(1)
# ... rendering with camera 1
engine.use_camera(2)
# ... rendering with camera 2
```

---

## Renderer Component

The Renderer component displays a sprite on screen.

### Constructor

```python
renderer = ForgeEngine.Renderer(image_id, layer, alpha=255)
```

**Parameters:**
- `image_id` - Image ID from `engine.import_image()`
- `layer` (int) - Rendering layer (higher = rendered on top)
- `alpha` (int) - Opacity 0-255 (default: 255)

### Properties

```python
renderer.image_id              # Image to render
renderer.layer                 # int - Layer (higher = top)
renderer.alpha                 # int - Opacity (0-255)
renderer.visible               # bool - Should render?
renderer.always_render         # bool - Render even if off-screen?
renderer.is_overlay            # bool - Overlay (always on top)?
renderer.dirty                 # bool - Needs re-rendering?
renderer.cache_id              # Unique cache ID
```

### Methods

```python
renderer.update_properties()   # Mark as dirty (needs re-rendering)
```

### Layer System

Objects are rendered in layer order. Higher layers render on top:

```python
# Render order (lowest to highest):
bg = ForgeEngine.Renderer(image_id=bg_img, layer=0)      # Bottom
tiles = ForgeEngine.Renderer(image_id=tiles_img, layer=5)
player = ForgeEngine.Renderer(image_id=player_img, layer=10)
effects = ForgeEngine.Renderer(image_id=effect_img, layer=50)
ui = ForgeEngine.Renderer(image_id=ui_img, layer=100)    # Top
```

### Example

```python
# Load image
player_image = engine.import_image(r"assets\player.png")

# Create renderer
renderer = ForgeEngine.Renderer(
    image_id=player_image,
    layer=10,
    alpha=255
)
player.renderer = renderer

# Fade effect
renderer.alpha = 128  # 50% transparent

# Make invisible
renderer.alpha = 0

# Make fully opaque
renderer.alpha = 255

# Render off-screen (useful for objects outside viewport)
renderer.always_render = True

# Overlay mode (UI, always on top)
renderer.is_overlay = True
```

### Sprite Properties

By default, sprites are:
- Rendered at their transform position
- Scaled by transform scale
- Rotated by transform rotation
- Positioned with center at transform.x, transform.y

---

## TextRenderer Component

Renders text on screen.

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
- `text` (str) - Text string to display
- `font_path` (str) - Path to .ttf font file
- `font_size` (int) - Font size in pixels
- `color` (tuple) - (R, G, B) color
- `layer` (int) - Rendering layer
- `alpha` (int) - Opacity 0-255 (default: 255)

### Properties

```python
text_renderer.text               # str - Text to display
text_renderer.font_path          # str - Font path
text_renderer.font_size          # int - Font size
text_renderer.color              # tuple - (R, G, B) color
text_renderer.layer              # int - Layer
text_renderer.alpha              # int - Opacity
text_renderer.is_overlay         # bool - Overlay rendering?
text_renderer.always_render      # bool - Render if off-screen?
text_renderer.dirty              # bool - Needs re-rendering?
```

### Methods

```python
text_renderer.update_properties()  # Mark as dirty
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

# Change color
text_renderer.color = (255, 0, 0)  # Red

# Change size (requires reloading font)
text_renderer.font_size = 48
text_renderer.update_properties()

# Make overlay (UI on top)
text_renderer.is_overlay = True

# Always render (even off-screen)
text_renderer.always_render = True
```

### Common UI Text

```python
class UIScript:
    def update(self, thisObject, engine):
        fps = 1.0 / engine.deltaTime if engine.deltaTime > 0 else 0
        thisObject.textRenderer.text = f"FPS: {fps:.0f}"
```

---

## Rendering Pipeline

ForgeEngine supports multiple rendering backends through a pipeline system.

### Pygame Pipeline (Default)

```python
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
```

**Pros:**
- Easy to use
- Good 2D performance
- Well-documented
- Cross-platform

**Cons:**
- Limited advanced features

### ModernGL Pipeline

```python
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.modernGlPipeline)
```

**Pros:**
- Modern OpenGL API
- Higher performance potential

**Cons:**
- Requires OpenGL drivers
- Basic support only

---

## Rendering Order

Each frame, rendering happens in this order:

1. **Clear screen** with background color
2. **Collect renderers** - Get all Renderer components
3. **Sort by layer** - Arrange by layer (lower first)
4. **Render sprites** - Draw sprites by layer
5. **Render animation frames** - Use current animation frame if available
6. **Render text** - Draw TextRenderer components
7. **Update screen** - Display to window

### Example Render Order

```python
# These objects:
bg.renderer = Renderer(image_id=bg_img, layer=0)
player.renderer = Renderer(image_id=player_img, layer=10)
player.animation = Animation([...], ...)
ui.textRenderer = TextRenderer(text="Score: 100", layer=100)

# Render in this order:
# 1. bg_img at layer 0
# 2. player current animation frame at layer 10
# 3. "Score: 100" text at layer 100
```

---

## Color Format

Colors are RGB tuples (0-255 per channel):

```python
# Red
(255, 0, 0)

# Green
(0, 255, 0)

# Blue
(0, 0, 255)

# White
(255, 255, 255)

# Black
(0, 0, 0)

# Custom colors
(128, 64, 32)   # Dark orange
(200, 100, 200) # Light purple
```

### Opacity

Use the `alpha` parameter (separate from RGB):

```python
renderer = ForgeEngine.Renderer(image_id=img, layer=1, alpha=255)  # Fully opaque
renderer.alpha = 128  # 50% transparent
renderer.alpha = 64   # 75% transparent
renderer.alpha = 0    # Invisible
```

---

## Screen Coordinates vs World Coordinates

### Screen Coordinates
Relative to the window (0,0) at top-left:
```python
screen_x, screen_y = engine.screen_mouse_position
```

### World Coordinates
Relative to the game world (adjusted for camera):
```python
world_x, world_y = engine.world_mouse_position
```

### Conversion

The engine handles conversion automatically based on the active camera position and render zone.

---

## Performance Tips

### Layer Optimization

Use reasonable number of layers:

```python
# Good - organized layers
BG_LAYER = 0
TILEMAP_LAYER = 5
PLAYER_LAYER = 10
EFFECTS_LAYER = 20
UI_LAYER = 100

# Avoid - too many layers
for i in range(1000):
    obj.renderer.layer = i
```

### Off-Screen Rendering

By default, objects off-screen are not rendered (optimization). If needed:

```python
renderer.always_render = True
```

### Alpha Blending

Alpha blending has performance cost. Use sparingly:

```python
# Efficient - opaque
renderer.alpha = 255

# Less efficient - transparent
renderer.alpha = 128
```

### Overlay Mode

Overlay rendering is efficient for UI:

```python
ui_renderer.is_overlay = True
```

---

## Debugging Rendering

### Check What's Rendering

```python
class DebugScript:
    def update(self, thisObject, engine):
        renderers = [o.renderer for o in engine.objects if o.renderer and o.active]
        print(f"Rendering {len(renderers)} objects")
        
        for obj in engine.has_renderer_components:
            print(f"  {obj} at ({obj.transform.x}, {obj.transform.y}) layer {obj.renderer.layer}")
```

### Visualize Layers

```python
# Enable debug mode to see collision shapes
engine.debug = True

# Print render information
for obj in engine.has_renderer_components:
    print(f"Layer {obj.renderer.layer}: {obj}")
```

---

## Window Methods

Through `engine.window`:

```python
engine.window.width                # Window width
engine.window.height               # Window height
engine.window.title                # Window title
engine.window.initialize()         # Create window
engine.window.set_mouse_pos(pos)  # Set mouse position
engine.window.show_mouse()         # Show cursor
engine.window.hide_mouse()         # Hide cursor
engine.window.poll_events()        # Poll input
engine.window.get_events()         # Get events
engine.window.clear_screen(color)  # Clear with color
engine.window.update_screen()      # Update display
engine.window.load_image(path, id) # Load image
engine.window.load_audio(path, id) # Load audio
```

---

See also:
- [Objects & Components API](objects-and-components.md) - Component details
- [Engine API](engine.md) - Engine rendering methods
- [Guides: Sprites](../guides/sprites.md) - Practical sprite examples
