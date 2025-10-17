from faker import Faker
from ERPProvider import ErpProvider
from provider import PROVIDER_MAP

class DataFactory:
    """
    Uma fábrica de dados que usa reflexão e um mapa de provedores para
    popular objetos com dados falsos gerados pela biblioteca Faker.
    """
    def __init__(self, locale='pt_BR'):
        """
        Inicializa a fábrica com uma instância da Faker e adiciona provedores personalizados.
        """
        self.faker = Faker(locale)
        self.faker.add_provider(ErpProvider) 
        self.provider_map = PROVIDER_MAP

    def populate(self, obj):
        """
        Popula os atributos de um objeto com base no provider_map.
        """
        attributes = [attr for attr in dir(obj) if not attr.startswith('__') and not callable(getattr(obj, attr))]

        for attr_name in attributes:
            if attr_name in self.provider_map:
                map_value = self.provider_map[attr_name]
                
                provider_name = ""
                provider_args = {}

                if isinstance(map_value, str):
                    provider_name = map_value
                elif isinstance(map_value, tuple) and len(map_value) == 2:
                    provider_name, provider_args = map_value
                else:
                    continue

                try:
                    provider_method = getattr(self.faker, provider_name)
                    generated_value = provider_method(**provider_args)
                    setattr(obj, attr_name, generated_value)
                except AttributeError:
                    print(f"Aviso: Provedor '{provider_name}' não encontrado.")
                except Exception as e:
                    print(f"Erro ao gerar dados para '{attr_name}': {e}")
        return obj

class ProdutoConfecao:
    def __init__(self):
        self.sku = None
        self.nome_produto = None
        self.preco_venda = None
        self.quantidade_estoque = None
        self.tamanho = None
        self.cor = None
        self.tecido = None

class PedidoVenda:
     def __init__(self):
        self.id = None
        self.chave_acesso_nfe = None
        self.cfop = None
        self.status_pedido = None
        self.codigo_rastreamento = None

factory = DataFactory()
novo_produto = factory.populate(ProdutoConfecao())
novo_pedido = factory.populate(PedidoVenda())

print("--- Produto de Confecção ---")
print(f"SKU: {novo_produto.sku}")
print(f"Tamanho: {novo_produto.tamanho}")
print(f"Tecido: {novo_produto.tecido}")
print(f"Preço: {novo_produto.preco_venda}")

print("\n--- Pedido de Venda ---")
print(f"ID: {novo_pedido.id}")
print(f"Chave NF-e: {novo_pedido.chave_acesso_nfe}")
print(f"CFOP: {novo_pedido.cfop}")
print(f"Status: {novo_pedido.status_pedido}")
print(f"Rastreamento: {novo_pedido.codigo_rastreamento}")