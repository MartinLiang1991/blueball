import ctypes
import json
import time
import sys

from typing import Tuple, List, Callable, Union

# Python 3.12+ 支持 override，否则从 typing_extensions 导入
if sys.version_info >= (3, 12):
    from typing import override
else:
    try:
        from typing_extensions import override
    except ImportError:
        # 如果 typing_extensions 也不存在，定义一个空的装饰器
        def override(func):
            return func

from olaplug.OLAPlugDLLHelper import OLAPlugDLLHelper


class OLAPlugServer:

    def __init__(self):
        self.OLAObject = None
        self.UserCode = "5858956b17f147edb69fcb5b9faafdaf"
        self.SoftCode = "94ae74c79aed44d08de1d0c95ee07a68"
        self.FeatureList = "OLA|OLAPlus"
        self.CreateCOLAPlugInterFace()
        # 设置默认编码为UTF-8
        self.SetConfigByKey("DefaultEncoding", "1")

    def PtrToStringUTF8(self, ptr) -> str:
        """
        根据指针返回字符串
        :param ptr: 指针地址
        :return: 对应的字符串
        """
        if ptr==0:
            return ""

        try:
            str_ptr = ctypes.cast(ptr, ctypes.c_char_p)
            byte_str = str_ptr.value
            text = byte_str.decode("utf-8") if byte_str else ""
        except Exception as e:
            print(e)
        finally:
            OLAPlugDLLHelper.FreeStringPtr(ptr)

        return text

    def CreateCOLAPlugInterFace(self) -> int:
        if not self.OLAObject:
            self.OLAObject = OLAPlugDLLHelper.CreateCOLAPlugInterFace()
        return self.OLAObject

    def ReleaseObj(self) -> int:
        if self.OLAObject is None:
            return 1
        result = OLAPlugDLLHelper.DestroyCOLAPlugInterFace(self.OLAObject)
        self.OLAObject = None
        return result

    def SetConfig(self, configStr: Union[str, dict]) -> int:
        if not isinstance(configStr, str):
            configStr = json.dumps(configStr)
        return OLAPlugDLLHelper.SetConfig(self.OLAObject, configStr)

    def DestroyCOLAPlugInterFace(self) -> int:
        return OLAPlugDLLHelper.DestroyCOLAPlugInterFace(self.OLAObject)

    def Ver(self) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.Ver())

    def SetPath(self, path: str) -> int:
        return OLAPlugDLLHelper.SetPath(self.OLAObject, path)

    def GetPath(self) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetPath(self.OLAObject))

    def GetMachineCode(self) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetMachineCode(self.OLAObject))

    def GetBasePath(self) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetBasePath(self.OLAObject))

    def Reg(self, userCode: str, softCode: str, featureList: str) -> int:
        return OLAPlugDLLHelper.Reg(userCode, softCode, featureList)

    def BindWindow(self, hwnd: int, display: str, mouse: str, keypad: str, mode: int) -> int:
        return OLAPlugDLLHelper.BindWindow(self.OLAObject, hwnd, display, mouse, keypad, mode)

    def BindWindowEx(self, hwnd: int, display: str, mouse: str, keypad: str, pubstr: str, mode: int) -> int:
        return OLAPlugDLLHelper.BindWindowEx(self.OLAObject, hwnd, display, mouse, keypad, pubstr, mode)

    def UnBindWindow(self) -> int:
        return OLAPlugDLLHelper.UnBindWindow(self.OLAObject)

    def GetBindWindow(self) -> int:
        return OLAPlugDLLHelper.GetBindWindow(self.OLAObject)

    def ReleaseWindowsDll(self, hwnd: int) -> int:
        return OLAPlugDLLHelper.ReleaseWindowsDll(self.OLAObject, hwnd)

    def FreeStringPtr(self, ptr: int) -> int:
        return OLAPlugDLLHelper.FreeStringPtr(ptr)

    def FreeMemoryPtr(self, ptr: int) -> int:
        return OLAPlugDLLHelper.FreeMemoryPtr(ptr)

    def GetStringSize(self, ptr: int) -> int:
        return OLAPlugDLLHelper.GetStringSize(ptr)

    def GetStringFromPtr(self, ptr: int, lpString: str, size: int) -> int:
        return OLAPlugDLLHelper.GetStringFromPtr(ptr, lpString, size)

    def Delay(self, millisecond: int) -> int:
        return OLAPlugDLLHelper.Delay(millisecond)

    def Delays(self, minMillisecond: int, maxMillisecond: int) -> int:
        return OLAPlugDLLHelper.Delays(minMillisecond, maxMillisecond)

    def SetUAC(self, enable: int) -> int:
        return OLAPlugDLLHelper.SetUAC(self.OLAObject, enable)

    def CheckUAC(self) -> int:
        return OLAPlugDLLHelper.CheckUAC(self.OLAObject)

    def RunApp(self, appPath: str, mode: int) -> int:
        return OLAPlugDLLHelper.RunApp(self.OLAObject, appPath, mode)

    def ExecuteCmd(self, cmd: str, current_dir: str, time_out: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.ExecuteCmd(self.OLAObject, cmd, current_dir, time_out))

    def GetConfig(self, configKey: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetConfig(self.OLAObject, configKey))

    def SetConfigByKey(self, key: str, value: str) -> int:
        return OLAPlugDLLHelper.SetConfigByKey(self.OLAObject, key, value)

    def SendDropFiles(self, hwnd: int, file_path: str) -> int:
        return OLAPlugDLLHelper.SendDropFiles(self.OLAObject, hwnd, file_path)

    def GetRandomNumber(self, _min: int, _max: int) -> int:
        return OLAPlugDLLHelper.GetRandomNumber(self.OLAObject, _min, _max)

    def GetRandomDouble(self, _min: float, _max: float) -> float:
        return OLAPlugDLLHelper.GetRandomDouble(self.OLAObject, _min, _max)

    def ExcludePos(self, _json: str, _type: int, x1: int, y1: int, x2: int, y2: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.ExcludePos(self.OLAObject, _json, _type, x1, y1, x2, y2))

    def FindNearestPos(self, _json: str, _type: int, x: int, y: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindNearestPos(self.OLAObject, _json, _type, x, y))

    def SortPosDistance(self, _json: str, _type: int, x: int, y: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.SortPosDistance(self.OLAObject, _json, _type, x, y))

    def GetDenseRect(self, image: int, width: int, height: int, x1: int = None, y1: int = None, x2: int = None, y2: int = None) -> Tuple[int, int, int, int, int]:
        return OLAPlugDLLHelper.GetDenseRect(self.OLAObject, image, width, height, x1, y1, x2, y2)

    def PathPlanning(self, image: int, startX: int, startY: int, endX: int, endY: int, potentialRadius: float, searchRadius: float) -> List[dict]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.PathPlanning(self.OLAObject, image, startX, startY, endX, endY, potentialRadius, searchRadius))
        if result == "":
            return []
        return json.loads(result)

    def CreateGraph(self, _json: str) -> int:
        return OLAPlugDLLHelper.CreateGraph(self.OLAObject, _json)

    def GetGraph(self, graphPtr: int) -> int:
        return OLAPlugDLLHelper.GetGraph(self.OLAObject, graphPtr)

    def AddEdge(self, graphPtr: int, _from: str, to: str, weight: float, isDirected: bool) -> int:
        return OLAPlugDLLHelper.AddEdge(self.OLAObject, graphPtr, _from, to, weight, isDirected)

    def GetShortestPath(self, graphPtr: int, _from: str, to: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetShortestPath(self.OLAObject, graphPtr, _from, to))

    def GetShortestDistance(self, graphPtr: int, _from: str, to: str) -> float:
        return OLAPlugDLLHelper.GetShortestDistance(self.OLAObject, graphPtr, _from, to)

    def ClearGraph(self, graphPtr: int) -> int:
        return OLAPlugDLLHelper.ClearGraph(self.OLAObject, graphPtr)

    def DeleteGraph(self, graphPtr: int) -> int:
        return OLAPlugDLLHelper.DeleteGraph(self.OLAObject, graphPtr)

    def GetNodeCount(self, graphPtr: int) -> int:
        return OLAPlugDLLHelper.GetNodeCount(self.OLAObject, graphPtr)

    def GetEdgeCount(self, graphPtr: int) -> int:
        return OLAPlugDLLHelper.GetEdgeCount(self.OLAObject, graphPtr)

    def GetShortestPathToAllNodes(self, graphPtr: int, startNode: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetShortestPathToAllNodes(self.OLAObject, graphPtr, startNode))

    def GetMinimumSpanningTree(self, graphPtr: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetMinimumSpanningTree(self.OLAObject, graphPtr))

    def GetDirectedPathToAllNodes(self, graphPtr: int, startNode: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetDirectedPathToAllNodes(self.OLAObject, graphPtr, startNode))

    def GetMinimumArborescence(self, graphPtr: int, root: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetMinimumArborescence(self.OLAObject, graphPtr, root))

    def CreateGraphFromCoordinates(self, _json: str, connectAll: bool, maxDistance: float, useEuclideanDistance: bool) -> int:
        return OLAPlugDLLHelper.CreateGraphFromCoordinates(self.OLAObject, _json, connectAll, maxDistance, useEuclideanDistance)

    def AddCoordinateNode(self, graphPtr: int, name: str, x: float, y: float, connectToExisting: bool, maxDistance: float, useEuclideanDistance: bool) -> int:
        return OLAPlugDLLHelper.AddCoordinateNode(self.OLAObject, graphPtr, name, x, y, connectToExisting, maxDistance, useEuclideanDistance)

    def GetNodeCoordinates(self, graphPtr: int, name: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetNodeCoordinates(self.OLAObject, graphPtr, name))

    def SetNodeConnection(self, graphPtr: int, _from: str, to: str, canConnect: bool, weight: float) -> int:
        return OLAPlugDLLHelper.SetNodeConnection(self.OLAObject, graphPtr, _from, to, canConnect, weight)

    def GetNodeConnectionStatus(self, graphPtr: int, _from: str, to: str) -> int:
        return OLAPlugDLLHelper.GetNodeConnectionStatus(self.OLAObject, graphPtr, _from, to)

    def AsmCall(self, hwnd: int, asmStr: str, _type: int, baseAddr: int) -> int:
        return OLAPlugDLLHelper.AsmCall(self.OLAObject, hwnd, asmStr, _type, baseAddr)

    def Assemble(self, asmStr: str, baseAddr: int, arch: int, mode: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.Assemble(self.OLAObject, asmStr, baseAddr, arch, mode))

    def Disassemble(self, asmCode: str, baseAddr: int, arch: int, mode: int, showType: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.Disassemble(self.OLAObject, asmCode, baseAddr, arch, mode, showType))

    def DrawGuiCleanup(self) -> int:
        return OLAPlugDLLHelper.DrawGuiCleanup(self.OLAObject)

    def DrawGuiSetGuiActive(self, active: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetGuiActive(self.OLAObject, active)

    def DrawGuiIsGuiActive(self) -> int:
        return OLAPlugDLLHelper.DrawGuiIsGuiActive(self.OLAObject)

    def DrawGuiSetGuiClickThrough(self, enabled: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetGuiClickThrough(self.OLAObject, enabled)

    def DrawGuiIsGuiClickThrough(self) -> int:
        return OLAPlugDLLHelper.DrawGuiIsGuiClickThrough(self.OLAObject)

    def DrawGuiRectangle(self, x: int, y: int, width: int, height: int, mode: int, lineThickness: float) -> int:
        return OLAPlugDLLHelper.DrawGuiRectangle(self.OLAObject, x, y, width, height, mode, lineThickness)

    def DrawGuiCircle(self, x: int, y: int, radius: int, mode: int, lineThickness: float) -> int:
        return OLAPlugDLLHelper.DrawGuiCircle(self.OLAObject, x, y, radius, mode, lineThickness)

    def DrawGuiLine(self, x1: int, y1: int, x2: int, y2: int, lineThickness: float) -> int:
        return OLAPlugDLLHelper.DrawGuiLine(self.OLAObject, x1, y1, x2, y2, lineThickness)

    def DrawGuiText(self, text: str, x: int, y: int, fontPath: str, fontSize: int, align: int) -> int:
        return OLAPlugDLLHelper.DrawGuiText(self.OLAObject, text, x, y, fontPath, fontSize, align)

    def DrawGuiImage(self, imagePath: str, x: int, y: int) -> int:
        return OLAPlugDLLHelper.DrawGuiImage(self.OLAObject, imagePath, x, y)

    def DrawGuiWindow(self, title: str, x: int, y: int, width: int, height: int, style: int) -> int:
        return OLAPlugDLLHelper.DrawGuiWindow(self.OLAObject, title, x, y, width, height, style)

    def DrawGuiPanel(self, parentHandle: int, x: int, y: int, width: int, height: int) -> int:
        return OLAPlugDLLHelper.DrawGuiPanel(self.OLAObject, parentHandle, x, y, width, height)

    def DrawGuiButton(self, parentHandle: int, text: str, x: int, y: int, width: int, height: int) -> int:
        return OLAPlugDLLHelper.DrawGuiButton(self.OLAObject, parentHandle, text, x, y, width, height)

    def DrawGuiSetPosition(self, handle: int, x: int, y: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetPosition(self.OLAObject, handle, x, y)

    def DrawGuiSetSize(self, handle: int, width: int, height: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetSize(self.OLAObject, handle, width, height)

    def DrawGuiSetColor(self, handle: int, r: int, g: int, b: int, a: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetColor(self.OLAObject, handle, r, g, b, a)

    def DrawGuiSetAlpha(self, handle: int, alpha: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetAlpha(self.OLAObject, handle, alpha)

    def DrawGuiSetDrawMode(self, handle: int, mode: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetDrawMode(self.OLAObject, handle, mode)

    def DrawGuiSetLineThickness(self, handle: int, thickness: float) -> int:
        return OLAPlugDLLHelper.DrawGuiSetLineThickness(self.OLAObject, handle, thickness)

    def DrawGuiSetFont(self, handle: int, fontPath: str, fontSize: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetFont(self.OLAObject, handle, fontPath, fontSize)

    def DrawGuiSetTextAlign(self, handle: int, align: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetTextAlign(self.OLAObject, handle, align)

    def DrawGuiSetText(self, handle: int, text: str) -> int:
        return OLAPlugDLLHelper.DrawGuiSetText(self.OLAObject, handle, text)

    def DrawGuiSetWindowTitle(self, handle: int, title: str) -> int:
        return OLAPlugDLLHelper.DrawGuiSetWindowTitle(self.OLAObject, handle, title)

    def DrawGuiSetWindowStyle(self, handle: int, style: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetWindowStyle(self.OLAObject, handle, style)

    def DrawGuiSetWindowTopMost(self, handle: int, topMost: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetWindowTopMost(self.OLAObject, handle, topMost)

    def DrawGuiSetWindowTransparency(self, handle: int, alpha: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetWindowTransparency(self.OLAObject, handle, alpha)

    def DrawGuiDeleteObject(self, handle: int) -> int:
        return OLAPlugDLLHelper.DrawGuiDeleteObject(self.OLAObject, handle)

    def DrawGuiClearAll(self) -> int:
        return OLAPlugDLLHelper.DrawGuiClearAll(self.OLAObject)

    def DrawGuiSetVisible(self, handle: int, visible: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetVisible(self.OLAObject, handle, visible)

    def DrawGuiSetZOrder(self, handle: int, zOrder: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetZOrder(self.OLAObject, handle, zOrder)

    def DrawGuiSetParent(self, handle: int, parentHandle: int) -> int:
        return OLAPlugDLLHelper.DrawGuiSetParent(self.OLAObject, handle, parentHandle)

    def DrawGuiSetButtonCallback(self, handle: int, callback: Callable[[int], None]) -> int:
        return OLAPlugDLLHelper.DrawGuiSetButtonCallback(self.OLAObject, handle, callback)

    def DrawGuiSetMouseCallback(self, handle: int, callback: Callable[[int, int, int, int], None]) -> int:
        return OLAPlugDLLHelper.DrawGuiSetMouseCallback(self.OLAObject, handle, callback)

    def DrawGuiGetDrawObjectType(self, handle: int) -> int:
        return OLAPlugDLLHelper.DrawGuiGetDrawObjectType(self.OLAObject, handle)

    def DrawGuiGetPosition(self, handle: int, x: int = None, y: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.DrawGuiGetPosition(self.OLAObject, handle, x, y)

    def DrawGuiGetSize(self, handle: int, width: int = None, height: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.DrawGuiGetSize(self.OLAObject, handle, width, height)

    def DrawGuiIsPointInObject(self, handle: int, x: int, y: int) -> int:
        return OLAPlugDLLHelper.DrawGuiIsPointInObject(self.OLAObject, handle, x, y)

    def SetMemoryMode(self, mode: int) -> int:
        return OLAPlugDLLHelper.SetMemoryMode(self.OLAObject, mode)

    def ExportDriver(self, driver_path: str, _type: int) -> int:
        return OLAPlugDLLHelper.ExportDriver(self.OLAObject, driver_path, _type)

    def LoadDriver(self, driver_name: str, driver_path: str) -> int:
        return OLAPlugDLLHelper.LoadDriver(self.OLAObject, driver_name, driver_path)

    def UnloadDriver(self, driver_name: str) -> int:
        return OLAPlugDLLHelper.UnloadDriver(self.OLAObject, driver_name)

    def DriverTest(self) -> int:
        return OLAPlugDLLHelper.DriverTest(self.OLAObject)

    def LoadPdb(self) -> int:
        return OLAPlugDLLHelper.LoadPdb(self.OLAObject)

    def HideProcess(self, pid: int, enable: int) -> int:
        return OLAPlugDLLHelper.HideProcess(self.OLAObject, pid, enable)

    def ProtectProcess(self, pid: int, enable: int) -> int:
        return OLAPlugDLLHelper.ProtectProcess(self.OLAObject, pid, enable)

    def AddProtectPID(self, pid: int, mode: int, allow_pid: int) -> int:
        return OLAPlugDLLHelper.AddProtectPID(self.OLAObject, pid, mode, allow_pid)

    def RemoveProtectPID(self, pid: int) -> int:
        return OLAPlugDLLHelper.RemoveProtectPID(self.OLAObject, pid)

    def AddAllowPID(self, pid: int) -> int:
        return OLAPlugDLLHelper.AddAllowPID(self.OLAObject, pid)

    def RemoveAllowPID(self, pid: int) -> int:
        return OLAPlugDLLHelper.RemoveAllowPID(self.OLAObject, pid)

    def InjectDll(self, pid: int, dll_path: str, mode: int) -> int:
        return OLAPlugDLLHelper.InjectDll(self.OLAObject, pid, dll_path, mode)

    def FakeProcess(self, pid: int, fake_pid: int) -> int:
        return OLAPlugDLLHelper.FakeProcess(self.OLAObject, pid, fake_pid)

    def StartHotkeyHook(self) -> int:
        return OLAPlugDLLHelper.StartHotkeyHook(self.OLAObject)

    def StopHotkeyHook(self) -> int:
        return OLAPlugDLLHelper.StopHotkeyHook(self.OLAObject)

    def RegisterHotkey(self, keycode: int, modifiers: int, callback: Callable[[int, int], None]) -> int:
        return OLAPlugDLLHelper.RegisterHotkey(self.OLAObject, keycode, modifiers, callback)

    def UnregisterHotkey(self, keycode: int, modifiers: int) -> int:
        return OLAPlugDLLHelper.UnregisterHotkey(self.OLAObject, keycode, modifiers)

    def RegisterMouseButton(self, button: int, _type: int, callback: Callable[[int, int, int, int], None]) -> int:
        return OLAPlugDLLHelper.RegisterMouseButton(self.OLAObject, button, _type, callback)

    def UnregisterMouseButton(self, button: int, _type: int) -> int:
        return OLAPlugDLLHelper.UnregisterMouseButton(self.OLAObject, button, _type)

    def RegisterMouseWheel(self, callback: Callable[[int, int, int, int], None]) -> int:
        return OLAPlugDLLHelper.RegisterMouseWheel(self.OLAObject, callback)

    def UnregisterMouseWheel(self) -> int:
        return OLAPlugDLLHelper.UnregisterMouseWheel(self.OLAObject)

    def RegisterMouseMove(self, callback: Callable[[int, int], None]) -> int:
        return OLAPlugDLLHelper.RegisterMouseMove(self.OLAObject, callback)

    def UnregisterMouseMove(self) -> int:
        return OLAPlugDLLHelper.UnregisterMouseMove(self.OLAObject)

    def RegisterMouseDrag(self, callback: Callable[[int, int], None]) -> int:
        return OLAPlugDLLHelper.RegisterMouseDrag(self.OLAObject, callback)

    def UnregisterMouseDrag(self) -> int:
        return OLAPlugDLLHelper.UnregisterMouseDrag(self.OLAObject)

    def JsonCreateObject(self) -> int:
        return OLAPlugDLLHelper.JsonCreateObject()

    def JsonCreateArray(self) -> int:
        return OLAPlugDLLHelper.JsonCreateArray()

    def JsonParse(self, _str: str, err: int = None) -> Tuple[int, int]:
        return OLAPlugDLLHelper.JsonParse(_str, err)

    def JsonStringify(self, obj: int, indent: int, err: int = None) -> Tuple[str, int]:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.JsonStringify(obj, indent, err))

    def JsonFree(self, obj: int) -> int:
        return OLAPlugDLLHelper.JsonFree(obj)

    def JsonGetValue(self, obj: int, key: str, err: int = None) -> Tuple[int, int]:
        return OLAPlugDLLHelper.JsonGetValue(obj, key, err)

    def JsonGetArrayItem(self, arr: int, index: int, err: int = None) -> Tuple[int, int]:
        return OLAPlugDLLHelper.JsonGetArrayItem(arr, index, err)

    def JsonGetString(self, obj: int, key: str, err: int = None) -> Tuple[str, int]:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.JsonGetString(obj, key, err))

    def JsonGetNumber(self, obj: int, key: str, err: int = None) -> Tuple[float, int]:
        return OLAPlugDLLHelper.JsonGetNumber(obj, key, err)

    def JsonGetBool(self, obj: int, key: str, err: int = None) -> Tuple[int, int]:
        return OLAPlugDLLHelper.JsonGetBool(obj, key, err)

    def JsonGetSize(self, obj: int, err: int = None) -> Tuple[int, int]:
        return OLAPlugDLLHelper.JsonGetSize(obj, err)

    def JsonSetValue(self, obj: int, key: str, value: int) -> int:
        return OLAPlugDLLHelper.JsonSetValue(obj, key, value)

    def JsonArrayAppend(self, arr: int, value: int) -> int:
        return OLAPlugDLLHelper.JsonArrayAppend(arr, value)

    def JsonSetString(self, obj: int, key: str, value: str) -> int:
        return OLAPlugDLLHelper.JsonSetString(obj, key, value)

    def JsonSetNumber(self, obj: int, key: str, value: float) -> int:
        return OLAPlugDLLHelper.JsonSetNumber(obj, key, value)

    def JsonSetBool(self, obj: int, key: str, value: int) -> int:
        return OLAPlugDLLHelper.JsonSetBool(obj, key, value)

    def JsonDeleteKey(self, obj: int, key: str) -> int:
        return OLAPlugDLLHelper.JsonDeleteKey(obj, key)

    def JsonClear(self, obj: int) -> int:
        return OLAPlugDLLHelper.JsonClear(obj)

    def GenerateMouseTrajectory(self, startX: int, startY: int, endX: int, endY: int) -> List[dict]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.GenerateMouseTrajectory(self.OLAObject, startX, startY, endX, endY))
        if result == "":
            return []
        return json.loads(result)

    def KeyDown(self, vk_code: int) -> int:
        return OLAPlugDLLHelper.KeyDown(self.OLAObject, vk_code)

    def KeyUp(self, vk_code: int) -> int:
        return OLAPlugDLLHelper.KeyUp(self.OLAObject, vk_code)

    def KeyPress(self, vk_code: int) -> int:
        return OLAPlugDLLHelper.KeyPress(self.OLAObject, vk_code)

    def LeftDown(self) -> int:
        return OLAPlugDLLHelper.LeftDown(self.OLAObject)

    def LeftUp(self) -> int:
        return OLAPlugDLLHelper.LeftUp(self.OLAObject)

    def MoveTo(self, x: int, y: int) -> int:
        return OLAPlugDLLHelper.MoveTo(self.OLAObject, x, y)

    def MoveToWithoutSimulator(self, x: int, y: int) -> int:
        return OLAPlugDLLHelper.MoveToWithoutSimulator(self.OLAObject, x, y)

    def RightClick(self) -> int:
        return OLAPlugDLLHelper.RightClick(self.OLAObject)

    def RightDown(self) -> int:
        return OLAPlugDLLHelper.RightDown(self.OLAObject)

    def RightUp(self) -> int:
        return OLAPlugDLLHelper.RightUp(self.OLAObject)

    def GetCursorShape(self) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetCursorShape(self.OLAObject))

    def GetCursorImage(self) -> int:
        return OLAPlugDLLHelper.GetCursorImage(self.OLAObject)

    def KeyPressStr(self, keyStr: str, delay: int) -> int:
        return OLAPlugDLLHelper.KeyPressStr(self.OLAObject, keyStr, delay)

    def SendString(self, hwnd: int, _str: str) -> int:
        return OLAPlugDLLHelper.SendString(self.OLAObject, hwnd, _str)

    def SendStringEx(self, hwnd: int, addr: int, _len: int, _type: int) -> int:
        return OLAPlugDLLHelper.SendStringEx(self.OLAObject, hwnd, addr, _len, _type)

    def KeyPressChar(self, keyStr: str) -> int:
        return OLAPlugDLLHelper.KeyPressChar(self.OLAObject, keyStr)

    def KeyDownChar(self, keyStr: str) -> int:
        return OLAPlugDLLHelper.KeyDownChar(self.OLAObject, keyStr)

    def KeyUpChar(self, keyStr: str) -> int:
        return OLAPlugDLLHelper.KeyUpChar(self.OLAObject, keyStr)

    def MoveR(self, rx: int, ry: int) -> int:
        return OLAPlugDLLHelper.MoveR(self.OLAObject, rx, ry)

    def MiddleClick(self) -> int:
        return OLAPlugDLLHelper.MiddleClick(self.OLAObject)

    def MoveToEx(self, x: int, y: int, w: int, h: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.MoveToEx(self.OLAObject, x, y, w, h))

    def GetCursorPos(self, x: int = None, y: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.GetCursorPos(self.OLAObject, x, y)

    def MiddleUp(self) -> int:
        return OLAPlugDLLHelper.MiddleUp(self.OLAObject)

    def MiddleDown(self) -> int:
        return OLAPlugDLLHelper.MiddleDown(self.OLAObject)

    def LeftClick(self) -> int:
        return OLAPlugDLLHelper.LeftClick(self.OLAObject)

    def LeftDoubleClick(self) -> int:
        return OLAPlugDLLHelper.LeftDoubleClick(self.OLAObject)

    def WheelUp(self) -> int:
        return OLAPlugDLLHelper.WheelUp(self.OLAObject)

    def WheelDown(self) -> int:
        return OLAPlugDLLHelper.WheelDown(self.OLAObject)

    def WaitKey(self, vk_code: int, time_out: int) -> int:
        return OLAPlugDLLHelper.WaitKey(self.OLAObject, vk_code, time_out)

    def EnableMouseAccuracy(self, enable: int) -> int:
        return OLAPlugDLLHelper.EnableMouseAccuracy(self.OLAObject, enable)

    def DoubleToData(self, double_value: float) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.DoubleToData(self.OLAObject, double_value))

    def FloatToData(self, float_value: float) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FloatToData(self.OLAObject, float_value))

    def StringToData(self, string_value: str, _type: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.StringToData(self.OLAObject, string_value, _type))

    def Int64ToInt32(self, v: int) -> int:
        return OLAPlugDLLHelper.Int64ToInt32(self.OLAObject, v)

    def Int32ToInt64(self, v: int) -> int:
        return OLAPlugDLLHelper.Int32ToInt64(self.OLAObject, v)

    def FindData(self, hwnd: int, addr_range: str, data: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindData(self.OLAObject, hwnd, addr_range, data))

    def FindDataEx(self, hwnd: int, addr_range: str, data: str, step: int, multi_thread: int, mode: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindDataEx(self.OLAObject, hwnd, addr_range, data, step, multi_thread, mode))

    def FindDouble(self, hwnd: int, addr_range: str, double_value_min: float, double_value_max: float) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindDouble(self.OLAObject, hwnd, addr_range, double_value_min, double_value_max))

    def FindDoubleEx(self, hwnd: int, addr_range: str, double_value_min: float, double_value_max: float, step: int, multi_thread: int, mode: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindDoubleEx(self.OLAObject, hwnd, addr_range, double_value_min, double_value_max, step, multi_thread, mode))

    def FindFloat(self, hwnd: int, addr_range: str, float_value_min: float, float_value_max: float) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindFloat(self.OLAObject, hwnd, addr_range, float_value_min, float_value_max))

    def FindFloatEx(self, hwnd: int, addr_range: str, float_value_min: float, float_value_max: float, step: int, multi_thread: int, mode: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindFloatEx(self.OLAObject, hwnd, addr_range, float_value_min, float_value_max, step, multi_thread, mode))

    def FindInt(self, hwnd: int, addr_range: str, int_value_min: int, int_value_max: int, _type: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindInt(self.OLAObject, hwnd, addr_range, int_value_min, int_value_max, _type))

    def FindIntEx(self, hwnd: int, addr_range: str, int_value_min: int, int_value_max: int, _type: int, step: int, multi_thread: int, mode: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindIntEx(self.OLAObject, hwnd, addr_range, int_value_min, int_value_max, _type, step, multi_thread, mode))

    def FindString(self, hwnd: int, addr_range: str, string_value: str, _type: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindString(self.OLAObject, hwnd, addr_range, string_value, _type))

    def FindStringEx(self, hwnd: int, addr_range: str, string_value: str, _type: int, step: int, multi_thread: int, mode: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.FindStringEx(self.OLAObject, hwnd, addr_range, string_value, _type, step, multi_thread, mode))

    def ReadData(self, hwnd: int, addr: str, _len: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.ReadData(self.OLAObject, hwnd, addr, _len))

    def ReadDataAddr(self, hwnd: int, addr: int, _len: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.ReadDataAddr(self.OLAObject, hwnd, addr, _len))

    def ReadDataAddrToBin(self, hwnd: int, addr: int, _len: int) -> int:
        return OLAPlugDLLHelper.ReadDataAddrToBin(self.OLAObject, hwnd, addr, _len)

    def ReadDataToBin(self, hwnd: int, addr: str, _len: int) -> int:
        return OLAPlugDLLHelper.ReadDataToBin(self.OLAObject, hwnd, addr, _len)

    def ReadDouble(self, hwnd: int, addr: str) -> float:
        return OLAPlugDLLHelper.ReadDouble(self.OLAObject, hwnd, addr)

    def ReadDoubleAddr(self, hwnd: int, addr: int) -> float:
        return OLAPlugDLLHelper.ReadDoubleAddr(self.OLAObject, hwnd, addr)

    def ReadFloat(self, hwnd: int, addr: str) -> float:
        return OLAPlugDLLHelper.ReadFloat(self.OLAObject, hwnd, addr)

    def ReadFloatAddr(self, hwnd: int, addr: int) -> float:
        return OLAPlugDLLHelper.ReadFloatAddr(self.OLAObject, hwnd, addr)

    def ReadInt(self, hwnd: int, addr: str, _type: int) -> int:
        return OLAPlugDLLHelper.ReadInt(self.OLAObject, hwnd, addr, _type)

    def ReadIntAddr(self, hwnd: int, addr: int, _type: int) -> int:
        return OLAPlugDLLHelper.ReadIntAddr(self.OLAObject, hwnd, addr, _type)

    def ReadString(self, hwnd: int, addr: str, _type: int, _len: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.ReadString(self.OLAObject, hwnd, addr, _type, _len))

    def ReadStringAddr(self, hwnd: int, addr: int, _type: int, _len: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.ReadStringAddr(self.OLAObject, hwnd, addr, _type, _len))

    def WriteData(self, hwnd: int, addr: str, data: str) -> int:
        return OLAPlugDLLHelper.WriteData(self.OLAObject, hwnd, addr, data)

    def WriteDataFromBin(self, hwnd: int, addr: str, data: int, _len: int) -> int:
        return OLAPlugDLLHelper.WriteDataFromBin(self.OLAObject, hwnd, addr, data, _len)

    def WriteDataAddr(self, hwnd: int, addr: int, data: str) -> int:
        return OLAPlugDLLHelper.WriteDataAddr(self.OLAObject, hwnd, addr, data)

    def WriteDataAddrFromBin(self, hwnd: int, addr: int, data: int, _len: int) -> int:
        return OLAPlugDLLHelper.WriteDataAddrFromBin(self.OLAObject, hwnd, addr, data, _len)

    def WriteDouble(self, hwnd: int, addr: str, double_value: float) -> int:
        return OLAPlugDLLHelper.WriteDouble(self.OLAObject, hwnd, addr, double_value)

    def WriteDoubleAddr(self, hwnd: int, addr: int, double_value: float) -> int:
        return OLAPlugDLLHelper.WriteDoubleAddr(self.OLAObject, hwnd, addr, double_value)

    def WriteFloat(self, hwnd: int, addr: str, float_value: float) -> int:
        return OLAPlugDLLHelper.WriteFloat(self.OLAObject, hwnd, addr, float_value)

    def WriteFloatAddr(self, hwnd: int, addr: int, float_value: float) -> int:
        return OLAPlugDLLHelper.WriteFloatAddr(self.OLAObject, hwnd, addr, float_value)

    def WriteInt(self, hwnd: int, addr: str, _type: int, value: int) -> int:
        return OLAPlugDLLHelper.WriteInt(self.OLAObject, hwnd, addr, _type, value)

    def WriteIntAddr(self, hwnd: int, addr: int, _type: int, value: int) -> int:
        return OLAPlugDLLHelper.WriteIntAddr(self.OLAObject, hwnd, addr, _type, value)

    def WriteString(self, hwnd: int, addr: str, _type: int, value: str) -> int:
        return OLAPlugDLLHelper.WriteString(self.OLAObject, hwnd, addr, _type, value)

    def WriteStringAddr(self, hwnd: int, addr: int, _type: int, value: str) -> int:
        return OLAPlugDLLHelper.WriteStringAddr(self.OLAObject, hwnd, addr, _type, value)

    def SetMemoryHwndAsProcessId(self, enable: int) -> int:
        return OLAPlugDLLHelper.SetMemoryHwndAsProcessId(self.OLAObject, enable)

    def FreeProcessMemory(self, hwnd: int) -> int:
        return OLAPlugDLLHelper.FreeProcessMemory(self.OLAObject, hwnd)

    def GetModuleBaseAddr(self, hwnd: int, module_name: str) -> int:
        return OLAPlugDLLHelper.GetModuleBaseAddr(self.OLAObject, hwnd, module_name)

    def GetModuleSize(self, hwnd: int, module_name: str) -> int:
        return OLAPlugDLLHelper.GetModuleSize(self.OLAObject, hwnd, module_name)

    def GetRemoteApiAddress(self, hwnd: int, base_addr: int, fun_name: str) -> int:
        return OLAPlugDLLHelper.GetRemoteApiAddress(self.OLAObject, hwnd, base_addr, fun_name)

    def VirtualAllocEx(self, hwnd: int, addr: int, size: int, _type: int) -> int:
        return OLAPlugDLLHelper.VirtualAllocEx(self.OLAObject, hwnd, addr, size, _type)

    def VirtualFreeEx(self, hwnd: int, addr: int) -> int:
        return OLAPlugDLLHelper.VirtualFreeEx(self.OLAObject, hwnd, addr)

    def VirtualProtectEx(self, hwnd: int, addr: int, size: int, _type: int, protect: int) -> int:
        return OLAPlugDLLHelper.VirtualProtectEx(self.OLAObject, hwnd, addr, size, _type, protect)

    def VirtualQueryEx(self, hwnd: int, addr: int, pmbi: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.VirtualQueryEx(self.OLAObject, hwnd, addr, pmbi))

    def CreateRemoteThread(self, hwnd: int, lpStartAddress: int, lpParameter: int, dwCreationFlags: int, lpThreadId: int = None) -> Tuple[int, int]:
        return OLAPlugDLLHelper.CreateRemoteThread(self.OLAObject, hwnd, lpStartAddress, lpParameter, dwCreationFlags, lpThreadId)

    def CloseHandle(self, handle: int) -> int:
        return OLAPlugDLLHelper.CloseHandle(self.OLAObject, handle)

    def Ocr(self, x1: int, y1: int, x2: int, y2: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.Ocr(self.OLAObject, x1, y1, x2, y2))

    def OcrFromPtr(self, ptr: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.OcrFromPtr(self.OLAObject, ptr))

    def OcrFromBmpData(self, ptr: int, size: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.OcrFromBmpData(self.OLAObject, ptr, size))

    def OcrDetails(self, x1: int, y1: int, x2: int, y2: int) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.OcrDetails(self.OLAObject, x1, y1, x2, y2))
        if result == "":
            return {}
        return json.loads(result)

    def OcrFromPtrDetails(self, ptr: int) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.OcrFromPtrDetails(self.OLAObject, ptr))
        if result == "":
            return {}
        return json.loads(result)

    def OcrFromBmpDataDetails(self, ptr: int, size: int) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.OcrFromBmpDataDetails(self.OLAObject, ptr, size))
        if result == "":
            return {}
        return json.loads(result)

    def OcrV5(self, x1: int, y1: int, x2: int, y2: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.OcrV5(self.OLAObject, x1, y1, x2, y2))

    def OcrV5Details(self, x1: int, y1: int, x2: int, y2: int) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.OcrV5Details(self.OLAObject, x1, y1, x2, y2))
        if result == "":
            return {}
        return json.loads(result)

    def OcrV5FromPtr(self, ptr: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.OcrV5FromPtr(self.OLAObject, ptr))

    def OcrV5FromPtrDetails(self, ptr: int) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.OcrV5FromPtrDetails(self.OLAObject, ptr))
        if result == "":
            return {}
        return json.loads(result)

    def GetOcrConfig(self, configKey: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetOcrConfig(self.OLAObject, configKey))

    def SetOcrConfig(self, configStr: str) -> int:
        return OLAPlugDLLHelper.SetOcrConfig(self.OLAObject, configStr)

    def SetOcrConfigByKey(self, key: str, value: str) -> int:
        return OLAPlugDLLHelper.SetOcrConfigByKey(self.OLAObject, key, value)

    def OcrFromDict(self, x1: int, y1: int, x2: int, y2: int, colorJson: Union[str, List[dict]], dict_name: str, matchVal: float) -> str:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        return self.PtrToStringUTF8(OLAPlugDLLHelper.OcrFromDict(self.OLAObject, x1, y1, x2, y2, colorJson, dict_name, matchVal))

    def OcrFromDictDetails(self, x1: int, y1: int, x2: int, y2: int, colorJson: Union[str, List[dict]], dict_name: str, matchVal: float) -> dict:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.OcrFromDictDetails(self.OLAObject, x1, y1, x2, y2, colorJson, dict_name, matchVal))
        if result == "":
            return {}
        return json.loads(result)

    def OcrFromDictPtr(self, ptr: int, colorJson: Union[str, List[dict]], dict_name: str, matchVal: float) -> str:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        return self.PtrToStringUTF8(OLAPlugDLLHelper.OcrFromDictPtr(self.OLAObject, ptr, colorJson, dict_name, matchVal))

    def OcrFromDictPtrDetails(self, ptr: int, colorJson: Union[str, List[dict]], dict_name: str, matchVal: float) -> dict:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.OcrFromDictPtrDetails(self.OLAObject, ptr, colorJson, dict_name, matchVal))
        if result == "":
            return {}
        return json.loads(result)

    def FindStr(self, x1: int, y1: int, x2: int, y2: int, _str: str, colorJson: Union[str, List[dict]], _dict: str, matchVal: float, outX: int = None, outY: int = None) -> Tuple[int, int, int]:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        return OLAPlugDLLHelper.FindStr(self.OLAObject, x1, y1, x2, y2, _str, colorJson, _dict, matchVal, outX, outY)

    def FindStrDetail(self, x1: int, y1: int, x2: int, y2: int, _str: str, colorJson: Union[str, List[dict]], _dict: str, matchVal: float) -> dict:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FindStrDetail(self.OLAObject, x1, y1, x2, y2, _str, colorJson, _dict, matchVal))
        if result == "":
            return {}
        return json.loads(result)

    def FindStrAll(self, x1: int, y1: int, x2: int, y2: int, _str: str, colorJson: Union[str, List[dict]], _dict: str, matchVal: float) -> List[dict]:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FindStrAll(self.OLAObject, x1, y1, x2, y2, _str, colorJson, _dict, matchVal))
        if result == "":
            return []
        return json.loads(result)

    def FindStrFromPtr(self, source: int, _str: str, colorJson: Union[str, List[dict]], _dict: str, matchVal: float) -> dict:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FindStrFromPtr(self.OLAObject, source, _str, colorJson, _dict, matchVal))
        if result == "":
            return {}
        return json.loads(result)

    def FindStrFromPtrAll(self, source: int, _str: str, colorJson: Union[str, List[dict]], _dict: str, matchVal: float) -> List[dict]:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FindStrFromPtrAll(self.OLAObject, source, _str, colorJson, _dict, matchVal))
        if result == "":
            return []
        return json.loads(result)

    def FastNumberOcrFromPtr(self, source: int, numbers: str, colorJson: Union[str, List[dict]], matchVal: float) -> int:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        return OLAPlugDLLHelper.FastNumberOcrFromPtr(self.OLAObject, source, numbers, colorJson, matchVal)

    def FastNumberOcr(self, x1: int, y1: int, x2: int, y2: int, numbers: str, colorJson: Union[str, List[dict]], matchVal: float) -> int:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        return OLAPlugDLLHelper.FastNumberOcr(self.OLAObject, x1, y1, x2, y2, numbers, colorJson, matchVal)

    def Capture(self, x1: int, y1: int, x2: int, y2: int, file: str) -> int:
        return OLAPlugDLLHelper.Capture(self.OLAObject, x1, y1, x2, y2, file)

    def GetScreenDataBmp(self, x1: int, y1: int, x2: int, y2: int, data: int = None, dataLen: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.GetScreenDataBmp(self.OLAObject, x1, y1, x2, y2, data, dataLen)

    def GetScreenData(self, x1: int, y1: int, x2: int, y2: int, data: int = None, dataLen: int = None, stride: int = None) -> Tuple[int, int, int, int]:
        return OLAPlugDLLHelper.GetScreenData(self.OLAObject, x1, y1, x2, y2, data, dataLen, stride)

    def GetScreenDataPtr(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return OLAPlugDLLHelper.GetScreenDataPtr(self.OLAObject, x1, y1, x2, y2)

    def CaptureGif(self, x1: int, y1: int, x2: int, y2: int, file: str, delay: int, time: int) -> int:
        return OLAPlugDLLHelper.CaptureGif(self.OLAObject, x1, y1, x2, y2, file, delay, time)

    def GetImageData(self, imgPtr: int, data: int = None, size: int = None, stride: int = None) -> Tuple[int, int, int, int]:
        return OLAPlugDLLHelper.GetImageData(self.OLAObject, imgPtr, data, size, stride)

    def MatchImageFromPath(self, source: str, templ: str, matchVal: float, _type: int, angle: float, scale: float) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchImageFromPath(self.OLAObject, source, templ, matchVal, _type, angle, scale))
        if result == "":
            return {}
        return json.loads(result)

    def MatchImageFromPathAll(self, source: str, templ: str, matchVal: float, _type: int, angle: float, scale: float) -> List[dict]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchImageFromPathAll(self.OLAObject, source, templ, matchVal, _type, angle, scale))
        if result == "":
            return []
        return json.loads(result)

    def MatchImagePtrFromPath(self, source: int, templ: str, matchVal: float, _type: int, angle: float, scale: float) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchImagePtrFromPath(self.OLAObject, source, templ, matchVal, _type, angle, scale))
        if result == "":
            return {}
        return json.loads(result)

    def MatchImagePtrFromPathAll(self, source: int, templ: str, matchVal: float, _type: int, angle: float, scale: float) -> List[dict]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchImagePtrFromPathAll(self.OLAObject, source, templ, matchVal, _type, angle, scale))
        if result == "":
            return []
        return json.loads(result)

    def GetColor(self, x: int, y: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetColor(self.OLAObject, x, y))

    def GetColorPtr(self, source: int, x: int, y: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetColorPtr(self.OLAObject, source, x, y))

    def CopyImage(self, sourcePtr: int) -> int:
        return OLAPlugDLLHelper.CopyImage(self.OLAObject, sourcePtr)

    def FreeImagePath(self, path: str) -> int:
        return OLAPlugDLLHelper.FreeImagePath(self.OLAObject, path)

    def FreeImageAll(self) -> int:
        return OLAPlugDLLHelper.FreeImageAll(self.OLAObject)

    def LoadImage(self, path: str) -> int:
        return OLAPlugDLLHelper.LoadImage(self.OLAObject, path)

    def LoadImageFromBmpData(self, data: int, dataSize: int) -> int:
        return OLAPlugDLLHelper.LoadImageFromBmpData(self.OLAObject, data, dataSize)

    def LoadImageFromRGBData(self, width: int, height: int, scan0: int, stride: int) -> int:
        return OLAPlugDLLHelper.LoadImageFromRGBData(self.OLAObject, width, height, scan0, stride)

    def FreeImagePtr(self, screenPtr: int) -> int:
        return OLAPlugDLLHelper.FreeImagePtr(self.OLAObject, screenPtr)

    def MatchWindowsFromPtr(self, x1: int, y1: int, x2: int, y2: int, templ: int, matchVal: float, _type: int, angle: float, scale: float) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchWindowsFromPtr(self.OLAObject, x1, y1, x2, y2, templ, matchVal, _type, angle, scale))
        if result == "":
            return {}
        return json.loads(result)

    def MatchImageFromPtr(self, source: int, templ: int, matchVal: float, _type: int, angle: float, scale: float) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchImageFromPtr(self.OLAObject, source, templ, matchVal, _type, angle, scale))
        if result == "":
            return {}
        return json.loads(result)

    def MatchImageFromPtrAll(self, source: int, templ: int, matchVal: float, _type: int, angle: float, scale: float) -> List[dict]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchImageFromPtrAll(self.OLAObject, source, templ, matchVal, _type, angle, scale))
        if result == "":
            return []
        return json.loads(result)

    def MatchWindowsFromPtrAll(self, x1: int, y1: int, x2: int, y2: int, templ: int, matchVal: float, _type: int, angle: float, scale: float) -> List[dict]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchWindowsFromPtrAll(self.OLAObject, x1, y1, x2, y2, templ, matchVal, _type, angle, scale))
        if result == "":
            return []
        return json.loads(result)

    def MatchWindowsFromPath(self, x1: int, y1: int, x2: int, y2: int, templ: str, matchVal: float, _type: int, angle: float, scale: float) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchWindowsFromPath(self.OLAObject, x1, y1, x2, y2, templ, matchVal, _type, angle, scale))
        if result == "":
            return {}
        return json.loads(result)

    def MatchWindowsFromPathAll(self, x1: int, y1: int, x2: int, y2: int, templ: str, matchVal: float, _type: int, angle: float, scale: float) -> List[dict]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchWindowsFromPathAll(self.OLAObject, x1, y1, x2, y2, templ, matchVal, _type, angle, scale))
        if result == "":
            return []
        return json.loads(result)

    def MatchWindowsThresholdFromPtr(self, x1: int, y1: int, x2: int, y2: int, colorJson: Union[str, List[dict]], templ: int, matchVal: float, angle: float, scale: float) -> dict:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchWindowsThresholdFromPtr(self.OLAObject, x1, y1, x2, y2, colorJson, templ, matchVal, angle, scale))
        if result == "":
            return {}
        return json.loads(result)

    def MatchWindowsThresholdFromPtrAll(self, x1: int, y1: int, x2: int, y2: int, colorJson: Union[str, List[dict]], templ: int, matchVal: float, angle: float, scale: float) -> List[dict]:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchWindowsThresholdFromPtrAll(self.OLAObject, x1, y1, x2, y2, colorJson, templ, matchVal, angle, scale))
        if result == "":
            return []
        return json.loads(result)

    def MatchWindowsThresholdFromPath(self, x1: int, y1: int, x2: int, y2: int, colorJson: Union[str, List[dict]], templ: str, matchVal: float, angle: float, scale: float) -> dict:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchWindowsThresholdFromPath(self.OLAObject, x1, y1, x2, y2, colorJson, templ, matchVal, angle, scale))
        if result == "":
            return {}
        return json.loads(result)

    def MatchWindowsThresholdFromPathAll(self, x1: int, y1: int, x2: int, y2: int, colorJson: Union[str, List[dict]], templ: str, matchVal: float, angle: float, scale: float) -> List[dict]:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchWindowsThresholdFromPathAll(self.OLAObject, x1, y1, x2, y2, colorJson, templ, matchVal, angle, scale))
        if result == "":
            return []
        return json.loads(result)

    def ShowMatchWindow(self, flag: int) -> int:
        return OLAPlugDLLHelper.ShowMatchWindow(self.OLAObject, flag)

    def CalculateSSIM(self, image1: int, image2: int) -> float:
        return OLAPlugDLLHelper.CalculateSSIM(self.OLAObject, image1, image2)

    def CalculateHistograms(self, image1: int, image2: int) -> float:
        return OLAPlugDLLHelper.CalculateHistograms(self.OLAObject, image1, image2)

    def CalculateMSE(self, image1: int, image2: int) -> float:
        return OLAPlugDLLHelper.CalculateMSE(self.OLAObject, image1, image2)

    def SaveImageFromPtr(self, ptr: int, path: str) -> int:
        return OLAPlugDLLHelper.SaveImageFromPtr(self.OLAObject, ptr, path)

    def ReSize(self, ptr: int, width: int, height: int) -> int:
        return OLAPlugDLLHelper.ReSize(self.OLAObject, ptr, width, height)

    def FindColor(self, x1: int, y1: int, x2: int, y2: int, color1: str, color2: str, _dir: int, x: int = None, y: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.FindColor(self.OLAObject, x1, y1, x2, y2, color1, color2, _dir, x, y)

    def FindColorList(self, x1: int, y1: int, x2: int, y2: int, color1: str, color2: str) -> List[dict]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FindColorList(self.OLAObject, x1, y1, x2, y2, color1, color2))
        if result == "":
            return []
        return json.loads(result)

    def FindMultiColor(self, x1: int, y1: int, x2: int, y2: int, colorJson: Union[str, List[dict]], pointJson: Union[str, List[dict]], _dir: int, x: int = None, y: int = None) -> Tuple[int, int, int]:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        if not isinstance(pointJson, str):
            pointJson = json.dumps(pointJson)
        return OLAPlugDLLHelper.FindMultiColor(self.OLAObject, x1, y1, x2, y2, colorJson, pointJson, _dir, x, y)

    def FindMultiColorList(self, x1: int, y1: int, x2: int, y2: int, colorJson: Union[str, List[dict]], pointJson: Union[str, List[dict]]) -> List[dict]:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        if not isinstance(pointJson, str):
            pointJson = json.dumps(pointJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FindMultiColorList(self.OLAObject, x1, y1, x2, y2, colorJson, pointJson))
        if result == "":
            return []
        return json.loads(result)

    def FindMultiColorFromPtr(self, ptr: int, colorJson: Union[str, List[dict]], pointJson: Union[str, List[dict]], _dir: int, x: int = None, y: int = None) -> Tuple[int, int, int]:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        if not isinstance(pointJson, str):
            pointJson = json.dumps(pointJson)
        return OLAPlugDLLHelper.FindMultiColorFromPtr(self.OLAObject, ptr, colorJson, pointJson, _dir, x, y)

    def FindMultiColorListFromPtr(self, ptr: int, colorJson: Union[str, List[dict]], pointJson: Union[str, List[dict]]) -> List[dict]:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        if not isinstance(pointJson, str):
            pointJson = json.dumps(pointJson)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FindMultiColorListFromPtr(self.OLAObject, ptr, colorJson, pointJson))
        if result == "":
            return []
        return json.loads(result)

    def GetImageSize(self, ptr: int, width: int = None, height: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.GetImageSize(self.OLAObject, ptr, width, height)

    def FindColorBlock(self, x1: int, y1: int, x2: int, y2: int, colorList: Union[str, List[dict]], count: int, width: int, height: int, x: int = None, y: int = None) -> Tuple[int, int, int]:
        if not isinstance(colorList, str):
            colorList = json.dumps(colorList)
        return OLAPlugDLLHelper.FindColorBlock(self.OLAObject, x1, y1, x2, y2, colorList, count, width, height, x, y)

    def FindColorBlockPtr(self, ptr: int, colorList: Union[str, List[dict]], count: int, width: int, height: int, x: int = None, y: int = None) -> Tuple[int, int, int]:
        if not isinstance(colorList, str):
            colorList = json.dumps(colorList)
        return OLAPlugDLLHelper.FindColorBlockPtr(self.OLAObject, ptr, colorList, count, width, height, x, y)

    def FindColorBlockList(self, x1: int, y1: int, x2: int, y2: int, colorList: Union[str, List[dict]], count: int, width: int, height: int, _type: int) -> List[dict]:
        if not isinstance(colorList, str):
            colorList = json.dumps(colorList)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FindColorBlockList(self.OLAObject, x1, y1, x2, y2, colorList, count, width, height, _type))
        if result == "":
            return []
        return json.loads(result)

    def FindColorBlockListPtr(self, ptr: int, colorList: Union[str, List[dict]], count: int, width: int, height: int, _type: int) -> List[dict]:
        if not isinstance(colorList, str):
            colorList = json.dumps(colorList)
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FindColorBlockListPtr(self.OLAObject, ptr, colorList, count, width, height, _type))
        if result == "":
            return []
        return json.loads(result)

    def GetColorNum(self, x1: int, y1: int, x2: int, y2: int, colorList: Union[str, List[dict]]) -> int:
        if not isinstance(colorList, str):
            colorList = json.dumps(colorList)
        return OLAPlugDLLHelper.GetColorNum(self.OLAObject, x1, y1, x2, y2, colorList)

    def GetColorNumPtr(self, ptr: int, colorList: Union[str, List[dict]]) -> int:
        if not isinstance(colorList, str):
            colorList = json.dumps(colorList)
        return OLAPlugDLLHelper.GetColorNumPtr(self.OLAObject, ptr, colorList)

    def Cropped(self, image: int, x1: int, y1: int, x2: int, y2: int) -> int:
        return OLAPlugDLLHelper.Cropped(self.OLAObject, image, x1, y1, x2, y2)

    def GetThresholdImageFromMultiColorPtr(self, ptr: int, colorJson: Union[str, List[dict]]) -> int:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        return OLAPlugDLLHelper.GetThresholdImageFromMultiColorPtr(self.OLAObject, ptr, colorJson)

    def GetThresholdImageFromMultiColor(self, x1: int, y1: int, x2: int, y2: int, colorJson: Union[str, List[dict]]) -> int:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        return OLAPlugDLLHelper.GetThresholdImageFromMultiColor(self.OLAObject, x1, y1, x2, y2, colorJson)

    def IsSameImage(self, ptr: int, ptr2: int) -> int:
        return OLAPlugDLLHelper.IsSameImage(self.OLAObject, ptr, ptr2)

    def ShowImage(self, ptr: int) -> int:
        return OLAPlugDLLHelper.ShowImage(self.OLAObject, ptr)

    def ShowImageFromFile(self, file: str) -> int:
        return OLAPlugDLLHelper.ShowImageFromFile(self.OLAObject, file)

    def SetColorsToNewColor(self, ptr: int, colorJson: Union[str, List[dict]], color: str) -> int:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        return OLAPlugDLLHelper.SetColorsToNewColor(self.OLAObject, ptr, colorJson, color)

    def RemoveOtherColors(self, ptr: int, colorJson: Union[str, List[dict]]) -> int:
        if not isinstance(colorJson, str):
            colorJson = json.dumps(colorJson)
        return OLAPlugDLLHelper.RemoveOtherColors(self.OLAObject, ptr, colorJson)

    def DrawRectangle(self, ptr: int, x1: int, y1: int, x2: int, y2: int, thickness: int, color: str) -> int:
        return OLAPlugDLLHelper.DrawRectangle(self.OLAObject, ptr, x1, y1, x2, y2, thickness, color)

    def DrawCircle(self, ptr: int, x: int, y: int, radius: int, thickness: int, color: str) -> int:
        return OLAPlugDLLHelper.DrawCircle(self.OLAObject, ptr, x, y, radius, thickness, color)

    def DrawFillPoly(self, ptr: int, pointJson: Union[str, List[dict]], color: str) -> int:
        if not isinstance(pointJson, str):
            pointJson = json.dumps(pointJson)
        return OLAPlugDLLHelper.DrawFillPoly(self.OLAObject, ptr, pointJson, color)

    def DecodeQRCode(self, ptr: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.DecodeQRCode(self.OLAObject, ptr))

    def CreateQRCode(self, _str: str, pixelsPerModule: int) -> int:
        return OLAPlugDLLHelper.CreateQRCode(self.OLAObject, _str, pixelsPerModule)

    def CreateQRCodeEx(self, _str: str, pixelsPerModule: int, version: int, correction_level: int, mode: int, structure_number: int) -> int:
        return OLAPlugDLLHelper.CreateQRCodeEx(self.OLAObject, _str, pixelsPerModule, version, correction_level, mode, structure_number)

    def MatchAnimationFromPtr(self, x1: int, y1: int, x2: int, y2: int, templ: int, matchVal: float, _type: int, angle: float, scale: float, delay: int, time: int, threadCount: int) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchAnimationFromPtr(self.OLAObject, x1, y1, x2, y2, templ, matchVal, _type, angle, scale, delay, time, threadCount))
        if result == "":
            return {}
        return json.loads(result)

    def MatchAnimationFromPath(self, x1: int, y1: int, x2: int, y2: int, templ: str, matchVal: float, _type: int, angle: float, scale: float, delay: int, time: int, threadCount: int) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.MatchAnimationFromPath(self.OLAObject, x1, y1, x2, y2, templ, matchVal, _type, angle, scale, delay, time, threadCount))
        if result == "":
            return {}
        return json.loads(result)

    def RemoveImageDiff(self, image1: int, image2: int) -> int:
        return OLAPlugDLLHelper.RemoveImageDiff(self.OLAObject, image1, image2)

    def GetImageBmpData(self, imgPtr: int, data: int = None, size: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.GetImageBmpData(self.OLAObject, imgPtr, data, size)

    def FreeImageData(self, screenPtr: int) -> int:
        return OLAPlugDLLHelper.FreeImageData(self.OLAObject, screenPtr)

    def ScalePixels(self, ptr: int, pixelsPerModule: int) -> int:
        return OLAPlugDLLHelper.ScalePixels(self.OLAObject, ptr, pixelsPerModule)

    def CreateImage(self, width: int, height: int, color: str) -> int:
        return OLAPlugDLLHelper.CreateImage(self.OLAObject, width, height, color)

    def SetPixel(self, image: int, x: int, y: int, color: str) -> int:
        return OLAPlugDLLHelper.SetPixel(self.OLAObject, image, x, y, color)

    def SetPixelList(self, image: int, points: Union[str, List[dict]], color: str) -> int:
        if not isinstance(points, str):
            points = json.dumps(points)
        return OLAPlugDLLHelper.SetPixelList(self.OLAObject, image, points, color)

    def ConcatImage(self, image1: int, image2: int, gap: int, color: str, _dir: int) -> int:
        return OLAPlugDLLHelper.ConcatImage(self.OLAObject, image1, image2, gap, color, _dir)

    def CoverImage(self, image1: int, image2: int, x: int, y: int, alpha: float) -> int:
        return OLAPlugDLLHelper.CoverImage(self.OLAObject, image1, image2, x, y, alpha)

    def RotateImage(self, image: int, angle: float) -> int:
        return OLAPlugDLLHelper.RotateImage(self.OLAObject, image, angle)

    def ImageToBase64(self, image: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.ImageToBase64(self.OLAObject, image))

    def Base64ToImage(self, base64: str) -> int:
        return OLAPlugDLLHelper.Base64ToImage(self.OLAObject, base64)

    def Hex2ARGB(self, hex: str, a: int = None, r: int = None, g: int = None, b: int = None) -> Tuple[int, int, int, int, int]:
        return OLAPlugDLLHelper.Hex2ARGB(self.OLAObject, hex, a, r, g, b)

    def Hex2RGB(self, hex: str, r: int = None, g: int = None, b: int = None) -> Tuple[int, int, int, int]:
        return OLAPlugDLLHelper.Hex2RGB(self.OLAObject, hex, r, g, b)

    def ARGB2Hex(self, a: int, r: int, g: int, b: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.ARGB2Hex(self.OLAObject, a, r, g, b))

    def RGB2Hex(self, r: int, g: int, b: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.RGB2Hex(self.OLAObject, r, g, b))

    def Hex2HSV(self, hex: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.Hex2HSV(self.OLAObject, hex))

    def RGB2HSV(self, r: int, g: int, b: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.RGB2HSV(self.OLAObject, r, g, b))

    def CmpColor(self, x1: int, y1: int, colorStart: str, colorEnd: str) -> int:
        return OLAPlugDLLHelper.CmpColor(self.OLAObject, x1, y1, colorStart, colorEnd)

    def CmpColorPtr(self, ptr: int, x: int, y: int, colorStart: str, colorEnd: str) -> int:
        return OLAPlugDLLHelper.CmpColorPtr(self.OLAObject, ptr, x, y, colorStart, colorEnd)

    def CmpColorHex(self, hex: str, colorStart: str, colorEnd: str) -> int:
        return OLAPlugDLLHelper.CmpColorHex(self.OLAObject, hex, colorStart, colorEnd)

    def GetConnectedComponents(self, ptr: int, points: Union[str, List[dict]], tolerance: int) -> int:
        if not isinstance(points, str):
            points = json.dumps(points)
        return OLAPlugDLLHelper.GetConnectedComponents(self.OLAObject, ptr, points, tolerance)

    def DetectPointerDirection(self, ptr: int, x: int, y: int) -> float:
        return OLAPlugDLLHelper.DetectPointerDirection(self.OLAObject, ptr, x, y)

    def DetectPointerDirectionByFeatures(self, ptr: int, templatePtr: int, x: int, y: int, useTemplate: bool) -> float:
        return OLAPlugDLLHelper.DetectPointerDirectionByFeatures(self.OLAObject, ptr, templatePtr, x, y, useTemplate)

    def FastMatch(self, ptr: int, templatePtr: int, matchVal: float, _type: int, angle: float, scale: float) -> dict:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.FastMatch(self.OLAObject, ptr, templatePtr, matchVal, _type, angle, scale))
        if result == "":
            return {}
        return json.loads(result)

    def FastROI(self, ptr: int) -> int:
        return OLAPlugDLLHelper.FastROI(self.OLAObject, ptr)

    def GetROIRegion(self, ptr: int, x1: int = None, y1: int = None, x2: int = None, y2: int = None) -> Tuple[int, int, int, int, int]:
        return OLAPlugDLLHelper.GetROIRegion(self.OLAObject, ptr, x1, y1, x2, y2)

    def GetForegroundPoints(self, ptr: int) -> List[dict]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.GetForegroundPoints(self.OLAObject, ptr))
        if result == "":
            return []
        return json.loads(result)

    def ConvertColor(self, ptr: int, _type: int) -> int:
        return OLAPlugDLLHelper.ConvertColor(self.OLAObject, ptr, _type)

    def Threshold(self, ptr: int, thresh: float, maxVal: float, _type: int) -> int:
        return OLAPlugDLLHelper.Threshold(self.OLAObject, ptr, thresh, maxVal, _type)

    def RemoveIslands(self, ptr: int, minArea: int) -> int:
        return OLAPlugDLLHelper.RemoveIslands(self.OLAObject, ptr, minArea)

    def MorphGradient(self, ptr: int, kernelSize: int) -> int:
        return OLAPlugDLLHelper.MorphGradient(self.OLAObject, ptr, kernelSize)

    def MorphTophat(self, ptr: int, kernelSize: int) -> int:
        return OLAPlugDLLHelper.MorphTophat(self.OLAObject, ptr, kernelSize)

    def MorphBlackhat(self, ptr: int, kernelSize: int) -> int:
        return OLAPlugDLLHelper.MorphBlackhat(self.OLAObject, ptr, kernelSize)

    def Dilation(self, ptr: int, kernelSize: int) -> int:
        return OLAPlugDLLHelper.Dilation(self.OLAObject, ptr, kernelSize)

    def Erosion(self, ptr: int, kernelSize: int) -> int:
        return OLAPlugDLLHelper.Erosion(self.OLAObject, ptr, kernelSize)

    def GaussianBlur(self, ptr: int, kernelSize: int) -> int:
        return OLAPlugDLLHelper.GaussianBlur(self.OLAObject, ptr, kernelSize)

    def Sharpen(self, ptr: int) -> int:
        return OLAPlugDLLHelper.Sharpen(self.OLAObject, ptr)

    def CannyEdge(self, ptr: int, kernelSize: int) -> int:
        return OLAPlugDLLHelper.CannyEdge(self.OLAObject, ptr, kernelSize)

    def Flip(self, ptr: int, flipCode: int) -> int:
        return OLAPlugDLLHelper.Flip(self.OLAObject, ptr, flipCode)

    def MorphOpen(self, ptr: int, kernelSize: int) -> int:
        return OLAPlugDLLHelper.MorphOpen(self.OLAObject, ptr, kernelSize)

    def MorphClose(self, ptr: int, kernelSize: int) -> int:
        return OLAPlugDLLHelper.MorphClose(self.OLAObject, ptr, kernelSize)

    def Skeletonize(self, ptr: int) -> int:
        return OLAPlugDLLHelper.Skeletonize(self.OLAObject, ptr)

    def ImageStitchFromPath(self, path: str, trajectory: int = None) -> Tuple[int, int]:
        return OLAPlugDLLHelper.ImageStitchFromPath(self.OLAObject, path, trajectory)

    def ImageStitchCreate(self) -> int:
        return OLAPlugDLLHelper.ImageStitchCreate(self.OLAObject)

    def ImageStitchAppend(self, imageStitch: int, image: int) -> int:
        return OLAPlugDLLHelper.ImageStitchAppend(self.OLAObject, imageStitch, image)

    def ImageStitchGetResult(self, imageStitch: int, trajectory: int = None) -> Tuple[int, int]:
        return OLAPlugDLLHelper.ImageStitchGetResult(self.OLAObject, imageStitch, trajectory)

    def ImageStitchFree(self, imageStitch: int) -> int:
        return OLAPlugDLLHelper.ImageStitchFree(self.OLAObject, imageStitch)

    def CreateDatabase(self, dbName: str, password: str) -> int:
        return OLAPlugDLLHelper.CreateDatabase(self.OLAObject, dbName, password)

    def OpenDatabase(self, dbName: str, password: str) -> int:
        return OLAPlugDLLHelper.OpenDatabase(self.OLAObject, dbName, password)

    def GetDatabaseError(self, db: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetDatabaseError(self.OLAObject, db))

    def CloseDatabase(self, db: int) -> int:
        return OLAPlugDLLHelper.CloseDatabase(self.OLAObject, db)

    def GetAllTableNames(self, db: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetAllTableNames(self.OLAObject, db))

    def GetTableInfo(self, db: int, tableName: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetTableInfo(self.OLAObject, db, tableName))

    def GetTableInfoDetail(self, db: int, tableName: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetTableInfoDetail(self.OLAObject, db, tableName))

    def ExecuteSql(self, db: int, sql: str) -> int:
        return OLAPlugDLLHelper.ExecuteSql(self.OLAObject, db, sql)

    def ExecuteScalar(self, db: int, sql: str) -> int:
        return OLAPlugDLLHelper.ExecuteScalar(self.OLAObject, db, sql)

    def ExecuteReader(self, db: int, sql: str) -> int:
        return OLAPlugDLLHelper.ExecuteReader(self.OLAObject, db, sql)

    def Read(self, stmt: int) -> int:
        return OLAPlugDLLHelper.Read(self.OLAObject, stmt)

    def GetDataCount(self, stmt: int) -> int:
        return OLAPlugDLLHelper.GetDataCount(self.OLAObject, stmt)

    def GetColumnCount(self, stmt: int) -> int:
        return OLAPlugDLLHelper.GetColumnCount(self.OLAObject, stmt)

    def GetColumnName(self, stmt: int, iCol: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetColumnName(self.OLAObject, stmt, iCol))

    def GetColumnIndex(self, stmt: int, columnName: str) -> int:
        return OLAPlugDLLHelper.GetColumnIndex(self.OLAObject, stmt, columnName)

    def GetColumnType(self, stmt: int, iCol: int) -> int:
        return OLAPlugDLLHelper.GetColumnType(self.OLAObject, stmt, iCol)

    def Finalize(self, stmt: int) -> int:
        return OLAPlugDLLHelper.Finalize(self.OLAObject, stmt)

    def GetDouble(self, stmt: int, iCol: int) -> float:
        return OLAPlugDLLHelper.GetDouble(self.OLAObject, stmt, iCol)

    def GetInt32(self, stmt: int, iCol: int) -> int:
        return OLAPlugDLLHelper.GetInt32(self.OLAObject, stmt, iCol)

    def GetInt64(self, stmt: int, iCol: int) -> int:
        return OLAPlugDLLHelper.GetInt64(self.OLAObject, stmt, iCol)

    def GetString(self, stmt: int, iCol: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetString(self.OLAObject, stmt, iCol))

    def GetDoubleByColumnName(self, stmt: int, columnName: str) -> float:
        return OLAPlugDLLHelper.GetDoubleByColumnName(self.OLAObject, stmt, columnName)

    def GetInt32ByColumnName(self, stmt: int, columnName: str) -> int:
        return OLAPlugDLLHelper.GetInt32ByColumnName(self.OLAObject, stmt, columnName)

    def GetInt64ByColumnName(self, stmt: int, columnName: str) -> int:
        return OLAPlugDLLHelper.GetInt64ByColumnName(self.OLAObject, stmt, columnName)

    def GetStringByColumnName(self, stmt: int, columnName: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetStringByColumnName(self.OLAObject, stmt, columnName))

    def InitOlaDatabase(self, db: int) -> int:
        return OLAPlugDLLHelper.InitOlaDatabase(self.OLAObject, db)

    def InitOlaImageFromDir(self, db: int, _dir: str, cover: int) -> int:
        return OLAPlugDLLHelper.InitOlaImageFromDir(self.OLAObject, db, _dir, cover)

    def RemoveOlaImageFromDir(self, db: int, _dir: str) -> int:
        return OLAPlugDLLHelper.RemoveOlaImageFromDir(self.OLAObject, db, _dir)

    def ExportOlaImageDir(self, db: int, _dir: str, exportDir: str) -> int:
        return OLAPlugDLLHelper.ExportOlaImageDir(self.OLAObject, db, _dir, exportDir)

    def ImportOlaImage(self, db: int, _dir: str, fileName: str, cover: int) -> int:
        return OLAPlugDLLHelper.ImportOlaImage(self.OLAObject, db, _dir, fileName, cover)

    def GetOlaImage(self, db: int, _dir: str, fileName: str) -> int:
        return OLAPlugDLLHelper.GetOlaImage(self.OLAObject, db, _dir, fileName)

    def RemoveOlaImage(self, db: int, _dir: str, fileName: str) -> int:
        return OLAPlugDLLHelper.RemoveOlaImage(self.OLAObject, db, _dir, fileName)

    def SetDbConfig(self, db: int, key: str, value: str) -> int:
        return OLAPlugDLLHelper.SetDbConfig(self.OLAObject, db, key, value)

    def GetDbConfig(self, db: int, key: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetDbConfig(self.OLAObject, db, key))

    def RemoveDbConfig(self, db: int, key: str) -> int:
        return OLAPlugDLLHelper.RemoveDbConfig(self.OLAObject, db, key)

    def SetDbConfigEx(self, key: str, value: str) -> int:
        return OLAPlugDLLHelper.SetDbConfigEx(self.OLAObject, key, value)

    def GetDbConfigEx(self, key: str) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetDbConfigEx(self.OLAObject, key))

    def RemoveDbConfigEx(self, key: str) -> int:
        return OLAPlugDLLHelper.RemoveDbConfigEx(self.OLAObject, key)

    def InitDictFromDir(self, db: int, dict_name: str, dict_path: str, cover: int) -> int:
        return OLAPlugDLLHelper.InitDictFromDir(self.OLAObject, db, dict_name, dict_path, cover)

    def ImportDictWord(self, db: int, dict_name: str, pic_file_name: str, cover: int) -> int:
        return OLAPlugDLLHelper.ImportDictWord(self.OLAObject, db, dict_name, pic_file_name, cover)

    def ExportDict(self, db: int, dict_name: str, export_dir: str) -> int:
        return OLAPlugDLLHelper.ExportDict(self.OLAObject, db, dict_name, export_dir)

    def RemoveDict(self, db: int, dict_name: str) -> int:
        return OLAPlugDLLHelper.RemoveDict(self.OLAObject, db, dict_name)

    def RemoveDictWord(self, db: int, dict_name: str, word: str) -> int:
        return OLAPlugDLLHelper.RemoveDictWord(self.OLAObject, db, dict_name, word)

    def GetDictImage(self, db: int, dict_name: str, word: str, gap: int, _dir: int) -> int:
        return OLAPlugDLLHelper.GetDictImage(self.OLAObject, db, dict_name, word, gap, _dir)

    def SetWindowState(self, hwnd: int, state: int) -> int:
        return OLAPlugDLLHelper.SetWindowState(self.OLAObject, hwnd, state)

    def FindWindow(self, class_name: str, title: str) -> int:
        return OLAPlugDLLHelper.FindWindow(self.OLAObject, class_name, title)

    def GetClipboard(self) -> int:
        return OLAPlugDLLHelper.GetClipboard(self.OLAObject)

    def SetClipboard(self, text: str) -> int:
        return OLAPlugDLLHelper.SetClipboard(self.OLAObject, text)

    def SendPaste(self, hwnd: int) -> int:
        return OLAPlugDLLHelper.SendPaste(self.OLAObject, hwnd)

    def GetWindow(self, hwnd: int, flag: int) -> int:
        return OLAPlugDLLHelper.GetWindow(self.OLAObject, hwnd, flag)

    def GetWindowTitle(self, hwnd: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetWindowTitle(self.OLAObject, hwnd))

    def GetWindowClass(self, hwnd: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetWindowClass(self.OLAObject, hwnd))

    def GetWindowRect(self, hwnd: int, x1: int = None, y1: int = None, x2: int = None, y2: int = None) -> Tuple[int, int, int, int, int]:
        return OLAPlugDLLHelper.GetWindowRect(self.OLAObject, hwnd, x1, y1, x2, y2)

    def GetWindowProcessPath(self, hwnd: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetWindowProcessPath(self.OLAObject, hwnd))

    def GetWindowState(self, hwnd: int, flag: int) -> int:
        return OLAPlugDLLHelper.GetWindowState(self.OLAObject, hwnd, flag)

    def GetForegroundWindow(self) -> int:
        return OLAPlugDLLHelper.GetForegroundWindow(self.OLAObject)

    def GetWindowProcessId(self, hwnd: int) -> int:
        return OLAPlugDLLHelper.GetWindowProcessId(self.OLAObject, hwnd)

    def GetClientSize(self, hwnd: int, width: int = None, height: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.GetClientSize(self.OLAObject, hwnd, width, height)

    def GetMousePointWindow(self) -> int:
        return OLAPlugDLLHelper.GetMousePointWindow(self.OLAObject)

    def GetSpecialWindow(self, flag: int) -> int:
        return OLAPlugDLLHelper.GetSpecialWindow(self.OLAObject, flag)

    def GetClientRect(self, hwnd: int, x1: int = None, y1: int = None, x2: int = None, y2: int = None) -> Tuple[int, int, int, int, int]:
        return OLAPlugDLLHelper.GetClientRect(self.OLAObject, hwnd, x1, y1, x2, y2)

    def SetWindowText(self, hwnd: int, title: str) -> int:
        return OLAPlugDLLHelper.SetWindowText(self.OLAObject, hwnd, title)

    def SetWindowSize(self, hwnd: int, width: int, height: int) -> int:
        return OLAPlugDLLHelper.SetWindowSize(self.OLAObject, hwnd, width, height)

    def SetClientSize(self, hwnd: int, width: int, height: int) -> int:
        return OLAPlugDLLHelper.SetClientSize(self.OLAObject, hwnd, width, height)

    def SetWindowTransparent(self, hwnd: int, alpha: int) -> int:
        return OLAPlugDLLHelper.SetWindowTransparent(self.OLAObject, hwnd, alpha)

    def FindWindowEx(self, parent: int, class_name: str, title: str) -> int:
        return OLAPlugDLLHelper.FindWindowEx(self.OLAObject, parent, class_name, title)

    def FindWindowByProcess(self, process_name: str, class_name: str, title: str) -> int:
        return OLAPlugDLLHelper.FindWindowByProcess(self.OLAObject, process_name, class_name, title)

    def MoveWindow(self, hwnd: int, x: int, y: int) -> int:
        return OLAPlugDLLHelper.MoveWindow(self.OLAObject, hwnd, x, y)

    def GetScaleFromWindows(self, hwnd: int) -> float:
        return OLAPlugDLLHelper.GetScaleFromWindows(self.OLAObject, hwnd)

    def GetWindowDpiAwarenessScale(self, hwnd: int) -> float:
        return OLAPlugDLLHelper.GetWindowDpiAwarenessScale(self.OLAObject, hwnd)

    def EnumProcess(self, name: str) -> List[str]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.EnumProcess(self.OLAObject, name))
        if result == "":
            return []
        return result.split(",")

    def EnumWindow(self, parent: int, title: str, className: str, _filter: int) -> List[str]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.EnumWindow(self.OLAObject, parent, title, className, _filter))
        if result == "":
            return []
        return result.split(",")

    def EnumWindowByProcess(self, process_name: str, title: str, class_name: str, _filter: int) -> List[str]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.EnumWindowByProcess(self.OLAObject, process_name, title, class_name, _filter))
        if result == "":
            return []
        return result.split(",")

    def EnumWindowByProcessId(self, pid: int, title: str, class_name: str, _filter: int) -> List[str]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.EnumWindowByProcessId(self.OLAObject, pid, title, class_name, _filter))
        if result == "":
            return []
        return result.split(",")

    def EnumWindowSuper(self, spec1: str, flag1: int, type1: int, spec2: str, flag2: int, type2: int, sort: int) -> List[str]:
        result = self.PtrToStringUTF8(OLAPlugDLLHelper.EnumWindowSuper(self.OLAObject, spec1, flag1, type1, spec2, flag2, type2, sort))
        if result == "":
            return []
        return result.split(",")

    def GetPointWindow(self, x: int, y: int) -> int:
        return OLAPlugDLLHelper.GetPointWindow(self.OLAObject, x, y)

    def GetProcessInfo(self, pid: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetProcessInfo(self.OLAObject, pid))

    def ShowTaskBarIcon(self, hwnd: int, show: int) -> int:
        return OLAPlugDLLHelper.ShowTaskBarIcon(self.OLAObject, hwnd, show)

    def FindWindowByProcessId(self, process_id: int, className: str, title: str) -> int:
        return OLAPlugDLLHelper.FindWindowByProcessId(self.OLAObject, process_id, className, title)

    def GetWindowThreadId(self, hwnd: int) -> int:
        return OLAPlugDLLHelper.GetWindowThreadId(self.OLAObject, hwnd)

    def FindWindowSuper(self, spec1: str, flag1: int, type1: int, spec2: str, flag2: int, type2: int) -> int:
        return OLAPlugDLLHelper.FindWindowSuper(self.OLAObject, spec1, flag1, type1, spec2, flag2, type2)

    def ClientToScreen(self, hwnd: int, x: int = None, y: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.ClientToScreen(self.OLAObject, hwnd, x, y)

    def ScreenToClient(self, hwnd: int, x: int = None, y: int = None) -> Tuple[int, int, int]:
        return OLAPlugDLLHelper.ScreenToClient(self.OLAObject, hwnd, x, y)

    def GetForegroundFocus(self) -> int:
        return OLAPlugDLLHelper.GetForegroundFocus(self.OLAObject)

    def SetWindowDisplay(self, hwnd: int, affinity: int) -> int:
        return OLAPlugDLLHelper.SetWindowDisplay(self.OLAObject, hwnd, affinity)

    def IsDisplayDead(self, x1: int, y1: int, x2: int, y2: int, time: int) -> int:
        return OLAPlugDLLHelper.IsDisplayDead(self.OLAObject, x1, y1, x2, y2, time)

    def GetWindowsFps(self, x1: int, y1: int, x2: int, y2: int) -> int:
        return OLAPlugDLLHelper.GetWindowsFps(self.OLAObject, x1, y1, x2, y2)

    def TerminateProcess(self, pid: int) -> int:
        return OLAPlugDLLHelper.TerminateProcess(self.OLAObject, pid)

    def TerminateProcessTree(self, pid: int) -> int:
        return OLAPlugDLLHelper.TerminateProcessTree(self.OLAObject, pid)

    def GetCommandLine(self, hwnd: int) -> str:
        return self.PtrToStringUTF8(OLAPlugDLLHelper.GetCommandLine(self.OLAObject, hwnd))

    def CheckFontSmooth(self) -> int:
        return OLAPlugDLLHelper.CheckFontSmooth(self.OLAObject)

    def SetFontSmooth(self, enable: int) -> int:
        return OLAPlugDLLHelper.SetFontSmooth(self.OLAObject, enable)

    def EnableDebugPrivilege(self) -> int:
        return OLAPlugDLLHelper.EnableDebugPrivilege(self.OLAObject)

    def SystemStart(self, applicationName: str, commandLine: str) -> int:
        return OLAPlugDLLHelper.SystemStart(self.OLAObject, applicationName, commandLine)

    def CreateChildProcess(self, applicationName: str, commandLine: str, currentDirectory: str, showType: int, parentProcessId: int) -> int:
        return OLAPlugDLLHelper.CreateChildProcess(self.OLAObject, applicationName, commandLine, currentDirectory, showType, parentProcessId)


    def Query(self, db: int, sql: str) -> List[dict]:
        data = []  # 存储查询结果
        stmt = self.ExecuteReader(db, sql)  # 执行查询，获取语句句柄

        # 获取列名
        column_names = []
        for i in range(self.GetColumnCount(stmt)):
            column_names.append(self.GetColumnName(stmt, i))

        # 读取数据
        while self.Read(stmt):
            row = {}
            for column_name in column_names:
                i_col = self.GetColumnIndex(stmt, column_name)
                column_type = self.GetColumnType(stmt, i_col)

                # 根据列类型处理数据
                if column_type == 1:  # SQLITE_INTEGER
                    row[column_name] = self.GetInt64(stmt, i_col)
                elif column_type == 2:  # SQLITE_FLOAT
                    row[column_name] = self.GetDouble(stmt, i_col)
                elif column_type == 3:  # SQLITE_TEXT
                    row[column_name] = self.GetString(stmt, i_col)
                elif column_type == 4:  # SQLITE_BLOB
                    row[column_name] = self.GetString(stmt, i_col)  # 假设 BLOB 转为字符串
                elif column_type == 5:  # SQLITE_NULL
                    row[column_name] = None

            data.append(row)

        # 释放资源
        self.Finalize(stmt)
        return data

    def hotkey(self, *args: str, interval: float = 0.05) -> int:
        keys = [k.lower() if isinstance(k, str) else k for k in args]
        try:
            for key in keys:
                OLAPlugDLLHelper.KeyDownChar(self.OLAObject, key)
                time.sleep(interval)
            for key in reversed(keys):
                OLAPlugDLLHelper.KeyUpChar(self.OLAObject, key)
                time.sleep(interval)
            return 1
        except Exception as e:
            print(f"Error occurred during hotkey: {e}")
            # 可选：强制释放所有已按下的键
            for key in reversed(keys):
                OLAPlugDLLHelper.KeyUpChar(self.OLAObject, key)
            return 0

