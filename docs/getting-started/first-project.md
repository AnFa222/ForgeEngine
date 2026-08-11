# Your First Project

In this guide, we'll create a complete, playable game from scratch using ForgeEngine. By the end, you'll have a game with a player character that you can move around and a camera that follows them.

## Project Setup

### Create Project Directory

```bash
mkdir my-forge-game
cd my-forge-game
```

### Directory Structure

Create the following directory structure:

```
my-forge-game/
├── game.py
├── player_script.py
├── camera_script.py
└── assets/
    ├── images/
    │   ├── player.png
    │   └── ground.png
    └── fonts/
        └── Arial.ttf
```

## Step 1: Prepare Assets

You'll need:
- `player.png` - A sprite for the player (at least 64x64 pixels)
- `ground.png` - A platform/ground tile (at least 128x128 pixels)
- `Arial.ttf` - A TrueType font (can use any .ttf file you have)

If you don't have these, you can create simple placeholder images or download them from free resources.

## Step 2: Create Player Script

Create `player_script.py`:

```python
from ForgeEngine import Key

class PlayerScript:
    def __init__(self):
        self.speed = 500  # pixels per second
        
    def start(self, thisObject, engine):
        """Called once when the game starts"""
        print("Player spawned!")
    
    def early_update(self, thisObject, engine):
        """Called before physics update each frame"""
        # Get input
        horizontal_input = engine.get_key(Key.RIGHT) - engine.get_key(Key.LEFT)
        jump_input = engine.get_key_down(Key.SPACE)
        
        # Apply horizontal movement
        if horizontal_input != 0:
            thisObject.kinematic.velocity_x = horizontal_input * self.speed
        else:
            thisObject.kinematic.velocity_x = 0
        
        # Apply jump
        if jump_input and thisObject.kinematic.on_ground:
            thisObject.kinematic.velocity_y = -800  # Negative because Y increases downward
    
    def update(self, thisObject, engine):
        """Called after physics update each frame"""
        # We can add additional logic here if needed
        pass
```

## Step 3: Create Camera Script

Create `camera_script.py`:

```python
class CameraScript:
    def __init__(self, player_object):
        self.player = player_object
        self.offset_x = 0
        self.offset_y = -100
    
    def update(self, thisObject, engine):
        """Follow the player"""
        if self.player.transform:
            # Center camera on player with offset
            camera_width = thisObject.camera.render_zone_width
            camera_height = thisObject.camera.render_zone_height
            
            thisObject.transform.x = (
                self.player.transform.x + self.offset_x - camera_width // 2
            )
            thisObject.transform.y = (
                self.player.transform.y + self.offset_y - camera_height // 2
            )
```

## Step 4: Create Main Game File

Create `game.py`:

```python
import ForgeEngine
from player_script import PlayerScript
from camera_script import CameraScript

# ==== Initialize Engine ====
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 1280
engine.window.height = 720
engine.window.title = "My First ForgeEngine Game"
engine.window.initialize()

# Optional: Enable debug mode to see collision shapes
engine.debug = False

# ==== Load Assets ====
print("Loading assets...")
player_image = engine.import_image(r"assets\images\player.png")
ground_image = engine.import_image(r"assets\images\ground.png")

# ==== Create Scene ====
scene = ForgeEngine.Scene("main_level")
scene.background_color = (135, 206, 235)  # Sky blue

# ==== Create Camera ====
print("Creating camera...")
camera = ForgeEngine.Object(engine)
camera.transform = ForgeEngine.Transform(x=0, y=0)
camera.camera = ForgeEngine.Camera(1)
camera.camera.render_zone_width = 1280
camera.camera.render_zone_height = 720
scene.add_object(camera)

# ==== Create Player ====
print("Creating player...")
player = ForgeEngine.Object(engine)
player.script = PlayerScript()
player.transform = ForgeEngine.Transform(x=640, y=300, scale_x=1, scale_y=1)
player.renderer = ForgeEngine.Renderer(image_id=player_image, layer=10, alpha=255)

# Add collision (assuming player sprite is 64x64)
player.collider = ForgeEngine.Collider(
    shape=ForgeEngine.Rectangle(width=64, height=64),
    x_offset=0,
    y_offset=0
)

# Add physics
player.kinematic = ForgeEngine.Kinematic()
player.kinematic.gravity = 2000  # Gravity acceleration
player.kinematic.friction = 5    # Air friction

scene.add_object(player)

# ==== Create Ground ====
print("Creating ground platforms...")
# Create ground at y=500
for i in range(-2, 5):
    ground = ForgeEngine.Object(engine)
    ground.transform = ForgeEngine.Transform(
        x=i * 300,
        y=500,
        scale_x=1,
        scale_y=1
    )
    ground.renderer = ForgeEngine.Renderer(
        image_id=ground_image,
        layer=5,
        alpha=255
    )
    ground.collider = ForgeEngine.Collider(
        shape=ForgeEngine.Rectangle(width=300, height=50),
        x_offset=0,
        y_offset=0
    )
    scene.add_object(ground)

# ==== Create Additional Ground ====
for i in range(0, 5):
    ground2 = ForgeEngine.Object(engine)
    ground2.transform = ForgeEngine.Transform(
        x=1500 + i * 300,
        y=600,
        scale_x=1,
        scale_y=1
    )
    ground2.renderer = ForgeEngine.Renderer(
        image_id=ground_image,
        layer=5,
        alpha=255
    )
    ground2.collider = ForgeEngine.Collider(
        shape=ForgeEngine.Rectangle(width=300, height=50),
        x_offset=0,
        y_offset=0
    )
    scene.add_object(ground2)

# ==== Setup Camera Script ====
camera.script = CameraScript(player)

# ==== Load and Run ====
print("Starting game...")
engine.add_scene(scene)
engine.load_scene("main_level")
engine.main_loop()
```

## Step 5: Run Your Game

```bash
python game.py
```

## Game Controls

- **LEFT ARROW** - Move left
- **RIGHT ARROW** - Move right
- **SPACE** - Jump
- **Close window** - Exit game

## Extending Your Game

### Add a UI Element

```python
# Add to game.py, after creating the scene
overlay = ForgeEngine.Object(engine)
overlay.transform = ForgeEngine.Transform(x=50, y=50)
overlay.textRenderer = ForgeEngine.TextRenderer(
    text="Use arrow keys to move, SPACE to jump",
    font_path=r"assets\fonts\Arial.ttf",
    font_size=24,
    color=(255, 255, 255),
    layer=1000,
    alpha=255
)
overlay.textRenderer.is_overlay = True  # Render on top of everything
scene.add_object(overlay)
```

### Add Animation

```python
# Modify player_script.py to use animation
class PlayerScript:
    def __init__(self, idle_image, run_image):
        self.idle_image = idle_image
        self.run_image = run_image
        self.speed = 500
        
    def early_update(self, thisObject, engine):
        horizontal_input = engine.get_key(Key.RIGHT) - engine.get_key(Key.LEFT)
        jump_input = engine.get_key_down(Key.SPACE)
        
        if horizontal_input != 0:
            thisObject.kinematic.velocity_x = horizontal_input * self.speed
            # Change animation
            if hasattr(self, 'animation'):
                thisObject.animation.play()
        else:
            thisObject.kinematic.velocity_x = 0
            # Stop animation
            if hasattr(self, 'animation'):
                thisObject.animation.pause()
        
        if jump_input and thisObject.kinematic.on_ground:
            thisObject.kinematic.velocity_y = -800
```

## Troubleshooting

### "FileNotFoundError: assets/images/player.png"

**Solution:** Make sure your asset files exist in the correct directory. Check the paths in your game.py match your file structure.

### Player falls through the ground

**Solution:** Ensure your collider dimensions match your sprite dimensions. If a sprite is 64x64, use `Rectangle(width=64, height=64)`.

### Camera doesn't follow player

**Solution:** Make sure the camera script is attached to the camera object:
```python
camera.script = CameraScript(player)
```

### Game runs but nothing appears

**Solution:** Check that:
1. The window was initialized: `engine.window.initialize()`
2. Assets are loaded: `engine.import_image(...)`
3. The scene was loaded: `engine.load_scene("main_level")`
4. Objects are added to the scene: `scene.add_object(...)`

## Next Steps

- Learn more about [Components](../architecture/systems.md)
- Explore [Physics](../guides/physics.md)
- Create [Animations](../guides/animation.md)
- Read other [Tutorials](../tutorials/)

Congratulations! You've created your first ForgeEngine game! 🎉
