from mailbox import MH

from mpi4py import MPI
import numpy as np
import pickle as picles

def isPar(numero):

    resto = numero%2

    if resto == 0:
        return True
    else:
        return False


def salvar_arquivo(numero_de_matrizes):
    print("Entrando na função de escrever um arquivo...")
    matrizes = []

    for _ in range(numero_de_matrizes):
        #matriz = np.random.random((3,3))
        matriz = np.array([1,2,3,4])
        matrizes.append(matriz)
    with open("matrizParaCalcular.pickle","wb") as matrizCalculada:
        picles.dump(matrizes, matrizCalculada)


def carregar_arquivo():
    with open("matrizParaCalcular.pickle", "rb") as matrizCalculada:
        arquivoLido = picles.load(matrizCalculada)

    return arquivoLido



if __name__ == '__main__':

    arquivoSalvo = True

    if arquivoSalvo:

        com = MPI.COMM_WORLD
        rank = com.Get_rank() #Rank atual...
        rank_total = com.Get_size() #Pegando numero de processos(Ranks total)
        matrizes = carregar_arquivo()



        if isPar(rank) == True:

            if rank == 0:   #Verificando se é o primeiro par. pois ele não tem de quem receber...
                matrix_calcular = np.array_split(matrizes,rank_total)
                valor_matriz = []
                if len(matrix_calcular) != 1:

                    valor_matriz = np.dot(matrix_calcular[rank][0],matrix_calcular[rank][1])  #Fazer o calculo interno das matrizes...
                    print(valor_matriz)
                    valor_enviar = {"valor":valor_matriz}

                    req = com.isend(valor_enviar,dest=rank+1,tag=rank+1)
                    req.wait()
                else:
                    if rank_total == 1:
                       valor_enviar = {"valor":matrix_calcular[rank]}

                    else:
                        valor_enviar = {"valor": matrix_calcular[rank]}
                        req = com.isend(valor_enviar, dest=rank+1, tag=rank+1)
                        req.wait()

            else:

                matrix_calcular = np.array_split(matrizes, rank_total)
                valor_matriz = None
                res = com.irecv(source=rank, tag=rank)
                dado_recebido = res.wait()
                if len(matrix_calcular) != 1:
                    matrix_calcular[rank] = np.dot(matrix_calcular[0], matrix_calcular[1])
                matrix_recebida = dado_recebido['valor']
                dado_enviar = np.dot(matrix_calcular, matrix_recebida)
                matriz_enviar = {"valor": dado_enviar}
                req = com.isend(dest=rank + 1, tag=rank + 1)
                req.wait()

        else:
            if rank == rank_total-1:
                matrix_calcular = np.array_split(matrizes,rank_total)
                valor_matriz = None
                res = com.irecv(source=rank,tag=rank)
                dado_recebido = res.wait()
                if len(matrix_calcular) != 1:
                    matrix_calcular[rank] = np.dot(matrix_calcular[0],matrix_calcular[1])

                valor_recebido = dado_recebido['valor']
                valor_matriz = np.dot(matrix_calcular,valor_recebido)
                print(f"A multiplicação final eh: {valor_matriz}")
            else:
                matrix_calcular = np.array_split(matrizes,rank_total)
                valor_matriz = None
                res = com.irecv(source=rank, tag=rank)
                dado_recebido = res.wait()
                if len(matrix_calcular) != 1:
                    matrix_calcular[rank] = np.dot(matrix_calcular[0], matrix_calcular[1])
                matrix_recebida = dado_recebido['valor']
                dado_enviar = np.dot(matrix_calcular,matrix_recebida)
                matriz_enviar = {"valor":dado_enviar}
                req = com.isend(dest= rank+1,tag= rank+1)
                req.wait()



    else:
        nMatrizes = int(input("Digite o numero de matrizes: "))
        salvar_arquivo(nMatrizes)
        print(f"Conteudo do arquivo: {carregar_arquivo()}")