# On928Off456On3=
# 931

def main():
    while True:
        data = input()
        if 'exit' == data:
            break

        soma = 0
        flag = False
        num = ''
        for i in range(len(data)):
            if data[i:i + 3] == 'Off':
                flag = False

            elif data[i:i + 2] == 'On':
                flag = True

            elif data[i] == '=':
                if num:                     # soma o digito onde se encontra à "soma" e é resetado e printado para o ecra
                    soma += int(num)
                print(soma)
                soma = 0
                num = ''

            elif flag:                      # caso a flag seja true signifca que começa a somar os valores
                if data[i].isdigit():       # caso seja um inteiro
                    num += data[i]          # dá append desse inteiro há string "num"
                else:
                    if num:                 # caso encontre um dígito que não seja inteiro, soma o digito onde se encontra e reseta a “string” "num"
                        soma += int(num)
                    num = ''

        if num:                             # caso tenha acabado a sequencia de valores e ainda está a ser processado um inteiro, então este é adicionado à "soma"
            soma += int(num)


if __name__ == "__main__":
    main()
