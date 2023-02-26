class Styles:
    VAPORWAVE: str = 'vaporwave'
    POST_APOCALIPTIC: str = 'post apocaliptic'
    GOTHIC: str = 'gothic'
    FANTASY: str = 'fantasy'
    SCIFI: str = 'sci-fi'
    CYBER: str = 'cyber'
    CYBERNETIC: str = 'cybernetic'
    CYBERPUNK: str = 'cyberpunk'
    BIOPUNK: str = 'biopunk'
    STEAMPUNK: str = 'steampunk'
    DIESELPUNK: str = 'dieselpunk'
    AFROFUTURISM: str = 'afrofuturism'
    MENPHIS: str = 'menphis'


class PhotoStyles(Styles):
    pass

class ArtStyles:
    pass

class ArtistStyles:
    pass


class BWIllustrationStyles(Styles, ArtStyles):
    STENCIL: str = 'stencil'
    PENCIL_DRAW: str = 'pencil drawing'
    PENSIL_SKETCH: str = 'pencil sketch'
    BALLPOINT_PEN: str = 'ballpoint pen art'
    NEWSPAPER_TOON: str = 'political cartoon from U.S. newspaper'
    CHARCOAL: str = 'charcoal sketch'
    WOODCUT: str = 'woodcut'
    TO_COLOR: str = 'coloring-in sheet'
    ETCHING: str = 'etching'


class ColorIllustrationStyles(Styles, ArtStyles):
    CRAYON: str = 'crayon'
    CHILD_DRAW: str = "child's drawing"
    ACRYLIC_ON_CANVAS: str = 'acrylic on canvas'
    WATER_COLOR: str = 'water color'
    COLOR_PENCIL: str = 'coloured pencil'
    COLOR_PENCIL_DETAIL: str = 'coloured pencil, detailed'
    OIL: str = 'oil painting'
    AIRBRUSH: str = 'airbrush'
    PASTELS: str = 'pastels'
    JAP: str = 'ukiyo-e'
    CHIN: str = 'chinise watercolor'
    ALEGRIA: str = 'alegria'
    COLLAGE: str = 'collage'
    VECTOR: str = 'vector art'
    WATERCOLOR_PEN: str = 'watercolor & pen'
    PRINTING: str = 'screen printing'
    LOW_POLY: str = 'low poply'
    LAYERED_PAPER: str = 'layered paper'
    STORY: str = 'story book'
    DIGITAL: str = 'digital painting'
    STICKER: str = 'sticker illustration'
    COMIC: str = 'comic book'
    ANIME: str = 'Anime'
    PIXAR: str = 'Pixar'
    DISNEY_OLD: str = 'vintage Disney'
    DISNEY_90: str = 'Disney 1990s, cel shading'
    GHIBLI: str = 'Studio Ghibli'
    H_BARBERA: str = 'Hanna Barbera, 1990s'
    PIXEL: str = 'pixel art'
    VINTAGE: str = '1970s grainy vintage illustration'

class IllustrationStyles(BWIllustrationStyles, ColorIllustrationStyles):
    pass


