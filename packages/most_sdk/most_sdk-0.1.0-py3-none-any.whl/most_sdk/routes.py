class Enrichment:
    def __init__(self, client):
        """MOST Enrichment Wrapper
        :param most_sdk.client.Client client: MOST SDK client
        :rtype: most_sdk.routes.Enrichment
        """

        self.client = client
        self.domain = 'big-data/enrichment'

    def base(self, path: str, query: str, cpf: str, birthdate: str) -> dict:
        data = {
            'query': query,
            'parameters': {'cpf': cpf, 'data_nascimento': birthdate},
        }

        return self.client.post(path=f'{self.domain}/{path}', original_data=data)

    def query(self, query: str, cpf: str, birthdate: str) -> dict:
        return self.base(path='', query=query, cpf=cpf, birthdate=birthdate)

    def send(self, query: str, cpf: str, birthdate: str) -> dict:
        return self.base(path='async', query=query, cpf=cpf, birthdate=birthdate)

    def get(
        self,
        protocol: str = '',
    ) -> dict:
        path = 'async/status'

        data = {
            'processId': protocol,
        }

        return self.client.post(path=f'{self.domain}/{path}', original_data=data)
