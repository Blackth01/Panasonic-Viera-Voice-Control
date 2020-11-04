from app import app

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port='5050', ssl_context=('server.crt', 'server.key'))
    app.run(host='0.0.0.0', port='5050', ssl_context='adhoc')
