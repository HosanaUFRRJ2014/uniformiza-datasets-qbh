# Uniformização/Unificação dos datasets

Pega os datasets IOACAS e MIR e os "mergeia" em um.

Este algoritmo precede a execução de [lsh](https://github.com/HosanaUFRRJ2014/lsh).


**Importante:** Para o algoritmo funcionar, é preciso ter os três datasets dentro da pasta deste repositório para o código funcionar. Estes não estão disponibizados neste repositório devido a direitos autorais. Dois deles, podem ser recuperados do site [MIREX](https://www.music-ir.org/mirex/wiki/2019:Query_by_Singing/Humming#Data). O terceiro dataset, o dataset de ruído, pode ser encontrado em [The Lakh MIDI Dataset v0.1](https://colinraffel.com/projects/lmd/) (Baixar o dataset LMD-matched). 


## Etapas:
A fim de obter um dataset unificado, executar as etapas abaixo:

1. **Recuperar os datasets originais** [do MIXEX, seção "Data"](https://www.musicir.org/mirex/wiki/2019:Query_by_Singing/Humming#Data).

    Colocá-los na pasta do reposítório. TODO: verificar pequenas modificações manuais feitas nos datasets antes de executar o algoritmo. Houve uniformização manual do nome das pastas.


2. **Executar o arquivo de uniformização/unificação `normalize.py`**

   Este comando gera uma pasta contendo as queries, outra as músicas (pasta songs).
   Gera também os seguintes arquivos:
	- *expected_results.list*  - Contém uma lista que relaciona cada query com o nome (sem extensão) esperado da música dos datasets unificados.
	- *ioacas_query_correlation_file.list*  - Relaciona os nomes das queries do dataset unificado com os do dataset IOACAS.
	- *ioacas_song_correlation_file.list* - Relaciona os nomes das músicas do dataset unificado com os do dataset IOACAS.
	- *midi_songs.list* - Lista das músicas em formato MIDI.
	- *mir_query_correlation_file.list* - Relaciona os nomes das queries do dataset unificado com os do dataset MIR.
	- *mir_song_correlation_file.list* - Relaciona os nomes das músicas do dataset unificado com os do dataset MIR.
  
3. **Transformar as queries do formato MID para WAV.**

   3.1. Instalar, em seu Sistema Operacional, o programa Timidity.
	```
		sudo apt update
		sudo apt install timidity  # funciona no Ubuntu 18.04
	```

   3.2. Executar o arquivo `convert_midi_to_wav.py`
        Este passo é necessário pois as bibliotecas Python de extração de feature não funcionam para arquivos do formato MID.
        Ao menos, no momento da criação deste repositório, não havia biblioteca Python que o fizesse.
        As músicas convertidas ficarão na pasta `songs_wav.`

4. ** Adicionar músicas de ruído na pasta de músicas**

    Para aumentar o dataset e verificar se o algoritmo está funcionando em boa velocidade e acurácia.

	4.1. Criar lista das músicas presentes no dataset de ruído
	```
		grep .*[\.mid]$ -r -l | sort > midi.list

	```