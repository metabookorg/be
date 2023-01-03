import openai
import typing as tp
import os


openai.api_key = os.getenv(key='OPENAI_APIKEY', default='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')


class GPT3:

    models_map: tp.Dict[int, str] = {
        0: 'text-ada-001',
        1: 'text-babbage-001',
        2: 'text-curie-001',
        3: 'text-davinci-003'
    }

    @classmethod
    def _get_max_tokens(cls, level: int, max_tokens: int, text_in: str) -> int:
        maximum = 4000 if level == 4 else 2048
        return min(max_tokens, maximum - len(text_in))

    @classmethod
    def _get_temperature(cls, creativity_risk: float) -> float:
        return max(min(float(creativity_risk), 1), 0)

    @classmethod
    def _get_stop(cls, one_sentence_mode: bool) -> str | None:
        return "." if one_sentence_mode else None

    @classmethod
    def _get_penalty(cls, variability: float) -> float:
        return max(min(float(variability), 2), -2)

    @classmethod
    def create(cls, level: int, text_in: str, max_tokens: int, creativity_risk: float,
               suffix: str = None, one_sentence_mode: bool = False, topic_variability: float = 0,
               word_variability: float = 0) -> str:
        # TODO: use logit_bias
        if level not in cls.models_map:
            level = 4
        response = openai.Completion.create(
            model=cls.models_map[level],
            prompt=text_in,
            suffix=suffix,
            max_tokens=cls._get_max_tokens(level=level, max_tokens=max_tokens, text_in=text_in),
            temperature=cls._get_temperature(creativity_risk=creativity_risk),
            stop=cls._get_stop(one_sentence_mode=one_sentence_mode),
            presence_penalty=cls._get_penalty(variability=topic_variability),
            frequence_penalty=cls._get_penalty(variability=word_variability)
        )
        return response['choices'][0]['text']

    @classmethod
    def edit(cls, text: str, edit: str, creativity_risk: float):
        raise Exception('GPT3.edit(...) not yet implemented!')


class Dalle2:


    @classmethod
    def _check_img(cls, image: str) -> bool:
        return True

    @classmethod
    def _get_size(cls, size: str) -> str:
        size = size.upper()
        if size == 'L':
            pic_size = "1024x1024"
        elif size == 'M':
            pic_size = "512x512"
        else:
            pic_size = "256x256"
        return pic_size

    @classmethod
    def _get_n(cls, n: int) -> int:
        return max(min(int(n), 10), 1)

    @classmethod
    def _get_format(cls, url_mode: bool):
        return'url' if url_mode else 'b64_json'

    @classmethod
    def create(cls, description: str, n: int = 1, size: str = 'L',
               url_mode: bool = False) -> tp.Union[bytes, tp.List[str]]:

        response = openai.Image.create(
            prompt=description,
            n=cls._get_n(n=n),
            size=cls._get_size(size=size),
            response_format=cls._get_format(url_mode=url_mode)
        )
        return [img['url'] for img in response['data']] if url_mode else response['data']

    @classmethod
    def edit(cls, image: str, mask: str, description: str,
             n: int = 1, size: str = 'L', url_mode: bool = False) -> tp.Union[bytes, tp.List[str]]:
        if not cls._check_img(image=image):
            raise Exception(f"Invalid image: it cannot be edited by Dalle2")
        if not cls._check_img(image=mask):
            raise Exception(f"Invalid mask: image cannot be edited by Dalle2")
        response = openai.Image.create_edit(
            image=image,
            mask=mask,
            prompt=description,
            n=cls._get_n(n=n),
            size=cls._get_size(size=size),
            response_format=cls._get_format(url_mode=url_mode)
        )
        return [img['url'] for img in response['data']] if url_mode else response['data']

    @classmethod
    def create_variations(cls, image: str, n: int = 1, size: str = 'L',
                          url_mode: bool = False) -> tp.Union[bytes, tp.List[str]]:
        if not cls._check_img(image=image):
            raise Exception(f"Invalid image: variations cannot be created by Dalle2")

        response = openai.Image.create(
            image=image,
            n=cls._get_n(n=n),
            size=cls._get_size(size=size),
            response_format=self._get_format(url_mode=url_mode)
        )
        return [img['url'] for img in response['data']] if url_mode else response['data']
