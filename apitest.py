from airpy.server import Server

server = Server()


def main():
    genres = server.get_genres()
    for genre in genres.by_name():
        print(genre)

main()
