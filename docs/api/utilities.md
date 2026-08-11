# Utilities API

ForgeEngine provides utility classes and functions for math, file I/O, and other common tasks.

## Math Utilities (fMath)

### Static Methods

#### Linear Interpolation

```python
from ForgeEngine import fMath

result = fMath.lerp(a, b, t)
```

Interpolates between two values.

**Parameters:**
- `a` (float) - Start value
- `b` (float) - End value
- `t` (float) - Interpolation factor (0-1, or beyond)

**Returns:** Interpolated value

**Example:**
```python
# Fade between 0 and 255
alpha_start = 0
alpha_end = 255
for t in [0, 0.25, 0.5, 0.75, 1.0]:
    alpha = fMath.lerp(alpha_start, alpha_end, t)
    print(alpha)  # 0, 63.75, 127.5, 191.25, 255
```

#### Distance Between Points

```python
distance = fMath.distance(p1, p2)
```

Calculates Euclidean distance between two 2D points.

**Parameters:**
- `p1` (tuple) - First point (x, y)
- `p2` (tuple) - Second point (x, y)

**Returns:** Distance as float

**Example:**
```python
player_pos = (100, 100)
enemy_pos = (150, 150)

dist = fMath.distance(player_pos, enemy_pos)
print(dist)  # ~70.71 (hypotenuse of 50-50-70.71 triangle)

# Check if close enough
if dist < 50:
    print("Player is close to enemy")
```

#### Almost Equal

```python
is_equal = fMath.almost_equal(a, b, epsilon=1e-6)
```

Checks if two floats are approximately equal (within epsilon).

**Parameters:**
- `a` (float) - First value
- `b` (float) - Second value
- `epsilon` (float) - Tolerance (default: 1e-6)

**Returns:** bool

**Example:**
```python
if fMath.almost_equal(1.0, 1.0000001):
    print("Values are practically equal")
```

#### Clamp Value

```python
clamped = fMath.clamp(value, min_val, max_val)
```

Clamps a value to a range.

**Example:**
```python
# Clamp player health to 0-100
health = 150
health = fMath.clamp(health, 0, 100)
print(health)  # 100

# Clamp alpha to 0-255
alpha = -50
alpha = fMath.clamp(alpha, 0, 255)
print(alpha)  # 0
```

#### Remap Range

```python
remapped = fMath.remap(value, in_min, in_max, out_min, out_max)
```

Remaps a value from one range to another.

**Example:**
```python
# Convert 0-100 score to 0-255 color value
score = 75
color_value = fMath.remap(score, 0, 100, 0, 255)
print(color_value)  # 191.25

# Convert screen coordinates to world coordinates
screen_x = 400
world_x = fMath.remap(screen_x, 0, 800, camera_left, camera_right)
```

#### Wrap Value

```python
wrapped = fMath.wrap(value, min_val, max_val)
```

Wraps a value within a range (wraps around).

**Example:**
```python
# Wrap angle to 0-360
angle = 450
angle = fMath.wrap(angle, 0, 360)
print(angle)  # 90

# Wrap screen position (for scrolling)
x = 1000
x = fMath.wrap(x, 0, 800)
print(x)  # 200
```

---

## Vector2 Class

### Constructor

```python
from ForgeEngine import fMath

v = fMath.Vector2(x, y)
```

**Parameters:**
- `x` (float) - X component (default: 0)
- `y` (float) - Y component (default: 0)

### Properties

```python
v.x          # float - X component
v.y          # float - Y component
```

### Operations

#### Arithmetic

```python
v1 = fMath.Vector2(10, 20)
v2 = fMath.Vector2(5, 10)

# Addition
v3 = v1 + v2  # Vector2(15, 30)

# Subtraction
v4 = v1 - v2  # Vector2(5, 10)

# Scalar multiplication
v5 = v1 * 2   # Vector2(20, 40)
v6 = v1 / 2   # Vector2(5, 10)

# In-place operations
v1 += v2      # v1 is now Vector2(15, 30)
v1 -= v2
v1 *= 2
v1 /= 2

# Negation
v7 = -v1      # Negative of v1
```

#### Comparison

```python
v1 = fMath.Vector2(10, 20)
v2 = fMath.Vector2(10, 20)
v3 = fMath.Vector2(5, 10)

if v1 == v2:
    print("Vectors are equal")

if v1 != v3:
    print("Vectors are different")
```

#### String Representation

```python
v = fMath.Vector2(10, 20)
print(repr(v))   # Vector2(10.0, 20.0)
print(str(v))    # (10.0, 20.0)
```

### Example: Movement

```python
class PlayerScript:
    def __init__(self):
        self.velocity = fMath.Vector2(0, 0)
        self.speed = 300
    
    def early_update(self, thisObject, engine):
        # Get input direction
        direction_x = engine.get_key(Key.RIGHT) - engine.get_key(Key.LEFT)
        direction_y = engine.get_key(Key.DOWN) - engine.get_key(Key.UP)
        
        direction = fMath.Vector2(direction_x, direction_y)
        
        # Move
        self.velocity = direction * self.speed
        thisObject.transform.x += self.velocity.x * engine.deltaTime
        thisObject.transform.y += self.velocity.y * engine.deltaTime
```

---

## File I/O Functions

### Save and Load JSON

```python
from ForgeEngine import save_json, load_json

# Save
data = {'name': 'player', 'level': 5, 'score': 1000}
save_json(data, r"assets\save.json")

# Load
data = load_json(r"assets\save.json", default={})
print(data['score'])  # 1000
```

### Save and Load Text

```python
from ForgeEngine import save_text, load_text

# Save
save_text(r"data\log.txt", "Game log data")

# Load
content = load_text(r"data\log.txt", default="No log")
print(content)
```

### Save and Load Binary

```python
from ForgeEngine import save_binary, load_binary

# Save
binary_data = b'\x00\x01\x02\x03'
save_binary(r"data\binary.dat", binary_data)

# Load
data = load_binary(r"data\binary.dat", default=b'')
```

### Example: Save Game

```python
class SaveManager:
    @staticmethod
    def save_game(player, filename):
        data = {
            'player_x': player.transform.x,
            'player_y': player.transform.y,
            'health': player.health,
            'score': player.score,
            'level': player.current_level,
        }
        save_json(data, filename)
    
    @staticmethod
    def load_game(filename):
        data = load_json(filename, default=None)
        if data:
            return data
        return None

# Usage
player_data = {'x': 400, 'y': 300, 'health': 100}
save_json(player_data, r"saves\player.json")

loaded_data = load_json(r"saves\player.json")
```

---

## Build System

### Building Executables

```python
from ForgeEngine import Build

build = Build(
    main_script='game.py',
    output_name='MyGame',
    extra_data=['assets/'],
    console=True,
    onefile=True
)

build.run()
```

**Parameters:**
- `main_script` (str) - Entry point script
- `output_name` (str) - Output executable name
- `extra_data` (list) - Directories/files to include
- `console` (bool) - Show console window? (default: False)
- `onefile` (bool) - Single executable file? (default: True)

### Methods

```python
build.add_asset(path)    # Add asset to build
build.clean()            # Clean build artifacts
```

### Example

```python
import ForgeEngine

# Create build configuration
build = ForgeEngine.Build(
    main_script='game.py',
    output_name='MyGame',
    extra_data=['assets/'],
    console=True,
    onefile=True
)

# Add assets
build.add_asset('assets/images')
build.add_asset('assets/audio')

# Build
build.run()

# Output: dist/MyGame.exe (Windows)
#         dist/MyGame (macOS/Linux)
```

---

## Random Utilities

```python
from ForgeEngine import randomUtils

# Check if function exists in implementation
# Current implementation unclear
```

**Note:** Random utilities may be available. Check implementation for available functions.

---

## Common Utility Patterns

### Game State Manager

```python
class GameState:
    def __init__(self):
        self.data = {}
    
    def save(self, filename):
        save_json(self.data, filename)
    
    def load(self, filename):
        self.data = load_json(filename, default={})
    
    def set(self, key, value):
        self.data[key] = value
    
    def get(self, key, default=None):
        return self.data.get(key, default)

# Usage
state = GameState()
state.set('player_level', 5)
state.set('high_score', 10000)
state.save(r"data\game_state.json")
```

### Configuration Manager

```python
class Config:
    def __init__(self):
        self.config = load_json(r"config\game.json", default={
            'width': 800,
            'height': 600,
            'debug': False,
            'volume': 100
        })
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
    
    def save(self):
        save_json(self.config, r"config\game.json")

# Usage
config = Config()
width = config.get('width')
```

### Data Validation

```python
class DataValidator:
    @staticmethod
    def validate_player_data(data):
        required_keys = ['name', 'level', 'score']
        
        for key in required_keys:
            if key not in data:
                return False
        
        # Validate ranges
        if not (1 <= data['level'] <= 100):
            return False
        
        if data['score'] < 0:
            return False
        
        return True

# Usage
player_data = load_json('player.json')
if DataValidator.validate_player_data(player_data):
    print("Valid")
else:
    print("Invalid data")
```

---

## Performance Notes

### Vector2 Operations

Vector2 operations are efficient:
- Addition/subtraction: O(1)
- Multiplication/division: O(1)
- Comparison: O(1)

### File I/O

File operations are slow - avoid in game loop:

```python
# BAD - Slow, in update loop
def update(self, thisObject, engine):
    data = load_json(r"config\game.json")  # Don't do this!
    thisObject.transform.x = data['x']

# GOOD - Load once at startup
class Game:
    def __init__(self):
        self.config = load_json(r"config\game.json")
    
    def update(self):
        x = self.config['x']  # Fast
```

---

## Error Handling

### Safe Loading

```python
def safe_load_config(filename):
    try:
        data = load_json(filename)
        return data
    except FileNotFoundError:
        print(f"Config file not found: {filename}")
        return {}
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}
```

---

See also:
- [Engine API](engine.md) - Engine methods
- [Objects & Components API](objects-and-components.md) - Component details
- [Guides: Common Tasks](../guides/common-tasks.md) - Practical examples
