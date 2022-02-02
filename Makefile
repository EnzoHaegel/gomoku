BIN		=	pbrain-gomoku-ai

MAIN	=	pbrain-gomoku-ai.py


all:		$(BIN)

$(BIN):
			ln -s $(MAIN) $(BIN)
			chmod +x $(BIN)

clean:
			rm -f $(BIN)

fclean:		clean

re:			fclean	all
