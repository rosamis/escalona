all:
	chmod +x escalona

clean:
	rm -rf *.out

doc: $(OBJ) 
	doxygen config.dox