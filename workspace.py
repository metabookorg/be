import typing as tp


from metabook.txt import GPT3
from metabook.img import Dalle2
from metabook.txt import TxtAnalyzer

class ImgPromptCreator:
    def __init__(self, characters: tp.Dict[str, str], style: str):
        self.characters: tp.Dict[str, str] = characters
        self.style: str = style

    def create(self, sentence: str):
        prompt = f"Text: {sentence}\nProduce a brief scene description considering:\n"
        for k, v in self.characters.items():
            prompt += f"{k} is {v}\n"

        return GPT3.create(text_in=prompt, creativity_risk=0.5)

    def create2(self, sentence: str):
        prompt = ""
        for k, v in self.characters.items():
            prompt += f"{k}, {v}; "
        prompt = f"{prompt[:-2]}. "
        prompt += f"{sentence}. "
        prompt += f"{self.style} style"
        return prompt
    """
    
    """


def run1():
    sentence = 'One day, Pit and Rover were walking through the forest when they stumbled upon a strange portal.'
    chars = {'Pit': 'a brave kid', 'Rover': 'the trusty dog of Pit'}
    prompt = f"Text: {sentence}\nProduce a very short scene description considering\n"
    for k,v in chars.items():
        prompt += f"{k}: {v}\n"
    print(f"PROMPT:\n{prompt}")
    print(GPT3.create(text_in=prompt, creativity_risk=0.5))

    """
    PROMPT:
    Text: One day, Pit and Rover were walking through the forest when they stumbled upon a strange portal.
    Produce a scene description considering:
    Pit is a brave kid
    Rover is the trusty dog of Pit
    
    
    The sun was setting as Pit and Rover ventured through the forest. Pit, a brave kid, was determined to explore the unknown, while Rover, his trusty dog, followed closely behind. Suddenly, they stopped in their tracks as they noticed a mysterious portal in the distance. Pit's eyes lit up with excitement, and Rover's tail began to wag as they both stepped closer to investigate.
    
    -------------------------------------------------------
    
    PROMPT:
    Text: One day, Pit and Rover were walking through the forest when they stumbled upon a strange portal.
    Produce a brief scene description considering:
    Pit is a brave kid
    Rover is the trusty dog of Pit
    
    
    Pit and Rover cautiously approach the strange portal, their eyes wide with curiosity. 
    Pit takes a deep breath and bravely steps through the portal, Rover close behind him. 
    As they travel through the portal, the bright colors and strange sounds of a new world fill their senses. 
    Pit smiles at the wonders that await them and takes a few more steps forward, Rover faithfully trotting along beside him.

    
    
    
    
    """


if __name__ == '__main__':
    story = [
        "Once upon a time, there was a kid named Pit and his trusty dog, Rover",
        "Pit was quite the adventurous type and always looking for a new challenge",
        "One day, Pit and Rover were walking through the forest when they stumbled upon a strange portal",
        "When Pit looked inside the portal, he saw a world unlike anything he had ever seen before",
        "It was a world of advanced technology, far in the future",
        "Pit and Rover decided to take a chance and jumped in",
        "When they arrived in the future world, they were greeted by an AI bot",
        "The AI bot told them that they had been chosen to take part in an extreme adventure",
        "The AI bot explained that the adventure would take them to different parts of the world, and that they would have to complete various tasks in order to succeed",
        "Pit and Rover were both excited and scared at the same time",
        "Pit and Rover set out on their adventure, and they were amazed by the things they saw and the places they went",
        "They encountered robots, aliens, and other strange creatures",
        "They also faced many dangers and had to use their wits to survive",
        "After a long and difficult journey, Pit and Rover finally reached the end of their adventure",
        "They had succeeded in their mission and were rewarded with a huge amount of treasure",
        "Pit and Rover returned home with their bounty and shared their amazing story with everyone",
        "From that day on, they were known as the bravest adventurers in the world",
        ]

    #analyzer = TxtAnalyzer(text='. '.join(story))
    #analyzer.analyze()
    #for k, v in analyzer.characters.items():
    #    print(f"{k}: {v}")
    text = '. '.join(story)#[f'{idx}. {el}.\n' for idx, el in enumerate(story)])
    prompt = '.\n '.join([f'{idx}. {el}' for idx, el in enumerate(story)])#f"Text:{text}"
    print(prompt)
    suffix = 'For each numbered sentence list all the characters in it.'
    print('RESULTS:\n')
    print(GPT3.create(text_in=prompt, suffix=suffix, creativity_risk=0.2))