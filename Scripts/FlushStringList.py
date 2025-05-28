
with open('C:\\Users\\Carlos\\Desktop\\Carlos\\Source\\Python\\Scripts\\input.txt') as baseFile:
    lines = baseFile.readlines()

resultList = [] 

for linha in lines:
    if (linha not in resultList) and (linha.find('Added:', 0, 15) or linha.find('Modified:', 0, 15) or linha.find('Rename:', 0, 15) or linha.find('Deleted:', 0, 15)):
        resultList.append(linha)

print(f"Registros originais: {lines.count} Registros processados: {resultList.count}");

resultList.sort()

resultFile = open('C:\\Users\\Carlos\\Desktop\\Carlos\\Source\\Python\\Scripts\\output.txt', 'w')
resultFile.writelines(resultList)
resultFile.close

