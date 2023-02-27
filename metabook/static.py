from enum import Enum


__all__ = (
    "ImgStyle"
)


class StrEnum(str, Enum):
    pass


class ImgStyle(StrEnum):

    # - class Styles(StrEnum):
    VAPORWAVE = 'vaporwave'
    POST_APOCALIPTIC = 'post apocaliptic'
    GOTHIC = 'gothic'
    FANTASY = 'fantasy'
    SCIFI = 'sci-fi'
    CYBER = 'cyber'
    CYBERNETIC = 'cybernetic'
    CYBERPUNK = 'cyberpunk'
    BIOPUNK = 'biopunk'
    STEAMPUNK = 'steampunk'
    DIESELPUNK = 'dieselpunk'
    AFROFUTURISM = 'afrofuturism'
    MEMPHIS = 'memphis'

    # - class BWIllustrationStyles(Styles, ArtStyles):
    STENCIL = 'stencil'
    PENCIL_DRAW = 'pencil drawing'
    PENSIL_SKETCH = 'pencil sketch'
    BALLPOINT_PEN = 'ballpoint pen art'
    NEWSPAPER_TOON = 'political cartoon from U.S. newspaper'
    CHARCOAL = 'charcoal sketch'
    WOODCUT = 'woodcut'
    TO_COLOR = 'coloring-in sheet'
    ETCHING = 'etching'

    # - class ColorIllustrationStyles(Styles, ArtStyles):
    CRAYON = 'crayon'
    CHILD_DRAW = "child's drawing"
    ACRYLIC_ON_CANVAS = 'acrylic on canvas'
    WATER_COLOR = 'water color'
    COLOR_PENCIL = 'coloured pencil'
    COLOR_PENCIL_DETAIL = 'coloured pencil, detailed'
    OIL = 'oil painting'
    AIRBRUSH = 'airbrush'
    PASTELS = 'pastels'
    JAP = 'ukiyo-e'
    CHIN = 'chinese watercolor'
    ALEGRIA = 'alegria'
    COLLAGE = 'collage'
    VECTOR = 'vector art'
    WATERCOLOR_PEN = 'watercolor & pen'
    PRINTING = 'screen printing'
    LOW_POLY = 'low poply'
    LAYERED_PAPER = 'layered paper'
    STORY = 'story book'
    DIGITAL = 'digital painting'
    STICKER = 'sticker illustration'
    COMIC = 'comic book'
    ANIME = 'Anime'
    PIXAR = 'Pixar'
    DISNEY_OLD = 'vintage Disney'
    DISNEY_90 = 'Disney 1990s, cel shading'
    GHIBLI = 'Studio Ghibli'
    H_BARBERA = 'Hanna Barbera, 1990s'
    PIXEL = 'pixel art'
    VINTAGE = '1970s grainy vintage illustration'

from PIL.ImageFile import ImageFile
#class IllustrationStyles(BWIllustrationStyles, ColorIllustrationStyles):
 #   pass


