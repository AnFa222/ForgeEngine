# Input API

Input in ForgeEngine is handled through keyboard and mouse events. This API reference covers all input-related functionality.

## Key Constants

The `Key` enum defines all available input codes. Use these with input methods.

### Keyboard Keys

```python
from ForgeEngine import Key

# Letters
Key.A, Key.B, Key.C, ... Key.Z

# Numbers
Key.NUM_0, Key.NUM_1, ... Key.NUM_9

# Function keys
Key.F1, Key.F2, ... Key.F12

# Navigation
Key.UP, Key.DOWN, Key.LEFT, Key.RIGHT
Key.HOME, Key.END, Key.PAGEUP, Key.PAGEDOWN

# Modifiers
Key.LSHIFT, Key.RSHIFT
Key.LCTRL, Key.RCTRL
Key.LALT, Key.RALT

# Special
Key.SPACE
Key.ENTER
Key.ESC
Key.TAB
Key.BACKSPACE
Key.CAPSLOCK
Key.INSERT
Key.DELETE

# Numpad
Key.KP_0, Key.KP_1, ... Key.KP_9
Key.KP_PLUS
Key.KP_MINUS
Key.KP_MULTIPLY
Key.KP_DIVIDE
Key.KP_ENTER
Key.KP_PERIOD

# Symbols
Key.MINUS
Key.EQUALS
Key.LEFTBRACKET
Key.RIGHTBRACKET
Key.BACKSLASH
Key.SEMICOLON
Key.APOSTROPHE
Key.COMMA
Key.PERIOD
Key.SLASH
Key.GRAVE
```

### Mouse Buttons

```python
Key.MOUSE_LEFT       # Left mouse button
Key.MOUSE_MIDDLE     # Middle/wheel mouse button
Key.MOUSE_RIGHT      # Right mouse button
```

## Input Methods

### Keyboard Input

#### Check if Key is Held

```python
if engine.get_key(ForgeEngine.Key.W):
    # Key is currently pressed
    player.move_forward()
```

Returns True if the key is currently held down. Useful for continuous actions.

#### Check if Key Was Pressed This Frame

```python
if engine.get_key_down(ForgeEngine.Key.SPACE):
    # Key was just pressed this frame
    player.jump()
```

Returns True only on the first frame the key is pressed. Useful for one-time actions.

#### Check if Key Was Released This Frame

```python
if engine.get_key_up(ForgeEngine.Key.ESC):
    # Key was just released this frame
    show_pause_menu()
```

Returns True only on the first frame the key is released.

### Mouse Button Input

#### Check if Mouse Button is Held

```python
if engine.get_mouse_button(ForgeEngine.Key.MOUSE_LEFT):
    # Left button is pressed
    fire_weapon()
```

#### Check if Mouse Button Was Pressed This Frame

```python
if engine.get_mouse_button_down(ForgeEngine.Key.MOUSE_RIGHT):
    # Right button was just pressed
    use_ability()
```

#### Check if Mouse Button Was Released This Frame

```python
if engine.get_mouse_button_up(ForgeEngine.Key.MOUSE_MIDDLE):
    # Middle button was just released
    deselect()
```

### Mouse Position

#### Screen Position

```python
screen_x, screen_y = engine.screen_mouse_position
```

Position relative to the window. (0, 0) is top-left of window.

#### World Position

```python
world_x, world_y = engine.world_mouse_position
```

Position relative to the game world (camera-adjusted). Use this for gameplay logic.

#### Set Mouse Position

```python
engine.set_mouse_position((x, y))
```

Move the mouse cursor to a specific screen position.

### Mouse Cursor Visibility

```python
engine.show_mouse()   # Show mouse cursor
engine.hide_mouse()   # Hide mouse cursor
```

## Input State Properties

### Currently Held Keys

```python
engine.pressed_keys
```

Set of keys currently held down. Usually you'll use `get_key()` instead, but this provides raw access:

```python
if ForgeEngine.Key.W in engine.pressed_keys:
    # W is held
    pass
```

### Keys Pressed This Frame

```python
engine.frame_pressed_keys
```

Set of keys pressed this frame. Usually you'll use `get_key_down()` instead:

```python
if ForgeEngine.Key.SPACE in engine.frame_pressed_keys:
    # Space was just pressed
    pass
```

### Keys Released This Frame

```python
engine.frame_released_keys
```

Set of keys released this frame. Usually you'll use `get_key_up()` instead.

### Mouse Button States

```python
engine.pressed_mouse_buttons          # Currently held buttons
engine.frame_pressed_mouse_buttons    # Just pressed buttons
engine.frame_released_mouse_buttons   # Just released buttons
```

## Examples

### Player Movement Script

```python
from ForgeEngine import Key

class PlayerScript:
    def __init__(self):
        self.speed = 500  # pixels per second
        self.jump_force = 800
    
    def early_update(self, thisObject, engine):
        # Horizontal movement
        horizontal = 0
        if engine.get_key(Key.LEFT):
            horizontal -= 1
        if engine.get_key(Key.RIGHT):
            horizontal += 1
        
        thisObject.kinematic.velocity_x = horizontal * self.speed
        
        # Jumping
        if engine.get_key_down(Key.SPACE) and thisObject.kinematic.on_ground:
            thisObject.kinematic.velocity_y = -self.jump_force
```

### Shooting System

```python
from ForgeEngine import Key

class PlayerScript:
    def __init__(self):
        self.can_shoot = True
        self.shoot_cooldown = 0.2
        self.elapsed_since_shoot = 0
    
    def update(self, thisObject, engine):
        # Update cooldown
        self.elapsed_since_shoot += engine.deltaTime
        
        # Shoot on mouse click
        if engine.get_mouse_button_down(Key.MOUSE_LEFT) and self.can_shoot:
            world_x, world_y = engine.world_mouse_position
            self.shoot(world_x, world_y)
            
            self.can_shoot = False
            self.elapsed_since_shoot = 0
        
        # Check if cooldown is over
        if self.elapsed_since_shoot >= self.shoot_cooldown:
            self.can_shoot = True
    
    def shoot(self, x, y):
        # Implement shooting logic
        print(f"Shooting at {x}, {y}")
```

### Menu Navigation

```python
from ForgeEngine import Key

class MenuScript:
    def __init__(self, menu_items):
        self.menu_items = menu_items
        self.selected_index = 0
    
    def update(self, thisObject, engine):
        # Navigate menu
        if engine.get_key_down(Key.UP):
            self.selected_index = max(0, self.selected_index - 1)
        if engine.get_key_down(Key.DOWN):
            self.selected_index = min(len(self.menu_items) - 1, self.selected_index + 1)
        
        # Select item
        if engine.get_key_down(Key.ENTER):
            self.select_item(self.menu_items[self.selected_index])
        
        # Cancel
        if engine.get_key_down(Key.ESC):
            self.close_menu()
    
    def select_item(self, item):
        print(f"Selected: {item}")
    
    def close_menu(self):
        print("Menu closed")
```

### Point-and-Click

```python
from ForgeEngine import Key

class PlayerScript:
    def update(self, thisObject, engine):
        # Move to mouse position on click
        if engine.get_mouse_button_down(Key.MOUSE_LEFT):
            target_x, target_y = engine.world_mouse_position
            self.move_to(thisObject, target_x, target_y)
    
    def move_to(self, thisObject, x, y):
        direction_x = x - thisObject.transform.x
        direction_y = y - thisObject.transform.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
        
        if distance > 5:  # Stop if close enough
            speed = 300
            thisObject.kinematic.velocity_x = (direction_x / distance) * speed
            thisObject.kinematic.velocity_y = (direction_y / distance) * speed
        else:
            thisObject.kinematic.velocity_x = 0
            thisObject.kinematic.velocity_y = 0
```

## Input Processing Order

Each frame:

1. Window polls raw input from OS
2. Input mapped to Key constants (via pipeline)
3. `handle_input()` processes input:
   - Clears frame-specific sets
   - Builds `pressed_keys` set from raw input
   - Calculates `frame_pressed_keys` (newly pressed)
   - Calculates `frame_released_keys` (newly released)
4. Scripts query input via `engine.get_key()`, etc.

## Performance Notes

- Input checking is O(1) (set lookup)
- Input methods are very fast
- No performance penalty for checking many keys
- Game loop polls input once per frame

## Input Latency

Input is checked once per frame. If your game runs at 60 FPS:
- Maximum input latency: 16.67ms (one frame)
- Actual latency typically 0-16.67ms depending on frame timing

For responsive input, ensure high frame rate and short frame times.

## Remapping Keys

Currently, key mappings are hard-coded in the pipeline files. To remap keys, you need to edit:
- `pygameKeyMapping.py` (for Pygame)
- `modernglKeyMapping.py` (for ModernGL)

See [Extending ForgeEngine](../guides/extending.md) for more information.

## Event System

ForgeEngine also supports window events:

```python
from ForgeEngine import Event

# Check for quit event
if Event.QUIT in engine.window.get_events():
    engine.running = False
```

## Common Input Patterns

### Debouncing

```python
class DebounceScript:
    def __init__(self, key, duration):
        self.key = key
        self.duration = duration
        self.elapsed = 0
        self.last_pressed = False
    
    def is_pressed(self, engine):
        """Returns True only after debounce duration"""
        if engine.get_key(self.key):
            self.elapsed += engine.deltaTime
            if self.elapsed >= self.duration and not self.last_pressed:
                self.last_pressed = True
                return True
        else:
            self.elapsed = 0
            self.last_pressed = False
        
        return False
```

### Input Buffering

```python
class InputBuffer:
    def __init__(self, buffer_size=10):
        self.buffer = []
        self.buffer_size = buffer_size
    
    def add_input(self, input_name, engine):
        if engine.get_key_down(input_name):
            self.buffer.append(input_name)
            if len(self.buffer) > self.buffer_size:
                self.buffer.pop(0)
    
    def check_sequence(self, sequence):
        """Check if buffer ends with sequence"""
        if len(self.buffer) < len(sequence):
            return False
        
        return self.buffer[-len(sequence):] == sequence
```

See also:
- [Engine API](engine.md) for input methods
- [Guides: Input Handling](../guides/input.md) for practical examples
