import re

class VendingMachine:
    def __init__(self):  # Inicialização das variaveis
        self.state = 'IDLE'
        self.coins = {"1c": 0, "2c": 0, "5c": 0, "10c": 0, "20c": 0, "50c": 0, "1e": 0, "2e": 0}
        self.total_cents = 0
        self.saldo = "0e00c"

    def read_coins(self, data):  # Função que le as moedas no input e valida las, printa tambem quando alguma delas é invalida
        if not data.startswith("MOEDA"):
            return print("Comando inválido")

        regex = re.compile(r"\d+[ce]")  # regex para verificar a validade das moedas
        values = regex.findall(data)
        list = []
        for value in values:
            if value in self.coins.keys():  # verifica se uma dada moeda é valida(faz parte do dicionario de moedas validas)
                self.coins[value] += 1
            else:
                list.append(value)
        print('maq: ', end="")
        for coin in list:
            print(f'{coin} - moeda inválida;', end="")

        self.saldo = self.sum_coins()  # soma de todas as moedas no dicionario de moedas
        print(f'saldo = {self.saldo.split(",")[0]}')
        self.state = 'CALL_IN_PROGRESS'

    def sum_coins(self):  # Função que soma das moedas presentes no dicionario de moedas, utilizaçao da variavel total_coins para devolver o valor completo do valor do saldo (desformatado)
        self.total_cents = 0
        for coin, count in self.coins.items():
            if coin.endswith("c"):
                self.total_cents += count * int(coin[:-1])
                # print(coin[:-1])
            elif coin.endswith("e"):
                self.total_cents += count * int(coin[:-1]) * 100
        eur = self.total_cents // 100
        cents = self.total_cents % 100
        return f"{eur}e{cents:02d}c,{self.total_cents}"

    def saldoTOtotal_cents(self, total_cents):  # Função que converte o valor do saldo "desformatado" para "formatado"
        eur = total_cents // 100
        cents = self.total_cents % 100
        return f"{eur}e{cents:02d}c"

    def is_valid_phone_number(self, numero):  # Função que valida se os numeros de telefone sao validos e calcula o saldo para cada condiçao correspondente
        regex1 = re.compile(r"6[04]1[0-9][0-9][0-9][0-9][0-9][0-9]")
        regex2 = re.compile(r"(00)\d+")
        regex3 = re.compile(r"2[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]")
        regex4 = re.compile(r"800[0-9][0-9][0-9][0-9][0-9][0-9]")
        regex5 = re.compile(r"808[0-9][0-9][0-9][0-9][0-9][0-9]")

        if re.match(regex1, numero):
            print('maq: "Esse número não é permitido neste telefone. Queira discar novo número!"')
            return 'CALL_IN_PROGRESS'
        elif re.match(regex2, numero):
            if int(self.total_cents) >= 150:
                self.total_cents -= 150
                saldoF = self.saldoTOtotal_cents(self.total_cents)
                print(f"maq: saldo = {saldoF}")
                return 'CALL_IN_PROGRESS'
            else:
                print('maq: "Saldo insuficiente. Faça o carregamento!"')
                return 'IDLE'
        elif re.match(regex3, numero):
            if int(self.total_cents) >= 25:
                self.total_cents = self.total_cents - 25
                saldoF = self.saldoTOtotal_cents(self.total_cents)
                print(f'maq: "saldo = {saldoF}"')
                return 'CALL_IN_PROGRESS'
            else:
                print('maq: "Saldo insuficiente. Faça o carregamento!"')
                return 'IDLE'
        elif re.match(regex4, numero):
            if int(self.total_cents) >= 0:
                self.total_cents -= 0
                saldoF = self.saldoTOtotal_cents(self.total_cents)
                print(f'maq: "saldo = {saldoF}"')
                return 'CALL_IN_PROGRESS'
            else:
                print('maq: "Saldo insuficiente. Faça o carregamento!"')
                return 'IDLE'
        elif re.match(regex5, numero):
            if int(self.total_cents) >= 10:
                self.total_cents -= 10
                saldoF = self.saldoTOtotal_cents(self.total_cents)
                print(f'maq: "saldo = {saldoF}"')
                return 'CALL_IN_PROGRESS'
            else:
                print('maq: "Saldo insuficiente. Faça o carregamento!"')
                return 'IDLE'
        else:
            print("Número Inválido")
            return 'IDLE'

    def process_command(self, data):  # Processa todos os estados e "chama" as funçoes necessárias
        if data == "LEVANTAR":
            print('maq: "Introduza moedas."')
            self.state = 'COINS_INSERTION'
            return

        if self.state == 'COINS_INSERTION':
            self.read_coins(data)
            return

        if data.startswith("T="):
            numero = data.split("=")[1]
            self.state = self.is_valid_phone_number(numero)
            if self.state == 'CALL_IN_PROGRESS':
                return
            elif self.state == 'IDLE':
                self.state = 'IDLE'
                print("Comando não reconhecido")

        if data == "POUSAR":
            self.state = 'IDLE'
            saldoF = self.saldoTOtotal_cents(self.total_cents)
            print(f"maq: troco={saldoF}; Volte sempre!")
            return

        if data == "ABORTAR":
            self.state = 'IDLE'
            saldoF = self.saldoTOtotal_cents(self.total_cents)
            print(f"maq: troco={saldoF}, processo abortado!")
            return

        print("Comando não reconhecido")

def main():
    vm = VendingMachine()
    while True:
        data = input()
        vm.process_command(data)

if __name__ == "__main__":
    main()

# MOEDA 10c, 30c, 50c, 2e.
# T=601181818
# T=641181818
# T=253604470
# T=800123456
# T=808123456
