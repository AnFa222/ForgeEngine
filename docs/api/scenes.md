# Scene Management API

Scenes are containers for game objects and manage the game world state.

## Scene Class

### Constructor

```python
scene = ForgeEngine.Scene(scene_id)
```

**Parameters:**
- `scene_id` (str) - Unique identifier for this scene

**Example:**
```python
main_scene = ForgeEngine.Scene("main_level")
menu_scene = ForgeEngine.Scene("menu")
```

### Properties

```python
scene.scene_id               # str - Scene identifier
scene.background_color       # tuple - (R, G, B) background color
scene.objects                # list - Objects in this scene
scene.objects_to_destroy     # list - Objects queued for destruction
```

### Methods

#### Adding Objects

```python
scene.add_object(obj)
```

Adds an object to the scene. The object will be updated and rendered each frame.

**Example:**
```python
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)
scene.add_object(player)
```

#### Destroying Objects

```python
scene.destroy_object(obj)
```

Queues an object for destruction. It will be removed next frame.

**Parameters:**
- `obj` - Object to destroy

**Example:**
```python
# Remove player when defeated
scene.destroy_object(player)

# Remove all enemies
for obj in engine.objects[:]:  # Copy list to avoid modification issues
    if obj.has_tag("enemy"):
        scene.destroy_object(obj)
```

**Important:** Always use `scene.destroy_object()`, don't modify `scene.objects` directly.

---

## Engine Scene Management

### Adding Scenes to Engine

```python
engine.add_scene(scene)
```

Registers a scene with the engine.

**Example:**
```python
main_scene = ForgeEngine.Scene("main")
menu_scene = ForgeEngine.Scene("menu")

engine.add_scene(main_scene)
engine.add_scene(menu_scene)
```

### Loading Scenes

```python
engine.load_scene(scene_id)
```

Loads and activates a scene.

**Effect:**
- Scene becomes `engine.current_scene`
- Scene objects become `engine.objects`
- Scene background color becomes `engine.background_color`

**Example:**
```python
# Load main level
engine.load_scene("main")

# Later, transition to next level
engine.load_scene("level_2")
```

### Scene Properties

```python
engine.current_scene         # Currently active scene
engine.scenes                # Dict of all scenes
engine.objects               # Objects in current scene
engine.background_color      # Current scene background
```

---

## Scene Lifecycle

```
Create Scene
    ↓
Add Objects to Scene
    ↓
Register with Engine (add_scene)
    ↓
Load Scene (load_scene)
    ↓
Main Loop Starts
    ├─ Each Frame: Update & Render Scene Objects
    ├─ Destroy Objects (if destroy_object called)
    └─ Loop Continues
    ↓
Load Different Scene (load_scene) or Exit (running = False)
    ↓
Cleanup
```

---

## Multiple Scenes Example

```python
import ForgeEngine

engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 800
engine.window.height = 600
engine.window.initialize()

# Create menu scene
menu_scene = ForgeEngine.Scene("menu")
menu_scene.background_color = (50, 50, 50)

menu_text = ForgeEngine.Object(engine)
menu_text.transform = ForgeEngine.Transform(x=400, y=300)
menu_text.textRenderer = ForgeEngine.TextRenderer(
    text="Press SPACE to Start",
    font_path=r"assets\Arial.ttf",
    font_size=32,
    color=(255, 255, 255),
    layer=1
)
menu_scene.add_object(menu_text)

# Create game scene
game_scene = ForgeEngine.Scene("game")
game_scene.background_color = (135, 206, 235)

player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)
player.add_tag("player")
game_scene.add_object(player)

# Register scenes
engine.add_scene(menu_scene)
engine.add_scene(game_scene)

# Start with menu
engine.load_scene("menu")

# Load game on spacebar (would need to be in script)
class MenuScript:
    def update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.SPACE):
            engine.load_scene("game")

menu_text.script = MenuScript()

engine.main_loop()
```

---

## Scene Transitions

### Simple Transition

```python
class TransitionScript:
    def __init__(self, next_scene_id, trigger_key):
        self.next_scene = next_scene_id
        self.trigger_key = trigger_key
    
    def update(self, thisObject, engine):
        if engine.get_key_down(self.trigger_key):
            engine.load_scene(self.next_scene)
```

### Fade Transition

```python
class FadeTransitionScript:
    def __init__(self, next_scene_id, duration):
        self.next_scene = next_scene_id
        self.duration = duration
        self.elapsed = 0
        self.fading = False
    
    def update(self, thisObject, engine):
        if self.fading:
            self.elapsed += engine.deltaTime
            
            # Calculate fade alpha
            alpha = int((self.elapsed / self.duration) * 255)
            thisObject.renderer.alpha = min(255, alpha)
            
            if self.elapsed >= self.duration:
                engine.load_scene(self.next_scene)
    
    def start_fade(self):
        self.fading = True
        self.elapsed = 0
```

### Conditional Loading

```python
class ProgressScript:
    def __init__(self):
        self.level = 1
        self.score = 0
    
    def update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.ENTER):
            if self.score >= 100:
                self.level += 1
                engine.load_scene(f"level_{self.level}")
            else:
                engine.load_scene("menu")  # Back to menu if not enough points
```

---

## Scene Properties

### Background Color

```python
scene.background_color = (R, G, B)

# Examples
scene.background_color = (0, 0, 0)         # Black
scene.background_color = (135, 206, 235)   # Sky blue
scene.background_color = (255, 255, 255)   # White
```

---

## Best Practices

### Organization

```python
# Structure scenes logically
class GameManager:
    def __init__(self, engine):
        self.engine = engine
        self.scenes = {}
        self.create_scenes()
    
    def create_scenes(self):
        # Create all scenes here
        self.scenes['menu'] = self.create_menu_scene()
        self.scenes['game'] = self.create_game_scene()
        self.scenes['pause'] = self.create_pause_scene()
        
        for scene_id, scene in self.scenes.items():
            self.engine.add_scene(scene)
    
    def create_menu_scene(self):
        scene = ForgeEngine.Scene("menu")
        # ... setup menu
        return scene
    
    def create_game_scene(self):
        scene = ForgeEngine.Scene("game")
        # ... setup game
        return scene
    
    def create_pause_scene(self):
        scene = ForgeEngine.Scene("pause")
        # ... setup pause menu
        return scene
    
    def load_scene(self, scene_id):
        self.engine.load_scene(scene_id)
```

### Cleanup

```python
class LevelScript:
    def __init__(self, next_level):
        self.next_level = next_level
    
    def update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.ENTER):
            # Destroy all game objects before loading next scene
            for obj in engine.objects[:]:
                if not obj.has_tag("persistent"):
                    engine.current_scene.destroy_object(obj)
            
            engine.load_scene(self.next_level)
```

### Using Tags for Scene Organization

```python
# Mark objects that persist across scenes
persistent_camera = ForgeEngine.Object(engine)
persistent_camera.add_tag("persistent")

# Or mark objects specific to a scene
for obj in engine.objects:
    obj.add_tag("menu_object")

# Later, clean up specific objects
for obj in engine.objects[:]:
    if obj.has_tag("menu_object"):
        engine.current_scene.destroy_object(obj)
```

---

## Debugging Scenes

### Print Scene Info

```python
class DebugScript:
    def update(self, thisObject, engine):
        print(f"Current scene: {engine.current_scene.scene_id}")
        print(f"Objects in scene: {len(engine.objects)}")
        print(f"Registered scenes: {list(engine.scenes.keys())}")
```

### List Scene Objects

```python
def print_scene_contents(engine):
    scene = engine.current_scene
    print(f"\n=== Scene: {scene.scene_id} ===")
    print(f"Background: {scene.background_color}")
    print(f"Objects ({len(scene.objects)}):")
    
    for obj in scene.objects:
        tags = ", ".join(obj.tags) if obj.tags else "no tags"
        components = []
        if obj.transform: components.append("Transform")
        if obj.renderer: components.append("Renderer")
        if obj.kinematic: components.append("Kinematic")
        if obj.collider: components.append("Collider")
        
        component_str = ", ".join(components) if components else "no components"
        print(f"  - {obj} | Tags: {tags} | Components: {component_str}")
```

---

## Common Patterns

### Level System

```python
class LevelManager:
    def __init__(self, engine):
        self.engine = engine
        self.current_level = 1
        self.max_levels = 5
        
        for i in range(1, self.max_levels + 1):
            scene = self.create_level(i)
            self.engine.add_scene(scene)
    
    def create_level(self, level_num):
        scene = ForgeEngine.Scene(f"level_{level_num}")
        
        # Load level-specific assets and objects
        # ...
        
        return scene
    
    def next_level(self):
        if self.current_level < self.max_levels:
            self.current_level += 1
            self.engine.load_scene(f"level_{self.current_level}")
        else:
            self.engine.load_scene("game_over")
    
    def previous_level(self):
        if self.current_level > 1:
            self.current_level -= 1
            self.engine.load_scene(f"level_{self.current_level}")
```

### Scene Stacking

```python
class SceneStack:
    def __init__(self, engine):
        self.engine = engine
        self.stack = []
    
    def push(self, scene_id):
        self.stack.append(scene_id)
        self.engine.load_scene(scene_id)
    
    def pop(self):
        if len(self.stack) > 1:
            self.stack.pop()
            self.engine.load_scene(self.stack[-1])
    
    def peek(self):
        return self.stack[-1] if self.stack else None
```

---

See also:
- [Engine API](engine.md) - Scene management methods
- [Objects & Components API](objects-and-components.md) - Object details
- [Guides: Common Tasks](../guides/common-tasks.md) - Scene examples
