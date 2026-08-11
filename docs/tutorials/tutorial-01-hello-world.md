# Tutorial 1: Hello World

Create your first ForgeEngine game - a simple colored window with a moving sprite.

## Overview

In this tutorial, you'll:
- Set up a ForgeEngine project
- Create a window
- Add a sprite
- Move it with the keyboard

**Time:** ~15 minutes
**Difficulty:** Beginner

---

## Step 1: Project Setup

Create a folder for your project:

```
my_game/
├── game.py           # Main game file
├── assets/           # Game assets
│   └── player.png    # Player sprite
```

---

## Step 2: Create a Sprite

You'll need an image file. For now, create a simple placeholder:

1. Open any image editor (Paint, GIMP, Photoshop, etc.)
2. Create a 64x64 pixel image
3. Fill it with a color (e.g., red, blue, or green)
4. Save as `assets/player.png`

Or download a free sprite from [OpenGameArt.org](https://opengameart.org/)

---

## Step 3: Create the Game File

Create `game.py`:

```python
import ForgeEngine

# Create engine
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)

# Configure window
engine.window.width = 800
engine.window.height = 600
engine.window.title = "Hello World"
engine.window.initialize()

# Create scene
scene = ForgeEngine.Scene("main")
scene.background_color = (135, 206, 235)  # Sky blue

# Load image
player_image = engine.import_image(r"assets\player.png")

# Create player object
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)
player.renderer = ForgeEngine.Renderer(image_id=player_image, layer=1)

# Add to scene
scene.add_object(player)

# Register scene
engine.add_scene(scene)
engine.load_scene("main")

# Start game loop
engine.main_loop()
```

### Run the Game

```bash
python game.py
```

You should see a window with your sprite in the center.

---

## Step 4: Add Movement

Add a script to move the player:

```python
import ForgeEngine

# Movement script
class PlayerScript:
    def __init__(self):
        self.speed = 300  # pixels per second
    
    def early_update(self, thisObject, engine):
        # Get input
        horizontal = engine.get_key(ForgeEngine.Key.RIGHT) - engine.get_key(ForgeEngine.Key.LEFT)
        vertical = engine.get_key(ForgeEngine.Key.DOWN) - engine.get_key(ForgeEngine.Key.UP)
        
        # Apply movement
        thisObject.transform.x += horizontal * self.speed * engine.deltaTime
        thisObject.transform.y += vertical * self.speed * engine.deltaTime

# Create engine
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)

# Configure window
engine.window.width = 800
engine.window.height = 600
engine.window.title = "Hello World"
engine.window.initialize()

# Create scene
scene = ForgeEngine.Scene("main")
scene.background_color = (135, 206, 235)

# Load image
player_image = engine.import_image(r"assets\player.png")

# Create player object
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)
player.renderer = ForgeEngine.Renderer(image_id=player_image, layer=1)
player.script = PlayerScript()  # Add script

# Add to scene
scene.add_object(player)

# Register scene
engine.add_scene(scene)
engine.load_scene("main")

# Start game loop
engine.main_loop()
```

### Try It Out

- Arrow keys or WASD to move
- Player moves around the screen

---

## Step 5: Add Bouncing

Constrain the player to stay on screen:

```python
class PlayerScript:
    def __init__(self, width=800, height=600):
        self.speed = 300
        self.width = width
        self.height = height
        self.player_size = 64
    
    def early_update(self, thisObject, engine):
        # Get input
        horizontal = engine.get_key(ForgeEngine.Key.RIGHT) - engine.get_key(ForgeEngine.Key.LEFT)
        vertical = engine.get_key(ForgeEngine.Key.DOWN) - engine.get_key(ForgeEngine.Key.UP)
        
        # Apply movement
        thisObject.transform.x += horizontal * self.speed * engine.deltaTime
        thisObject.transform.y += vertical * self.speed * engine.deltaTime
        
        # Keep on screen
        if thisObject.transform.x < 0:
            thisObject.transform.x = 0
        if thisObject.transform.x > self.width - self.player_size:
            thisObject.transform.x = self.width - self.player_size
        
        if thisObject.transform.y < 0:
            thisObject.transform.y = 0
        if thisObject.transform.y > self.height - self.player_size:
            thisObject.transform.y = self.height - self.player_size
```

---

## Completed Code

```python
import ForgeEngine

class PlayerScript:
    def __init__(self):
        self.speed = 300
        self.width = 800
        self.height = 600
        self.size = 64
    
    def early_update(self, thisObject, engine):
        # Input
        dx = engine.get_key(ForgeEngine.Key.RIGHT) - engine.get_key(ForgeEngine.Key.LEFT)
        dy = engine.get_key(ForgeEngine.Key.DOWN) - engine.get_key(ForgeEngine.Key.UP)
        
        # Movement
        thisObject.transform.x += dx * self.speed * engine.deltaTime
        thisObject.transform.y += dy * self.speed * engine.deltaTime
        
        # Bounds
        thisObject.transform.x = max(0, min(thisObject.transform.x, self.width - self.size))
        thisObject.transform.y = max(0, min(thisObject.transform.y, self.height - self.size))

# Setup
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 800
engine.window.height = 600
engine.window.title = "Hello World"
engine.window.initialize()

scene = ForgeEngine.Scene("main")
scene.background_color = (135, 206, 235)

# Player
player_img = engine.import_image(r"assets\player.png")
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)
player.renderer = ForgeEngine.Renderer(image_id=player_img, layer=1)
player.script = PlayerScript()

scene.add_object(player)

# Run
engine.add_scene(scene)
engine.load_scene("main")
engine.main_loop()
```

---

## What's Next?

- Learn about [Physics and Gravity](tutorial-02-movement.md)
- Explore [Collision Detection](tutorial-03-collisions.md)
- See [Common Tasks](../guides/common-tasks.md)

---

## Troubleshooting

### Black Screen
- Make sure `assets/player.png` exists
- Check file paths use proper forward/backward slashes
- Verify pygame is installed: `pip install pygame`

### Sprite Not Moving
- Check key input in tutorial code
- Try pressing arrow keys (not WASD)
- Print debug info: `print(thisObject.transform.x)`

### Game Crashes
- Check Python version (3.6+)
- Verify ForgeEngine is installed
- Look for error messages in console

---

See also:
- [Getting Started](../getting-started/setup.md)
- [API Reference](../api/overview.md)
- [Common Tasks](../guides/common-tasks.md)
