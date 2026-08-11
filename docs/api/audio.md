# Audio API

ForgeEngine provides audio playback functionality through the Audio component.

## Audio Component

The Audio component handles sound playback for game objects.

### Constructor

```python
audio = ForgeEngine.Audio(audio_id)
```

**Parameters:**
- `audio_id` - Audio ID from `engine.import_audio()`

### Properties

```python
audio.audio_id         # Audio file ID
audio.play             # bool - Should play this frame?
audio.stop             # bool - Should stop this frame?
```

### Methods

```python
audio.play_sound()     # Queue sound to play this frame
audio.stop_sound()     # Queue sound to stop this frame
```

### How It Works

1. Call `audio.play_sound()` or `audio.stop_sound()`
2. At end of frame, engine processes audio queue
3. Sounds play/stop
4. Flags are reset for next frame

**Note:** Audio is event-based, not continuous. Set the flags each frame you want the action to occur.

---

## Loading Audio

### Import Audio File

```python
audio_id = engine.import_audio(path)
```

**Parameters:**
- `path` (str) - Path to audio file (.wav, .mp3, etc.)

**Returns:** Unique ID for the audio

**Example:**
```python
# Load audio files
jump_sound = engine.import_audio(r"assets\jump.wav")
background_music = engine.import_audio(r"assets\music.mp3")
coin_sound = engine.import_audio("assets/coin.wav")
```

---

## Basic Example

```python
# Load audio
jump_sound = engine.import_audio(r"assets\jump.wav")

# Create object with audio
player = ForgeEngine.Object(engine)
player.audio = ForgeEngine.Audio(audio_id=jump_sound)

# Play sound in script
class PlayerScript:
    def update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.SPACE):
            # Jump
            thisObject.kinematic.velocity_y = -800
            
            # Play jump sound
            thisObject.audio.play_sound()
```

---

## Multiple Audio Tracks

### Multiple Audio Components

Note: Currently, objects support one audio component. For multiple sounds:

```python
class PlayerScript:
    def __init__(self, engine):
        self.jump_sound_id = engine.import_audio(r"assets\jump.wav")
        self.land_sound_id = engine.import_audio(r"assets\land.wav")
        self.damage_sound_id = engine.import_audio(r"assets\damage.wav")
    
    def play_sound(self, thisObject, sound_id):
        thisObject.audio.audio_id = sound_id
        thisObject.audio.play_sound()
    
    def update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.SPACE):
            self.play_sound(thisObject, self.jump_sound_id)
```

---

## Sound Effects

### Jump Sound

```python
class PlayerScript:
    def __init__(self):
        self.jump_sound = None
    
    def start(self, thisObject, engine):
        self.jump_sound = engine.import_audio(r"assets\sfx\jump.wav")
        thisObject.audio = ForgeEngine.Audio(audio_id=self.jump_sound)
    
    def early_update(self, thisObject, engine):
        if engine.get_key_down(ForgeEngine.Key.SPACE) and thisObject.kinematic.on_ground:
            thisObject.kinematic.velocity_y = -800
            thisObject.audio.audio_id = self.jump_sound
            thisObject.audio.play_sound()
```

### Damage Sound

```python
class CharacterScript:
    def __init__(self):
        self.health = 100
        self.damage_sound = None
    
    def start(self, thisObject, engine):
        self.damage_sound = engine.import_audio(r"assets\sfx\damage.wav")
        thisObject.audio = ForgeEngine.Audio(audio_id=self.damage_sound)
    
    def take_damage(self, thisObject, amount):
        self.health -= amount
        thisObject.audio.audio_id = self.damage_sound
        thisObject.audio.play_sound()
        
        if self.health <= 0:
            print("Character defeated!")
```

### Coin Collection

```python
class CoinScript:
    def __init__(self):
        self.coin_sound = None
    
    def start(self, thisObject, engine):
        self.coin_sound = engine.import_audio(r"assets\sfx\coin.wav")
    
    def update(self, thisObject, engine):
        # Check collision
        others = [o for o in engine.objects if o != thisObject]
        collisions = engine.check_collision(thisObject, others)
        
        if collisions:
            for obj in collisions:
                if obj.has_tag("player"):
                    # Play sound
                    obj.audio.audio_id = self.coin_sound
                    obj.audio.play_sound()
                    
                    # Remove coin
                    engine.current_scene.destroy_object(thisObject)
```

---

## Background Music

### Single Track

```python
class GameScript:
    def __init__(self):
        self.music_obj = None
    
    def start(self, thisObject, engine):
        music_id = engine.import_audio(r"assets\music\game_theme.mp3")
        
        # Create object for music
        self.music_obj = ForgeEngine.Object(engine)
        self.music_obj.audio = ForgeEngine.Audio(audio_id=music_id)
        
        engine.current_scene.add_object(self.music_obj)
        
        # Play music
        self.music_obj.audio.play_sound()
```

### Looped Music

```python
class MusicManager:
    def __init__(self, engine):
        self.engine = engine
        self.current_music = None
        self.music_tracks = {}
        
        # Load all music
        self.music_tracks['menu'] = engine.import_audio(r"assets\music\menu.mp3")
        self.music_tracks['game'] = engine.import_audio(r"assets\music\game.mp3")
        self.music_tracks['boss'] = engine.import_audio(r"assets\music\boss.mp3")
    
    def play_music(self, track_name):
        # Stop current music
        if self.current_music:
            self.current_music.audio.stop_sound()
        
        # Play new music
        self.current_music = ForgeEngine.Object(self.engine)
        self.current_music.audio = ForgeEngine.Audio(
            audio_id=self.music_tracks[track_name]
        )
        self.current_music.add_tag("music")
        
        self.engine.current_scene.add_object(self.current_music)
        self.current_music.audio.play_sound()
    
    def stop_music(self):
        if self.current_music:
            self.current_music.audio.stop_sound()
            self.engine.current_scene.destroy_object(self.current_music)
            self.current_music = None
```

---

## Sound Manager

### Centralized Audio Control

```python
class SoundManager:
    def __init__(self, engine):
        self.engine = engine
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        """Load all game sounds"""
        self.sounds = {
            'jump': self.engine.import_audio(r"assets\sfx\jump.wav"),
            'land': self.engine.import_audio(r"assets\sfx\land.wav"),
            'damage': self.engine.import_audio(r"assets\sfx\damage.wav"),
            'coin': self.engine.import_audio(r"assets\sfx\coin.wav"),
            'menu_select': self.engine.import_audio(r"assets\sfx\select.wav"),
        }
    
    def play_sound(self, sound_name, position=None):
        """Play a sound effect"""
        if sound_name not in self.sounds:
            print(f"Sound '{sound_name}' not found!")
            return
        
        # Create object for sound
        sound_obj = ForgeEngine.Object(self.engine)
        sound_obj.audio = ForgeEngine.Audio(audio_id=self.sounds[sound_name])
        sound_obj.add_tag("sfx")
        
        if position:
            sound_obj.transform = ForgeEngine.Transform(x=position[0], y=position[1])
        
        self.engine.current_scene.add_object(sound_obj)
        sound_obj.audio.play_sound()
        
        # Cleanup after sound finishes (simplified)
        # In reality, would need to track sound duration
        return sound_obj

# Usage
sound_manager = SoundManager(engine)
sound_manager.play_sound('jump')
sound_manager.play_sound('coin', position=(400, 300))
```

---

## Audio File Formats

**Supported:** WAV, MP3, and other formats supported by the rendering pipeline

**Recommended:**
- WAV for sound effects (uncompressed, better for short sounds)
- MP3 for music (compressed, saves space)

### File Locations

```
assets/
├── sfx/              # Sound effects
│   ├── jump.wav
│   ├── land.wav
│   ├── damage.wav
│   └── coin.wav
└── music/            # Background music
    ├── menu.mp3
    ├── game.mp3
    └── boss.mp3
```

---

## Timing Audio

### Synchronize with Animation

```python
class CharacterScript:
    def __init__(self):
        self.attack_sound = None
        self.attack_animation = None
    
    def start(self, thisObject, engine):
        self.attack_sound = engine.import_audio(r"assets\sfx\attack.wav")
        thisObject.audio = ForgeEngine.Audio(audio_id=self.attack_sound)
        
        # Animation frames
        frame1 = engine.import_image(r"assets\attack_1.png")
        frame2 = engine.import_image(r"assets\attack_2.png")
        frame3 = engine.import_image(r"assets\attack_3.png")
        
        self.attack_animation = ForgeEngine.Animation(
            frame_ids=[frame1, frame2, frame3],
            frame_duration=0.1,
            loop=False
        )
        thisObject.animation = self.attack_animation
    
    def attack(self, thisObject):
        # Start animation
        thisObject.animation.play()
        
        # Play sound
        thisObject.audio.audio_id = self.attack_sound
        thisObject.audio.play_sound()
```

### Delayed Sound

```python
class ExplosionScript:
    def __init__(self):
        self.explosion_sound = None
        self.time_until_sound = 0.5  # 500ms delay
        self.elapsed = 0
    
    def start(self, thisObject, engine):
        self.explosion_sound = engine.import_audio(r"assets\sfx\explosion.wav")
        thisObject.audio = ForgeEngine.Audio(audio_id=self.explosion_sound)
    
    def update(self, thisObject, engine):
        self.elapsed += engine.deltaTime
        
        # Play sound after delay
        if self.elapsed >= self.time_until_sound:
            thisObject.audio.play_sound()
            self.time_until_sound = float('inf')  # Only play once
```

---

## Current Limitations

Based on current implementation:

- **One audio component per object** - To play multiple sounds, use object pool
- **No volume control** - Volume is fixed
- **No audio state queries** - Can't check if sound is playing
- **Limited audio formats** - Depends on rendering pipeline
- **No 3D audio** - All audio is 2D

---

## Workarounds

### Play Multiple Sounds

```python
class MultiSoundPlayer:
    def play_sound(self, engine, audio_id):
        # Create temporary object for sound
        temp = ForgeEngine.Object(engine)
        temp.audio = ForgeEngine.Audio(audio_id=audio_id)
        temp.add_tag("temp_audio")
        
        engine.current_scene.add_object(temp)
        temp.audio.play_sound()
        
        # Could queue for removal after duration
```

### Fade Audio

```python
class FadeAudioScript:
    def __init__(self, target_audio, duration):
        self.target_audio = target_audio
        self.duration = duration
        self.elapsed = 0
    
    def update(self, thisObject, engine):
        # Note: No direct volume control, would need custom implementation
        self.elapsed += engine.deltaTime
        
        if self.elapsed >= self.duration:
            self.target_audio.stop_sound()
```

---

See also:
- [Engine API](engine.md) - Audio loading methods
- [Objects & Components API](objects-and-components.md) - Component details
- [Guides: Audio](../guides/audio.md) - Audio examples
