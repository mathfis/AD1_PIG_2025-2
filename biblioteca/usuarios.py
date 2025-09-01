from datetime import datetime

class Usuario:
    def __init__(self, cpf: str, nome: str, data_nascimento: str, email: str):
        self.cpf = self.validar_cpf(cpf)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.email = email
        self.reservas = []
        
    @staticmethod
    def validar_cpf(cpf: str) -> str:
        """Validação simplificada: apenas formata e verifica se tem 11 dígitos"""
        cpf_limpo = ''.join(char for char in cpf if char.isdigit())
        
        if len(cpf_limpo) != 11:
            raise ValueError("CPF deve ter 11 dígitos")
        
        # Verifica se não é uma sequência repetida (ex: 111.111.111-11)
        if all(digito == cpf_limpo[0] for digito in cpf_limpo):
            raise ValueError("CPF não pode ter todos os dígitos iguais")
    
        # Saída formatada
        return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
    
    def criar_reserva(self, voo_id: str, assento_id: str):
        """Cria uma reserva para o usuário"""
        if assento_id.upper().startswith('E') and not self.eh_maior_de_idade():
            raise ValueError("Assento de emergência não permitido para menores")
        
        for reserva in self.reservas:
            if (reserva['voo_id'] == voo_id and 
                reserva['assento_id'] == assento_id and 
                reserva['status'] == 'confirmada'):
                raise ValueError(f"Já existe reserva ativa para voo {voo_id}, assento {assento_id}")
        
        reserva = {
            'voo_id': voo_id,
            'assento_id': assento_id,
            'data_reserva': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'status': 'confirmada'
        }
        
        self.reservas.append(reserva)
        
    def cancelar_reserva(self, voo_id: str, assento_id: str):
        """Cancela uma reserva do usuário"""
        for reserva in self.reservas:
            if (reserva['voo_id'] == voo_id and 
                reserva['assento_id'] == assento_id and 
                reserva['status'] == 'confirmada'):
                
                reserva['status'] = 'cancelada'
                reserva['data_cancelamento'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                return
        
        raise ValueError(f"Reserva não encontrada para Voo: {voo_id}, Assento: {assento_id}")
    
    def modificar_reserva(self, voo_id_antigo: str, assento_id_antigo: str, 
                         voo_id_novo: str, assento_id_novo: str):
        """Modifica uma reserva existente"""
        self.cancelar_reserva(voo_id_antigo, assento_id_antigo)
        self.criar_reserva(voo_id_novo, assento_id_novo)

    def calcular_idade(self) -> int:
        """Calcula a idade do usuário"""
        partes_data = self.data_nascimento.split('/')
        if len(partes_data) != 3:
            raise ValueError("Data de nascimento deve estar no formato DD/MM/AAAA")
        
        try:
            dia = int(partes_data[0])
            mes = int(partes_data[1])
            ano = int(partes_data[2])
        except ValueError:
            raise ValueError("Data de nascimento deve conter apenas números")
        
        hoje = datetime.now()
        idade = hoje.year - ano
        
        if (hoje.month, hoje.day) < (mes, dia):
            idade -= 1
            
        if idade < 0:
            raise ValueError("Data de nascimento não pode ser no futuro")
            
        return idade

    def eh_maior_de_idade(self) -> bool:
        """Retorna True se o usuário tiver 18 anos ou mais"""
        return self.calcular_idade() >= 18

def carregar_usuarios() -> list:
    """Carrega usuários do arquivo texto"""
    usuarios = []
    
    try:
        with open('dados/usuarios.txt', 'r', encoding='utf-8') as file:
            for linha in file:
                linha = linha.strip()
                if linha:
                    partes = linha.split(';')
                    if len(partes) >= 4:
                        cpf = partes[0]
                        nome = partes[1]
                        data_nascimento = partes[2]
                        email = partes[3]
                        
                        usuario = Usuario(cpf, nome, data_nascimento, email)
                        
                        if len(partes) > 4 and partes[4]:
                            for reserva_str in partes[4].split(','):
                                if '-' in reserva_str:
                                    voo_id, assento_id = reserva_str.split('-', 1)
                                    usuario.reservas.append({
                                        'voo_id': voo_id,
                                        'assento_id': assento_id,
                                        'status': 'confirmada'
                                    })
                        
                        usuarios.append(usuario)
                        
    except FileNotFoundError:
        return []
    
    return usuarios

def salvar_usuarios(usuarios: list):
    """Salva lista de usuários no arquivo texto"""
    try:
        with open('dados/usuarios.txt', 'a'):
            pass
    except FileNotFoundError:
        import os
        os.makedirs('dados', exist_ok=True)
    
    with open('dados/usuarios.txt', 'w', encoding='utf-8') as file:
        for usuario in usuarios:
            reservas_str = ','.join([
                f"{r['voo_id']}-{r['assento_id']}" 
                for r in usuario.reservas 
                if r['status'] == 'confirmada'
            ])
            
            linha = f"{usuario.cpf};{usuario.nome};{usuario.data_nascimento};{usuario.email};{reservas_str}\n"
            file.write(linha)


# TESTE SIMPLES
if __name__ == "__main__":
    # Teste básico
    try:
        usuario = Usuario("52998224725", "Maria Silva", "15/05/1995", "maria@email.com")
        usuario.criar_reserva("V123", "A15")
        print("OK! Usuario e reserva criados com sucesso")
        print(f"OK! Maior de idade: {usuario.eh_maior_de_idade()}")
        
        # Teste persistência
        salvar_usuarios([usuario])
        usuarios_carregados = carregar_usuarios()
        print(f"OK! {len(usuarios_carregados)} usuarios carregados")
        
    except Exception as e:
        print(f"ERRO: {e}")