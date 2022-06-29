from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os, logging, logging.config
import multiprocessing

from bboxAPI.routes import bboxAPIRouter
from lib import TLKCoreService


app = FastAPI()
logger = None

@app.on_event('startup')
def init_data():
    global logger
    log_dir_path = "api_middleware_log"
    log_file_path = "logging-api-middleware.conf"
    # log_file_path = "logging.conf"
    os.makedirs(log_dir_path, exist_ok=True)
    logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
    # logging.config.fileConfig(log_file_path)
    logger = logging.getLogger("apimiddleware")
    logger.info("logger being initialized successfully")
    app.logger = logger
    
    uvicornAccessLogger = logging.getLogger("uvicorn.access")
    uvicornAccessLogger.addHandler(logger.handlers[0])          # The first one is filehandler
    uvicornErrorLogger = logging.getLogger("uvicorn.error")
    uvicornErrorLogger.addHandler(logger.handlers[0])           # The first one is filehandler

    tlkCoreService = TLKCoreService.TLKCoreService()
    logger.debug(f"tlkCoreService version: v{tlkCoreService.queryTLKCoreVer()}, tlkCoreService.running: {tlkCoreService.running}")
    app.tlkCoreService = tlkCoreService

    # app.testVariable = {"var1": 100, "var2": 200}

    # tlkCoreService = TLKCoreService.TLKCoreService()
    # logger.info(f"tlkCoreService.running: {tlkCoreService.running}")
    # app.tlkCoreService = tlkCoreService

@app.on_event('shutdown')
def on_shutdown(): 
    global logger
    tlkCoreService = app.tlkCoreService
    logger.info("------------------ shutdown event triggered ---------------------")
    if tlkCoreService:
        del tlkCoreService
        logger.info("deleted tlkCoreService instance")

async def catch_exceptions_middleware(request:Request, call_next):
    logger = request.app.logger
    try:
        return await call_next(request)
    except Exception as e:
        # you probably want some kind of logging here
        errMessage = f"Internal server error: {e}"
        logger.error(errMessage)
        return Response(errMessage, status_code=500)

app.middleware('http')(catch_exceptions_middleware)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bboxAPIRouter, prefix="/api/bbox")

if __name__ == '__main__':
    uvicorn.run(app, port=5001, host='0.0.0.0') # 如果用fastapi-mqtt的話，不能寫這行
    # uvicorn.run(app, port=5001, host='0.0.0.0', workers=2) # 如果用fastapi-mqtt的話，不能寫這行
    
    # uvicorn.run("run:app", port=5001, host='0.0.0.0')
    
    # multiprocessing.freeze_support()
    # uvicorn.run("run:app", port=5001, host='0.0.0.0', reload=False, workers=2)  # (X) 在windows上好像會報錯
    # uvicorn.run(app, port=5001, host='0.0.0.0', reload=True)      # (X)
    # uvicorn.run("run:app", port=5001, host='0.0.0.0', reload=True)  # (O)