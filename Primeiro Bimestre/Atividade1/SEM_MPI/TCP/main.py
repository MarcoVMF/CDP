import multiprocessing
from consumidor import main as consumidor
from produtor import main as produtor


if __name__ == "__main__":
    consumidor_process = multiprocessing.Process(target=consumidor, name="Consumidor")

    produtor_process = multiprocessing.Process(target=produtor, name="Produtor")

    consumidor_process.start()
    produtor_process.start()

    consumidor_process.join()