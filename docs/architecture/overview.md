# Architecture Overview

## High-Level Architecture

ForgeEngine follows a **component-based entity architecture** pattern, which provides flexibility and reusability for game development. Here's how all the pieces fit together:

```mermaid
graph TB
    subgraph Application["Application Layer"]
        GameScript["Game Script<br/>(game.py)"]
        ObjectScripts["Object Scripts<br/>(Behaviors)"]
    end
    
    subgraph Engine["ForgeEngine Core"]
        EngineCore["Engine<br/>(Main Orchestrator)"]
        SceneManager["Scene Manager"]
        ObjectManager["Object Manager"]
    end
    
    subgraph Systems["Game Systems"]
        InputSys["Input System"]
        PhysicsSys["Physics System"]
        RenderSys["Rendering System"]
        AnimationSys["Animation System"]
        AudioSys["Audio System"]
        CollisionSys["Collision System"]
    end
    
    subgraph ComponentLayer["Component-Based Objects"]
        Transform["Transform Component"]
        Renderer["Renderer Component"]
        TextRenderer["TextRenderer Component"]
        Collider["Collider Component"]
        Kinematic["Kinematic Component"]
        Camera["Camera Component"]
        Audio["Audio Component"]
        Animation["Animation Component"]
    end
    
    subgraph Pipeline["Rendering Pipeline"]
        PygamePipe["Pygame Pipeline"]
        ModernGLPipe["ModernGL Pipeline"]
    end
    
    GameScript -->|Creates| EngineCore
    ObjectScripts -->|Attached to| ObjectManager
    EngineCore -->|Manages| SceneManager
    EngineCore -->|Manages| ObjectManager
    EngineCore -->|Coordinates| Systems
    ObjectManager -->|Composed of| ComponentLayer
    Systems -->|Use| ComponentLayer
    RenderSys -->|Renders via| Pipeline
    InputSys -->|Updates| ComponentLayer
    PhysicsSys -->|Updates| Transform
    CollisionSys -->|Detects| Collider
    AnimationSys -->|Updates| Animation
