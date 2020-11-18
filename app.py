import src.factory as factory

app = factory.create_app()

if __name__ == "__main__":
    # app.run(ssl_context="adhoc")
    app.run()
