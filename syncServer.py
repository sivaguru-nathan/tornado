from tornado import web, escape, ioloop, httpclient, gen
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import status
import time

class RequestName(web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "POST")

    def get(self):
        name=self.get_argument("name",None)
        print("request recieved")
        time.sleep(5)
        if name:
            self.set_status(status.HTTP_200_OK)
            self.write(name)
        else:
            response = escape.json_encode({"result":"success"})
            self.set_status(status.HTTP_200_OK)
            self.write(response)
        print("response send")

    def post(self):
        details = escape.json_decode(self.request.body)
        print (type(details),details)
        self.write(details)

application=web.Application([
    (r"/request",RequestName)
], debug=True)

if __name__ == "__main__":
    host="0.0.0.0"
    port = 8888
    print("Listening at port {0}".format(port))
    application.listen(port)
    ioloop.IOLoop.instance().start()