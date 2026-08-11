# Project Structure

ForgeEngine is organized into logical modules and directories:

```
ForgeEngine/
├── __init__.py                    # Package initialization & exports
├── engine.py                      # Main Engine class
├── object.py                      # Object class (entity)
├── scene.py                       # Scene class (world container)
├── events.py                      # Event definitions
├── keys.py                        # Key/input constants
├── time.py                        # Time management
├── build.py                       # Build system for packaging
├── pipelines.py                   # Pipeline identifiers
│
├── # System Files
├── checkCollision.py              # Collision detection (SAT algorithm)
├── utils.py                       # Utility functions
├── fileUtils.py                   # File I/O helpers
├── mathUtils.py                   # Math utilities (Vector2, etc.)
├── log.py                         # Logging/error handling
├── transformations.py             # Transform calculations
├── randomUtils.py                 # Random utilities
│
├── # Rendering Pipelines
├── pygamePipeline.py              # Pygame rendering backend
├── pygameKeyMapping.py            # Pygame key mapping
├── modernglPipeline.py            # ModernGL rendering backend
├── modernglKeyMapping.py          # ModernGL key mapping
│
├── # Components
├── objectComponents/
│   ├── transformComponent.py      # Transform component (position, rotation, scale)
│   ├── rendererComponent.py       # Renderer component (sprite rendering)
│   ├── textRendererComponent.py   # Text renderer component
│   ├── colliderComponent.py       # Collider component (collision shapes)
│   ├── kinematicComponent.py      # Kinematic component (physics)
│   ├── cameraComponent.py         # Camera component (viewport)
│   ├── animationComponent.py      # Animation component (sprite animation)
│   ├── audioComponent.py          # Audio component (sound)
│   └── log.py                     # Component logging
│
├── LICENSE                        # GNU GPL-3.0 license
├── README.md                      # Main README
└── docs/                          # Documentation (you are here)
```

## Module Responsibilities

### Core Engine (`engine.py`)
- Manages the main game loop
- Orchestrates all systems
- Handles scene loading and object management
- Processes input events
- Coordinates rendering

### Objects (`object.py`)
- Represents game entities
- Container for components
- Provides script interface
- Manages tags for categorization

### Scenes (`scene.py`)
- Container for objects
- Manages background color
- Provides object lifecycle management
- Enables scene transitions

### Components (`objectComponents/`)
Each component provides specific functionality to objects:

- **Transform** - Position, rotation, and scale
- **Renderer** - Renders sprites with layers
- **TextRenderer** - Renders text with overlay support
- **Collider** - Defines collision shapes (Rectangle, Polygon)
- **Kinematic** - Physics with gravity and velocity
- **Camera** - Defines viewport and render zones
- **Animation** - Frame-based sprite animation
- **Audio** - Audio playback control

### Collision System (`checkCollision.py`)
- Implements Separating Axis Theorem (SAT) algorithm
- Rectangle vs Rectangle collision
- Polygon vs Polygon collision
- Collision response handling

### Input System
- **keys.py** - Key and button constants
- **pygameKeyMapping.py** - Maps Pygame events to engine keys
- **modernglKeyMapping.py** - Maps ModernGL events to engine keys

### Rendering Pipelines
- **pygamePipeline.py** - Pygame rendering implementation
- **modernglPipeline.py** - ModernGL rendering implementation
- Abstracts rendering details from engine

### Utilities
- **mathUtils.py** - Math functions (lerp, distance, Vector2, etc.)
- **fileUtils.py** - File I/O (load/save JSON, text, binary)
- **utils.py** - Screen boundary checking
- **log.py** - Error logging
- **randomUtils.py** - Random value generation

## Component System Details

### What is a Component?

A component is a small, focused piece of functionality that can be attached to an Object. For example:

```python
obj = ForgeEngine.Object(engine)
obj.transform = ForgeEngine.Transform(x=100, y=200)  # Component
obj.renderer = ForgeEngine.Renderer(image_id=img, layer=1)  # Component
obj.kinematic = ForgeEngine.Kinematic()  # Component
obj.script = MyCustomScript()  # Component
```

### Component Lifecycle

Each component has optional lifecycle methods:

1. **Initialization** - Component is created and attached
2. **Start** - Called once when scene loads (via script)
3. **Early Update** - Called before physics
4. **Update** - Called after physics
5. **Rendering** - Rendered each frame (automatic for Renderer)
6. **Destruction** - Component destroyed when object is removed

### Required Component Relationships

Some components require others to function properly:

- **Renderer** requires **Transform** (needs position)
- **Collider** requires **Transform** (needs position)
- **Camera** requires **Transform** (needs position)
- **TextRenderer** requires **Transform** (needs position)

If these requirements aren't met, ForgeEngine logs warnings and disables the component.

## Object Hierarchy

```
Scene
└── Objects[]
    ├── Object 1
    │   ├── Transform
    │   ├── Renderer
    │   ├── Collider
    │   ├── Kinematic
    │   ├── Animation
    │   └── Script
    │
    ├── Object 2 (Camera)
    │   ├── Transform
    │   ├── Camera
    │   └── Script
    │
    └── Object 3 (UI)
        ├── Transform
        ├── TextRenderer
        └── Script
```

## Data Flow

### Initialization Flow

```
1. Create Engine
2. Create Scene
3. Create Objects and Components
4. Load Assets (images, audio)
5. Add Objects to Scene
6. Add Scene to Engine
7. Load Scene
8. Call engine.main_loop()
```

### Game Loop Flow

```
Each Frame:
1. Poll Window Events (QUIT, etc.)
2. Get Components (collect all active components)
3. Calculate Delta Time
4. Handle Input (keyboard, mouse)
5. Update Timers
6. Early Update (scripts run first)
7. Physics Update (kinematic, collision)
8. Animation Update
9. Update (scripts run second)
10. Render (all visible objects)
11. Audio Update (play/stop sounds)
```

See [Game Loop Lifecycle](lifecycle.md) for detailed information.

## Design Patterns Used

### Component Pattern
Objects are composed of components that define their behavior. This provides flexibility and reusability.

### Scene-Based Architecture
Games are divided into scenes that can be loaded/unloaded as needed.

### Pipeline Pattern
The rendering system uses a pipeline pattern to support multiple backends (Pygame, ModernGL).

### Event-Driven Input
Input is collected each frame and made available to scripts via engine methods.

### Scripting System
Scripts attached to objects provide custom behavior without modifying engine code.

## Extensibility Points

ForgeEngine can be extended in several ways:

1. **Custom Scripts** - Attach to objects for custom behavior
2. **Custom Components** - Create new component types (advanced)
3. **Rendering Pipelines** - Implement new rendering backends
4. **Collision Shapes** - Add custom collision shape types
5. **Math Utilities** - Extend mathUtils with custom functions

## Dependencies

### Core Requirements
- Python 3.x

### Rendering
- pygame (for Pygame pipeline) OR
- glfw, moderngl, numpy, pillow (for ModernGL pipeline)

### Building
- pyinstaller (optional, for packaging)

## Performance Considerations

### Object Management
- Objects are collected into component lists each frame
- Active objects are cached to avoid repeated iteration

### Rendering
- Objects are rendered by layer for proper depth sorting
- Layer caching optimizes rendering

### Collision
- SAT algorithm efficiently handles polygon collisions
- Rectangle collisions are optimized

### Physics
- Kinematic updates only process moving objects
- Frame-based updates match game loop timing
