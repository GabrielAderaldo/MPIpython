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
        matriz = np.matrix('1,2,3;4,5,6;7,8,9')
        matrizes.append(matriz)
    with open("matrizParaCalcular.pickle","wb") as matrizCalculada:
        picles.dump(matrizes, matrizCalculada)


def carregar_arquivo():
    with open("matrizParaCalcular.pickle", "rb") as matrizCalculada:
        arquivoLido = picles.load(matrizCalculada)

    return arquivoLido

def pegar_Matrix(matriz,numero_ranks):
    matrix = np.array_split(matriz,rank_total)
    return matrix


def soma(dado,dado2):
    valor_somar = int(dado["valor"])
    valor_somar2 = int(dado2)

    return valor_somar + valor_somar2



if __name__ == '__main__':

    arquivoSalvo = True

    if arquivoSalvo:

        com = MPI.COMM_WORLD
        rank = com.Get_rank() #Rank atual...
        rank_total = com.Get_size() #Pegando numero de processos(Ranks total)
        matrizes = carregar_arquivo()
        valor_matrix_total = pegar_Matrix(matrizes, rank_total)
        print(valor_matrix_total)

        if rank == 0:
            print(f"entrou no rank: {rank}")
            valor_matrix_rank = valor_matrix_total[rank]
            if len(valor_matrix_rank) != 1:
                for i in range(len(valor_matrix_rank)-1):
                    multi = np.dot(valor_matrix_rank[i], valor_matrix_rank[i+1])

            else:
                multi = valor_matrix_rank[0]
            arquivo_enviar = {"valor": multi}
            enviador = com.isend(arquivo_enviar,dest=rank+1,tag=rank+1)
            enviador.wait()
        if rank != 0 and rank != rank_total-1:
            print(f"entrou no rank: {rank}")
            recebidor = com.irecv(source=rank-1,tag=rank)
            dado_recebido = recebidor.wait()
            valor_matrix_rank = valor_matrix_total[rank]
            if len(valor_matrix_rank) != 1:
                for i in range(len(valor_matrix_rank)-1):
                    multi = np.dot(valor_matrix_rank[i], valor_matrix_rank[i + 1])
            else:
                multi = valor_matrix_rank[0]
            #Fazer multiplicação de fora
            dado_trabalhado = dado_recebido['valor']
            valor_enviar = np.dot(multi,dado_trabalhado)
            dado_enviado = {"valor":valor_enviar}
            enviador = com.isend(dado_enviado,dest=rank+1,tag=rank+1)
            enviador.wait()

        if rank == rank_total-1:
            valor_matrix_rank = valor_matrix_total[rank]
            print(f"entrou no rank: {rank}")
            recebidor = com.irecv(source=rank - 1,tag=rank)
            dado_recebido = recebidor.wait()
            valor_enviar = dado_recebido['valor']

            if len(valor_matrix_rank) != 1:
                print(range(len(valor_matrix_rank)-1))
                for i in range(len(valor_matrix_rank)-1):
                    multi = np.dot(valor_matrix_rank[i], valor_matrix_rank[i + 1])
            else:
                multi = valor_matrix_rank[0]
            valor_final = np.dot(multi,valor_enviar)
            print(f"Aqui meu valor final: {valor_final}")









    else:
        nMatrizes = int(input("Digite o numero de matrizes: "))
        salvar_arquivo(nMatrizes)
        print(f"Conteudo do arquivo: {carregar_arquivo()}")