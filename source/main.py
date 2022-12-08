"""Cria e exporta os dados dos campeões, seus dados e skins.

Discord: Balaclava#1912
GitHub: https://github.com/controlado
"""

from json import dump
from timeit import timeit
from typing import Any

from requests.sessions import Session


class Riot:
    """Cria e exporta os dados dos campeões, seus dados e skins.

    O processo é feito através de requests.

    Parâmetros:
        session (requests.Session): Sessão, necessária pra requisições.
        skins_data (dict): Todos os dados dos campeões e suas skins.

    Métodos:
        request: Faz uma requisição e retorna o JSON da resposta.
        get_champions: Retorna uma lista com todos os dados e skins dos campeões.
        get_champion_skins: Retorna uma lista com todas as skins de um campeão.
        get_skins_data: Retorna os dados de todas as skins do League of Legends.
        get_champion_id: Retorna o ID do campeão baseado no splashPath.

    Métodos estáticos:
        get_splash_art: Retorna a URL da arte do item requisitado (pode ser um campeão ou uma skin).
        export: Salva um conteúdo em algum arquivo JSON que passar no parâmetro.
    """

    def __init__(self) -> None:
        """Instancia a classe Riot.

        Inicia uma sessão e puxa os dados das skins do
        League of Legends, que são necessárias para os
        métodos da classe.
        """
        self.session = Session()
        self.skins_data = self.get_skins_data()

    def request(self, *args, **kwargs) -> Any:
        """Faz uma requisição e retorna o JSON da resposta."""
        response = self.session.request(*args, **kwargs)
        return response.json()

    def get_champions(self) -> list[dict]:
        """Retorna uma lista com todos os dados e skins dos campeões.

        Através do skin_data, gera uma lista com as informações e dados
        de cada campeão do League of Legends, pra conseguir as skins do
        mesmo de forma efetiva, o método chama o get_champion_skins().

        Retorna:
            list[dict]: Lista com os campeões, seus dados e skins.
        """
        return [
            {
                "id": champion_id,
                "name": self.skins_data[skin]["name"],
                "art": self.get_splash_art(champion_id, skin),
                "skins": self.get_champion_skins(champion_id)
            }
            for skin in self.skins_data
            if self.skins_data[skin]["isBase"]
            if (champion_id := self.get_champion_id(skin))
        ]

    def get_champion_skins(self, champion_id: str) -> list[dict]:
        """Retorna uma lista com todas as skins de um campeão.

        Através do skin_data, gera uma lista com as informações de
        cada skin desse campeão, verificando se o id do campeão da
        skin é referente ao champion_id (parâmetro do método).

        Parâmetros:
            champion_id (str): ID do campeão.

        Retorna:
            list[dict]: Skins do campeão (baseado no ID do mesmo).
        """
        return [
            {
                "id": skin,
                "name": self.skins_data[skin]["name"],
                "rarity": self.skins_data[skin]["rarity"],
                "art": self.get_splash_art(champion_id, skin)
            }
            for skin in self.skins_data
            if not self.skins_data[skin]["isBase"]
            if self.get_champion_id(skin) == champion_id
        ]

    def get_skins_data(self) -> dict:
        """Retorna os dados de todas as skins do League of Legends.

        Faz uma requisição GET para uma URL da Riot e retorna o JSON do
        resultado dessa requisição, a sessão não precisa ser preparada.
        """
        url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins.json"
        return self.request(method="get", url=url)

    def get_champion_id(self, skin_index: int) -> str:
        """Retorna o ID do campeão baseado no splashPath."""
        endpoint = self.skins_data[skin_index]["splashPath"]
        endpoint_splited = endpoint.split("/")
        return endpoint_splited[-2]

    @staticmethod
    def get_splash_art(champion_id: int, skin_id: int) -> str:
        """Retorna a URL da arte do item requisitado (pode ser um campeão ou uma skin)."""
        return f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/champion-splashes/{champion_id}/{skin_id}.jpg"

    @staticmethod
    def export(output_file: str, content: Any) -> None:
        """Salva um conteúdo em algum arquivo JSON que passar no parâmetro.

        Parâmetros:
            output_file (str): Arquivo que o conteúdo será importado.
            content (Any): O conteúdo que vai ser importado.
        """
        with open(output_file, "w", encoding="UTF-8") as opened_file:
            dump(content, opened_file, indent=4, ensure_ascii=False)


def main():
    """Função pra executar o código corretamente."""
    riot = Riot()
    data = riot.get_champions()
    riot.export("response.json", data)


if __name__ == "__main__":
    main()  # função principal.
