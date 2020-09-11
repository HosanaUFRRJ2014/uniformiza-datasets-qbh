# Uniformização/Unificação dos datasets

Pega os datasets IOACAS e MIR e os "mergeia" em um.

Este algoritmo precede a execução de [lsh](https://github.com/HosanaUFRRJ2014/lsh).


**Importante:** Para o algoritmo funcionar, é preciso ter os dois datasets dentro da pasta deste repositório para o código funcionar. Estes não estão disponibizados neste repositório devido a direitos autorais. Dois deles, podem ser recuperados do site [MIREX](https://www.music-ir.org/mirex/wiki/2019:Query_by_Singing/Humming#Data). Para que possa ocorrer a expansão deste dataset é preciso adicionar um terceiro dataset. Este terceiro dataset, o dataset de ruído, pode ser encontrado em [The Lakh MIDI Dataset v0.1](https://colinraffel.com/projects/lmd/) (Baixar o dataset LMD-matched). 


## Etapas:
A fim de obter um dataset unificado, executar as etapas abaixo:
Para ajuda via comando, consulte `python main.py --help`

1. **Renomear pasta deste repositório para `uniformiza_dataset`**

2. **Recuperar os datasets originais** [do MIXEX, seção "Data"](https://www.musicir.org/mirex/wiki/2019:Query_by_Singing/Humming#Data).

    Colocá-los na pasta do reposítório. TODO: verificar pequenas modificações manuais feitas nos datasets antes de executar o algoritmo. Houve uniformização manual do nome das pastas.


3. **Executar a uniformização/unificação**

		python main.py -norm True -expand False
	
   Este comando gera uma pasta contendo as queries, outra as músicas (pasta songs).
   Gera também os seguintes arquivos:
	- *expected_results.list*  - Contém uma lista que relaciona cada query com o nome (sem extensão) esperado da música dos datasets unificados.
	- *ioacas_query_correlation_file.list*  - Relaciona os nomes das queries do dataset unificado com os do dataset IOACAS.
	- *ioacas_song_correlation_file.list* - Relaciona os nomes das músicas do dataset unificado com os do dataset IOACAS.
	- *midi_songs.list* - Lista das músicas em formato MIDI.
	- *mir_query_correlation_file.list* - Relaciona os nomes das queries do dataset unificado com os do dataset MIR.
	- *mir_song_correlation_file.list* - Relaciona os nomes das músicas do dataset unificado com os do dataset MIR.
  

4. **Adicionar músicas de ruído na pasta de músicas**

    Para aumentar o dataset e verificar se o algoritmo está funcionando em boa velocidade e acurácia.

	3.1. Criar lista das músicas presentes no dataset de ruído
	
		grep .*[\.mid]$ -r -l | sort > midi.list
	

	3.2. Executar comando de expansão do dataset

		python main.py -norm False -expand True


5. **(Opcional) Transformar as queries do formato MID para WAV.**

   5.1. Instalar, em seu Sistema Operacional, o programa Timidity.
	
		sudo apt update
		sudo apt install timidity  # funciona no Ubuntu 18.04
	

   5.2. Executar a conversão

   		
   		python main.py -norm False -expand False -convert $CONVERSION_OPTION
   		
		CONVERSION_OPTION válidos:
			- "only_mirex" - converte apenas os datasets e IOACAS do MIREX.
			- "only_lmd" - converte apenas o datasets vindo do LMD
			- "all" - converte todos os três datasets envolvidos
			- "none" - não converte nenhum dataset (opção padrão)

    As músicas convertidas ficarão na pasta `songs_wav.`
	**NOTA:** As opções que envolvem a conversão do dataset LMD trazem consigo um excessivo consumo de memória de disco. Numa das tentativas de conversão, cerca de 7 mil músicas convertidas ocuparam mais de 200 GB.
