import matplotlib.pyplot as plt


# {(F.21),(M,34)}

def main():
    with open("myheart.csv") as file1:
        matrix = ([list(line.replace("\n", "").split(',')) for line in file1.readlines()])

    dict_list = []
    for line in matrix[1:]:  # exclude the header line
        dict_from_csv = {}
        for i, elem in enumerate(line):
            dict_from_csv[matrix[0][i]] = elem  # for each line elem, associate it to its header relative
        dict_list.append(dict_from_csv)

    def funDpS(dict_list):  # função que calcula a distribuição da doença por sexo

        dictaux = {'M': 0, 'F': 0}
        for dict in dict_list:
            if dict.get('sexo') == 'M' and dict.get('temDoença') == '1':
                dictaux['M'] += 1

            elif dict.get('sexo') == 'F' and dict.get('temDoença') == '1':
                dictaux['F'] += 1

        return dictaux

    def funDpEE(dict_list):  # função que calcula a distribuição da doença por escalões etários
        dictaux2 = []
        for dict in dict_list:
            dictaux2.append(dict.get('idade'))

        min1 = min(dictaux2)
        max1 = max(dictaux2)

        i = int(min1)
        intervalos = {}
        while i < int(max1):
            if i >= 30:
                intervalos[i, i + 4] = 0
                i += 5
            else:
                i += 1

        for dict in dict_list:
            idade = dict['idade']
            for (k1, k2) in intervalos.keys():
                if k1 <= int(idade) <= k2 and dict.get('temDoença') == '1':
                    intervalos[(k1, k2)] += 1

        return intervalos

    def remove_items(list, item):  # função auxiliar que remove os 0s
        res = [i for i in list if i != item]

        return res

    def funDpNC(dict_list):  # função que calcula a distribuição da doença por níveis de colesterol
        dictaux2 = []
        for dict in dict_list:
            dictaux2.append(int(dict.get('colesterol')))
        dictaux2 = remove_items(dictaux2, 0)
        min1 = min(dictaux2)
        max1 = max(dictaux2)

        i = int(min1)
        intervalos = {}
        while i < int(max1):
            if i > 0:
                intervalos[i, i + 9] = 0
                i += 10
            else:
                i += 1

        for dict in dict_list:
            colesterol = dict['colesterol']
            for (k1, k2) in intervalos.keys():
                if k1 <= int(colesterol) <= k2 and dict.get('temDoença') == '1':
                    intervalos[(k1, k2)] += 1

        return intervalos

    def printDpSTable(dict_list):  # função que imprime na forma de uma tabela uma distribuição
        headers = ['M', 'F']

        print("_" * 13)
        print(f'{headers[0]: <10}{headers[1]:}')
        print("-" * 13)
        for key, value in dict_list.items():
            print(f"{value: <9}", end=' ')

        return ' '

    def printTable(dict_list1, dict_list2,
                   dict_list3):  # função que apresenta as tabelas correspondentes às distribuições pedidas
        print("_" * 21)
        print("| sexo | nº doentes |")
        print("-" * 21)
        for sexo, nr in dict_list1.items():
            print(f"| {sexo:<4} |       {nr:>4} |")
        print("-" * 21)

        print("_" * 22)
        print("| idade | nº doentes |")
        print("-" * 22)
        for idade, nr in dict_list2.items():
            print(f"| {idade[0]:<1}-{idade[1]:<1} | {nr:>10} |")
        print("-" * 22)

        print("_" * 29)
        print("| colesterol  |  nº doentes |")
        print("-" * 29)
        for colesterol, nr in dict_list3.items():
            print(f"| {colesterol[0]:<3}-{colesterol[1]:<3}           | {nr:>5} |")
        print("-" * 29)

        return ' '

    def printTableWMP(dict_list1, dict_list2,
                      dict_list3):  # função que apresenta as tabelas correspondentes às distribuições pedidas(com matplotlib)
        labels = ['Masculino', 'Feminino']
        values = [dict_list1['M'], dict_list1['F']]
        # Create bar chart
        fig, ax = plt.subplots()
        ax.bar(labels, values)
        # Add labels and title
        ax.set_xlabel('Sexo')
        ax.set_ylabel('nº de doentes')
        ax.set_title('Distribuição da doença por sexo')
        # Show plot
        plt.show()

        age_ranges = [f"{x[0]}-{x[1]}" for x in dict_list2.keys()]
        counts = list(dict_list2.values())
        fig, ax = plt.subplots()
        ax.bar(age_ranges, counts)
        ax.set_xlabel('Intervalo de idades')
        ax.set_ylabel('nº de doentes')
        ax.set_title('Distribuição da doença por escalões etários')
        plt.show()

        height_ranges = [f"{x[0]}-{x[1]}" for x in dict_list3.keys()]
        counts = list(dict_list3.values())
        fig, ax = plt.subplots()
        ax.barh(height_ranges, counts)
        ax.set_xlabel('nº de doentes')
        ax.set_ylabel('Intervalo de valores do colesterol')
        ax.set_title('Distribuição da doença por níveis de colesterol')
        plt.show()

    print(dict_list)
    print(funDpS(dict_list))
    print(funDpEE(dict_list))
    print(funDpNC(dict_list))
    print(printDpSTable(funDpS(dict_list)))
    print(printTable(funDpS(dict_list), funDpEE(dict_list), funDpNC(dict_list)))
    printTableWMP(funDpS(dict_list), funDpEE(dict_list), funDpNC(dict_list))


if __name__ == "__main__":
    main()
