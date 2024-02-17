# Por Extenso

Transforma algarismos em texto por extenso, observando as regras gramaticais

# Utilização

```
>>> import por_extenso
>>> por_extenso.numeros(2_980_033)
"dois milhões, novecentos e oitenta mil e trinta e três"
>>> por_extenso.moeda(193_034_001.01, moeda="real")
"R$ 193.034.001,01 (cento e noventa e três milhões, trinta e quatro mil e um reais e um centavo)"
```


## Regras

### Valores em moeda nacional ou estrangeira

Separam-se com vírgula as classes de números (milhar, milhão, bilhão etc.), já os algarismos dentro de cada classe são ligados com a conjunção "e" e, também, com os centavos.

Exemplos em reais:

1. R$ 385,62: trezentos e oitenta e cinco reais e sessenta e dois centavos.
2. R$ 28.385,62: vinte e oito mil, trezentos e oitenta e cinco reais e sessenta e dois centavos.
3. R$ 7.442.928.385,62: sete bilhões, quatrocentos e quarenta e dois milhões, novecentos e vinte e oito mil, trezentos e oitenta e cinco reais e sessenta e dois centavos.
4. R$ 1.000,00: mil reais.
5. R$ 5.000.000,00: cinco milhões de reais.
6. R$ 5.123.450,00: cinco milhões, cento e vinte e três mil, quatrocentos e cinquenta reais.

Exemplos em moeda estrangeira:

1. US$ 2.564.823,38: dois milhões, quinhentos e sessenta e quatro mil, oitocentos e vinte e três dólares americanos e trinta e oito centavos.
2. € 825.236,15: oitocentos e vinte e cinco mil, duzentos e trinta e seis euros e quinze centavos.
3. ¥ 10.815.018: dez milhões, oitocentos e quinze mil e dezoito ienes.
4. US$ 54.000.000,00: cinquenta e quatro milhões de dólares americanos.
5. € 5.022.600,32: cinco milhões, vinte e dois mil e seiscentos euros e trinta e dois centavos.

Entre o milhão e o milhar se o valor é inferior a 101, a separação é feita com a conjunção "e".

Exemplos em reais:

- R$ 2.612.100,00: dois milhões, seiscentos e doze mil e cem reais
- R$ 132.010.098,00: cento e trinta e dois milhões, dez mil e noventa e oito reais

Quando o valor apresenta "zero centavo" (exemplos 4, 5 e 6), os algarismos "00" correspondentes aos centavos não são lidos nem escritos por extenso.

Exemplo:

- Não se diz, vinte reais e zero centavo.

Valores redondos de milhão para cima (exemplos 5 e 10) são grafados com a preposição "de".

Exemplos:

- 5 milhões de reais;
- 42,8 bilhões de dólares.

Quando a centena é redonda ou inicia com zero, utiliza-se a preposição "e".

Exemplos:

- R$ 5.018,00 (cinco mil e dezoito reais);
- R$ 2.600,00 (dois mil e seiscentos reais).

Se a fração da moeda não estiver precedida de um valor inteiro, deve-se mencionar a moeda à qual a fração pertence.

Exemplos:

1) R$ 0,01: um centavo de real.
2) R$ 0,62: sessenta e dois centavos de real.
3) R$ 0,624: seiscentos e vinte e quatro milésimos de real.
4) R$ 8,056: oito reais e cinquenta e seis milésimos.
5) R$ 38,5328: trinta e oito reais e cinco mil, trezentos e vinte e oito décimos de milésimo.
6) R$ 0,03380: três mil, trezentos e oitenta centésimos de milésimo de real.
7) US$ 0,02: dois centavos de dólar americano (2 cents).
8) US$ 9,81452: nove dólares americanos e oitenta e um mil, quatrocentos e cinquenta e dois centésimos de milésimo.
9) € 0,28: vinte e oito centavos de euro (28 euro cents).
10) € 1.459,238562: mil, quatrocentos e cinquenta e nove euros e duzentos e trinta e oito mil, quinhentos e sessenta e dois milionésimos.

### Por extenso

| Caso                         | Exemplo                                                                                                                             |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Números de um a dez          | cinco zebras;<br>dois tamanduás;<br>nove formigas.                                                                                      |
| Números de primeiro a décimo | primeiro lugar;<br>quarta posição;<br>décimo piso.                                                                                  |
| Números cem e mil            | cem cadernos;<br>mil viaturas.                                                                                                      |
| Início das frases            | Quinze passageiros desembarcaram.<br>Vinte e seis visitantes chegaram.<br>Sessenta funcionários despedidos.                         |
| Números fracionários         | dois terços dos eleitores;<br>um quarto da população;<br>um quinto dos alunos.                                                      |
| Transcrição de documentos    | Aos vinte e dois dias do mês de abril de mil e quinhentos;<br>Aos quinze dias do mês de julho de mil novecentos e cinquenta e dois. |

### Com algorismos

| Caso                                                   | Exemplo                                                                                     |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Números a partir de 11                                 | 35 zebras;<br>17 tamanduás;<br>62 formigas.                                                 |
| Números a partir de 11º                                | 53.º lugar;<br>78.º posição;<br>24.º piso.                                                  |
| Números inferiores e superiores a dez na mesma frase   | Compre, 15 maçãs, 8 peras, 12 bananas e 3 melões<br>Na amostra 25 solteiras e 4 viúvas.     |
| Números decimais                                       | 10,3 habitantes por quilômetro quadrado;<br>1,2 celular por pessoa;<br>1,8 filho por casal. |
| Números grandes quebrados                              | 2985 participantes;<br>223 487 eleitores;<br>6598 documentos.                               |
| Horas                                                  | às 8 horas;<br>às 17h30;<br>das 9h às 12h.                                                  |
| Datas                                                  | dia 9;<br>24/11/1980;<br>década de 90.                                                      |
| Idades                                                 | 6 anos;<br>10 anos;<br>8 meses.                                                             |
| Endereços                                              | Rua Santa Clara, 2541<br>Rua do Riachuelo, 164 ap. 404<br>Rua do Pila, 27 3.º andar         |
| Valores monetários                                     | 8 reais;<br>2 centavos;<br>5 dólares.                                                       |
| Porcentagens                                           | 1%<br>5%<br>10%                                                                             |
| Seriação                                               | 4.º Congresso Nacional;<br>8.ª Feira do Livro;<br>2.ª Conferência Financeira.               |
| Sequência                                              | capítulo 6;<br>canal 9;<br>modelo 3.                                                        |
| Temperatura                                            | 8 graus;<br>34 graus;<br>2 graus negativos.                                                 |
| Latitudes e longitudes                                 | 10 graus de latitude;<br>2 graus de longitude.                                              |
| Comprimentos                                           | 1 metro;<br>3 centímetros;<br>6 quilômetros.                                                |
| Pesos                                                  | 5 quilos;<br>7 toneladas;<br>3 quilogramas.                                                 |
| Capacidades                                            | 5 mililitros;<br>8 decilitros;<br>6 litros.                                                 |
| Áreas                                                  | 9 metros quadrados;<br>6 quilômetros quadrados;<br>10 centímetros quadrados.                |
| Volumes                                                | 2 metros cúbicos;<br>3 decímetros cúbicos;<br>8 metros cúbicos.                             |
| Resultados esportivos                                  | ganhou por 3 a 1;<br>venceu por 7 a 4;<br>perdeu por 5 a 2.                                 |
| Resultados de votação                                  | 9 votos a 8;<br>15 votos a 4;<br>10 votos a 2.                                              |

## Mistos

| Caso                                        | Exemplo                                                                                     |
| ------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Números grandes redondos                    | 620 mil;<br>70 milhões;<br>5 bilhões.                                                       |
| Números acima de mil mesmo que não inteiros | 2 mil;<br>1,3 mil;<br>4,6 mil.                                                              |

## Referências

<https://www.normaculta.com.br/escrever-numeros-por-extenso-ou-em-algarismos/>
<https://www.normaculta.com.br/numeros-por-extenso/>
<https://www12.senado.leg.br/manualdecomunicacao/estilos/numeros>
<https://www.professornews.com.br/component/content/article/6872-como-escrever-valor-por-extenso>
<https://museulinguaportuguesa.org.br/numeros-por-extenso/>
