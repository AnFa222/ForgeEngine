# Physics & Collision API

ForgeEngine provides physics simulation and collision detection for 2D games.

## Kinematic Component

The Kinematic component simulates physics with gravity, velocity, and friction.

### Constructor

```python
kinematic = ForgeEngine.Kinematic()
```

No parameters required. Initialize with default values.

### Properties

```python
kinematic.velocity_x         # float - Current X velocity (pixels/second)
kinematic.velocity_y         # float - Current Y velocity (pixels/second)
kinematic.gravity            # float - Gravity acceleration (pixels/second²)
kinematic.gravity_direction  # float - Gravity direction in degrees (default: 90 = down)
kinematic.friction           # float - Air friction coefficient (0-1)
kinematic.on_ground          # bool - Is object on ground?
```

### How It Works

Each frame:

1. Apply gravity (if not on ground): `velocity += gravity * direction * deltaTime`
2. Apply friction: `velocity *= (1 - friction * deltaTime)`
3. Update position: `position += velocity * deltaTime`
4. Check collisions
5. Resolve collisions (stop movement, zero velocity)
6. Update `on_ground` state

### Example

```python
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)

# Add physics
kinematic = ForgeEngine.Kinematic()
kinematic.gravity = 2000          # Gravity pulls objects down
kinematic.friction = 5            # Air resistance
player.kinematic = kinematic

# Add collider for collision detection
player.collider = ForgeEngine.Collider(
    shape=ForgeEngine.Rectangle(width=64, height=64),
    x_offset=0,
    y_offset=0
)

# In script:
class PlayerScript:
    def early_update(self, thisObject, engine):
        # Jump
        if engine.get_key_down(ForgeEngine.Key.SPACE) and thisObject.kinematic.on_ground:
            thisObject.kinematic.velocity_y = -800  # Jump upward
        
        # Horizontal movement
        if engine.get_key(ForgeEngine.Key.LEFT):
            thisObject.kinematic.velocity_x = -300
        elif engine.get_key(ForgeEngine.Key.RIGHT):
            thisObject.kinematic.velocity_x = 300
        else:
            thisObject.kinematic.velocity_x = 0
```

### Gravity Direction

Gravity is applied in a specific direction (default: 90°, straight down):

```python
# Gravity pulls down (default)
kinematic.gravity_direction = 90

# Gravity pulls left
kinematic.gravity_direction = 180

# Gravity pulls up
kinematic.gravity_direction = 270

# Gravity pulls right
kinematic.gravity_direction = 0

# Custom angle
kinematic.gravity_direction = 45  # Diagonal
```

---

## Collider Component

The Collider component defines a collision shape for detecting collisions.

### Constructor

```python
collider = ForgeEngine.Collider(shape, x_offset, y_offset)
```

**Parameters:**
- `shape` - Collision shape (Rectangle or Polygon)
- `x_offset` (float) - Offset from transform position
- `y_offset` (float) - Offset from transform position

### Properties

```python
collider.shape       # Collision shape (Rectangle or Polygon)
collider.x_offset    # float - X offset
collider.y_offset    # float - Y offset
```

### Example

```python
# Rectangle collider
collider = ForgeEngine.Collider(
    shape=ForgeEngine.Rectangle(width=64, height=128),
    x_offset=0,
    y_offset=0
)
obj.collider = collider

# Polygon collider
points = [
    (0, 0),
    (100, 0),
    (100, 100),
    (0, 100)
]
collider = ForgeEngine.Collider(
    shape=ForgeEngine.Polygon(points),
    x_offset=0,
    y_offset=0
)
obj.collider = collider
```

---

## Rectangle Shape

### Constructor

```python
rect = ForgeEngine.Rectangle(width, height)
```

**Parameters:**
- `width` (float) - Width in pixels
- `height` (float) - Height in pixels

### Example

```python
# 64x64 square
shape = ForgeEngine.Rectangle(width=64, height=64)

# 100x50 rectangle
shape = ForgeEngine.Rectangle(width=100, height=50)

collider = ForgeEngine.Collider(shape=shape, x_offset=0, y_offset=0)
obj.collider = collider
```

### Tips

- Width and height should match sprite size for accurate collisions
- Use offsets to adjust collision bounds if needed

---

## Polygon Shape

### Constructor

```python
polygon = ForgeEngine.Polygon(points)
```

**Parameters:**
- `points` (list) - List of (x, y) tuples defining polygon vertices
  - **Must be convex** (no indentations)
  - Vertices should be in order (clockwise or counter-clockwise)

### Properties

```python
polygon.points      # list - Polygon vertices
```

### Example

```python
# Triangle
triangle = ForgeEngine.Polygon([
    (0, 0),
    (100, 0),
    (50, 100)
])

# Pentagon
pentagon = ForgeEngine.Polygon([
    (50, 0),
    (100, 25),
    (90, 75),
    (10, 75),
    (0, 25)
])

# Using in collider
collider = ForgeEngine.Collider(shape=triangle, x_offset=0, y_offset=0)
obj.collider = collider
```

### Convexity Requirement

Polygons **must be convex**. The engine will log an error if you try to use a non-convex polygon:

```python
# INVALID - Non-convex (concave)
invalid = ForgeEngine.Polygon([
    (0, 0),
    (100, 0),
    (50, 50),    # This point makes it non-convex
    (100, 100),
    (0, 100)
])
# ERROR: "Polygon is not convex"

# VALID - Convex
valid = ForgeEngine.Polygon([
    (0, 0),
    (100, 0),
    (100, 100),
    (0, 100)
])
```

---

## Collision Detection

### Checking Collisions

```python
collisions = engine.check_collision(obj, other_objects)
```

**Parameters:**
- `obj` - Object to check collisions for
- `other_objects` - List of objects to check against

**Returns:** List of objects that collided with `obj`

### Example

```python
class PlayerScript:
    def update(self, thisObject, engine):
        # Get all other objects
        others = [o for o in engine.objects if o != thisObject]
        
        # Check collision
        collisions = engine.check_collision(thisObject, others)
        
        # Handle collisions
        for obj in collisions:
            if obj.has_tag("enemy"):
                print("Collided with enemy!")
            elif obj.has_tag("coin"):
                print("Picked up coin!")
```

### How Collision Works

ForgeEngine uses the Separating Axis Theorem (SAT) algorithm:

1. Test all potential separating axes (edge normals)
2. Project both shapes onto each axis
3. If projections don't overlap, shapes don't collide
4. If all axes have overlapping projections, shapes collide

Supports:
- Rectangle vs Rectangle
- Polygon vs Polygon
- Rectangle vs Polygon

---

## Collision Resolution

### Automatic (for Kinematic Objects)

For objects with Kinematic components:

1. **X-axis collision**: Position reverted, `velocity_x = 0`
2. **Y-axis collision**: Position reverted, `velocity_y = 0`, `on_ground = True` (if colliding below)

### Manual (for Static Objects)

For objects without Kinematic:

```python
class CustomPhysicsScript:
    def update(self, thisObject, engine):
        # Check collision
        others = [o for o in engine.objects if o != thisObject]
        collisions = engine.check_collision(thisObject, others)
        
        if collisions:
            # Handle collision manually
            for obj in collisions:
                self.handle_collision(thisObject, obj)
    
    def handle_collision(self, obj1, obj2):
        # Implement custom collision response
        print(f"{obj1} hit {obj2}")
```

---

## Physics Examples

### Jumping

```python
class JumpScript:
    def early_update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.SPACE):
            if thisObject.kinematic.on_ground:
                thisObject.kinematic.velocity_y = -800
```

### Projectile

```python
class ProjectileScript:
    def __init__(self, velocity_x, velocity_y):
        self.initial_velocity_x = velocity_x
        self.initial_velocity_y = velocity_y
    
    def start(self, thisObject, engine):
        thisObject.kinematic.velocity_x = self.initial_velocity_x
        thisObject.kinematic.velocity_y = self.initial_velocity_y
        thisObject.kinematic.gravity = 1000  # Apply gravity
    
    def update(self, thisObject, engine):
        # Check if hit something
        others = [o for o in engine.objects if o != thisObject]
        collisions = engine.check_collision(thisObject, others)
        
        if collisions:
            # Destroy projectile on hit
            engine.current_scene.destroy_object(thisObject)
```

### Sliding

```python
class SlidingScript:
    def __init__(self):
        self.is_sliding = False
        self.slide_speed = 1000
        self.slide_direction = 1
    
    def early_update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.SHIFT):
            self.is_sliding = True
            self.slide_direction = 1 if engine.get_key(ForgeEngine.Key.RIGHT) else -1
        
        if self.is_sliding:
            thisObject.kinematic.velocity_x = self.slide_speed * self.slide_direction
        
        if thisObject.kinematic.on_ground and not engine.get_key(ForgeEngine.Key.SHIFT):
            self.is_sliding = False
```

### Dash Ability

```python
class DashScript:
    def __init__(self):
        self.can_dash = True
        self.dash_cooldown = 1.0
        self.elapsed = 0
    
    def update(self, thisObject, engine):
        self.elapsed += engine.deltaTime
        
        if self.elapsed >= self.dash_cooldown:
            self.can_dash = True
        
        if engine.get_key_down(ForgeEngine.Key.LSHIFT) and self.can_dash:
            self.dash(thisObject, engine)
            self.can_dash = False
            self.elapsed = 0
    
    def dash(self, thisObject, engine):
        direction = 1 if engine.get_key(ForgeEngine.Key.RIGHT) else -1
        thisObject.kinematic.velocity_x = direction * 2000
```

---

## Performance Notes

### Collision Detection Cost

- **Rectangle vs Rectangle**: Very fast
- **Polygon vs Polygon**: Slower (depends on vertex count)
- **Mixed**: Moderate speed

### Optimization Tips

1. Disable colliders on off-screen objects
2. Use rectangles instead of polygons when possible
3. Only check collisions for relevant objects
4. Spatial partitioning for large scenes (Unclear from implementation)

### Large Scenes

For games with many colliding objects:

```python
# Only check collisions for relevant objects
def check_nearby_collisions(player, engine, range=500):
    nearby = [
        obj for obj in engine.objects
        if abs(obj.transform.x - player.transform.x) < range
        and abs(obj.transform.y - player.transform.y) < range
    ]
    return engine.check_collision(player, nearby)
```

---

## Debugging Collision

### Enable Debug Visualization

```python
engine.debug = True
```

This renders collision shapes:
- **Red polygon**: Rectangle colliders
- **Cyan polygon**: Polygon colliders

### Print Collision Info

```python
if collisions:
    for obj in collisions:
        print(f"Hit: {obj}")
        if obj.collider:
            print(f"  Shape type: {type(obj.collider.shape).__name__}")
            print(f"  Position: {obj.transform.x}, {obj.transform.y}")
```

---

See also:
- [Objects & Components API](objects-and-components.md) - Component details
- [Engine API](engine.md) - Engine methods
- [Physics Guide](../guides/physics.md) - Practical physics examples
