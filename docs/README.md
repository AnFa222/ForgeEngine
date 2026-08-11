# ForgeEngine Documentation

Welcome to the ForgeEngine documentation! This guide covers everything you need to know to build games with ForgeEngine.

This Guide Is AI Generated. Not All Information Is 100% Accurate.

## Quick Navigation

- **[Getting Started](getting-started/installation.md)** — Installation, setup, and first steps
- **[Architecture Overview](architecture/overview.md)** — High-level design and structure
- **[API Documentation](api/overview.md)** — Complete API reference
- **[Guides](guides/common-tasks.md)** — Common tasks and best practices
- **[Tutorials](tutorials/tutorial-01-hello-world.md)** — Learn by doing

## What is ForgeEngine?

ForgeEngine is a lightweight **2D game engine written in Python** designed for rapidly building games and interactive experiences. It provides:

- **Component-based architecture** for flexible game object design
- **Multiple rendering backends** (Pygame and ModernGL)
- **Physics simulation** with gravity, friction, and collision detection
- **Input handling** for keyboard and mouse
- **Animation system** with frame-based sprites
- **Audio playback** capabilities
- **Camera system** with viewport control
- **Scriptable objects** for custom behavior
- **Build system** for packaging games into standalone executables

## Key Concepts

### Objects & Components
Everything in ForgeEngine is an Object. Objects are composed of Components that define their behavior:

```python
# Create a game object
player = ForgeEngine.Object(engine)

# Attach components
player.transform = ForgeEngine.Transform(x=100, y=200)
player.renderer = ForgeEngine.Renderer(image_id=my_image)
player.kinematic = ForgeEngine.Kinematic()
player.script = MyPlayerScript()
```

### Scenes
Scenes are containers for objects. You can load different scenes to transition between game states:

```python
scene = ForgeEngine.Scene("main_level")
scene.add_object(player)
engine.add_scene(scene)
engine.load_scene("main_level")
```

### The Game Loop
ForgeEngine automatically manages the game loop. Each frame:

1. Processes input
2. Updates physics
3. Updates animations
4. Runs object scripts
5. Renders everything

## Supported Platforms

- Windows
- macOS
- Linux

## Requirements

- Python 3.x
- pygame (for Pygame pipeline) or glfw + moderngl (for ModernGL pipeline)

## Quick Start

1. **Install ForgeEngine:** Clone the repository or install via pip
2. **Create a game script:** See [Getting Started](getting-started/first-project.md)
3. **Build your game:** Use the provided Build system to create executables

## Example

Here's a minimal game:

```python
import ForgeEngine

# Create engine
engine = ForgeEngine.Engine(render_pipeline=ForgeEngine.pygamePipeline)
engine.window.width = 800
engine.window.height = 600
engine.window.title = "My Game"
engine.window.initialize()

# Load an image
image = engine.import_image(r"assets\player.png")

# Create a scene
scene = ForgeEngine.Scene("main")
scene.background_color = (50, 150, 255)

# Create a game object
player = ForgeEngine.Object(engine)
player.transform = ForgeEngine.Transform(x=400, y=300)
player.renderer = ForgeEngine.Renderer(image_id=image, layer=1)

scene.add_object(player)
engine.add_scene(scene)
engine.load_scene("main")

# Run the game
engine.main_loop()
```

## Documentation Sections

### [Getting Started](getting-started/installation.md)
- [Installation & Setup](getting-started/installation.md)
- [Configuration](getting-started/setup.md)
- [Your First Project](getting-started/first-project.md)
- [Troubleshooting](getting-started/troubleshooting.md)

### [Architecture](architecture/overview.md)
- [High-Level Overview](architecture/overview.md)
- [Project Structure](architecture/project-structure.md)
- [Major Systems](architecture/systems.md)
- [Data Flow & Lifecycle](architecture/data-flow.md)
- [Game Loop](architecture/lifecycle.md)

### [API Reference](api/overview.md)
- [Engine API](api/engine.md)
- [Object & Components](api/objects-and-components.md)
- [Input System](api/input.md)
- [Physics & Collision](api/physics.md)
- [Rendering](api/rendering.md)
- [Scene Management](api/scenes.md)
- [Utilities](api/utilities.md)

### [Guides](guides/common-tasks.md)
- [Common Tasks](guides/common-tasks.md)
- [Working with Sprites](guides/sprites.md)
- [Physics & Collisions](guides/physics.md)
- [Input Handling](guides/input.md)
- [Cameras & Views](guides/cameras.md)
- [Animation](guides/animation.md)
- [Audio](guides/audio.md)
- [Building Executables](guides/building.md)
- [Extending the Engine](guides/extending.md)
- [Debugging](guides/debugging.md)

### [Tutorials](tutorials/)
- [Tutorial 1: Hello World](tutorials/tutorial-01-hello-world.md)
- [Tutorial 2: Player Movement](tutorials/tutorial-02-movement.md)
- [Tutorial 3: Collision Detection](tutorials/tutorial-03-collisions.md)
- [Tutorial 4: Complete Game](tutorials/tutorial-04-complete-game.md)

### [Internals](internals/)
- [Rendering Pipeline](internals/rendering.md)
- [Input System](internals/input.md)
- [Physics Engine](internals/physics.md)
- [Collision Detection](internals/collision.md)

## Contributing

See [Contributing Guide](contributing.md) for information on how to contribute to ForgeEngine.

## License

ForgeEngine is licensed under the GNU General Public License v3.0. See LICENSE file for details.

## Support

- Check the [Troubleshooting Guide](getting-started/troubleshooting.md)
- Review the [Tutorials](tutorials/)
- Visit the GitHub repository for issues and discussions
