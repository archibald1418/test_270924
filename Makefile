
COMPOSE=sudo docker compose

all:
	${COMPOSE} up -d
stop:
	${COMPOSE} stop
clean:
	${COMPOSE} down
fclean:
	${COMPOSE} down
buildall:
	${COMPOSE} build 
buildraw:
	${COMPOSE} build --no-cache
re: fclean all
