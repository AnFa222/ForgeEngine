from .engine import Engine
from .object import Object
from .objectComponents.cameraComponent import Camera
from .objectComponents.rendererComponent import Renderer
from .objectComponents.transformComponent import Transform
from .objectComponents.colliderComponent import Collider, Rectangle, Polygon
from .objectComponents.textRendererComponent import TextRenderer
from .objectComponents.audioComponent import Audio
from .build import Build
from .log import error
from .pipelines import pygamePipeline, modernGlPipeline
import sys
import shutil
import importlib

print("Forge engine has been initialized.") #Forge stands for "Framework for Object Rendering & Game Environments"


