from fastapi import APIRouter, status   #, Response, Request, Depends
# from fastapi.responses import StreamingResponse
from starlette.requests import Request
from starlette.responses import Response
import os, sys, time
import threading
import psutil
from .schemas import serializeDict
# from .models import RFMode
# from lib.TMYPublic import RetCode, RFMode
from lib.TMYPublic import *
from lib.TMYUtils import RetType
# from config import TW_TZ
from tools import helper

HEART_BEAT = False
bboxAPIRouter = APIRouter()

@bboxAPIRouter.post('/general/{apiFuncName}', tags=["BBoxAPI"])
async def general(response:Response, request:Request, apiFuncName:str, payload:dict):
    tlkCoreService = request.app.tlkCoreService
    logger = request.app.logger
    logger.info(f"apiFuncName: {apiFuncName}, payload: {payload}")

    try:
        apiFunc = getattr(tlkCoreService, apiFuncName, None)
        if not apiFunc:
            errMessage = f"API Function {apiFuncName} is not implemented by TLK Core Service"
            logger.info(errMessage)
            response.status_code = status.HTTP_501_NOT_IMPLEMENTED
            return {"message": errMessage}    
        
        # Convert pure int to python Enum class
        enumTypeFields = payload.pop("enumTypeFields", None)
        if enumTypeFields:
            for enumTypeField in enumTypeFields:
                enumTypeString = enumTypeField.get("type", None)
                if enumTypeString:
                    enumType = getattr(sys.modules[__name__], enumTypeString)
                    enumTypeValue = enumTypeField["value"]
                    if isinstance(enumTypeValue, int):
                        enumTypeValue = enumType(enumTypeValue)
                    else:
                        enumTypeValue = enumType[enumTypeValue]
                    
                    fieldName = enumTypeField["field"]
                    payload[fieldName] = enumTypeValue
                    
        # For test purpose
        start_time = time.perf_counter()
        result = apiFunc(**payload)
        logger.info(f"apiFuncName: {apiFuncName}, response: {result}, took {round((time.perf_counter() - start_time), 3)} secs")
    except Exception as e:
        logger.error(f"Error occurred during calling '{apiFuncName}' API: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": str(e)}
    
    if type(result) is RetType:
        # result = {**result.__dict__, "codeName": result.RetCode.name}
        pass
    else:
        # result = {"RetCode": 0, "codeName": "OK", "RetMsg": "", "RetData": result}
        result = {"RetCode": 0, "name": "OK", "RetMsg": "", "RetData": result}

    request.app.tlkCoreService = tlkCoreService
    return {"message": "success", "payload": result}

@bboxAPIRouter.post('/shutdown', tags=["BBoxAPI"])
async def shutdown(response:Response, request:Request):
    tlkCoreService = request.app.tlkCoreService
    logger = request.app.logger
    logger.info(f"Received /shutdown API request")
    try:
        if tlkCoreService:
            del tlkCoreService
            logger.info("deleted tlkCoreService successfully")
    except Exception as e:
        logger.error(f"Error occurred during calling 'setRFMode' API: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": str(e)}
    
    return {"message": "success", "payload": None}

# @bboxAPIRouter.post('/setRFMode', tags=["BBoxAPI"])
# async def setRFMode(response:Response, request:Request, payload:dict):
#     tlkCoreService = request.app.tlkCoreService
#     logger = request.app.logger
#     logger.info(f"apiFuncName: setRFMode, payload: {payload}")
#     try:
#         mode = RFMode.TX
#         if payload["rfMode"] == 2:
#             mode = RFMode.RX
#         logger.info(f"setRFMode: {mode}")
#         result = tlkCoreService.setRFMode(payload["sn"], mode)
#         logger.info(f"apiFuncName: setRFMode response: {result}")

#         # # test
#         # getRFMode = getattr(tlkCoreService, "getRFMode", None)
#         # logger.info(f"getRFMode: {getRFMode('D2144E020-28')}")
#     except Exception as e:
#         logger.error(f"Error occurred during calling 'setRFMode' API: {e}")
#         response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
#         return {"message": str(e)}
    
#     request.app.tlkCoreService = tlkCoreService
#     return {"message": "success", "payload": result}

@bboxAPIRouter.get("/")
@bboxAPIRouter.get("/home")
def home():
    # strFilePath: D:\Leamon\project\TLK_cross_platform_middleware\FastAPI\src\bboxAPI
    # strFilePath = os.path.dirname(os.path.abspath(__file__))
    # print("strFilePath:", strFilePath)

    # D:\Leamon\project\TLK_cross_platform_middleware\FastAPI\src
    # strFilePath = os.path.dirname(sys.modules['__main__'].__file__)
    # print("strFilePath:", strFilePath)
    
    return "I'm still alive"

@bboxAPIRouter.get("/check_heart_beat")
def check_heart_beat():
    global HEART_BEAT
    HEART_BEAT = True
    return {"message": "success"}

def self_terminate():
    global HEART_BEAT
    if not HEART_BEAT:
        pid = os.getpid()
        ppid = psutil.Process(pid).ppid()
        print("os.getpid(): ", pid)
        print("ppid: ", ppid)
        time.sleep(1)
        
        itself = psutil.Process(pid)
        itself.kill()
        print("process being kill")

        # parent = psutil.Process(ppid)
        # for child in parent.children(recursive=True):  # or parent.children() for recursive=False
        #     child.kill()
        #     print("child process being kill")
        # parent.kill()
        # print("parent process being kill")
        
    else:
        print("API Middleware Still Alive")
        HEART_BEAT = False

@bboxAPIRouter.get("/kill")
async def kill():
    threading.Thread(target=self_terminate, daemon=True).start()
    return {"success": True}

@bboxAPIRouter.on_event("startup")
async def startup():
    print("bboxAPIRouter startup event...")

    heartbeatHandler = helper.MyInterval(self_terminate, 300, threading.Event())
    heartbeatHandler.start()

# @bboxAPIRouter.get("/getPid")
# async def getPid():
#     pid = os.getpid()
#     print("os.getpid(): ", pid)
#     return {"pid": pid}

# @bboxAPIRouter.get("/test_var1")
# def test_var1(response:Response, request:Request):
#     testVariable = request.app.testVariable
#     print("before: ", testVariable)
#     testVariable.update({"var1": testVariable["var1"] + 1})
#     print("after: ", testVariable)
#     return testVariable

# @bboxAPIRouter.get("/test_var2")
# def test_var2(response:Response, request:Request):
#     testVariable = request.app.testVariable
#     print("before: ", testVariable)
#     testVariable.update({"var2": testVariable["var2"] + 1})
#     print("after: ", testVariable)
#     return testVariable