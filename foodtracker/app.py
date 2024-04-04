from transcribe import transcribe
from extract import extract

def main():
    corpus = transcribe('random2', 'New Recording')
    print(corpus)
    entities_and_weights = extract(corpus)
    print(entities_and_weights)



if __name__ == "__main__":
    main()