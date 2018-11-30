from tornado import web, escape, ioloop, httpclient, gen
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import status
import time

thread_pool = ThreadPoolExecutor()

@gen.coroutine
def async_sleep(seconds):
    yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + seconds)

class AsyncRequestName(web.RequestHandler):
    SUPPORTED_METHODS = ("GET", "POST")
    _thread_pool = thread_pool

    @gen.coroutine
    def get(self):
        name=self.get_argument("name",None)
        print("request recieved")
        # value = yield self.classMethod #to call methods synchronous
        yield async_sleep(5)
        if name:
            self.set_status(status.HTTP_200_OK)
            self.write(name)
            self.finish()
        else:
            response = escape.json_encode({"result":"success"})
            self.set_status(status.HTTP_200_OK)
            self.write(response)
            self.finish()
        print("response send")

    @gen.coroutine
    def post(self):
        details = escape.json_decode(self.request.body)
        print (type(details),details)
        self.write(details)

    # @run_on_executor(executor="_thread_pool")
    # def classMethod(self):
    #     value={1,2,3,4,5}
    #     return value

application=web.Application([
    (r"/request",AsyncRequestName)
], debug=True)

if __name__ == "__main__":
    host="0.0.0.0"
    port = 8880
    print("Listening at port {0}".format(port))
    application.listen(port)
    tornado_ioloop = ioloop.IOLoop.instance()
    # ioloop.PeriodicCallback(lambda: None, 500, tornado_ioloop).start()
    tornado_ioloop.start()