# biblioteca/avioes.py
class Aviao:
    def __init__(self, aviao_id: str, modelo: str, fileiras: int, assentos_por_fileira: int):
        self.aviao_id = aviao_id
        self.modelo = modelo
        self.fileiras = fileiras
        self.assentos_por_fileira = assentos_por_fileira
    
    def gerar_layout(self) -> dict:
        """
        Gera o layout de assentos conforme especificação da AD1.
        Retorna dicionário onde chaves são assentos (ex: "1A", "30F") e valores
        são dicionários com "posicao" e "classe".
        """
        layout = {}
        letras = [chr(65 + i) for i in range(self.assentos_por_fileira)]
        
        for fileira in range(1, self.fileiras + 1):
            for letra in letras:
                assento_id = f"{fileira}{letra}"
                
                # Definir posição conforme regras da AD1
                if letra == letras[0] or letra == letras[-1]:
                    posicao = "janela"
                elif letra == letras[1] or letra == letras[-2]:
                    posicao = "meio"
                else:
                    posicao = "corredor"
                
                # Definir classe conforme fileira (exemplo da AD1)
                if fileira <= 5:
                    classe = "primeira"
                elif fileira <= 10:
                    classe = "executiva"
                else:
                    classe = "econômica"
                
                layout[assento_id] = {
                    "posicao": posicao,
                    "classe": classe
                }
        
        return layout
    
    def validar_assento(self, assento_id: str) -> bool:
        """Valida se um assento existe no layout do avião"""
        return assento_id in self.gerar_layout()


def carregar_avioes(arquivo: str = "dados/avioes.txt") -> list:
    """Carrega aviões do arquivo texto no formato especificado"""
    avioes = []
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    partes = linha.split(';')
                    if len(partes) == 4:
                        aviao_id, modelo, fileiras, assentos_por_fileira = partes
                        aviao = Aviao(
                            aviao_id=aviao_id,
                            modelo=modelo,
                            fileiras=int(fileiras),
                            assentos_por_fileira=int(assentos_por_fileira)
                        )
                        avioes.append(aviao)
    except FileNotFoundError:
        # Arquivo não existe, retorna lista vazia
        return []
    
    return avioes


def salvar_avioes(avioes: list, arquivo: str = "dados/avioes.txt"):

    """Salva lista de aviões em arquivo texto no formato especificado"""
    with open(arquivo, 'w', encoding='utf-8') as f:
        for aviao in avioes:
            linha = f"{aviao.aviao_id};{aviao.modelo};{aviao.fileiras};{aviao.assentos_por_fileira}\n"
            f.write(linha)

if __name__ == '__main__':
    # Criar avião de teste
    aviao = Aviao("B737", "Boeing 737", 30, 6)

    # Testar geração de layout
    layout = aviao.gerar_layout()
    print("Exemplo de assentos gerados:")
    print("1A:", layout["1A"])  # Primeira classe, janela
    print("7C:", layout["7C"])  # Executiva, corredor  
    print("15B:", layout["15B"])  # Econômica, meio
    print("30F:", layout["30F"])  # Econômica, janela

    # Testar validação de assentos
    print("\nValidação de assentos:")
    print("1A válido:", aviao.validar_assento("1A"))
    print("31A válido:", aviao.validar_assento("31A"))  # Deve ser False

    # # Testar persistência
    avioes = [aviao]
    salvar_avioes(avioes)
    avioes_carregados = carregar_avioes()
    print(f"\nAviões carregados: {len(avioes_carregados)}")