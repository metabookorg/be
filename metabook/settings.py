import pydantic as pdt

__all__ = (
    "BaseSettings",
    "OpenAISettings"
)


class BaseSettings(pdt.BaseSettings):
    development: bool = pdt.Field(env="DEVELOP_FLAG", default=False)
    #TODO: 'ENV'??
    env: str = pdt.Field(env='ENV', default='dev')

    @property
    def test_env(self) -> bool:
        return False if self.env == 'prod' else True



class OpenAISettings(BaseSettings):
    apikey: str = pdt.Field(env='OPENAI_APIKEY', default='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')

