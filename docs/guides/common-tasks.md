# Common Tasks Guide

This guide shows how to accomplish common game development tasks in ForgeEngine.

## Table of Contents

1. [Creating Game Objects](#creating-game-objects)
2. [Moving Objects](#moving-objects)
3. [Detecting Collisions](#detecting-collisions)
4. [Playing Sounds](#playing-sounds)
5. [Sprite Animation](#sprite-animation)
6. [Managing Score](#managing-score)
7. [Pausing the Game](#pausing-the-game)
8. [Scene Transitions](#scene-transitions)
9. [Spawning Objects](#spawning-objects)
10. [Camera Following](#camera-following)

---

## Creating Game Objects

### Basic Object

```python
obj = ForgeEngine.Object(engine)
obj.transform = ForgeEngine.Transform(x=100, y=200)
scene.add_object(obj)
```

### Object with Sprite

```python
image = engine.import_image(r"assets\sprite.png")

obj = ForgeEngine.Object(engine)
obj.transform = ForgeEngine.Transform(x=100, y=200)
obj.renderer = ForgeEngine.Renderer(image_id=image, layer=1)
scene.add_object(obj)
```

### Object with Physics

```python
image = engine.import_image(r"assets\character.png")

obj = ForgeEngine.Object(engine)
obj.transform = ForgeEngine.Transform(x=100, y=200)
obj.renderer = ForgeEngine.Renderer(image_id=image, layer=1)
obj.kinematic = ForgeEngine.Kinematic()
obj.kinematic.gravity = 2000
obj.collider = ForgeEngine.Collider(
    shape=ForgeEngine.Rectangle(width=64, height=64),
    x_offset=0,
    y_offset=0
)
scene.add_object(obj)
```

---

## Moving Objects

### Direct Position Change

```python
class SimpleMoveScript:
    def update(self, thisObject, engine):
        # Move right
        thisObject.transform.x += 100 * engine.deltaTime
        
        # Move down
        thisObject.transform.y += 50 * engine.deltaTime
```

### Keyboard Input

```python
from ForgeEngine import Key

class PlayerMoveScript:
    def __init__(self):
        self.speed = 300
    
    def early_update(self, thisObject, engine):
        # Get input
        horizontal = 0
        vertical = 0
        
        if engine.get_key(Key.LEFT):
            horizontal -= 1
        if engine.get_key(Key.RIGHT):
            horizontal += 1
        if engine.get_key(Key.UP):
            vertical -= 1
        if engine.get_key(Key.DOWN):
            vertical += 1
        
        # Apply movement
        thisObject.transform.x += horizontal * self.speed * engine.deltaTime
        thisObject.transform.y += vertical * self.speed * engine.deltaTime
```

### With Physics

```python
from ForgeEngine import Key

class PhysicsPlayerScript:
    def __init__(self):
        self.speed = 500
        self.jump_force = 800
    
    def early_update(self, thisObject, engine):
        # Horizontal movement
        horizontal = engine.get_key(Key.RIGHT) - engine.get_key(Key.LEFT)
        thisObject.kinematic.velocity_x = horizontal * self.speed
        
        # Jumping
        if engine.get_key_down(Key.SPACE) and thisObject.kinematic.on_ground:
            thisObject.kinematic.velocity_y = -self.jump_force
```

---

## Detecting Collisions

### Check Collision

```python
class CollisionScript:
    def update(self, thisObject, engine):
        # Get other objects
        others = [o for o in engine.objects if o != thisObject]
        
        # Check collision
        collisions = engine.check_collision(thisObject, others)
        
        # Handle collisions
        for obj in collisions:
            self.on_collision(thisObject, obj)
    
    def on_collision(self, thisObject, other):
        print(f"Collided with {other}")
```

### Collision by Tag

```python
class TagCollisionScript:
    def update(self, thisObject, engine):
        others = [o for o in engine.objects if o != thisObject]
        collisions = engine.check_collision(thisObject, others)
        
        for obj in collisions:
            if obj.has_tag("enemy"):
                self.hit_enemy(thisObject, obj)
            elif obj.has_tag("coin"):
                self.collect_coin(thisObject, obj)
            elif obj.has_tag("hazard"):
                self.hit_hazard(thisObject, obj)
    
    def hit_enemy(self, thisObject, enemy):
        pass
    
    def collect_coin(self, thisObject, coin):
        pass
    
    def hit_hazard(self, thisObject, hazard):
        pass
```

### Distance-Based Detection

```python
from ForgeEngine import fMath

class DistanceDetectionScript:
    def __init__(self, detection_range=200):
        self.range = detection_range
    
    def update(self, thisObject, engine):
        # Find nearby objects
        pos = (thisObject.transform.x, thisObject.transform.y)
        
        for obj in engine.objects:
            if obj == thisObject:
                continue
            
            other_pos = (obj.transform.x, obj.transform.y)
            distance = fMath.distance(pos, other_pos)
            
            if distance < self.range:
                self.on_nearby(thisObject, obj, distance)
    
    def on_nearby(self, thisObject, other, distance):
        print(f"{other} is nearby at distance {distance}")
```

---

## Playing Sounds

### Basic Sound

```python
class SoundScript:
    def __init__(self):
        self.sound_id = None
    
    def start(self, thisObject, engine):
        self.sound_id = engine.import_audio(r"assets\sound.wav")
        thisObject.audio = ForgeEngine.Audio(audio_id=self.sound_id)
    
    def update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.SPACE):
            thisObject.audio.play_sound()
```

### Event-Based Sound

```python
class CharacterScript:
    def __init__(self):
        self.jump_sound = None
        self.damage_sound = None
    
    def start(self, thisObject, engine):
        self.jump_sound = engine.import_audio(r"assets\jump.wav")
        self.damage_sound = engine.import_audio(r"assets\damage.wav")
        thisObject.audio = ForgeEngine.Audio(audio_id=self.jump_sound)
    
    def early_update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.SPACE) and thisObject.kinematic.on_ground:
            thisObject.kinematic.velocity_y = -800
            thisObject.audio.audio_id = self.jump_sound
            thisObject.audio.play_sound()
    
    def take_damage(self, thisObject, amount):
        thisObject.audio.audio_id = self.damage_sound
        thisObject.audio.play_sound()
```

---

## Sprite Animation

### Basic Animation

```python
class AnimationScript:
    def __init__(self):
        self.walk_animation = None
        self.idle_animation = None
    
    def start(self, thisObject, engine):
        # Load frames
        walk1 = engine.import_image(r"assets\walk1.png")
        walk2 = engine.import_image(r"assets\walk2.png")
        walk3 = engine.import_image(r"assets\walk3.png")
        idle = engine.import_image(r"assets\idle.png")
        
        # Create animations
        self.walk_animation = ForgeEngine.Animation(
            frame_ids=[walk1, walk2, walk3],
            frame_duration=0.1,
            loop=True
        )
        
        self.idle_animation = ForgeEngine.Animation(
            frame_ids=[idle],
            loop=True
        )
        
        thisObject.animation = self.idle_animation
    
    def early_update(self, thisObject, engine):
        # Switch animations
        if engine.get_key(ForgeEngine.Key.RIGHT):
            if thisObject.animation != self.walk_animation:
                thisObject.animation = self.walk_animation
                thisObject.animation.play()
        else:
            if thisObject.animation != self.idle_animation:
                thisObject.animation = self.idle_animation
                thisObject.animation.play()
```

---

## Managing Score

### Simple Score System

```python
class ScoreManager:
    def __init__(self):
        self.score = 0
        self.score_ui = None
    
    def add_score(self, points):
        self.score += points
        if self.score_ui:
            self.score_ui.textRenderer.text = f"Score: {self.score}"
    
    def get_score(self):
        return self.score
    
    def reset_score(self):
        self.score = 0

# Usage
score_manager = ScoreManager()

# Create score display
score_obj = ForgeEngine.Object(engine)
score_obj.transform = ForgeEngine.Transform(x=50, y=50)
score_obj.textRenderer = ForgeEngine.TextRenderer(
    text="Score: 0",
    font_path=r"assets\Arial.ttf",
    font_size=24,
    color=(255, 255, 255),
    layer=100
)
score_obj.textRenderer.is_overlay = True
score_manager.score_ui = score_obj
scene.add_object(score_obj)

# Add points
score_manager.add_score(10)
```

---

## Pausing the Game

### Simple Pause

```python
class PauseManager:
    def __init__(self, engine):
        self.engine = engine
        self.is_paused = False
        self.paused_objects = []
    
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.pause()
        else:
            self.resume()
    
    def pause(self):
        # Deactivate all objects except pause menu
        self.paused_objects = []
        for obj in self.engine.objects:
            if not obj.has_tag("pause_menu"):
                self.paused_objects.append(obj)
                obj.active = False
    
    def resume(self):
        # Reactivate objects
        for obj in self.paused_objects:
            obj.active = True
        self.paused_objects = []

# Usage
pause_manager = PauseManager(engine)

# Pause on ESC key
class PauseScript:
    def __init__(self, pause_manager):
        self.pause_manager = pause_manager
    
    def update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.ESC):
            self.pause_manager.toggle_pause()
```

---

## Scene Transitions

### Basic Transition

```python
class LevelCompleteScript:
    def __init__(self, next_scene_id):
        self.next_scene = next_scene_id
        self.completed = False
    
    def update(self, thisObject, engine):
        if self.completed and engine.get_key_down(ForgeEngine.Key.ENTER):
            engine.load_scene(self.next_scene)
    
    def level_complete(self):
        self.completed = True
```

### Fade Transition

```python
class FadeTransition:
    def __init__(self, engine):
        self.engine = engine
        self.fade_obj = None
        self.duration = 1.0
        self.elapsed = 0
        self.transitioning = False
        self.next_scene = None
    
    def start_fade_to_scene(self, scene_id, duration=1.0):
        self.next_scene = scene_id
        self.duration = duration
        self.elapsed = 0
        self.transitioning = True
        
        # Create fade overlay
        self.fade_obj = ForgeEngine.Object(self.engine)
        self.fade_obj.transform = ForgeEngine.Transform(x=0, y=0)
        self.fade_obj.add_tag("fade_overlay")
        
        self.engine.current_scene.add_object(self.fade_obj)
    
    def update(self):
        if not self.transitioning:
            return
        
        self.elapsed += self.engine.deltaTime
        progress = self.elapsed / self.duration
        
        if progress >= 1.0:
            # Load new scene
            self.engine.load_scene(self.next_scene)
            self.transitioning = False
        else:
            # Update fade
            # Note: Would need renderer for visual effect
            pass
```

---

## Spawning Objects

### Spawn at Position

```python
class SpawnerScript:
    def __init__(self, object_factory, spawn_rate=2):
        self.factory = object_factory
        self.spawn_rate = spawn_rate
        self.spawn_timer = 0
    
    def update(self, thisObject, engine):
        self.spawn_timer += engine.deltaTime
        
        if self.spawn_timer >= 1.0 / self.spawn_rate:
            self.spawn_object(thisObject, engine)
            self.spawn_timer = 0
    
    def spawn_object(self, at_obj, engine):
        new_obj = self.factory.create()
        new_obj.transform.x = at_obj.transform.x
        new_obj.transform.y = at_obj.transform.y
        engine.current_scene.add_object(new_obj)
```

### Random Spawn

```python
import random

class RandomSpawnerScript:
    def __init__(self, spawn_rate=1, spread=200):
        self.spawn_rate = spawn_rate
        self.spread = spread
        self.spawn_timer = 0
    
    def update(self, thisObject, engine):
        self.spawn_timer += engine.deltaTime
        
        if self.spawn_timer >= 1.0 / self.spawn_rate:
            x = thisObject.transform.x + random.randint(-self.spread, self.spread)
            y = thisObject.transform.y + random.randint(-self.spread, self.spread)
            
            self.spawn_at(engine, x, y)
            self.spawn_timer = 0
    
    def spawn_at(self, engine, x, y):
        # Create spawned object
        obj = ForgeEngine.Object(engine)
        obj.transform = ForgeEngine.Transform(x=x, y=y)
        engine.current_scene.add_object(obj)
```

---

## Camera Following

### Follow Object

```python
class FollowCameraScript:
    def __init__(self, target):
        self.target = target
        self.offset_x = 0
        self.offset_y = -50
    
    def update(self, thisObject, engine):
        if self.target and self.target.transform:
            cam_width = thisObject.camera.render_zone_width or 800
            cam_height = thisObject.camera.render_zone_height or 600
            
            thisObject.transform.x = (
                self.target.transform.x + self.offset_x - cam_width / 2
            )
            thisObject.transform.y = (
                self.target.transform.y + self.offset_y - cam_height / 2
            )
```

### Smooth Camera Follow

```python
from ForgeEngine import fMath

class SmoothFollowCameraScript:
    def __init__(self, target, smoothness=0.1):
        self.target = target
        self.smoothness = smoothness
    
    def update(self, thisObject, engine):
        if not self.target or not self.target.transform:
            return
        
        cam_width = thisObject.camera.render_zone_width or 800
        cam_height = thisObject.camera.render_zone_height or 600
        
        target_x = self.target.transform.x - cam_width / 2
        target_y = self.target.transform.y - cam_height / 2
        
        # Smoothly interpolate
        thisObject.transform.x = fMath.lerp(
            thisObject.transform.x,
            target_x,
            self.smoothness
        )
        thisObject.transform.y = fMath.lerp(
            thisObject.transform.y,
            target_y,
            self.smoothness
        )
```

---

## More Examples

See:
- [Tutorials](../tutorials/)
- [API Reference](../api/overview.md)
- [Guides](../../)
