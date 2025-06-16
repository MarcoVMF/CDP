from mpi4py import MPI
import consumidor
import produtor

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    #size = comm.Get_size()

    if rank == 0:
        print(f"[Rank {rank}] Sou o PRODUTOR")
        produtor.main()
    else:
        print(f"[Rank {rank}] Sou o CONSUMIDOR")
        consumidor.main()

if __name__ == "__main__":
    main()