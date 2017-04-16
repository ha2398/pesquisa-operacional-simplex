all:
	python3 ./fonte/tp1.py ${ENTRADA} ${SAIDA}

.PHONY: clean
clean:
	rm -rf ./fonte/__pycache__
	rm -rf *.txt