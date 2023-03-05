import re
import json


def fun1(processos):  # função que calcula a frequência de processos por ano (primeiro elemento da data);
    dict = {}
    for p in processos:
        if p.get("Ano") in dict:
            dict[p.get("Ano")] += 1
        else:
            dict[p.get("Ano")] = 1
    print(dict)


def fun2(processos):  # função que calcula a frequência de nomes próprios (o primeiro em cada nome) e apelidos (o último em cada nome) por séculos e apresenta os 5 mais usados;
    dictsec = {}

    for p in processos:
        ano = int(p.get("Ano"))
        sec = (ano - 1) // 100 + 1

        if sec not in dictsec:
            dictsec[sec] = {"Nomes": {}, "Apelidos": {}}

        nome = re.search(r"\w+\b", p.get("Nome")).group()
        pai = re.search(r"\w+\b", p.get("Pai")).group()
        mae = re.search(r"\w+\b", p.get("Mae")).group()
        sobrenome = re.search(r"\b\w+$", p.get("Nome")).group()
        sobrenomeP = re.search(r"\b\w+$", p.get("Pai")).group()
        sobrenomeM = re.search(r"\b\w+$", p.get("Mae")).group()

        dictsec[sec]["Nomes"][nome] = dictsec[sec]["Nomes"].get(nome, 0) + 1
        dictsec[sec]["Nomes"][pai] = dictsec[sec]["Nomes"].get(pai, 0) + 1
        dictsec[sec]["Nomes"][mae] = dictsec[sec]["Nomes"].get(mae, 0) + 1
        dictsec[sec]["Apelidos"][sobrenome] = dictsec[sec]["Apelidos"].get(sobrenome, 0) + 1
        dictsec[sec]["Apelidos"][sobrenomeP] = dictsec[sec]["Apelidos"].get(sobrenomeP, 0) + 1
        dictsec[sec]["Apelidos"][sobrenomeM] = dictsec[sec]["Apelidos"].get(sobrenomeM, 0) + 1

        dictsec[sec]["Nomes"] = dict(sorted(dictsec[sec]["Nomes"].items(), key=lambda x: x[1], reverse=True)[:5])
        dictsec[sec]["Apelidos"] = dict(sorted(dictsec[sec]["Apelidos"].items(), key=lambda x: x[1], reverse=True)[:5])

    print(dictsec)
    return dictsec


def fun3(processos):  # funçao que calcula a frequência dos vários tipos de relação: irmão, sobrinho, etc.;
    dictrel = {"pai": 0, "tio materno": 0, "tio paterno": 0, "irmao": 0, "avo materno": 0, "avo paterno": 0,
               "primo materno": 0, "primo paterno": 0, "sobrinho materno": 0, "sobrinho paterno": 0}

    for p in processos:

        rel = re.findall(
            r'\b(?i:pai|tio materno|tio paterno|irmao|avo materno|avo paterno|primo paterno|primo materno|sobrinho materno|sobrinho paterno)\b',
            p.get("Observacoes"))

        for s in rel:
            if s == "Pai":
                dictrel["pai"] += 1
            if s == "Tio Materno":
                dictrel["tio materno"] += 1
            if s == "Tio Paterno":
                dictrel["tio paterno"] += 1
            if s == "Irmao":
                dictrel["irmao"] += 1
            if s == "Avo Materno":
                dictrel["avo materno"] += 1
            if s == "Avo Paterno":
                dictrel["avo paterno"] += 1
            if s == "Primo Materno":
                dictrel["primo materno"] += 1
            if s == "Primo Paterno":
                dictrel["primo paterno"] += 1
            if s == "Sobrinho Materno":
                dictrel["sobrinho materno"] += 1
            if s == "Sobrinho Paterno":
                dictrel["sobrinho paterno"] += 1

        # print(rel)

    print(dictrel)
    return dictrel


def fun4(processos):  # função que converte os 20 primeiros registos num novo ficheiro de output, mas em formato Json.
    json_object = json.dumps(processos, indent=4)

    # print(json_object)
    with open("pessoas.json", "w") as outfile:
        outfile.write(json_object)


def parser():  # função que faz o parse do ficheiro e coloca os dados numa lista de dicionários
    with open("pessoas.txt") as file1:
        line1 = re.compile(r'Doc.danificado.')
        processos = []
        for lines in file1.readlines():
            if not line1.search(lines):
                line = re.compile(
                    r'(?P<Pasta>\d+)::(?P<Data>(?P<Ano>\d+)-(?P<Mes>\d+)-(?P<Dia>\d+))::(?P<Nome>[\w\s]+)::(?P<Pai>[\w\s]+)::(?P<Mae>[\w\s]+)::(?P<Observacoes>[^:]*)::')
                if line.search(lines):
                    processos.append(line.search(lines).groupdict())

    # print(processos)
    return processos


def main():
    fun1(parser())
    fun2(parser())
    fun3(parser())
    fun4(parser())


if __name__ == "__main__":
    main()
