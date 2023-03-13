import json
import re

def parser1(path, fields, out):
    with open(path, "r") as csv:
            header = csv.readline().strip().split(',')
            data = []
            for line in csv:
                col = {}
                for i in range(len(header)):
                    col[header[i]] = re.sub(r"\n","",fields.search(line).group(i+1))
                data.append(col)

    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    with open(out, "w") as Json:
        Json.write(json_data)

def fun1():
    path = "csv/alunos.csv"
    out = "json/alunos.json"
    fields = re.compile(r"(?P<Numero>\d+),(?P<Nome>[\w\s]+),(?P<Curso>[\w\s]+)")

    parser1(path, fields, out)

def parser2(path, fields, out):
    # Define a expressão regular para extrair os campos do cabeçalho
    regex = fields

    # Define o número padrão de colunas para os campos sem especificação explícita
    default_width = 1

    # Lê o arquivo CSV e extrai os dados
    with open(path, 'r') as file:
        lines = file.readlines()

    # Extrai o cabeçalho e determina o número de colunas para cada campo
    header = lines[0].strip()

    fields = []
    start = 0  # indice da pesquisa
    while True:
        match = regex.search(header, start)
        if match is None:
            break
        name = match.group(1)
        # print(name)
        # verifica se o grupo 3 é um int(tamanho do nr de valores), se nao for diz que o tamanho é default
        width = int(match.group(3)) \
            if match.group(2) \
            else default_width
        # print(width)
        fields.append((name, width))
        start = match.end()

    # Extrai os dados para cada linha do CSV e converte para o formato JSON
    output = []
    for line in lines[1:]:  # exclui o cabeçalho
        data = line.strip().split(',')
        record = {}  # armazenar os valores de cada campo
        offset = 0  # indice onde a proxima coluna começa
        for name, width in fields:
            value = data[offset:offset + width]  # se width for igual a 1 é representado como string, caso contrario é uma lista de inteiros
            # print(value)
            offset += width
            if width == 1:
                value = value[0]
                # print(value)
            else:
                value = [int(x) for x in value]
                # print(value)
            record[name] = value
            # print(record)
        output.append(record)

    # Imprime o resultado em formato JSON
    json_data = json.dumps(output, indent=4, ensure_ascii=False)

    with open(out, "w") as Json:
        Json.write(json_data)

def fun2():
    path = "csv/alunos2.csv"
    out = "json/alunos2.json"
    fields = re.compile(r'([^,]+?)(\{(\d+)})?,', re.ASCII)

    parser2(path, fields, out)


def parser3(path, fields, out):
    # Define a expressão regular para extrair os campos do cabeçalho
    regex = fields

    # Define o número padrão de colunas para os campos sem especificação explícita
    default_width = 1

    # Lê o arquivo CSV e extrai os dados
    with open(path, 'r') as file:
        lines = file.readlines()

    # Extrai o cabeçalho e determina o número de colunas para cada campo
    header = lines[0].strip()

    fields = []
    start = 0  # indice da pesquisa
    while True:
        match = regex.search(header, start)
        if match is None:
            break
        name = match.group(1)
        # print(name)
        # Verifica se os grupos 3 e 4 são inteiros (valores mínimo e máximo para o número de colunas)
        if match.group(3) and match.group(4):
            min_width = int(match.group(3))
            max_width = int(match.group(4))
        else:
            min_width = default_width
            max_width = default_width
        fields.append((name, min_width, max_width))
        start = match.end()

    # Calcula o número máximo de colunas
    max_columns = max([max_width for _, _, max_width in fields])

    # Extrai os dados para cada linha do CSV e converte para o formato JSON
    output = []
    for line in lines[1:]:  # exclui o cabeçalho
        data = line.strip().split(',')
        # print(data)
        # Preenche com valores vazios caso o número de colunas seja menor que o máximo
        data += [''] * (max_columns - len(data))
        record = {}  # armazenar os valores de cada campo
        offset = 0  # indice onde a proxima coluna começa
        for name, min_width, max_width in fields:
            # verifica se a diferença entre o comprimento total da linha data e o índice offset (que representa a posição atual do cursor na linha) é maior ou igual ao valor máximo permitido max_width.
            width = max_width if len(data) - offset >= max_width else min_width
            value = data[offset:offset + width]  # se width for igual a 1 é representado como string, caso contrario é uma lista de inteiros
            offset += width
            if width == 1:
                value = value[0]
            else:
                value = [int(x) for x in value if x]
            record[name] = value
        output.append(record)

    # Imprime o resultado em formato JSON
    json_data = json.dumps(output, indent=4, ensure_ascii=False)

    with open(out, "w") as Json:
        Json.write(json_data)

def fun3():
    path = "csv/alunos3.csv"
    out = "json/alunos3.json"
    fields = re.compile(r'([^,]+?)(\{(\d+),(\d+)})?,', re.ASCII)

    parser3(path, fields, out)

def parser4(path, fields, out):
    # Define a expressão regular para extrair os campos do cabeçalho
    regex = fields

    # Define o número padrão de colunas para os campos sem especificação explícita
    default_width = 1

    # Lê o arquivo CSV e extrai os dados
    with open(path, 'r') as file:
        lines = file.readlines()

    # Extrai o cabeçalho e determina o número de colunas para cada campo
    header = lines[0].strip()
    fields = []
    start = 0  # indice da pesquisa
    while True:
        match = regex.search(header, start)
        if match is None:
            break
        name = match.group(1)
        operation = match.group(5) if match.group(5) else None
        min_width = int(match.group(3)) if match.group(2) else default_width
        max_width = int(match.group(4)) if match.group(2) else min_width
        fields.append((name, operation, min_width, max_width))
        start = match.end()

    # Extrai os dados para cada linha do CSV e converte para o formato JSON
    output = []
    for line in lines[1:]:  # exclui o cabeçalho
        data = line.strip().split(',')
        record = {}
        offset = 0
        for name, operation, min_width, max_width in fields:
            if max_width == 1:
                width = min_width
            else:
                width = len(data) - offset if len(data) - offset <= max_width else max_width

            if min_width == 1 and width == 1:
                value = data[offset]
            else:
                values = data[offset:offset + width]
                if max_width == 1:
                    value = values[0] if values else None
                else:
                    value = [int(x) for x in values if x]

            if operation == "sum":
                value_sum = sum(value)
                record[name + "_sum"] = value_sum
            elif operation == "media":
                value_avg = sum(value) / len(value)
                record[name + "_avg"] = value_avg
            else:
                if len(value) == 1:
                    value = value[0]
                record[name] = value

            offset += width
        output.append(record)

    # Imprime o resultado em formato JSON
    json_data = json.dumps(output, indent=4, ensure_ascii=False)

    with open(out, "w") as Json:
        Json.write(json_data)

def fun4():
    path = "csv/alunos4.csv"
    out = "json/alunos4.json"
    fields = re.compile(r'([^,]+?)(\{(\d+)(?:,(\d+))?})?(?:::(sum|media))?(?:,|$)', re.ASCII)

    parser4(path, fields, out)

def fun5():
    path = "csv/alunos5.csv"
    out = "json/alunos5.json"
    fields = re.compile(r'([^,]+?)(\{(\d+)(?:,(\d+))?})?(?:::(sum|media))?(?:,|$)', re.ASCII)

    parser4(path, fields, out)

def main():
    fun1()
    fun2()
    fun3()
    fun4()
    fun5()

if __name__ == "__main__":
    main()
