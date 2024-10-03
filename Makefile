
COMPOSE=sudo docker compose

all:
	${COMPOSE} up -d
clean:
	${COMPOSE} stop
fclean:
	${COMPOSE} down
re: fclean all
