import os
from ctypes import *
from typing import List, Tuple, Literal, Callable

# 接口参数定义
class OLAPlugDLLHelper:
    DLL = "OLAPlug_x64.dll"

    # 回调函数持久化使用
    callbacks = {}

    _dll = WinDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), DLL))
    HotkeyDelegate = WINFUNCTYPE(None, c_int32, c_int32)
    MouseDelegate = WINFUNCTYPE(None, c_int32, c_int32, c_int32, c_int32)
    MouseWheelDelegate = WINFUNCTYPE(None, c_int32, c_int32, c_int32, c_int32)
    MouseMoveDelegate = WINFUNCTYPE(None, c_int32, c_int32)
    MouseDragDelegate = WINFUNCTYPE(None, c_int32, c_int32)
    DrawGuiButtonDelegate = WINFUNCTYPE(None, c_int64)
    DrawGuiMouseDelegate = WINFUNCTYPE(None, c_int64, c_int32, c_int32, c_int32)

    _dll.CreateCOLAPlugInterFace.argtypes = []
    _dll.CreateCOLAPlugInterFace.restype = c_int64

    _dll.DestroyCOLAPlugInterFace.argtypes = [c_int64]
    _dll.DestroyCOLAPlugInterFace.restype = c_int

    _dll.Ver.argtypes = []
    _dll.Ver.restype = c_int64

    _dll.SetPath.argtypes = [c_int64, c_char_p]
    _dll.SetPath.restype = c_int

    _dll.GetPath.argtypes = [c_int64]
    _dll.GetPath.restype = c_int64

    _dll.GetMachineCode.argtypes = [c_int64]
    _dll.GetMachineCode.restype = c_int64

    _dll.GetBasePath.argtypes = [c_int64]
    _dll.GetBasePath.restype = c_int64

    _dll.Reg.argtypes = [c_char_p, c_char_p, c_char_p]
    _dll.Reg.restype = c_int

    _dll.BindWindow.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_char_p, c_int]
    _dll.BindWindow.restype = c_int

    _dll.BindWindowEx.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
    _dll.BindWindowEx.restype = c_int

    _dll.UnBindWindow.argtypes = [c_int64]
    _dll.UnBindWindow.restype = c_int

    _dll.GetBindWindow.argtypes = [c_int64]
    _dll.GetBindWindow.restype = c_int64

    _dll.ReleaseWindowsDll.argtypes = [c_int64, c_int64]
    _dll.ReleaseWindowsDll.restype = c_int

    _dll.FreeStringPtr.argtypes = [c_int64]
    _dll.FreeStringPtr.restype = c_int

    _dll.FreeMemoryPtr.argtypes = [c_int64]
    _dll.FreeMemoryPtr.restype = c_int

    _dll.GetStringSize.argtypes = [c_int64]
    _dll.GetStringSize.restype = c_int

    _dll.GetStringFromPtr.argtypes = [c_int64, c_char_p, c_int]
    _dll.GetStringFromPtr.restype = c_int

    _dll.Delay.argtypes = [c_int]
    _dll.Delay.restype = c_int

    _dll.Delays.argtypes = [c_int, c_int]
    _dll.Delays.restype = c_int

    _dll.SetUAC.argtypes = [c_int64, c_int]
    _dll.SetUAC.restype = c_int

    _dll.CheckUAC.argtypes = [c_int64]
    _dll.CheckUAC.restype = c_int

    _dll.RunApp.argtypes = [c_int64, c_char_p, c_int]
    _dll.RunApp.restype = c_int

    _dll.ExecuteCmd.argtypes = [c_int64, c_char_p, c_char_p, c_int]
    _dll.ExecuteCmd.restype = c_int64

    _dll.GetConfig.argtypes = [c_int64, c_char_p]
    _dll.GetConfig.restype = c_int64

    _dll.SetConfig.argtypes = [c_int64, c_char_p]
    _dll.SetConfig.restype = c_int

    _dll.SetConfigByKey.argtypes = [c_int64, c_char_p, c_char_p]
    _dll.SetConfigByKey.restype = c_int

    _dll.SendDropFiles.argtypes = [c_int64, c_int64, c_char_p]
    _dll.SendDropFiles.restype = c_int

    _dll.GetRandomNumber.argtypes = [c_int64, c_int, c_int]
    _dll.GetRandomNumber.restype = c_int

    _dll.GetRandomDouble.argtypes = [c_int64, c_double, c_double]
    _dll.GetRandomDouble.restype = c_double

    _dll.ExcludePos.argtypes = [c_int64, c_char_p, c_int, c_int, c_int, c_int, c_int]
    _dll.ExcludePos.restype = c_int64

    _dll.FindNearestPos.argtypes = [c_int64, c_char_p, c_int, c_int, c_int]
    _dll.FindNearestPos.restype = c_int64

    _dll.SortPosDistance.argtypes = [c_int64, c_char_p, c_int, c_int, c_int]
    _dll.SortPosDistance.restype = c_int64

    _dll.GetDenseRect.argtypes = [c_int64, c_int64, c_int, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    _dll.GetDenseRect.restype = c_int

    _dll.PathPlanning.argtypes = [c_int64, c_int64, c_int, c_int, c_int, c_int, c_double, c_double]
    _dll.PathPlanning.restype = c_int64

    _dll.CreateGraph.argtypes = [c_int64, c_char_p]
    _dll.CreateGraph.restype = c_int64

    _dll.GetGraph.argtypes = [c_int64, c_int64]
    _dll.GetGraph.restype = c_int64

    _dll.AddEdge.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_double, c_bool]
    _dll.AddEdge.restype = c_int

    _dll.GetShortestPath.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.GetShortestPath.restype = c_int64

    _dll.GetShortestDistance.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.GetShortestDistance.restype = c_double

    _dll.ClearGraph.argtypes = [c_int64, c_int64]
    _dll.ClearGraph.restype = c_int

    _dll.DeleteGraph.argtypes = [c_int64, c_int64]
    _dll.DeleteGraph.restype = c_int

    _dll.GetNodeCount.argtypes = [c_int64, c_int64]
    _dll.GetNodeCount.restype = c_int

    _dll.GetEdgeCount.argtypes = [c_int64, c_int64]
    _dll.GetEdgeCount.restype = c_int

    _dll.GetShortestPathToAllNodes.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetShortestPathToAllNodes.restype = c_int64

    _dll.GetMinimumSpanningTree.argtypes = [c_int64, c_int64]
    _dll.GetMinimumSpanningTree.restype = c_int64

    _dll.GetDirectedPathToAllNodes.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetDirectedPathToAllNodes.restype = c_int64

    _dll.GetMinimumArborescence.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetMinimumArborescence.restype = c_int64

    _dll.CreateGraphFromCoordinates.argtypes = [c_int64, c_char_p, c_bool, c_double, c_bool]
    _dll.CreateGraphFromCoordinates.restype = c_int64

    _dll.AddCoordinateNode.argtypes = [c_int64, c_int64, c_char_p, c_double, c_double, c_bool, c_double, c_bool]
    _dll.AddCoordinateNode.restype = c_int

    _dll.GetNodeCoordinates.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetNodeCoordinates.restype = c_int64

    _dll.SetNodeConnection.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_bool, c_double]
    _dll.SetNodeConnection.restype = c_int

    _dll.GetNodeConnectionStatus.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.GetNodeConnectionStatus.restype = c_int

    _dll.AsmCall.argtypes = [c_int64, c_int64, c_char_p, c_int, c_int64]
    _dll.AsmCall.restype = c_int64

    _dll.Assemble.argtypes = [c_int64, c_char_p, c_int64, c_int, c_int]
    _dll.Assemble.restype = c_int64

    _dll.Disassemble.argtypes = [c_int64, c_char_p, c_int64, c_int, c_int, c_int]
    _dll.Disassemble.restype = c_int64

    _dll.DrawGuiCleanup.argtypes = [c_int64]
    _dll.DrawGuiCleanup.restype = c_int

    _dll.DrawGuiSetGuiActive.argtypes = [c_int64, c_int]
    _dll.DrawGuiSetGuiActive.restype = c_int

    _dll.DrawGuiIsGuiActive.argtypes = [c_int64]
    _dll.DrawGuiIsGuiActive.restype = c_int

    _dll.DrawGuiSetGuiClickThrough.argtypes = [c_int64, c_int]
    _dll.DrawGuiSetGuiClickThrough.restype = c_int

    _dll.DrawGuiIsGuiClickThrough.argtypes = [c_int64]
    _dll.DrawGuiIsGuiClickThrough.restype = c_int

    _dll.DrawGuiRectangle.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_int, c_double]
    _dll.DrawGuiRectangle.restype = c_int64

    _dll.DrawGuiCircle.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_double]
    _dll.DrawGuiCircle.restype = c_int64

    _dll.DrawGuiLine.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_double]
    _dll.DrawGuiLine.restype = c_int64

    _dll.DrawGuiText.argtypes = [c_int64, c_char_p, c_int, c_int, c_char_p, c_int, c_int]
    _dll.DrawGuiText.restype = c_int64

    _dll.DrawGuiImage.argtypes = [c_int64, c_char_p, c_int, c_int]
    _dll.DrawGuiImage.restype = c_int64

    _dll.DrawGuiWindow.argtypes = [c_int64, c_char_p, c_int, c_int, c_int, c_int, c_int]
    _dll.DrawGuiWindow.restype = c_int64

    _dll.DrawGuiPanel.argtypes = [c_int64, c_int64, c_int, c_int, c_int, c_int]
    _dll.DrawGuiPanel.restype = c_int64

    _dll.DrawGuiButton.argtypes = [c_int64, c_int64, c_char_p, c_int, c_int, c_int, c_int]
    _dll.DrawGuiButton.restype = c_int64

    _dll.DrawGuiSetPosition.argtypes = [c_int64, c_int64, c_int, c_int]
    _dll.DrawGuiSetPosition.restype = c_int

    _dll.DrawGuiSetSize.argtypes = [c_int64, c_int64, c_int, c_int]
    _dll.DrawGuiSetSize.restype = c_int

    _dll.DrawGuiSetColor.argtypes = [c_int64, c_int64, c_int, c_int, c_int, c_int]
    _dll.DrawGuiSetColor.restype = c_int

    _dll.DrawGuiSetAlpha.argtypes = [c_int64, c_int64, c_int]
    _dll.DrawGuiSetAlpha.restype = c_int

    _dll.DrawGuiSetDrawMode.argtypes = [c_int64, c_int64, c_int]
    _dll.DrawGuiSetDrawMode.restype = c_int

    _dll.DrawGuiSetLineThickness.argtypes = [c_int64, c_int64, c_double]
    _dll.DrawGuiSetLineThickness.restype = c_int

    _dll.DrawGuiSetFont.argtypes = [c_int64, c_int64, c_char_p, c_int]
    _dll.DrawGuiSetFont.restype = c_int

    _dll.DrawGuiSetTextAlign.argtypes = [c_int64, c_int64, c_int]
    _dll.DrawGuiSetTextAlign.restype = c_int

    _dll.DrawGuiSetText.argtypes = [c_int64, c_int64, c_char_p]
    _dll.DrawGuiSetText.restype = c_int

    _dll.DrawGuiSetWindowTitle.argtypes = [c_int64, c_int64, c_char_p]
    _dll.DrawGuiSetWindowTitle.restype = c_int

    _dll.DrawGuiSetWindowStyle.argtypes = [c_int64, c_int64, c_int]
    _dll.DrawGuiSetWindowStyle.restype = c_int

    _dll.DrawGuiSetWindowTopMost.argtypes = [c_int64, c_int64, c_int]
    _dll.DrawGuiSetWindowTopMost.restype = c_int

    _dll.DrawGuiSetWindowTransparency.argtypes = [c_int64, c_int64, c_int]
    _dll.DrawGuiSetWindowTransparency.restype = c_int

    _dll.DrawGuiDeleteObject.argtypes = [c_int64, c_int64]
    _dll.DrawGuiDeleteObject.restype = c_int

    _dll.DrawGuiClearAll.argtypes = [c_int64]
    _dll.DrawGuiClearAll.restype = c_int

    _dll.DrawGuiSetVisible.argtypes = [c_int64, c_int64, c_int]
    _dll.DrawGuiSetVisible.restype = c_int

    _dll.DrawGuiSetZOrder.argtypes = [c_int64, c_int64, c_int]
    _dll.DrawGuiSetZOrder.restype = c_int

    _dll.DrawGuiSetParent.argtypes = [c_int64, c_int64, c_int64]
    _dll.DrawGuiSetParent.restype = c_int

    _dll.DrawGuiSetButtonCallback.argtypes = [c_int64, c_int64, DrawGuiButtonDelegate]
    _dll.DrawGuiSetButtonCallback.restype = c_int

    _dll.DrawGuiSetMouseCallback.argtypes = [c_int64, c_int64, DrawGuiMouseDelegate]
    _dll.DrawGuiSetMouseCallback.restype = c_int

    _dll.DrawGuiGetDrawObjectType.argtypes = [c_int64, c_int64]
    _dll.DrawGuiGetDrawObjectType.restype = c_int

    _dll.DrawGuiGetPosition.argtypes = [c_int64, c_int64, POINTER(c_int), POINTER(c_int)]
    _dll.DrawGuiGetPosition.restype = c_int

    _dll.DrawGuiGetSize.argtypes = [c_int64, c_int64, POINTER(c_int), POINTER(c_int)]
    _dll.DrawGuiGetSize.restype = c_int

    _dll.DrawGuiIsPointInObject.argtypes = [c_int64, c_int64, c_int, c_int]
    _dll.DrawGuiIsPointInObject.restype = c_int

    _dll.SetMemoryMode.argtypes = [c_int64, c_int]
    _dll.SetMemoryMode.restype = c_int

    _dll.ExportDriver.argtypes = [c_int64, c_char_p, c_int]
    _dll.ExportDriver.restype = c_int

    _dll.LoadDriver.argtypes = [c_int64, c_char_p, c_char_p]
    _dll.LoadDriver.restype = c_int

    _dll.UnloadDriver.argtypes = [c_int64, c_char_p]
    _dll.UnloadDriver.restype = c_int

    _dll.DriverTest.argtypes = [c_int64]
    _dll.DriverTest.restype = c_int

    _dll.LoadPdb.argtypes = [c_int64]
    _dll.LoadPdb.restype = c_int

    _dll.HideProcess.argtypes = [c_int64, c_int64, c_int]
    _dll.HideProcess.restype = c_int

    _dll.ProtectProcess.argtypes = [c_int64, c_int64, c_int]
    _dll.ProtectProcess.restype = c_int

    _dll.AddProtectPID.argtypes = [c_int64, c_int64, c_int64, c_int64]
    _dll.AddProtectPID.restype = c_int

    _dll.RemoveProtectPID.argtypes = [c_int64, c_int64]
    _dll.RemoveProtectPID.restype = c_int

    _dll.AddAllowPID.argtypes = [c_int64, c_int64]
    _dll.AddAllowPID.restype = c_int

    _dll.RemoveAllowPID.argtypes = [c_int64, c_int64]
    _dll.RemoveAllowPID.restype = c_int

    _dll.InjectDll.argtypes = [c_int64, c_int64, c_char_p, c_int]
    _dll.InjectDll.restype = c_int

    _dll.FakeProcess.argtypes = [c_int64, c_int64, c_int64]
    _dll.FakeProcess.restype = c_int

    _dll.StartHotkeyHook.argtypes = [c_int64]
    _dll.StartHotkeyHook.restype = c_int

    _dll.StopHotkeyHook.argtypes = [c_int64]
    _dll.StopHotkeyHook.restype = c_int

    _dll.RegisterHotkey.argtypes = [c_int64, c_int, c_int, HotkeyDelegate]
    _dll.RegisterHotkey.restype = c_int

    _dll.UnregisterHotkey.argtypes = [c_int64, c_int, c_int]
    _dll.UnregisterHotkey.restype = c_int

    _dll.RegisterMouseButton.argtypes = [c_int64, c_int, c_int, MouseDelegate]
    _dll.RegisterMouseButton.restype = c_int

    _dll.UnregisterMouseButton.argtypes = [c_int64, c_int, c_int]
    _dll.UnregisterMouseButton.restype = c_int

    _dll.RegisterMouseWheel.argtypes = [c_int64, MouseWheelDelegate]
    _dll.RegisterMouseWheel.restype = c_int

    _dll.UnregisterMouseWheel.argtypes = [c_int64]
    _dll.UnregisterMouseWheel.restype = c_int

    _dll.RegisterMouseMove.argtypes = [c_int64, MouseMoveDelegate]
    _dll.RegisterMouseMove.restype = c_int

    _dll.UnregisterMouseMove.argtypes = [c_int64]
    _dll.UnregisterMouseMove.restype = c_int

    _dll.RegisterMouseDrag.argtypes = [c_int64, MouseDragDelegate]
    _dll.RegisterMouseDrag.restype = c_int

    _dll.UnregisterMouseDrag.argtypes = [c_int64]
    _dll.UnregisterMouseDrag.restype = c_int

    _dll.JsonCreateObject.argtypes = []
    _dll.JsonCreateObject.restype = c_int64

    _dll.JsonCreateArray.argtypes = []
    _dll.JsonCreateArray.restype = c_int64

    _dll.JsonParse.argtypes = [c_char_p, POINTER(c_int)]
    _dll.JsonParse.restype = c_int64

    _dll.JsonStringify.argtypes = [c_int64, c_int, POINTER(c_int)]
    _dll.JsonStringify.restype = c_int64

    _dll.JsonFree.argtypes = [c_int64]
    _dll.JsonFree.restype = c_int

    _dll.JsonGetValue.argtypes = [c_int64, c_char_p, POINTER(c_int)]
    _dll.JsonGetValue.restype = c_int64

    _dll.JsonGetArrayItem.argtypes = [c_int64, c_int, POINTER(c_int)]
    _dll.JsonGetArrayItem.restype = c_int64

    _dll.JsonGetString.argtypes = [c_int64, c_char_p, POINTER(c_int)]
    _dll.JsonGetString.restype = c_int64

    _dll.JsonGetNumber.argtypes = [c_int64, c_char_p, POINTER(c_int)]
    _dll.JsonGetNumber.restype = c_double

    _dll.JsonGetBool.argtypes = [c_int64, c_char_p, POINTER(c_int)]
    _dll.JsonGetBool.restype = c_int

    _dll.JsonGetSize.argtypes = [c_int64, POINTER(c_int)]
    _dll.JsonGetSize.restype = c_int

    _dll.JsonSetValue.argtypes = [c_int64, c_char_p, c_int64]
    _dll.JsonSetValue.restype = c_int

    _dll.JsonArrayAppend.argtypes = [c_int64, c_int64]
    _dll.JsonArrayAppend.restype = c_int

    _dll.JsonSetString.argtypes = [c_int64, c_char_p, c_char_p]
    _dll.JsonSetString.restype = c_int

    _dll.JsonSetNumber.argtypes = [c_int64, c_char_p, c_double]
    _dll.JsonSetNumber.restype = c_int

    _dll.JsonSetBool.argtypes = [c_int64, c_char_p, c_int]
    _dll.JsonSetBool.restype = c_int

    _dll.JsonDeleteKey.argtypes = [c_int64, c_char_p]
    _dll.JsonDeleteKey.restype = c_int

    _dll.JsonClear.argtypes = [c_int64]
    _dll.JsonClear.restype = c_int

    _dll.GenerateMouseTrajectory.argtypes = [c_int64, c_int, c_int, c_int, c_int]
    _dll.GenerateMouseTrajectory.restype = c_int64

    _dll.KeyDown.argtypes = [c_int64, c_int]
    _dll.KeyDown.restype = c_int

    _dll.KeyUp.argtypes = [c_int64, c_int]
    _dll.KeyUp.restype = c_int

    _dll.KeyPress.argtypes = [c_int64, c_int]
    _dll.KeyPress.restype = c_int

    _dll.LeftDown.argtypes = [c_int64]
    _dll.LeftDown.restype = c_int

    _dll.LeftUp.argtypes = [c_int64]
    _dll.LeftUp.restype = c_int

    _dll.MoveTo.argtypes = [c_int64, c_int, c_int]
    _dll.MoveTo.restype = c_int

    _dll.MoveToWithoutSimulator.argtypes = [c_int64, c_int, c_int]
    _dll.MoveToWithoutSimulator.restype = c_int

    _dll.RightClick.argtypes = [c_int64]
    _dll.RightClick.restype = c_int

    _dll.RightDown.argtypes = [c_int64]
    _dll.RightDown.restype = c_int

    _dll.RightUp.argtypes = [c_int64]
    _dll.RightUp.restype = c_int

    _dll.GetCursorShape.argtypes = [c_int64]
    _dll.GetCursorShape.restype = c_int64

    _dll.GetCursorImage.argtypes = [c_int64]
    _dll.GetCursorImage.restype = c_int64

    _dll.KeyPressStr.argtypes = [c_int64, c_char_p, c_int]
    _dll.KeyPressStr.restype = c_int

    _dll.SendString.argtypes = [c_int64, c_int64, c_char_p]
    _dll.SendString.restype = c_int

    _dll.SendStringEx.argtypes = [c_int64, c_int64, c_int64, c_int, c_int]
    _dll.SendStringEx.restype = c_int

    _dll.KeyPressChar.argtypes = [c_int64, c_char_p]
    _dll.KeyPressChar.restype = c_int

    _dll.KeyDownChar.argtypes = [c_int64, c_char_p]
    _dll.KeyDownChar.restype = c_int

    _dll.KeyUpChar.argtypes = [c_int64, c_char_p]
    _dll.KeyUpChar.restype = c_int

    _dll.MoveR.argtypes = [c_int64, c_int, c_int]
    _dll.MoveR.restype = c_int

    _dll.MiddleClick.argtypes = [c_int64]
    _dll.MiddleClick.restype = c_int

    _dll.MoveToEx.argtypes = [c_int64, c_int, c_int, c_int, c_int]
    _dll.MoveToEx.restype = c_int64

    _dll.GetCursorPos.argtypes = [c_int64, POINTER(c_int), POINTER(c_int)]
    _dll.GetCursorPos.restype = c_int

    _dll.MiddleUp.argtypes = [c_int64]
    _dll.MiddleUp.restype = c_int

    _dll.MiddleDown.argtypes = [c_int64]
    _dll.MiddleDown.restype = c_int

    _dll.LeftClick.argtypes = [c_int64]
    _dll.LeftClick.restype = c_int

    _dll.LeftDoubleClick.argtypes = [c_int64]
    _dll.LeftDoubleClick.restype = c_int

    _dll.WheelUp.argtypes = [c_int64]
    _dll.WheelUp.restype = c_int

    _dll.WheelDown.argtypes = [c_int64]
    _dll.WheelDown.restype = c_int

    _dll.WaitKey.argtypes = [c_int64, c_int, c_int]
    _dll.WaitKey.restype = c_int

    _dll.EnableMouseAccuracy.argtypes = [c_int64, c_int]
    _dll.EnableMouseAccuracy.restype = c_int

    _dll.DoubleToData.argtypes = [c_int64, c_double]
    _dll.DoubleToData.restype = c_int64

    _dll.FloatToData.argtypes = [c_int64, c_float]
    _dll.FloatToData.restype = c_int64

    _dll.StringToData.argtypes = [c_int64, c_char_p, c_int]
    _dll.StringToData.restype = c_int64

    _dll.Int64ToInt32.argtypes = [c_int64, c_int64]
    _dll.Int64ToInt32.restype = c_int

    _dll.Int32ToInt64.argtypes = [c_int64, c_int]
    _dll.Int32ToInt64.restype = c_int64

    _dll.FindData.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.FindData.restype = c_int64

    _dll.FindDataEx.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int, c_int, c_int]
    _dll.FindDataEx.restype = c_int64

    _dll.FindDouble.argtypes = [c_int64, c_int64, c_char_p, c_double, c_double]
    _dll.FindDouble.restype = c_int64

    _dll.FindDoubleEx.argtypes = [c_int64, c_int64, c_char_p, c_double, c_double, c_int, c_int, c_int]
    _dll.FindDoubleEx.restype = c_int64

    _dll.FindFloat.argtypes = [c_int64, c_int64, c_char_p, c_float, c_float]
    _dll.FindFloat.restype = c_int64

    _dll.FindFloatEx.argtypes = [c_int64, c_int64, c_char_p, c_float, c_float, c_int, c_int, c_int]
    _dll.FindFloatEx.restype = c_int64

    _dll.FindInt.argtypes = [c_int64, c_int64, c_char_p, c_int64, c_int64, c_int]
    _dll.FindInt.restype = c_int64

    _dll.FindIntEx.argtypes = [c_int64, c_int64, c_char_p, c_int64, c_int64, c_int, c_int, c_int, c_int]
    _dll.FindIntEx.restype = c_int64

    _dll.FindString.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int]
    _dll.FindString.restype = c_int64

    _dll.FindStringEx.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int, c_int, c_int, c_int]
    _dll.FindStringEx.restype = c_int64

    _dll.ReadData.argtypes = [c_int64, c_int64, c_char_p, c_int]
    _dll.ReadData.restype = c_int64

    _dll.ReadDataAddr.argtypes = [c_int64, c_int64, c_int64, c_int]
    _dll.ReadDataAddr.restype = c_int64

    _dll.ReadDataAddrToBin.argtypes = [c_int64, c_int64, c_int64, c_int]
    _dll.ReadDataAddrToBin.restype = c_int64

    _dll.ReadDataToBin.argtypes = [c_int64, c_int64, c_char_p, c_int]
    _dll.ReadDataToBin.restype = c_int64

    _dll.ReadDouble.argtypes = [c_int64, c_int64, c_char_p]
    _dll.ReadDouble.restype = c_double

    _dll.ReadDoubleAddr.argtypes = [c_int64, c_int64, c_int64]
    _dll.ReadDoubleAddr.restype = c_double

    _dll.ReadFloat.argtypes = [c_int64, c_int64, c_char_p]
    _dll.ReadFloat.restype = c_float

    _dll.ReadFloatAddr.argtypes = [c_int64, c_int64, c_int64]
    _dll.ReadFloatAddr.restype = c_float

    _dll.ReadInt.argtypes = [c_int64, c_int64, c_char_p, c_int]
    _dll.ReadInt.restype = c_int64

    _dll.ReadIntAddr.argtypes = [c_int64, c_int64, c_int64, c_int]
    _dll.ReadIntAddr.restype = c_int64

    _dll.ReadString.argtypes = [c_int64, c_int64, c_char_p, c_int, c_int]
    _dll.ReadString.restype = c_int64

    _dll.ReadStringAddr.argtypes = [c_int64, c_int64, c_int64, c_int, c_int]
    _dll.ReadStringAddr.restype = c_int64

    _dll.WriteData.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.WriteData.restype = c_int

    _dll.WriteDataFromBin.argtypes = [c_int64, c_int64, c_char_p, c_int64, c_int]
    _dll.WriteDataFromBin.restype = c_int

    _dll.WriteDataAddr.argtypes = [c_int64, c_int64, c_int64, c_char_p]
    _dll.WriteDataAddr.restype = c_int

    _dll.WriteDataAddrFromBin.argtypes = [c_int64, c_int64, c_int64, c_int64, c_int]
    _dll.WriteDataAddrFromBin.restype = c_int

    _dll.WriteDouble.argtypes = [c_int64, c_int64, c_char_p, c_double]
    _dll.WriteDouble.restype = c_int

    _dll.WriteDoubleAddr.argtypes = [c_int64, c_int64, c_int64, c_double]
    _dll.WriteDoubleAddr.restype = c_int

    _dll.WriteFloat.argtypes = [c_int64, c_int64, c_char_p, c_float]
    _dll.WriteFloat.restype = c_int

    _dll.WriteFloatAddr.argtypes = [c_int64, c_int64, c_int64, c_float]
    _dll.WriteFloatAddr.restype = c_int

    _dll.WriteInt.argtypes = [c_int64, c_int64, c_char_p, c_int, c_int64]
    _dll.WriteInt.restype = c_int

    _dll.WriteIntAddr.argtypes = [c_int64, c_int64, c_int64, c_int, c_int64]
    _dll.WriteIntAddr.restype = c_int

    _dll.WriteString.argtypes = [c_int64, c_int64, c_char_p, c_int, c_char_p]
    _dll.WriteString.restype = c_int

    _dll.WriteStringAddr.argtypes = [c_int64, c_int64, c_int64, c_int, c_char_p]
    _dll.WriteStringAddr.restype = c_int

    _dll.SetMemoryHwndAsProcessId.argtypes = [c_int64, c_int]
    _dll.SetMemoryHwndAsProcessId.restype = c_int

    _dll.FreeProcessMemory.argtypes = [c_int64, c_int64]
    _dll.FreeProcessMemory.restype = c_int

    _dll.GetModuleBaseAddr.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetModuleBaseAddr.restype = c_int64

    _dll.GetModuleSize.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetModuleSize.restype = c_int

    _dll.GetRemoteApiAddress.argtypes = [c_int64, c_int64, c_int64, c_char_p]
    _dll.GetRemoteApiAddress.restype = c_int64

    _dll.VirtualAllocEx.argtypes = [c_int64, c_int64, c_int64, c_int, c_int]
    _dll.VirtualAllocEx.restype = c_int64

    _dll.VirtualFreeEx.argtypes = [c_int64, c_int64, c_int64]
    _dll.VirtualFreeEx.restype = c_int

    _dll.VirtualProtectEx.argtypes = [c_int64, c_int64, c_int64, c_int, c_int, c_int]
    _dll.VirtualProtectEx.restype = c_int

    _dll.VirtualQueryEx.argtypes = [c_int64, c_int64, c_int64, c_int64]
    _dll.VirtualQueryEx.restype = c_int64

    _dll.CreateRemoteThread.argtypes = [c_int64, c_int64, c_int64, c_int64, c_int, POINTER(c_int64)]
    _dll.CreateRemoteThread.restype = c_int64

    _dll.CloseHandle.argtypes = [c_int64, c_int64]
    _dll.CloseHandle.restype = c_int

    _dll.Ocr.argtypes = [c_int64, c_int, c_int, c_int, c_int]
    _dll.Ocr.restype = c_int64

    _dll.OcrFromPtr.argtypes = [c_int64, c_int64]
    _dll.OcrFromPtr.restype = c_int64

    _dll.OcrFromBmpData.argtypes = [c_int64, c_int64, c_int]
    _dll.OcrFromBmpData.restype = c_int64

    _dll.OcrDetails.argtypes = [c_int64, c_int, c_int, c_int, c_int]
    _dll.OcrDetails.restype = c_int64

    _dll.OcrFromPtrDetails.argtypes = [c_int64, c_int64]
    _dll.OcrFromPtrDetails.restype = c_int64

    _dll.OcrFromBmpDataDetails.argtypes = [c_int64, c_int64, c_int]
    _dll.OcrFromBmpDataDetails.restype = c_int64

    _dll.OcrV5.argtypes = [c_int64, c_int, c_int, c_int, c_int]
    _dll.OcrV5.restype = c_int64

    _dll.OcrV5Details.argtypes = [c_int64, c_int, c_int, c_int, c_int]
    _dll.OcrV5Details.restype = c_int64

    _dll.OcrV5FromPtr.argtypes = [c_int64, c_int64]
    _dll.OcrV5FromPtr.restype = c_int64

    _dll.OcrV5FromPtrDetails.argtypes = [c_int64, c_int64]
    _dll.OcrV5FromPtrDetails.restype = c_int64

    _dll.GetOcrConfig.argtypes = [c_int64, c_char_p]
    _dll.GetOcrConfig.restype = c_int64

    _dll.SetOcrConfig.argtypes = [c_int64, c_char_p]
    _dll.SetOcrConfig.restype = c_int

    _dll.SetOcrConfigByKey.argtypes = [c_int64, c_char_p, c_char_p]
    _dll.SetOcrConfigByKey.restype = c_int

    _dll.OcrFromDict.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_double]
    _dll.OcrFromDict.restype = c_int64

    _dll.OcrFromDictDetails.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_double]
    _dll.OcrFromDictDetails.restype = c_int64

    _dll.OcrFromDictPtr.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_double]
    _dll.OcrFromDictPtr.restype = c_int64

    _dll.OcrFromDictPtrDetails.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_double]
    _dll.OcrFromDictPtrDetails.restype = c_int64

    _dll.FindStr.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_char_p, c_double, POINTER(c_int), POINTER(c_int)]
    _dll.FindStr.restype = c_int

    _dll.FindStrDetail.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_char_p, c_double]
    _dll.FindStrDetail.restype = c_int64

    _dll.FindStrAll.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_char_p, c_double]
    _dll.FindStrAll.restype = c_int64

    _dll.FindStrFromPtr.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_char_p, c_double]
    _dll.FindStrFromPtr.restype = c_int64

    _dll.FindStrFromPtrAll.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_char_p, c_double]
    _dll.FindStrFromPtrAll.restype = c_int64

    _dll.FastNumberOcrFromPtr.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_double]
    _dll.FastNumberOcrFromPtr.restype = c_int

    _dll.FastNumberOcr.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_double]
    _dll.FastNumberOcr.restype = c_int

    _dll.Capture.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p]
    _dll.Capture.restype = c_int

    _dll.GetScreenDataBmp.argtypes = [c_int64, c_int, c_int, c_int, c_int, POINTER(c_int64), POINTER(c_int)]
    _dll.GetScreenDataBmp.restype = c_int

    _dll.GetScreenData.argtypes = [c_int64, c_int, c_int, c_int, c_int, POINTER(c_int64), POINTER(c_int), POINTER(c_int)]
    _dll.GetScreenData.restype = c_int

    _dll.GetScreenDataPtr.argtypes = [c_int64, c_int, c_int, c_int, c_int]
    _dll.GetScreenDataPtr.restype = c_int64

    _dll.CaptureGif.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_int, c_int]
    _dll.CaptureGif.restype = c_int

    _dll.GetImageData.argtypes = [c_int64, c_int64, POINTER(c_int64), POINTER(c_int), POINTER(c_int)]
    _dll.GetImageData.restype = c_int

    _dll.MatchImageFromPath.argtypes = [c_int64, c_char_p, c_char_p, c_double, c_int, c_double, c_double]
    _dll.MatchImageFromPath.restype = c_int64

    _dll.MatchImageFromPathAll.argtypes = [c_int64, c_char_p, c_char_p, c_double, c_int, c_double, c_double]
    _dll.MatchImageFromPathAll.restype = c_int64

    _dll.MatchImagePtrFromPath.argtypes = [c_int64, c_int64, c_char_p, c_double, c_int, c_double, c_double]
    _dll.MatchImagePtrFromPath.restype = c_int64

    _dll.MatchImagePtrFromPathAll.argtypes = [c_int64, c_int64, c_char_p, c_double, c_int, c_double, c_double]
    _dll.MatchImagePtrFromPathAll.restype = c_int64

    _dll.GetColor.argtypes = [c_int64, c_int, c_int]
    _dll.GetColor.restype = c_int64

    _dll.GetColorPtr.argtypes = [c_int64, c_int64, c_int, c_int]
    _dll.GetColorPtr.restype = c_int64

    _dll.CopyImage.argtypes = [c_int64, c_int64]
    _dll.CopyImage.restype = c_int64

    _dll.FreeImagePath.argtypes = [c_int64, c_char_p]
    _dll.FreeImagePath.restype = c_int

    _dll.FreeImageAll.argtypes = [c_int64]
    _dll.FreeImageAll.restype = c_int

    _dll.LoadImage.argtypes = [c_int64, c_char_p]
    _dll.LoadImage.restype = c_int64

    _dll.LoadImageFromBmpData.argtypes = [c_int64, c_int64, c_int]
    _dll.LoadImageFromBmpData.restype = c_int64

    _dll.LoadImageFromRGBData.argtypes = [c_int64, c_int, c_int, c_int64, c_int]
    _dll.LoadImageFromRGBData.restype = c_int64

    _dll.FreeImagePtr.argtypes = [c_int64, c_int64]
    _dll.FreeImagePtr.restype = c_int

    _dll.MatchWindowsFromPtr.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_int64, c_double, c_int, c_double, c_double]
    _dll.MatchWindowsFromPtr.restype = c_int64

    _dll.MatchImageFromPtr.argtypes = [c_int64, c_int64, c_int64, c_double, c_int, c_double, c_double]
    _dll.MatchImageFromPtr.restype = c_int64

    _dll.MatchImageFromPtrAll.argtypes = [c_int64, c_int64, c_int64, c_double, c_int, c_double, c_double]
    _dll.MatchImageFromPtrAll.restype = c_int64

    _dll.MatchWindowsFromPtrAll.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_int64, c_double, c_int, c_double, c_double]
    _dll.MatchWindowsFromPtrAll.restype = c_int64

    _dll.MatchWindowsFromPath.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_double, c_int, c_double, c_double]
    _dll.MatchWindowsFromPath.restype = c_int64

    _dll.MatchWindowsFromPathAll.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_double, c_int, c_double, c_double]
    _dll.MatchWindowsFromPathAll.restype = c_int64

    _dll.MatchWindowsThresholdFromPtr.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_int64, c_double, c_double, c_double]
    _dll.MatchWindowsThresholdFromPtr.restype = c_int64

    _dll.MatchWindowsThresholdFromPtrAll.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_int64, c_double, c_double, c_double]
    _dll.MatchWindowsThresholdFromPtrAll.restype = c_int64

    _dll.MatchWindowsThresholdFromPath.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_double, c_double, c_double]
    _dll.MatchWindowsThresholdFromPath.restype = c_int64

    _dll.MatchWindowsThresholdFromPathAll.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_double, c_double, c_double]
    _dll.MatchWindowsThresholdFromPathAll.restype = c_int64

    _dll.ShowMatchWindow.argtypes = [c_int64, c_int]
    _dll.ShowMatchWindow.restype = c_int

    _dll.CalculateSSIM.argtypes = [c_int64, c_int64, c_int64]
    _dll.CalculateSSIM.restype = c_double

    _dll.CalculateHistograms.argtypes = [c_int64, c_int64, c_int64]
    _dll.CalculateHistograms.restype = c_double

    _dll.CalculateMSE.argtypes = [c_int64, c_int64, c_int64]
    _dll.CalculateMSE.restype = c_double

    _dll.SaveImageFromPtr.argtypes = [c_int64, c_int64, c_char_p]
    _dll.SaveImageFromPtr.restype = c_int

    _dll.ReSize.argtypes = [c_int64, c_int64, c_int, c_int]
    _dll.ReSize.restype = c_int64

    _dll.FindColor.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_int, POINTER(c_int), POINTER(c_int)]
    _dll.FindColor.restype = c_int

    _dll.FindColorList.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p]
    _dll.FindColorList.restype = c_int64

    _dll.FindMultiColor.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p, c_int, POINTER(c_int), POINTER(c_int)]
    _dll.FindMultiColor.restype = c_int

    _dll.FindMultiColorList.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_char_p]
    _dll.FindMultiColorList.restype = c_int64

    _dll.FindMultiColorFromPtr.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int, POINTER(c_int), POINTER(c_int)]
    _dll.FindMultiColorFromPtr.restype = c_int

    _dll.FindMultiColorListFromPtr.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.FindMultiColorListFromPtr.restype = c_int64

    _dll.GetImageSize.argtypes = [c_int64, c_int64, POINTER(c_int), POINTER(c_int)]
    _dll.GetImageSize.restype = c_int

    _dll.FindColorBlock.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_int, c_int, c_int, POINTER(c_int), POINTER(c_int)]
    _dll.FindColorBlock.restype = c_int

    _dll.FindColorBlockPtr.argtypes = [c_int64, c_int64, c_char_p, c_int, c_int, c_int, POINTER(c_int), POINTER(c_int)]
    _dll.FindColorBlockPtr.restype = c_int

    _dll.FindColorBlockList.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_int, c_int, c_int, c_int]
    _dll.FindColorBlockList.restype = c_int64

    _dll.FindColorBlockListPtr.argtypes = [c_int64, c_int64, c_char_p, c_int, c_int, c_int, c_int]
    _dll.FindColorBlockListPtr.restype = c_int64

    _dll.GetColorNum.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p]
    _dll.GetColorNum.restype = c_int

    _dll.GetColorNumPtr.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetColorNumPtr.restype = c_int

    _dll.Cropped.argtypes = [c_int64, c_int64, c_int, c_int, c_int, c_int]
    _dll.Cropped.restype = c_int64

    _dll.GetThresholdImageFromMultiColorPtr.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetThresholdImageFromMultiColorPtr.restype = c_int64

    _dll.GetThresholdImageFromMultiColor.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p]
    _dll.GetThresholdImageFromMultiColor.restype = c_int64

    _dll.IsSameImage.argtypes = [c_int64, c_int64, c_int64]
    _dll.IsSameImage.restype = c_int

    _dll.ShowImage.argtypes = [c_int64, c_int64]
    _dll.ShowImage.restype = c_int

    _dll.ShowImageFromFile.argtypes = [c_int64, c_char_p]
    _dll.ShowImageFromFile.restype = c_int

    _dll.SetColorsToNewColor.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.SetColorsToNewColor.restype = c_int64

    _dll.RemoveOtherColors.argtypes = [c_int64, c_int64, c_char_p]
    _dll.RemoveOtherColors.restype = c_int64

    _dll.DrawRectangle.argtypes = [c_int64, c_int64, c_int, c_int, c_int, c_int, c_int, c_char_p]
    _dll.DrawRectangle.restype = c_int64

    _dll.DrawCircle.argtypes = [c_int64, c_int64, c_int, c_int, c_int, c_int, c_char_p]
    _dll.DrawCircle.restype = c_int64

    _dll.DrawFillPoly.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.DrawFillPoly.restype = c_int64

    _dll.DecodeQRCode.argtypes = [c_int64, c_int64]
    _dll.DecodeQRCode.restype = c_int64

    _dll.CreateQRCode.argtypes = [c_int64, c_char_p, c_int]
    _dll.CreateQRCode.restype = c_int64

    _dll.CreateQRCodeEx.argtypes = [c_int64, c_char_p, c_int, c_int, c_int, c_int, c_int]
    _dll.CreateQRCodeEx.restype = c_int64

    _dll.MatchAnimationFromPtr.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_int64, c_double, c_int, c_double, c_double, c_int, c_int, c_int]
    _dll.MatchAnimationFromPtr.restype = c_int64

    _dll.MatchAnimationFromPath.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_char_p, c_double, c_int, c_double, c_double, c_int, c_int, c_int]
    _dll.MatchAnimationFromPath.restype = c_int64

    _dll.RemoveImageDiff.argtypes = [c_int64, c_int64, c_int64]
    _dll.RemoveImageDiff.restype = c_int64

    _dll.GetImageBmpData.argtypes = [c_int64, c_int64, POINTER(c_int64), POINTER(c_int)]
    _dll.GetImageBmpData.restype = c_int

    _dll.FreeImageData.argtypes = [c_int64, c_int64]
    _dll.FreeImageData.restype = c_int

    _dll.ScalePixels.argtypes = [c_int64, c_int64, c_int]
    _dll.ScalePixels.restype = c_int64

    _dll.CreateImage.argtypes = [c_int64, c_int, c_int, c_char_p]
    _dll.CreateImage.restype = c_int64

    _dll.SetPixel.argtypes = [c_int64, c_int64, c_int, c_int, c_char_p]
    _dll.SetPixel.restype = c_int

    _dll.SetPixelList.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.SetPixelList.restype = c_int

    _dll.ConcatImage.argtypes = [c_int64, c_int64, c_int64, c_int, c_char_p, c_int]
    _dll.ConcatImage.restype = c_int64

    _dll.CoverImage.argtypes = [c_int64, c_int64, c_int64, c_int, c_int, c_double]
    _dll.CoverImage.restype = c_int64

    _dll.RotateImage.argtypes = [c_int64, c_int64, c_double]
    _dll.RotateImage.restype = c_int64

    _dll.ImageToBase64.argtypes = [c_int64, c_int64]
    _dll.ImageToBase64.restype = c_int64

    _dll.Base64ToImage.argtypes = [c_int64, c_char_p]
    _dll.Base64ToImage.restype = c_int64

    _dll.Hex2ARGB.argtypes = [c_int64, c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    _dll.Hex2ARGB.restype = c_int

    _dll.Hex2RGB.argtypes = [c_int64, c_char_p, POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    _dll.Hex2RGB.restype = c_int

    _dll.ARGB2Hex.argtypes = [c_int64, c_int, c_int, c_int, c_int]
    _dll.ARGB2Hex.restype = c_int64

    _dll.RGB2Hex.argtypes = [c_int64, c_int, c_int, c_int]
    _dll.RGB2Hex.restype = c_int64

    _dll.Hex2HSV.argtypes = [c_int64, c_char_p]
    _dll.Hex2HSV.restype = c_int64

    _dll.RGB2HSV.argtypes = [c_int64, c_int, c_int, c_int]
    _dll.RGB2HSV.restype = c_int64

    _dll.CmpColor.argtypes = [c_int64, c_int, c_int, c_char_p, c_char_p]
    _dll.CmpColor.restype = c_int

    _dll.CmpColorPtr.argtypes = [c_int64, c_int64, c_int, c_int, c_char_p, c_char_p]
    _dll.CmpColorPtr.restype = c_int

    _dll.CmpColorHex.argtypes = [c_int64, c_char_p, c_char_p, c_char_p]
    _dll.CmpColorHex.restype = c_int

    _dll.GetConnectedComponents.argtypes = [c_int64, c_int64, c_char_p, c_int]
    _dll.GetConnectedComponents.restype = c_int64

    _dll.DetectPointerDirection.argtypes = [c_int64, c_int64, c_int, c_int]
    _dll.DetectPointerDirection.restype = c_double

    _dll.DetectPointerDirectionByFeatures.argtypes = [c_int64, c_int64, c_int64, c_int, c_int, c_bool]
    _dll.DetectPointerDirectionByFeatures.restype = c_double

    _dll.FastMatch.argtypes = [c_int64, c_int64, c_int64, c_double, c_int, c_double, c_double]
    _dll.FastMatch.restype = c_int64

    _dll.FastROI.argtypes = [c_int64, c_int64]
    _dll.FastROI.restype = c_int64

    _dll.GetROIRegion.argtypes = [c_int64, c_int64, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    _dll.GetROIRegion.restype = c_int

    _dll.GetForegroundPoints.argtypes = [c_int64, c_int64]
    _dll.GetForegroundPoints.restype = c_int64

    _dll.ConvertColor.argtypes = [c_int64, c_int64, c_int]
    _dll.ConvertColor.restype = c_int64

    _dll.Threshold.argtypes = [c_int64, c_int64, c_double, c_double, c_int]
    _dll.Threshold.restype = c_int64

    _dll.RemoveIslands.argtypes = [c_int64, c_int64, c_int]
    _dll.RemoveIslands.restype = c_int64

    _dll.MorphGradient.argtypes = [c_int64, c_int64, c_int]
    _dll.MorphGradient.restype = c_int64

    _dll.MorphTophat.argtypes = [c_int64, c_int64, c_int]
    _dll.MorphTophat.restype = c_int64

    _dll.MorphBlackhat.argtypes = [c_int64, c_int64, c_int]
    _dll.MorphBlackhat.restype = c_int64

    _dll.Dilation.argtypes = [c_int64, c_int64, c_int]
    _dll.Dilation.restype = c_int64

    _dll.Erosion.argtypes = [c_int64, c_int64, c_int]
    _dll.Erosion.restype = c_int64

    _dll.GaussianBlur.argtypes = [c_int64, c_int64, c_int]
    _dll.GaussianBlur.restype = c_int64

    _dll.Sharpen.argtypes = [c_int64, c_int64]
    _dll.Sharpen.restype = c_int64

    _dll.CannyEdge.argtypes = [c_int64, c_int64, c_int]
    _dll.CannyEdge.restype = c_int64

    _dll.Flip.argtypes = [c_int64, c_int64, c_int]
    _dll.Flip.restype = c_int64

    _dll.MorphOpen.argtypes = [c_int64, c_int64, c_int]
    _dll.MorphOpen.restype = c_int64

    _dll.MorphClose.argtypes = [c_int64, c_int64, c_int]
    _dll.MorphClose.restype = c_int64

    _dll.Skeletonize.argtypes = [c_int64, c_int64]
    _dll.Skeletonize.restype = c_int64

    _dll.ImageStitchFromPath.argtypes = [c_int64, c_char_p, POINTER(c_int64)]
    _dll.ImageStitchFromPath.restype = c_int64

    _dll.ImageStitchCreate.argtypes = [c_int64]
    _dll.ImageStitchCreate.restype = c_int64

    _dll.ImageStitchAppend.argtypes = [c_int64, c_int64, c_int64]
    _dll.ImageStitchAppend.restype = c_int

    _dll.ImageStitchGetResult.argtypes = [c_int64, c_int64, POINTER(c_int64)]
    _dll.ImageStitchGetResult.restype = c_int64

    _dll.ImageStitchFree.argtypes = [c_int64, c_int64]
    _dll.ImageStitchFree.restype = c_int

    # _dll.CreateDatabase.argtypes = [c_int64, c_char_p, c_char_p]
    # _dll.CreateDatabase.restype = c_int64

    _dll.OpenDatabase.argtypes = [c_int64, c_char_p, c_char_p]
    _dll.OpenDatabase.restype = c_int64

    _dll.GetDatabaseError.argtypes = [c_int64, c_int64]
    _dll.GetDatabaseError.restype = c_int64

    _dll.CloseDatabase.argtypes = [c_int64, c_int64]
    _dll.CloseDatabase.restype = c_int

    _dll.GetAllTableNames.argtypes = [c_int64, c_int64]
    _dll.GetAllTableNames.restype = c_int64

    _dll.GetTableInfo.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetTableInfo.restype = c_int64

    _dll.GetTableInfoDetail.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetTableInfoDetail.restype = c_int64

    _dll.ExecuteSql.argtypes = [c_int64, c_int64, c_char_p]
    _dll.ExecuteSql.restype = c_int

    _dll.ExecuteScalar.argtypes = [c_int64, c_int64, c_char_p]
    _dll.ExecuteScalar.restype = c_int

    _dll.ExecuteReader.argtypes = [c_int64, c_int64, c_char_p]
    _dll.ExecuteReader.restype = c_int64

    _dll.Read.argtypes = [c_int64, c_int64]
    _dll.Read.restype = c_int

    _dll.GetDataCount.argtypes = [c_int64, c_int64]
    _dll.GetDataCount.restype = c_int

    _dll.GetColumnCount.argtypes = [c_int64, c_int64]
    _dll.GetColumnCount.restype = c_int

    _dll.GetColumnName.argtypes = [c_int64, c_int64, c_int]
    _dll.GetColumnName.restype = c_int64

    _dll.GetColumnIndex.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetColumnIndex.restype = c_int

    _dll.GetColumnType.argtypes = [c_int64, c_int64, c_int]
    _dll.GetColumnType.restype = c_int

    _dll.Finalize.argtypes = [c_int64, c_int64]
    _dll.Finalize.restype = c_int

    _dll.GetDouble.argtypes = [c_int64, c_int64, c_int]
    _dll.GetDouble.restype = c_double

    _dll.GetInt32.argtypes = [c_int64, c_int64, c_int]
    _dll.GetInt32.restype = c_int

    _dll.GetInt64.argtypes = [c_int64, c_int64, c_int]
    _dll.GetInt64.restype = c_int64

    _dll.GetString.argtypes = [c_int64, c_int64, c_int]
    _dll.GetString.restype = c_int64

    _dll.GetDoubleByColumnName.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetDoubleByColumnName.restype = c_double

    _dll.GetInt32ByColumnName.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetInt32ByColumnName.restype = c_int

    _dll.GetInt64ByColumnName.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetInt64ByColumnName.restype = c_int64

    _dll.GetStringByColumnName.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetStringByColumnName.restype = c_int64

    _dll.InitOlaDatabase.argtypes = [c_int64, c_int64]
    _dll.InitOlaDatabase.restype = c_int

    _dll.InitOlaImageFromDir.argtypes = [c_int64, c_int64, c_char_p, c_int]
    _dll.InitOlaImageFromDir.restype = c_int

    _dll.RemoveOlaImageFromDir.argtypes = [c_int64, c_int64, c_char_p]
    _dll.RemoveOlaImageFromDir.restype = c_int

    _dll.ExportOlaImageDir.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.ExportOlaImageDir.restype = c_int

    _dll.ImportOlaImage.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int]
    _dll.ImportOlaImage.restype = c_int

    _dll.GetOlaImage.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.GetOlaImage.restype = c_int64

    _dll.RemoveOlaImage.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.RemoveOlaImage.restype = c_int

    _dll.SetDbConfig.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.SetDbConfig.restype = c_int

    _dll.GetDbConfig.argtypes = [c_int64, c_int64, c_char_p]
    _dll.GetDbConfig.restype = c_int64

    _dll.RemoveDbConfig.argtypes = [c_int64, c_int64, c_char_p]
    _dll.RemoveDbConfig.restype = c_int

    _dll.SetDbConfigEx.argtypes = [c_int64, c_char_p, c_char_p]
    _dll.SetDbConfigEx.restype = c_int

    _dll.GetDbConfigEx.argtypes = [c_int64, c_char_p]
    _dll.GetDbConfigEx.restype = c_int64

    _dll.RemoveDbConfigEx.argtypes = [c_int64, c_char_p]
    _dll.RemoveDbConfigEx.restype = c_int

    _dll.InitDictFromDir.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int]
    _dll.InitDictFromDir.restype = c_int

    _dll.ImportDictWord.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int]
    _dll.ImportDictWord.restype = c_int

    _dll.ExportDict.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.ExportDict.restype = c_int

    _dll.RemoveDict.argtypes = [c_int64, c_int64, c_char_p]
    _dll.RemoveDict.restype = c_int

    _dll.RemoveDictWord.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.RemoveDictWord.restype = c_int

    _dll.GetDictImage.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int, c_int]
    _dll.GetDictImage.restype = c_int64

    _dll.SetWindowState.argtypes = [c_int64, c_int64, c_int]
    _dll.SetWindowState.restype = c_int

    _dll.FindWindow.argtypes = [c_int64, c_char_p, c_char_p]
    _dll.FindWindow.restype = c_int64

    _dll.GetClipboard.argtypes = [c_int64]
    _dll.GetClipboard.restype = c_int64

    _dll.SetClipboard.argtypes = [c_int64, c_char_p]
    _dll.SetClipboard.restype = c_int

    _dll.SendPaste.argtypes = [c_int64, c_int64]
    _dll.SendPaste.restype = c_int

    _dll.GetWindow.argtypes = [c_int64, c_int64, c_int]
    _dll.GetWindow.restype = c_int64

    _dll.GetWindowTitle.argtypes = [c_int64, c_int64]
    _dll.GetWindowTitle.restype = c_int64

    _dll.GetWindowClass.argtypes = [c_int64, c_int64]
    _dll.GetWindowClass.restype = c_int64

    _dll.GetWindowRect.argtypes = [c_int64, c_int64, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    _dll.GetWindowRect.restype = c_int

    _dll.GetWindowProcessPath.argtypes = [c_int64, c_int64]
    _dll.GetWindowProcessPath.restype = c_int64

    _dll.GetWindowState.argtypes = [c_int64, c_int64, c_int]
    _dll.GetWindowState.restype = c_int

    _dll.GetForegroundWindow.argtypes = [c_int64]
    _dll.GetForegroundWindow.restype = c_int64

    _dll.GetWindowProcessId.argtypes = [c_int64, c_int64]
    _dll.GetWindowProcessId.restype = c_int

    _dll.GetClientSize.argtypes = [c_int64, c_int64, POINTER(c_int), POINTER(c_int)]
    _dll.GetClientSize.restype = c_int

    _dll.GetMousePointWindow.argtypes = [c_int64]
    _dll.GetMousePointWindow.restype = c_int64

    _dll.GetSpecialWindow.argtypes = [c_int64, c_int]
    _dll.GetSpecialWindow.restype = c_int64

    _dll.GetClientRect.argtypes = [c_int64, c_int64, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)]
    _dll.GetClientRect.restype = c_int

    _dll.SetWindowText.argtypes = [c_int64, c_int64, c_char_p]
    _dll.SetWindowText.restype = c_int

    _dll.SetWindowSize.argtypes = [c_int64, c_int64, c_int, c_int]
    _dll.SetWindowSize.restype = c_int

    _dll.SetClientSize.argtypes = [c_int64, c_int64, c_int, c_int]
    _dll.SetClientSize.restype = c_int

    _dll.SetWindowTransparent.argtypes = [c_int64, c_int64, c_int]
    _dll.SetWindowTransparent.restype = c_int

    _dll.FindWindowEx.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.FindWindowEx.restype = c_int64

    _dll.FindWindowByProcess.argtypes = [c_int64, c_char_p, c_char_p, c_char_p]
    _dll.FindWindowByProcess.restype = c_int64

    _dll.MoveWindow.argtypes = [c_int64, c_int64, c_int, c_int]
    _dll.MoveWindow.restype = c_int

    _dll.GetScaleFromWindows.argtypes = [c_int64, c_int64]
    _dll.GetScaleFromWindows.restype = c_double

    _dll.GetWindowDpiAwarenessScale.argtypes = [c_int64, c_int64]
    _dll.GetWindowDpiAwarenessScale.restype = c_double

    _dll.EnumProcess.argtypes = [c_int64, c_char_p]
    _dll.EnumProcess.restype = c_int64

    _dll.EnumWindow.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int]
    _dll.EnumWindow.restype = c_int64

    _dll.EnumWindowByProcess.argtypes = [c_int64, c_char_p, c_char_p, c_char_p, c_int]
    _dll.EnumWindowByProcess.restype = c_int64

    _dll.EnumWindowByProcessId.argtypes = [c_int64, c_int64, c_char_p, c_char_p, c_int]
    _dll.EnumWindowByProcessId.restype = c_int64

    _dll.EnumWindowSuper.argtypes = [c_int64, c_char_p, c_int, c_int, c_char_p, c_int, c_int, c_int]
    _dll.EnumWindowSuper.restype = c_int64

    _dll.GetPointWindow.argtypes = [c_int64, c_int, c_int]
    _dll.GetPointWindow.restype = c_int64

    _dll.GetProcessInfo.argtypes = [c_int64, c_int64]
    _dll.GetProcessInfo.restype = c_int64

    _dll.ShowTaskBarIcon.argtypes = [c_int64, c_int64, c_int]
    _dll.ShowTaskBarIcon.restype = c_int

    _dll.FindWindowByProcessId.argtypes = [c_int64, c_int64, c_char_p, c_char_p]
    _dll.FindWindowByProcessId.restype = c_int64

    _dll.GetWindowThreadId.argtypes = [c_int64, c_int64]
    _dll.GetWindowThreadId.restype = c_int64

    _dll.FindWindowSuper.argtypes = [c_int64, c_char_p, c_int, c_int, c_char_p, c_int, c_int]
    _dll.FindWindowSuper.restype = c_int64

    _dll.ClientToScreen.argtypes = [c_int64, c_int64, POINTER(c_int), POINTER(c_int)]
    _dll.ClientToScreen.restype = c_int

    _dll.ScreenToClient.argtypes = [c_int64, c_int64, POINTER(c_int), POINTER(c_int)]
    _dll.ScreenToClient.restype = c_int

    _dll.GetForegroundFocus.argtypes = [c_int64]
    _dll.GetForegroundFocus.restype = c_int64

    _dll.SetWindowDisplay.argtypes = [c_int64, c_int64, c_int]
    _dll.SetWindowDisplay.restype = c_int

    _dll.IsDisplayDead.argtypes = [c_int64, c_int, c_int, c_int, c_int, c_int]
    _dll.IsDisplayDead.restype = c_int

    _dll.GetWindowsFps.argtypes = [c_int64, c_int, c_int, c_int, c_int]
    _dll.GetWindowsFps.restype = c_int

    _dll.TerminateProcess.argtypes = [c_int64, c_int64]
    _dll.TerminateProcess.restype = c_int

    _dll.TerminateProcessTree.argtypes = [c_int64, c_int64]
    _dll.TerminateProcessTree.restype = c_int

    _dll.GetCommandLine.argtypes = [c_int64, c_int64]
    _dll.GetCommandLine.restype = c_int64

    _dll.CheckFontSmooth.argtypes = [c_int64]
    _dll.CheckFontSmooth.restype = c_int

    _dll.SetFontSmooth.argtypes = [c_int64, c_int]
    _dll.SetFontSmooth.restype = c_int

    _dll.EnableDebugPrivilege.argtypes = [c_int64]
    _dll.EnableDebugPrivilege.restype = c_int

    _dll.SystemStart.argtypes = [c_int64, c_char_p, c_char_p]
    _dll.SystemStart.restype = c_int

    _dll.CreateChildProcess.argtypes = [c_int64, c_char_p, c_char_p, c_char_p, c_int, c_int]
    _dll.CreateChildProcess.restype = c_int

    @classmethod
    def CreateCOLAPlugInterFace(cls):
        return cls._dll.CreateCOLAPlugInterFace()

    @classmethod
    def DestroyCOLAPlugInterFace(cls, instance):
        return cls._dll.DestroyCOLAPlugInterFace(instance)

    @classmethod
    def Ver(cls):
        return cls._dll.Ver()

    @classmethod
    def SetPath(cls, instance, path):
        return cls._dll.SetPath(instance, path.encode("utf-8"))

    @classmethod
    def GetPath(cls, instance):
        return cls._dll.GetPath(instance)

    @classmethod
    def GetMachineCode(cls, instance):
        return cls._dll.GetMachineCode(instance)

    @classmethod
    def GetBasePath(cls, instance):
        return cls._dll.GetBasePath(instance)

    @classmethod
    def Reg(cls, userCode, softCode, featureList):
        return cls._dll.Reg(userCode.encode("utf-8"), softCode.encode("utf-8"), featureList.encode("utf-8"))

    @classmethod
    def BindWindow(cls, instance, hwnd, display, mouse, keypad, mode):
        return cls._dll.BindWindow(instance, hwnd, display.encode("utf-8"), mouse.encode("utf-8"), keypad.encode("utf-8"), mode)

    @classmethod
    def BindWindowEx(cls, instance, hwnd, display, mouse, keypad, pubstr, mode):
        return cls._dll.BindWindowEx(instance, hwnd, display.encode("utf-8"), mouse.encode("utf-8"), keypad.encode("utf-8"), pubstr.encode("utf-8"), mode)

    @classmethod
    def UnBindWindow(cls, instance):
        return cls._dll.UnBindWindow(instance)

    @classmethod
    def GetBindWindow(cls, instance):
        return cls._dll.GetBindWindow(instance)

    @classmethod
    def ReleaseWindowsDll(cls, instance, hwnd):
        return cls._dll.ReleaseWindowsDll(instance, hwnd)

    @classmethod
    def FreeStringPtr(cls, ptr):
        return cls._dll.FreeStringPtr(ptr)

    @classmethod
    def FreeMemoryPtr(cls, ptr):
        return cls._dll.FreeMemoryPtr(ptr)

    @classmethod
    def GetStringSize(cls, ptr):
        return cls._dll.GetStringSize(ptr)

    @classmethod
    def GetStringFromPtr(cls, ptr, lpString, size):
        return cls._dll.GetStringFromPtr(ptr, lpString.encode("utf-8"), size)

    @classmethod
    def Delay(cls, millisecond):
        return cls._dll.Delay(millisecond)

    @classmethod
    def Delays(cls, minMillisecond, maxMillisecond):
        return cls._dll.Delays(minMillisecond, maxMillisecond)

    @classmethod
    def SetUAC(cls, instance, enable):
        return cls._dll.SetUAC(instance, enable)

    @classmethod
    def CheckUAC(cls, instance):
        return cls._dll.CheckUAC(instance)

    @classmethod
    def RunApp(cls, instance, appPath, mode):
        return cls._dll.RunApp(instance, appPath.encode("utf-8"), mode)

    @classmethod
    def ExecuteCmd(cls, instance, cmd, current_dir, time_out):
        return cls._dll.ExecuteCmd(instance, cmd.encode("utf-8"), current_dir.encode("utf-8"), time_out)

    @classmethod
    def GetConfig(cls, instance, configKey):
        return cls._dll.GetConfig(instance, configKey.encode("utf-8"))

    @classmethod
    def SetConfig(cls, instance, configStr):
        return cls._dll.SetConfig(instance, configStr.encode("utf-8"))

    @classmethod
    def SetConfigByKey(cls, instance, key, value):
        return cls._dll.SetConfigByKey(instance, key.encode("utf-8"), value.encode("utf-8"))

    @classmethod
    def SendDropFiles(cls, instance, hwnd, file_path):
        return cls._dll.SendDropFiles(instance, hwnd, file_path.encode("utf-8"))

    @classmethod
    def GetRandomNumber(cls, instance, _min, _max):
        return cls._dll.GetRandomNumber(instance, _min, _max)

    @classmethod
    def GetRandomDouble(cls, instance, _min, _max):
        return cls._dll.GetRandomDouble(instance, _min, _max)

    @classmethod
    def ExcludePos(cls, instance, _json, _type, x1, y1, x2, y2):
        return cls._dll.ExcludePos(instance, _json.encode("utf-8"), _type, x1, y1, x2, y2)

    @classmethod
    def FindNearestPos(cls, instance, _json, _type, x, y):
        return cls._dll.FindNearestPos(instance, _json.encode("utf-8"), _type, x, y)

    @classmethod
    def SortPosDistance(cls, instance, _json, _type, x, y):
        return cls._dll.SortPosDistance(instance, _json.encode("utf-8"), _type, x, y)

    @classmethod
    def GetDenseRect(cls, instance, image, width, height, x1 = None, y1 = None, x2 = None, y2 = None):
        x1 = c_int(0)
        y1 = c_int(0)
        x2 = c_int(0)
        y2 = c_int(0)
        result = cls._dll.GetDenseRect(instance, image, width, height, byref(x1), byref(y1), byref(x2), byref(y2))
        return result, x1.value, y1.value, x2.value, y2.value

    @classmethod
    def PathPlanning(cls, instance, image, startX, startY, endX, endY, potentialRadius, searchRadius):
        return cls._dll.PathPlanning(instance, image, startX, startY, endX, endY, potentialRadius, searchRadius)

    @classmethod
    def CreateGraph(cls, instance, _json):
        return cls._dll.CreateGraph(instance, _json.encode("utf-8"))

    @classmethod
    def GetGraph(cls, instance, graphPtr):
        return cls._dll.GetGraph(instance, graphPtr)

    @classmethod
    def AddEdge(cls, instance, graphPtr, _from, to, weight, isDirected):
        return cls._dll.AddEdge(instance, graphPtr, _from.encode("utf-8"), to.encode("utf-8"), weight, isDirected)

    @classmethod
    def GetShortestPath(cls, instance, graphPtr, _from, to):
        return cls._dll.GetShortestPath(instance, graphPtr, _from.encode("utf-8"), to.encode("utf-8"))

    @classmethod
    def GetShortestDistance(cls, instance, graphPtr, _from, to):
        return cls._dll.GetShortestDistance(instance, graphPtr, _from.encode("utf-8"), to.encode("utf-8"))

    @classmethod
    def ClearGraph(cls, instance, graphPtr):
        return cls._dll.ClearGraph(instance, graphPtr)

    @classmethod
    def DeleteGraph(cls, instance, graphPtr):
        return cls._dll.DeleteGraph(instance, graphPtr)

    @classmethod
    def GetNodeCount(cls, instance, graphPtr):
        return cls._dll.GetNodeCount(instance, graphPtr)

    @classmethod
    def GetEdgeCount(cls, instance, graphPtr):
        return cls._dll.GetEdgeCount(instance, graphPtr)

    @classmethod
    def GetShortestPathToAllNodes(cls, instance, graphPtr, startNode):
        return cls._dll.GetShortestPathToAllNodes(instance, graphPtr, startNode.encode("utf-8"))

    @classmethod
    def GetMinimumSpanningTree(cls, instance, graphPtr):
        return cls._dll.GetMinimumSpanningTree(instance, graphPtr)

    @classmethod
    def GetDirectedPathToAllNodes(cls, instance, graphPtr, startNode):
        return cls._dll.GetDirectedPathToAllNodes(instance, graphPtr, startNode.encode("utf-8"))

    @classmethod
    def GetMinimumArborescence(cls, instance, graphPtr, root):
        return cls._dll.GetMinimumArborescence(instance, graphPtr, root.encode("utf-8"))

    @classmethod
    def CreateGraphFromCoordinates(cls, instance, _json, connectAll, maxDistance, useEuclideanDistance):
        return cls._dll.CreateGraphFromCoordinates(instance, _json.encode("utf-8"), connectAll, maxDistance, useEuclideanDistance)

    @classmethod
    def AddCoordinateNode(cls, instance, graphPtr, name, x, y, connectToExisting, maxDistance, useEuclideanDistance):
        return cls._dll.AddCoordinateNode(instance, graphPtr, name.encode("utf-8"), x, y, connectToExisting, maxDistance, useEuclideanDistance)

    @classmethod
    def GetNodeCoordinates(cls, instance, graphPtr, name):
        return cls._dll.GetNodeCoordinates(instance, graphPtr, name.encode("utf-8"))

    @classmethod
    def SetNodeConnection(cls, instance, graphPtr, _from, to, canConnect, weight):
        return cls._dll.SetNodeConnection(instance, graphPtr, _from.encode("utf-8"), to.encode("utf-8"), canConnect, weight)

    @classmethod
    def GetNodeConnectionStatus(cls, instance, graphPtr, _from, to):
        return cls._dll.GetNodeConnectionStatus(instance, graphPtr, _from.encode("utf-8"), to.encode("utf-8"))

    @classmethod
    def AsmCall(cls, instance, hwnd, asmStr, _type, baseAddr):
        return cls._dll.AsmCall(instance, hwnd, asmStr.encode("utf-8"), _type, baseAddr)

    @classmethod
    def Assemble(cls, instance, asmStr, baseAddr, arch, mode):
        return cls._dll.Assemble(instance, asmStr.encode("utf-8"), baseAddr, arch, mode)

    @classmethod
    def Disassemble(cls, instance, asmCode, baseAddr, arch, mode, showType):
        return cls._dll.Disassemble(instance, asmCode.encode("utf-8"), baseAddr, arch, mode, showType)

    @classmethod
    def DrawGuiCleanup(cls, instance):
        return cls._dll.DrawGuiCleanup(instance)

    @classmethod
    def DrawGuiSetGuiActive(cls, instance, active):
        return cls._dll.DrawGuiSetGuiActive(instance, active)

    @classmethod
    def DrawGuiIsGuiActive(cls, instance):
        return cls._dll.DrawGuiIsGuiActive(instance)

    @classmethod
    def DrawGuiSetGuiClickThrough(cls, instance, enabled):
        return cls._dll.DrawGuiSetGuiClickThrough(instance, enabled)

    @classmethod
    def DrawGuiIsGuiClickThrough(cls, instance):
        return cls._dll.DrawGuiIsGuiClickThrough(instance)

    @classmethod
    def DrawGuiRectangle(cls, instance, x, y, width, height, mode, lineThickness):
        return cls._dll.DrawGuiRectangle(instance, x, y, width, height, mode, lineThickness)

    @classmethod
    def DrawGuiCircle(cls, instance, x, y, radius, mode, lineThickness):
        return cls._dll.DrawGuiCircle(instance, x, y, radius, mode, lineThickness)

    @classmethod
    def DrawGuiLine(cls, instance, x1, y1, x2, y2, lineThickness):
        return cls._dll.DrawGuiLine(instance, x1, y1, x2, y2, lineThickness)

    @classmethod
    def DrawGuiText(cls, instance, text, x, y, fontPath, fontSize, align):
        return cls._dll.DrawGuiText(instance, text.encode("utf-8"), x, y, fontPath.encode("utf-8"), fontSize, align)

    @classmethod
    def DrawGuiImage(cls, instance, imagePath, x, y):
        return cls._dll.DrawGuiImage(instance, imagePath.encode("utf-8"), x, y)

    @classmethod
    def DrawGuiWindow(cls, instance, title, x, y, width, height, style):
        return cls._dll.DrawGuiWindow(instance, title.encode("utf-8"), x, y, width, height, style)

    @classmethod
    def DrawGuiPanel(cls, instance, parentHandle, x, y, width, height):
        return cls._dll.DrawGuiPanel(instance, parentHandle, x, y, width, height)

    @classmethod
    def DrawGuiButton(cls, instance, parentHandle, text, x, y, width, height):
        return cls._dll.DrawGuiButton(instance, parentHandle, text.encode("utf-8"), x, y, width, height)

    @classmethod
    def DrawGuiSetPosition(cls, instance, handle, x, y):
        return cls._dll.DrawGuiSetPosition(instance, handle, x, y)

    @classmethod
    def DrawGuiSetSize(cls, instance, handle, width, height):
        return cls._dll.DrawGuiSetSize(instance, handle, width, height)

    @classmethod
    def DrawGuiSetColor(cls, instance, handle, r, g, b, a):
        return cls._dll.DrawGuiSetColor(instance, handle, r, g, b, a)

    @classmethod
    def DrawGuiSetAlpha(cls, instance, handle, alpha):
        return cls._dll.DrawGuiSetAlpha(instance, handle, alpha)

    @classmethod
    def DrawGuiSetDrawMode(cls, instance, handle, mode):
        return cls._dll.DrawGuiSetDrawMode(instance, handle, mode)

    @classmethod
    def DrawGuiSetLineThickness(cls, instance, handle, thickness):
        return cls._dll.DrawGuiSetLineThickness(instance, handle, thickness)

    @classmethod
    def DrawGuiSetFont(cls, instance, handle, fontPath, fontSize):
        return cls._dll.DrawGuiSetFont(instance, handle, fontPath.encode("utf-8"), fontSize)

    @classmethod
    def DrawGuiSetTextAlign(cls, instance, handle, align):
        return cls._dll.DrawGuiSetTextAlign(instance, handle, align)

    @classmethod
    def DrawGuiSetText(cls, instance, handle, text):
        return cls._dll.DrawGuiSetText(instance, handle, text.encode("utf-8"))

    @classmethod
    def DrawGuiSetWindowTitle(cls, instance, handle, title):
        return cls._dll.DrawGuiSetWindowTitle(instance, handle, title.encode("utf-8"))

    @classmethod
    def DrawGuiSetWindowStyle(cls, instance, handle, style):
        return cls._dll.DrawGuiSetWindowStyle(instance, handle, style)

    @classmethod
    def DrawGuiSetWindowTopMost(cls, instance, handle, topMost):
        return cls._dll.DrawGuiSetWindowTopMost(instance, handle, topMost)

    @classmethod
    def DrawGuiSetWindowTransparency(cls, instance, handle, alpha):
        return cls._dll.DrawGuiSetWindowTransparency(instance, handle, alpha)

    @classmethod
    def DrawGuiDeleteObject(cls, instance, handle):
        return cls._dll.DrawGuiDeleteObject(instance, handle)

    @classmethod
    def DrawGuiClearAll(cls, instance):
        return cls._dll.DrawGuiClearAll(instance)

    @classmethod
    def DrawGuiSetVisible(cls, instance, handle, visible):
        return cls._dll.DrawGuiSetVisible(instance, handle, visible)

    @classmethod
    def DrawGuiSetZOrder(cls, instance, handle, zOrder):
        return cls._dll.DrawGuiSetZOrder(instance, handle, zOrder)

    @classmethod
    def DrawGuiSetParent(cls, instance, handle, parentHandle):
        return cls._dll.DrawGuiSetParent(instance, handle, parentHandle)

    @classmethod
    def DrawGuiSetButtonCallback(cls, instance, handle, callback):
        callback = cls.DrawGuiButtonDelegate(callback)
        key = ("DrawGuiSetButtonCallback", instance)
        cls.callbacks[key] = callback
        return cls._dll.DrawGuiSetButtonCallback(instance, handle, callback)

    @classmethod
    def DrawGuiSetMouseCallback(cls, instance, handle, callback):
        callback = cls.DrawGuiMouseDelegate(callback)
        key = ("DrawGuiSetMouseCallback", instance)
        cls.callbacks[key] = callback
        return cls._dll.DrawGuiSetMouseCallback(instance, handle, callback)

    @classmethod
    def DrawGuiGetDrawObjectType(cls, instance, handle):
        return cls._dll.DrawGuiGetDrawObjectType(instance, handle)

    @classmethod
    def DrawGuiGetPosition(cls, instance, handle, x = None, y = None):
        x = c_int(0)
        y = c_int(0)
        result = cls._dll.DrawGuiGetPosition(instance, handle, byref(x), byref(y))
        return result, x.value, y.value

    @classmethod
    def DrawGuiGetSize(cls, instance, handle, width = None, height = None):
        width = c_int(0)
        height = c_int(0)
        result = cls._dll.DrawGuiGetSize(instance, handle, byref(width), byref(height))
        return result, width.value, height.value

    @classmethod
    def DrawGuiIsPointInObject(cls, instance, handle, x, y):
        return cls._dll.DrawGuiIsPointInObject(instance, handle, x, y)

    @classmethod
    def SetMemoryMode(cls, instance, mode):
        return cls._dll.SetMemoryMode(instance, mode)

    @classmethod
    def ExportDriver(cls, instance, driver_path, _type):
        return cls._dll.ExportDriver(instance, driver_path.encode("utf-8"), _type)

    @classmethod
    def LoadDriver(cls, instance, driver_name, driver_path):
        return cls._dll.LoadDriver(instance, driver_name.encode("utf-8"), driver_path.encode("utf-8"))

    @classmethod
    def UnloadDriver(cls, instance, driver_name):
        return cls._dll.UnloadDriver(instance, driver_name.encode("utf-8"))

    @classmethod
    def DriverTest(cls, instance):
        return cls._dll.DriverTest(instance)

    @classmethod
    def LoadPdb(cls, instance):
        return cls._dll.LoadPdb(instance)

    @classmethod
    def HideProcess(cls, instance, pid, enable):
        return cls._dll.HideProcess(instance, pid, enable)

    @classmethod
    def ProtectProcess(cls, instance, pid, enable):
        return cls._dll.ProtectProcess(instance, pid, enable)

    @classmethod
    def AddProtectPID(cls, instance, pid, mode, allow_pid):
        return cls._dll.AddProtectPID(instance, pid, mode, allow_pid)

    @classmethod
    def RemoveProtectPID(cls, instance, pid):
        return cls._dll.RemoveProtectPID(instance, pid)

    @classmethod
    def AddAllowPID(cls, instance, pid):
        return cls._dll.AddAllowPID(instance, pid)

    @classmethod
    def RemoveAllowPID(cls, instance, pid):
        return cls._dll.RemoveAllowPID(instance, pid)

    @classmethod
    def InjectDll(cls, instance, pid, dll_path, mode):
        return cls._dll.InjectDll(instance, pid, dll_path.encode("utf-8"), mode)

    @classmethod
    def FakeProcess(cls, instance, pid, fake_pid):
        return cls._dll.FakeProcess(instance, pid, fake_pid)

    @classmethod
    def StartHotkeyHook(cls, instance):
        return cls._dll.StartHotkeyHook(instance)

    @classmethod
    def StopHotkeyHook(cls, instance):
        return cls._dll.StopHotkeyHook(instance)

    @classmethod
    def RegisterHotkey(cls, instance, keycode, modifiers, callback):
        callback = cls.HotkeyDelegate(callback)
        key = ("RegisterHotkey", instance)
        cls.callbacks[key] = callback
        return cls._dll.RegisterHotkey(instance, keycode, modifiers, callback)

    @classmethod
    def UnregisterHotkey(cls, instance, keycode, modifiers):
        return cls._dll.UnregisterHotkey(instance, keycode, modifiers)

    @classmethod
    def RegisterMouseButton(cls, instance, button, _type, callback):
        callback = cls.MouseDelegate(callback)
        key = ("RegisterMouseButton", instance)
        cls.callbacks[key] = callback
        return cls._dll.RegisterMouseButton(instance, button, _type, callback)

    @classmethod
    def UnregisterMouseButton(cls, instance, button, _type):
        return cls._dll.UnregisterMouseButton(instance, button, _type)

    @classmethod
    def RegisterMouseWheel(cls, instance, callback):
        callback = cls.MouseWheelDelegate(callback)
        key = ("RegisterMouseWheel", instance)
        cls.callbacks[key] = callback
        return cls._dll.RegisterMouseWheel(instance, callback)

    @classmethod
    def UnregisterMouseWheel(cls, instance):
        return cls._dll.UnregisterMouseWheel(instance)

    @classmethod
    def RegisterMouseMove(cls, instance, callback):
        callback = cls.MouseMoveDelegate(callback)
        key = ("RegisterMouseMove", instance)
        cls.callbacks[key] = callback
        return cls._dll.RegisterMouseMove(instance, callback)

    @classmethod
    def UnregisterMouseMove(cls, instance):
        return cls._dll.UnregisterMouseMove(instance)

    @classmethod
    def RegisterMouseDrag(cls, instance, callback):
        callback = cls.MouseDragDelegate(callback)
        key = ("RegisterMouseDrag", instance)
        cls.callbacks[key] = callback
        return cls._dll.RegisterMouseDrag(instance, callback)

    @classmethod
    def UnregisterMouseDrag(cls, instance):
        return cls._dll.UnregisterMouseDrag(instance)

    @classmethod
    def JsonCreateObject(cls):
        return cls._dll.JsonCreateObject()

    @classmethod
    def JsonCreateArray(cls):
        return cls._dll.JsonCreateArray()

    @classmethod
    def JsonParse(cls, _str, err = None):
        err = c_int(0)
        result = cls._dll.JsonParse(_str.encode("utf-8"), byref(err))
        return result, err.value

    @classmethod
    def JsonStringify(cls, obj, indent, err = None):
        err = c_int(0)
        result = cls._dll.JsonStringify(obj, indent, byref(err))
        return result, err.value

    @classmethod
    def JsonFree(cls, obj):
        return cls._dll.JsonFree(obj)

    @classmethod
    def JsonGetValue(cls, obj, key, err = None):
        err = c_int(0)
        result = cls._dll.JsonGetValue(obj, key.encode("utf-8"), byref(err))
        return result, err.value

    @classmethod
    def JsonGetArrayItem(cls, arr, index, err = None):
        err = c_int(0)
        result = cls._dll.JsonGetArrayItem(arr, index, byref(err))
        return result, err.value

    @classmethod
    def JsonGetString(cls, obj, key, err = None):
        err = c_int(0)
        result = cls._dll.JsonGetString(obj, key.encode("utf-8"), byref(err))
        return result, err.value

    @classmethod
    def JsonGetNumber(cls, obj, key, err = None):
        err = c_int(0)
        result = cls._dll.JsonGetNumber(obj, key.encode("utf-8"), byref(err))
        return result, err.value

    @classmethod
    def JsonGetBool(cls, obj, key, err = None):
        err = c_int(0)
        result = cls._dll.JsonGetBool(obj, key.encode("utf-8"), byref(err))
        return result, err.value

    @classmethod
    def JsonGetSize(cls, obj, err = None):
        err = c_int(0)
        result = cls._dll.JsonGetSize(obj, byref(err))
        return result, err.value

    @classmethod
    def JsonSetValue(cls, obj, key, value):
        return cls._dll.JsonSetValue(obj, key.encode("utf-8"), value)

    @classmethod
    def JsonArrayAppend(cls, arr, value):
        return cls._dll.JsonArrayAppend(arr, value)

    @classmethod
    def JsonSetString(cls, obj, key, value):
        return cls._dll.JsonSetString(obj, key.encode("utf-8"), value.encode("utf-8"))

    @classmethod
    def JsonSetNumber(cls, obj, key, value):
        return cls._dll.JsonSetNumber(obj, key.encode("utf-8"), value)

    @classmethod
    def JsonSetBool(cls, obj, key, value):
        return cls._dll.JsonSetBool(obj, key.encode("utf-8"), value)

    @classmethod
    def JsonDeleteKey(cls, obj, key):
        return cls._dll.JsonDeleteKey(obj, key.encode("utf-8"))

    @classmethod
    def JsonClear(cls, obj):
        return cls._dll.JsonClear(obj)

    @classmethod
    def GenerateMouseTrajectory(cls, instance, startX, startY, endX, endY):
        return cls._dll.GenerateMouseTrajectory(instance, startX, startY, endX, endY)

    @classmethod
    def KeyDown(cls, instance, vk_code):
        return cls._dll.KeyDown(instance, vk_code)

    @classmethod
    def KeyUp(cls, instance, vk_code):
        return cls._dll.KeyUp(instance, vk_code)

    @classmethod
    def KeyPress(cls, instance, vk_code):
        return cls._dll.KeyPress(instance, vk_code)

    @classmethod
    def LeftDown(cls, instance):
        return cls._dll.LeftDown(instance)

    @classmethod
    def LeftUp(cls, instance):
        return cls._dll.LeftUp(instance)

    @classmethod
    def MoveTo(cls, instance, x, y):
        return cls._dll.MoveTo(instance, x, y)

    @classmethod
    def MoveToWithoutSimulator(cls, instance, x, y):
        return cls._dll.MoveToWithoutSimulator(instance, x, y)

    @classmethod
    def RightClick(cls, instance):
        return cls._dll.RightClick(instance)

    @classmethod
    def RightDown(cls, instance):
        return cls._dll.RightDown(instance)

    @classmethod
    def RightUp(cls, instance):
        return cls._dll.RightUp(instance)

    @classmethod
    def GetCursorShape(cls, instance):
        return cls._dll.GetCursorShape(instance)

    @classmethod
    def GetCursorImage(cls, instance):
        return cls._dll.GetCursorImage(instance)

    @classmethod
    def KeyPressStr(cls, instance, keyStr, delay):
        return cls._dll.KeyPressStr(instance, keyStr.encode("utf-8"), delay)

    @classmethod
    def SendString(cls, instance, hwnd, _str):
        return cls._dll.SendString(instance, hwnd, _str.encode("utf-8"))

    @classmethod
    def SendStringEx(cls, instance, hwnd, addr, _len, _type):
        return cls._dll.SendStringEx(instance, hwnd, addr, _len, _type)

    @classmethod
    def KeyPressChar(cls, instance, keyStr):
        return cls._dll.KeyPressChar(instance, keyStr.encode("utf-8"))

    @classmethod
    def KeyDownChar(cls, instance, keyStr):
        return cls._dll.KeyDownChar(instance, keyStr.encode("utf-8"))

    @classmethod
    def KeyUpChar(cls, instance, keyStr):
        return cls._dll.KeyUpChar(instance, keyStr.encode("utf-8"))

    @classmethod
    def MoveR(cls, instance, rx, ry):
        return cls._dll.MoveR(instance, rx, ry)

    @classmethod
    def MiddleClick(cls, instance):
        return cls._dll.MiddleClick(instance)

    @classmethod
    def MoveToEx(cls, instance, x, y, w, h):
        return cls._dll.MoveToEx(instance, x, y, w, h)

    @classmethod
    def GetCursorPos(cls, instance, x = None, y = None):
        x = c_int(0)
        y = c_int(0)
        result = cls._dll.GetCursorPos(instance, byref(x), byref(y))
        return result, x.value, y.value

    @classmethod
    def MiddleUp(cls, instance):
        return cls._dll.MiddleUp(instance)

    @classmethod
    def MiddleDown(cls, instance):
        return cls._dll.MiddleDown(instance)

    @classmethod
    def LeftClick(cls, instance):
        return cls._dll.LeftClick(instance)

    @classmethod
    def LeftDoubleClick(cls, instance):
        return cls._dll.LeftDoubleClick(instance)

    @classmethod
    def WheelUp(cls, instance):
        return cls._dll.WheelUp(instance)

    @classmethod
    def WheelDown(cls, instance):
        return cls._dll.WheelDown(instance)

    @classmethod
    def WaitKey(cls, instance, vk_code, time_out):
        return cls._dll.WaitKey(instance, vk_code, time_out)

    @classmethod
    def EnableMouseAccuracy(cls, instance, enable):
        return cls._dll.EnableMouseAccuracy(instance, enable)

    @classmethod
    def DoubleToData(cls, instance, double_value):
        return cls._dll.DoubleToData(instance, double_value)

    @classmethod
    def FloatToData(cls, instance, float_value):
        return cls._dll.FloatToData(instance, float_value)

    @classmethod
    def StringToData(cls, instance, string_value, _type):
        return cls._dll.StringToData(instance, string_value.encode("utf-8"), _type)

    @classmethod
    def Int64ToInt32(cls, instance, v):
        return cls._dll.Int64ToInt32(instance, v)

    @classmethod
    def Int32ToInt64(cls, instance, v):
        return cls._dll.Int32ToInt64(instance, v)

    @classmethod
    def FindData(cls, instance, hwnd, addr_range, data):
        return cls._dll.FindData(instance, hwnd, addr_range.encode("utf-8"), data.encode("utf-8"))

    @classmethod
    def FindDataEx(cls, instance, hwnd, addr_range, data, step, multi_thread, mode):
        return cls._dll.FindDataEx(instance, hwnd, addr_range.encode("utf-8"), data.encode("utf-8"), step, multi_thread, mode)

    @classmethod
    def FindDouble(cls, instance, hwnd, addr_range, double_value_min, double_value_max):
        return cls._dll.FindDouble(instance, hwnd, addr_range.encode("utf-8"), double_value_min, double_value_max)

    @classmethod
    def FindDoubleEx(cls, instance, hwnd, addr_range, double_value_min, double_value_max, step, multi_thread, mode):
        return cls._dll.FindDoubleEx(instance, hwnd, addr_range.encode("utf-8"), double_value_min, double_value_max, step, multi_thread, mode)

    @classmethod
    def FindFloat(cls, instance, hwnd, addr_range, float_value_min, float_value_max):
        return cls._dll.FindFloat(instance, hwnd, addr_range.encode("utf-8"), float_value_min, float_value_max)

    @classmethod
    def FindFloatEx(cls, instance, hwnd, addr_range, float_value_min, float_value_max, step, multi_thread, mode):
        return cls._dll.FindFloatEx(instance, hwnd, addr_range.encode("utf-8"), float_value_min, float_value_max, step, multi_thread, mode)

    @classmethod
    def FindInt(cls, instance, hwnd, addr_range, int_value_min, int_value_max, _type):
        return cls._dll.FindInt(instance, hwnd, addr_range.encode("utf-8"), int_value_min, int_value_max, _type)

    @classmethod
    def FindIntEx(cls, instance, hwnd, addr_range, int_value_min, int_value_max, _type, step, multi_thread, mode):
        return cls._dll.FindIntEx(instance, hwnd, addr_range.encode("utf-8"), int_value_min, int_value_max, _type, step, multi_thread, mode)

    @classmethod
    def FindString(cls, instance, hwnd, addr_range, string_value, _type):
        return cls._dll.FindString(instance, hwnd, addr_range.encode("utf-8"), string_value.encode("utf-8"), _type)

    @classmethod
    def FindStringEx(cls, instance, hwnd, addr_range, string_value, _type, step, multi_thread, mode):
        return cls._dll.FindStringEx(instance, hwnd, addr_range.encode("utf-8"), string_value.encode("utf-8"), _type, step, multi_thread, mode)

    @classmethod
    def ReadData(cls, instance, hwnd, addr, _len):
        return cls._dll.ReadData(instance, hwnd, addr.encode("utf-8"), _len)

    @classmethod
    def ReadDataAddr(cls, instance, hwnd, addr, _len):
        return cls._dll.ReadDataAddr(instance, hwnd, addr, _len)

    @classmethod
    def ReadDataAddrToBin(cls, instance, hwnd, addr, _len):
        return cls._dll.ReadDataAddrToBin(instance, hwnd, addr, _len)

    @classmethod
    def ReadDataToBin(cls, instance, hwnd, addr, _len):
        return cls._dll.ReadDataToBin(instance, hwnd, addr.encode("utf-8"), _len)

    @classmethod
    def ReadDouble(cls, instance, hwnd, addr):
        return cls._dll.ReadDouble(instance, hwnd, addr.encode("utf-8"))

    @classmethod
    def ReadDoubleAddr(cls, instance, hwnd, addr):
        return cls._dll.ReadDoubleAddr(instance, hwnd, addr)

    @classmethod
    def ReadFloat(cls, instance, hwnd, addr):
        return cls._dll.ReadFloat(instance, hwnd, addr.encode("utf-8"))

    @classmethod
    def ReadFloatAddr(cls, instance, hwnd, addr):
        return cls._dll.ReadFloatAddr(instance, hwnd, addr)

    @classmethod
    def ReadInt(cls, instance, hwnd, addr, _type):
        return cls._dll.ReadInt(instance, hwnd, addr.encode("utf-8"), _type)

    @classmethod
    def ReadIntAddr(cls, instance, hwnd, addr, _type):
        return cls._dll.ReadIntAddr(instance, hwnd, addr, _type)

    @classmethod
    def ReadString(cls, instance, hwnd, addr, _type, _len):
        return cls._dll.ReadString(instance, hwnd, addr.encode("utf-8"), _type, _len)

    @classmethod
    def ReadStringAddr(cls, instance, hwnd, addr, _type, _len):
        return cls._dll.ReadStringAddr(instance, hwnd, addr, _type, _len)

    @classmethod
    def WriteData(cls, instance, hwnd, addr, data):
        return cls._dll.WriteData(instance, hwnd, addr.encode("utf-8"), data.encode("utf-8"))

    @classmethod
    def WriteDataFromBin(cls, instance, hwnd, addr, data, _len):
        return cls._dll.WriteDataFromBin(instance, hwnd, addr.encode("utf-8"), data, _len)

    @classmethod
    def WriteDataAddr(cls, instance, hwnd, addr, data):
        return cls._dll.WriteDataAddr(instance, hwnd, addr, data.encode("utf-8"))

    @classmethod
    def WriteDataAddrFromBin(cls, instance, hwnd, addr, data, _len):
        return cls._dll.WriteDataAddrFromBin(instance, hwnd, addr, data, _len)

    @classmethod
    def WriteDouble(cls, instance, hwnd, addr, double_value):
        return cls._dll.WriteDouble(instance, hwnd, addr.encode("utf-8"), double_value)

    @classmethod
    def WriteDoubleAddr(cls, instance, hwnd, addr, double_value):
        return cls._dll.WriteDoubleAddr(instance, hwnd, addr, double_value)

    @classmethod
    def WriteFloat(cls, instance, hwnd, addr, float_value):
        return cls._dll.WriteFloat(instance, hwnd, addr.encode("utf-8"), float_value)

    @classmethod
    def WriteFloatAddr(cls, instance, hwnd, addr, float_value):
        return cls._dll.WriteFloatAddr(instance, hwnd, addr, float_value)

    @classmethod
    def WriteInt(cls, instance, hwnd, addr, _type, value):
        return cls._dll.WriteInt(instance, hwnd, addr.encode("utf-8"), _type, value)

    @classmethod
    def WriteIntAddr(cls, instance, hwnd, addr, _type, value):
        return cls._dll.WriteIntAddr(instance, hwnd, addr, _type, value)

    @classmethod
    def WriteString(cls, instance, hwnd, addr, _type, value):
        return cls._dll.WriteString(instance, hwnd, addr.encode("utf-8"), _type, value.encode("utf-8"))

    @classmethod
    def WriteStringAddr(cls, instance, hwnd, addr, _type, value):
        return cls._dll.WriteStringAddr(instance, hwnd, addr, _type, value.encode("utf-8"))

    @classmethod
    def SetMemoryHwndAsProcessId(cls, instance, enable):
        return cls._dll.SetMemoryHwndAsProcessId(instance, enable)

    @classmethod
    def FreeProcessMemory(cls, instance, hwnd):
        return cls._dll.FreeProcessMemory(instance, hwnd)

    @classmethod
    def GetModuleBaseAddr(cls, instance, hwnd, module_name):
        return cls._dll.GetModuleBaseAddr(instance, hwnd, module_name.encode("utf-8"))

    @classmethod
    def GetModuleSize(cls, instance, hwnd, module_name):
        return cls._dll.GetModuleSize(instance, hwnd, module_name.encode("utf-8"))

    @classmethod
    def GetRemoteApiAddress(cls, instance, hwnd, base_addr, fun_name):
        return cls._dll.GetRemoteApiAddress(instance, hwnd, base_addr, fun_name.encode("utf-8"))

    @classmethod
    def VirtualAllocEx(cls, instance, hwnd, addr, size, _type):
        return cls._dll.VirtualAllocEx(instance, hwnd, addr, size, _type)

    @classmethod
    def VirtualFreeEx(cls, instance, hwnd, addr):
        return cls._dll.VirtualFreeEx(instance, hwnd, addr)

    @classmethod
    def VirtualProtectEx(cls, instance, hwnd, addr, size, _type, protect):
        return cls._dll.VirtualProtectEx(instance, hwnd, addr, size, _type, protect)

    @classmethod
    def VirtualQueryEx(cls, instance, hwnd, addr, pmbi):
        return cls._dll.VirtualQueryEx(instance, hwnd, addr, pmbi)

    @classmethod
    def CreateRemoteThread(cls, instance, hwnd, lpStartAddress, lpParameter, dwCreationFlags, lpThreadId = None):
        lpThreadId = c_int64(0)
        result = cls._dll.CreateRemoteThread(instance, hwnd, lpStartAddress, lpParameter, dwCreationFlags, byref(lpThreadId))
        return result, lpThreadId.value

    @classmethod
    def CloseHandle(cls, instance, handle):
        return cls._dll.CloseHandle(instance, handle)

    @classmethod
    def Ocr(cls, instance, x1, y1, x2, y2):
        return cls._dll.Ocr(instance, x1, y1, x2, y2)

    @classmethod
    def OcrFromPtr(cls, instance, ptr):
        return cls._dll.OcrFromPtr(instance, ptr)

    @classmethod
    def OcrFromBmpData(cls, instance, ptr, size):
        return cls._dll.OcrFromBmpData(instance, ptr, size)

    @classmethod
    def OcrDetails(cls, instance, x1, y1, x2, y2):
        return cls._dll.OcrDetails(instance, x1, y1, x2, y2)

    @classmethod
    def OcrFromPtrDetails(cls, instance, ptr):
        return cls._dll.OcrFromPtrDetails(instance, ptr)

    @classmethod
    def OcrFromBmpDataDetails(cls, instance, ptr, size):
        return cls._dll.OcrFromBmpDataDetails(instance, ptr, size)

    @classmethod
    def OcrV5(cls, instance, x1, y1, x2, y2):
        return cls._dll.OcrV5(instance, x1, y1, x2, y2)

    @classmethod
    def OcrV5Details(cls, instance, x1, y1, x2, y2):
        return cls._dll.OcrV5Details(instance, x1, y1, x2, y2)

    @classmethod
    def OcrV5FromPtr(cls, instance, ptr):
        return cls._dll.OcrV5FromPtr(instance, ptr)

    @classmethod
    def OcrV5FromPtrDetails(cls, instance, ptr):
        return cls._dll.OcrV5FromPtrDetails(instance, ptr)

    @classmethod
    def GetOcrConfig(cls, instance, configKey):
        return cls._dll.GetOcrConfig(instance, configKey.encode("utf-8"))

    @classmethod
    def SetOcrConfig(cls, instance, configStr):
        return cls._dll.SetOcrConfig(instance, configStr.encode("utf-8"))

    @classmethod
    def SetOcrConfigByKey(cls, instance, key, value):
        return cls._dll.SetOcrConfigByKey(instance, key.encode("utf-8"), value.encode("utf-8"))

    @classmethod
    def OcrFromDict(cls, instance, x1, y1, x2, y2, colorJson, dict_name, matchVal):
        return cls._dll.OcrFromDict(instance, x1, y1, x2, y2, colorJson.encode("utf-8"), dict_name.encode("utf-8"), matchVal)

    @classmethod
    def OcrFromDictDetails(cls, instance, x1, y1, x2, y2, colorJson, dict_name, matchVal):
        return cls._dll.OcrFromDictDetails(instance, x1, y1, x2, y2, colorJson.encode("utf-8"), dict_name.encode("utf-8"), matchVal)

    @classmethod
    def OcrFromDictPtr(cls, instance, ptr, colorJson, dict_name, matchVal):
        return cls._dll.OcrFromDictPtr(instance, ptr, colorJson.encode("utf-8"), dict_name.encode("utf-8"), matchVal)

    @classmethod
    def OcrFromDictPtrDetails(cls, instance, ptr, colorJson, dict_name, matchVal):
        return cls._dll.OcrFromDictPtrDetails(instance, ptr, colorJson.encode("utf-8"), dict_name.encode("utf-8"), matchVal)

    @classmethod
    def FindStr(cls, instance, x1, y1, x2, y2, _str, colorJson, _dict, matchVal, outX = None, outY = None):
        outX = c_int(0)
        outY = c_int(0)
        result = cls._dll.FindStr(instance, x1, y1, x2, y2, _str.encode("utf-8"), colorJson.encode("utf-8"), _dict.encode("utf-8"), matchVal, byref(outX), byref(outY))
        return result, outX.value, outY.value

    @classmethod
    def FindStrDetail(cls, instance, x1, y1, x2, y2, _str, colorJson, _dict, matchVal):
        return cls._dll.FindStrDetail(instance, x1, y1, x2, y2, _str.encode("utf-8"), colorJson.encode("utf-8"), _dict.encode("utf-8"), matchVal)

    @classmethod
    def FindStrAll(cls, instance, x1, y1, x2, y2, _str, colorJson, _dict, matchVal):
        return cls._dll.FindStrAll(instance, x1, y1, x2, y2, _str.encode("utf-8"), colorJson.encode("utf-8"), _dict.encode("utf-8"), matchVal)

    @classmethod
    def FindStrFromPtr(cls, instance, source, _str, colorJson, _dict, matchVal):
        return cls._dll.FindStrFromPtr(instance, source, _str.encode("utf-8"), colorJson.encode("utf-8"), _dict.encode("utf-8"), matchVal)

    @classmethod
    def FindStrFromPtrAll(cls, instance, source, _str, colorJson, _dict, matchVal):
        return cls._dll.FindStrFromPtrAll(instance, source, _str.encode("utf-8"), colorJson.encode("utf-8"), _dict.encode("utf-8"), matchVal)

    @classmethod
    def FastNumberOcrFromPtr(cls, instance, source, numbers, colorJson, matchVal):
        return cls._dll.FastNumberOcrFromPtr(instance, source, numbers.encode("utf-8"), colorJson.encode("utf-8"), matchVal)

    @classmethod
    def FastNumberOcr(cls, instance, x1, y1, x2, y2, numbers, colorJson, matchVal):
        return cls._dll.FastNumberOcr(instance, x1, y1, x2, y2, numbers.encode("utf-8"), colorJson.encode("utf-8"), matchVal)

    @classmethod
    def Capture(cls, instance, x1, y1, x2, y2, file):
        return cls._dll.Capture(instance, x1, y1, x2, y2, file.encode("utf-8"))

    @classmethod
    def GetScreenDataBmp(cls, instance, x1, y1, x2, y2, data = None, dataLen = None):
        data = c_int64(0)
        dataLen = c_int(0)
        result = cls._dll.GetScreenDataBmp(instance, x1, y1, x2, y2, byref(data), byref(dataLen))
        return result, data.value, dataLen.value

    @classmethod
    def GetScreenData(cls, instance, x1, y1, x2, y2, data = None, dataLen = None, stride = None):
        data = c_int64(0)
        dataLen = c_int(0)
        stride = c_int(0)
        result = cls._dll.GetScreenData(instance, x1, y1, x2, y2, byref(data), byref(dataLen), byref(stride))
        return result, data.value, dataLen.value, stride.value

    @classmethod
    def GetScreenDataPtr(cls, instance, x1, y1, x2, y2):
        return cls._dll.GetScreenDataPtr(instance, x1, y1, x2, y2)

    @classmethod
    def CaptureGif(cls, instance, x1, y1, x2, y2, file, delay, time):
        return cls._dll.CaptureGif(instance, x1, y1, x2, y2, file.encode("utf-8"), delay, time)

    @classmethod
    def GetImageData(cls, instance, imgPtr, data = None, size = None, stride = None):
        data = c_int64(0)
        size = c_int(0)
        stride = c_int(0)
        result = cls._dll.GetImageData(instance, imgPtr, byref(data), byref(size), byref(stride))
        return result, data.value, size.value, stride.value

    @classmethod
    def MatchImageFromPath(cls, instance, source, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchImageFromPath(instance, source.encode("utf-8"), templ.encode("utf-8"), matchVal, _type, angle, scale)

    @classmethod
    def MatchImageFromPathAll(cls, instance, source, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchImageFromPathAll(instance, source.encode("utf-8"), templ.encode("utf-8"), matchVal, _type, angle, scale)

    @classmethod
    def MatchImagePtrFromPath(cls, instance, source, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchImagePtrFromPath(instance, source, templ.encode("utf-8"), matchVal, _type, angle, scale)

    @classmethod
    def MatchImagePtrFromPathAll(cls, instance, source, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchImagePtrFromPathAll(instance, source, templ.encode("utf-8"), matchVal, _type, angle, scale)

    @classmethod
    def GetColor(cls, instance, x, y):
        return cls._dll.GetColor(instance, x, y)

    @classmethod
    def GetColorPtr(cls, instance, source, x, y):
        return cls._dll.GetColorPtr(instance, source, x, y)

    @classmethod
    def CopyImage(cls, instance, sourcePtr):
        return cls._dll.CopyImage(instance, sourcePtr)

    @classmethod
    def FreeImagePath(cls, instance, path):
        return cls._dll.FreeImagePath(instance, path.encode("utf-8"))

    @classmethod
    def FreeImageAll(cls, instance):
        return cls._dll.FreeImageAll(instance)

    @classmethod
    def LoadImage(cls, instance, path):
        return cls._dll.LoadImage(instance, path.encode("utf-8"))

    @classmethod
    def LoadImageFromBmpData(cls, instance, data, dataSize):
        return cls._dll.LoadImageFromBmpData(instance, data, dataSize)

    @classmethod
    def LoadImageFromRGBData(cls, instance, width, height, scan0, stride):
        return cls._dll.LoadImageFromRGBData(instance, width, height, scan0, stride)

    @classmethod
    def FreeImagePtr(cls, instance, screenPtr):
        return cls._dll.FreeImagePtr(instance, screenPtr)

    @classmethod
    def MatchWindowsFromPtr(cls, instance, x1, y1, x2, y2, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchWindowsFromPtr(instance, x1, y1, x2, y2, templ, matchVal, _type, angle, scale)

    @classmethod
    def MatchImageFromPtr(cls, instance, source, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchImageFromPtr(instance, source, templ, matchVal, _type, angle, scale)

    @classmethod
    def MatchImageFromPtrAll(cls, instance, source, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchImageFromPtrAll(instance, source, templ, matchVal, _type, angle, scale)

    @classmethod
    def MatchWindowsFromPtrAll(cls, instance, x1, y1, x2, y2, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchWindowsFromPtrAll(instance, x1, y1, x2, y2, templ, matchVal, _type, angle, scale)

    @classmethod
    def MatchWindowsFromPath(cls, instance, x1, y1, x2, y2, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchWindowsFromPath(instance, x1, y1, x2, y2, templ.encode("utf-8"), matchVal, _type, angle, scale)

    @classmethod
    def MatchWindowsFromPathAll(cls, instance, x1, y1, x2, y2, templ, matchVal, _type, angle, scale):
        return cls._dll.MatchWindowsFromPathAll(instance, x1, y1, x2, y2, templ.encode("utf-8"), matchVal, _type, angle, scale)

    @classmethod
    def MatchWindowsThresholdFromPtr(cls, instance, x1, y1, x2, y2, colorJson, templ, matchVal, angle, scale):
        return cls._dll.MatchWindowsThresholdFromPtr(instance, x1, y1, x2, y2, colorJson.encode("utf-8"), templ, matchVal, angle, scale)

    @classmethod
    def MatchWindowsThresholdFromPtrAll(cls, instance, x1, y1, x2, y2, colorJson, templ, matchVal, angle, scale):
        return cls._dll.MatchWindowsThresholdFromPtrAll(instance, x1, y1, x2, y2, colorJson.encode("utf-8"), templ, matchVal, angle, scale)

    @classmethod
    def MatchWindowsThresholdFromPath(cls, instance, x1, y1, x2, y2, colorJson, templ, matchVal, angle, scale):
        return cls._dll.MatchWindowsThresholdFromPath(instance, x1, y1, x2, y2, colorJson.encode("utf-8"), templ.encode("utf-8"), matchVal, angle, scale)

    @classmethod
    def MatchWindowsThresholdFromPathAll(cls, instance, x1, y1, x2, y2, colorJson, templ, matchVal, angle, scale):
        return cls._dll.MatchWindowsThresholdFromPathAll(instance, x1, y1, x2, y2, colorJson.encode("utf-8"), templ.encode("utf-8"), matchVal, angle, scale)

    @classmethod
    def ShowMatchWindow(cls, instance, flag):
        return cls._dll.ShowMatchWindow(instance, flag)

    @classmethod
    def CalculateSSIM(cls, instance, image1, image2):
        return cls._dll.CalculateSSIM(instance, image1, image2)

    @classmethod
    def CalculateHistograms(cls, instance, image1, image2):
        return cls._dll.CalculateHistograms(instance, image1, image2)

    @classmethod
    def CalculateMSE(cls, instance, image1, image2):
        return cls._dll.CalculateMSE(instance, image1, image2)

    @classmethod
    def SaveImageFromPtr(cls, instance, ptr, path):
        return cls._dll.SaveImageFromPtr(instance, ptr, path.encode("utf-8"))

    @classmethod
    def ReSize(cls, instance, ptr, width, height):
        return cls._dll.ReSize(instance, ptr, width, height)

    @classmethod
    def FindColor(cls, instance, x1, y1, x2, y2, color1, color2, _dir, x = None, y = None):
        x = c_int(0)
        y = c_int(0)
        result = cls._dll.FindColor(instance, x1, y1, x2, y2, color1.encode("utf-8"), color2.encode("utf-8"), _dir, byref(x), byref(y))
        return result, x.value, y.value

    @classmethod
    def FindColorList(cls, instance, x1, y1, x2, y2, color1, color2):
        return cls._dll.FindColorList(instance, x1, y1, x2, y2, color1.encode("utf-8"), color2.encode("utf-8"))

    @classmethod
    def FindMultiColor(cls, instance, x1, y1, x2, y2, colorJson, pointJson, _dir, x = None, y = None):
        x = c_int(0)
        y = c_int(0)
        result = cls._dll.FindMultiColor(instance, x1, y1, x2, y2, colorJson.encode("utf-8"), pointJson.encode("utf-8"), _dir, byref(x), byref(y))
        return result, x.value, y.value

    @classmethod
    def FindMultiColorList(cls, instance, x1, y1, x2, y2, colorJson, pointJson):
        return cls._dll.FindMultiColorList(instance, x1, y1, x2, y2, colorJson.encode("utf-8"), pointJson.encode("utf-8"))

    @classmethod
    def FindMultiColorFromPtr(cls, instance, ptr, colorJson, pointJson, _dir, x = None, y = None):
        x = c_int(0)
        y = c_int(0)
        result = cls._dll.FindMultiColorFromPtr(instance, ptr, colorJson.encode("utf-8"), pointJson.encode("utf-8"), _dir, byref(x), byref(y))
        return result, x.value, y.value

    @classmethod
    def FindMultiColorListFromPtr(cls, instance, ptr, colorJson, pointJson):
        return cls._dll.FindMultiColorListFromPtr(instance, ptr, colorJson.encode("utf-8"), pointJson.encode("utf-8"))

    @classmethod
    def GetImageSize(cls, instance, ptr, width = None, height = None):
        width = c_int(0)
        height = c_int(0)
        result = cls._dll.GetImageSize(instance, ptr, byref(width), byref(height))
        return result, width.value, height.value

    @classmethod
    def FindColorBlock(cls, instance, x1, y1, x2, y2, colorList, count, width, height, x = None, y = None):
        x = c_int(0)
        y = c_int(0)
        result = cls._dll.FindColorBlock(instance, x1, y1, x2, y2, colorList.encode("utf-8"), count, width, height, byref(x), byref(y))
        return result, x.value, y.value

    @classmethod
    def FindColorBlockPtr(cls, instance, ptr, colorList, count, width, height, x = None, y = None):
        x = c_int(0)
        y = c_int(0)
        result = cls._dll.FindColorBlockPtr(instance, ptr, colorList.encode("utf-8"), count, width, height, byref(x), byref(y))
        return result, x.value, y.value

    @classmethod
    def FindColorBlockList(cls, instance, x1, y1, x2, y2, colorList, count, width, height, _type):
        return cls._dll.FindColorBlockList(instance, x1, y1, x2, y2, colorList.encode("utf-8"), count, width, height, _type)

    @classmethod
    def FindColorBlockListPtr(cls, instance, ptr, colorList, count, width, height, _type):
        return cls._dll.FindColorBlockListPtr(instance, ptr, colorList.encode("utf-8"), count, width, height, _type)

    @classmethod
    def GetColorNum(cls, instance, x1, y1, x2, y2, colorList):
        return cls._dll.GetColorNum(instance, x1, y1, x2, y2, colorList.encode("utf-8"))

    @classmethod
    def GetColorNumPtr(cls, instance, ptr, colorList):
        return cls._dll.GetColorNumPtr(instance, ptr, colorList.encode("utf-8"))

    @classmethod
    def Cropped(cls, instance, image, x1, y1, x2, y2):
        return cls._dll.Cropped(instance, image, x1, y1, x2, y2)

    @classmethod
    def GetThresholdImageFromMultiColorPtr(cls, instance, ptr, colorJson):
        return cls._dll.GetThresholdImageFromMultiColorPtr(instance, ptr, colorJson.encode("utf-8"))

    @classmethod
    def GetThresholdImageFromMultiColor(cls, instance, x1, y1, x2, y2, colorJson):
        return cls._dll.GetThresholdImageFromMultiColor(instance, x1, y1, x2, y2, colorJson.encode("utf-8"))

    @classmethod
    def IsSameImage(cls, instance, ptr, ptr2):
        return cls._dll.IsSameImage(instance, ptr, ptr2)

    @classmethod
    def ShowImage(cls, instance, ptr):
        return cls._dll.ShowImage(instance, ptr)

    @classmethod
    def ShowImageFromFile(cls, instance, file):
        return cls._dll.ShowImageFromFile(instance, file.encode("utf-8"))

    @classmethod
    def SetColorsToNewColor(cls, instance, ptr, colorJson, color):
        return cls._dll.SetColorsToNewColor(instance, ptr, colorJson.encode("utf-8"), color.encode("utf-8"))

    @classmethod
    def RemoveOtherColors(cls, instance, ptr, colorJson):
        return cls._dll.RemoveOtherColors(instance, ptr, colorJson.encode("utf-8"))

    @classmethod
    def DrawRectangle(cls, instance, ptr, x1, y1, x2, y2, thickness, color):
        return cls._dll.DrawRectangle(instance, ptr, x1, y1, x2, y2, thickness, color.encode("utf-8"))

    @classmethod
    def DrawCircle(cls, instance, ptr, x, y, radius, thickness, color):
        return cls._dll.DrawCircle(instance, ptr, x, y, radius, thickness, color.encode("utf-8"))

    @classmethod
    def DrawFillPoly(cls, instance, ptr, pointJson, color):
        return cls._dll.DrawFillPoly(instance, ptr, pointJson.encode("utf-8"), color.encode("utf-8"))

    @classmethod
    def DecodeQRCode(cls, instance, ptr):
        return cls._dll.DecodeQRCode(instance, ptr)

    @classmethod
    def CreateQRCode(cls, instance, _str, pixelsPerModule):
        return cls._dll.CreateQRCode(instance, _str.encode("utf-8"), pixelsPerModule)

    @classmethod
    def CreateQRCodeEx(cls, instance, _str, pixelsPerModule, version, correction_level, mode, structure_number):
        return cls._dll.CreateQRCodeEx(instance, _str.encode("utf-8"), pixelsPerModule, version, correction_level, mode, structure_number)

    @classmethod
    def MatchAnimationFromPtr(cls, instance, x1, y1, x2, y2, templ, matchVal, _type, angle, scale, delay, time, threadCount):
        return cls._dll.MatchAnimationFromPtr(instance, x1, y1, x2, y2, templ, matchVal, _type, angle, scale, delay, time, threadCount)

    @classmethod
    def MatchAnimationFromPath(cls, instance, x1, y1, x2, y2, templ, matchVal, _type, angle, scale, delay, time, threadCount):
        return cls._dll.MatchAnimationFromPath(instance, x1, y1, x2, y2, templ.encode("utf-8"), matchVal, _type, angle, scale, delay, time, threadCount)

    @classmethod
    def RemoveImageDiff(cls, instance, image1, image2):
        return cls._dll.RemoveImageDiff(instance, image1, image2)

    @classmethod
    def GetImageBmpData(cls, instance, imgPtr, data = None, size = None):
        data = c_int64(0)
        size = c_int(0)
        result = cls._dll.GetImageBmpData(instance, imgPtr, byref(data), byref(size))
        return result, data.value, size.value

    @classmethod
    def FreeImageData(cls, instance, screenPtr):
        return cls._dll.FreeImageData(instance, screenPtr)

    @classmethod
    def ScalePixels(cls, instance, ptr, pixelsPerModule):
        return cls._dll.ScalePixels(instance, ptr, pixelsPerModule)

    @classmethod
    def CreateImage(cls, instance, width, height, color):
        return cls._dll.CreateImage(instance, width, height, color.encode("utf-8"))

    @classmethod
    def SetPixel(cls, instance, image, x, y, color):
        return cls._dll.SetPixel(instance, image, x, y, color.encode("utf-8"))

    @classmethod
    def SetPixelList(cls, instance, image, points, color):
        return cls._dll.SetPixelList(instance, image, points.encode("utf-8"), color.encode("utf-8"))

    @classmethod
    def ConcatImage(cls, instance, image1, image2, gap, color, _dir):
        return cls._dll.ConcatImage(instance, image1, image2, gap, color.encode("utf-8"), _dir)

    @classmethod
    def CoverImage(cls, instance, image1, image2, x, y, alpha):
        return cls._dll.CoverImage(instance, image1, image2, x, y, alpha)

    @classmethod
    def RotateImage(cls, instance, image, angle):
        return cls._dll.RotateImage(instance, image, angle)

    @classmethod
    def ImageToBase64(cls, instance, image):
        return cls._dll.ImageToBase64(instance, image)

    @classmethod
    def Base64ToImage(cls, instance, base64):
        return cls._dll.Base64ToImage(instance, base64.encode("utf-8"))

    @classmethod
    def Hex2ARGB(cls, instance, hex, a = None, r = None, g = None, b = None):
        a = c_int(0)
        r = c_int(0)
        g = c_int(0)
        b = c_int(0)
        result = cls._dll.Hex2ARGB(instance, hex.encode("utf-8"), byref(a), byref(r), byref(g), byref(b))
        return result, a.value, r.value, g.value, b.value

    @classmethod
    def Hex2RGB(cls, instance, hex, r = None, g = None, b = None):
        r = c_int(0)
        g = c_int(0)
        b = c_int(0)
        result = cls._dll.Hex2RGB(instance, hex.encode("utf-8"), byref(r), byref(g), byref(b))
        return result, r.value, g.value, b.value

    @classmethod
    def ARGB2Hex(cls, instance, a, r, g, b):
        return cls._dll.ARGB2Hex(instance, a, r, g, b)

    @classmethod
    def RGB2Hex(cls, instance, r, g, b):
        return cls._dll.RGB2Hex(instance, r, g, b)

    @classmethod
    def Hex2HSV(cls, instance, hex):
        return cls._dll.Hex2HSV(instance, hex.encode("utf-8"))

    @classmethod
    def RGB2HSV(cls, instance, r, g, b):
        return cls._dll.RGB2HSV(instance, r, g, b)

    @classmethod
    def CmpColor(cls, instance, x1, y1, colorStart, colorEnd):
        return cls._dll.CmpColor(instance, x1, y1, colorStart.encode("utf-8"), colorEnd.encode("utf-8"))

    @classmethod
    def CmpColorPtr(cls, instance, ptr, x, y, colorStart, colorEnd):
        return cls._dll.CmpColorPtr(instance, ptr, x, y, colorStart.encode("utf-8"), colorEnd.encode("utf-8"))

    @classmethod
    def CmpColorHex(cls, instance, hex, colorStart, colorEnd):
        return cls._dll.CmpColorHex(instance, hex.encode("utf-8"), colorStart.encode("utf-8"), colorEnd.encode("utf-8"))

    @classmethod
    def GetConnectedComponents(cls, instance, ptr, points, tolerance):
        return cls._dll.GetConnectedComponents(instance, ptr, points.encode("utf-8"), tolerance)

    @classmethod
    def DetectPointerDirection(cls, instance, ptr, x, y):
        return cls._dll.DetectPointerDirection(instance, ptr, x, y)

    @classmethod
    def DetectPointerDirectionByFeatures(cls, instance, ptr, templatePtr, x, y, useTemplate):
        return cls._dll.DetectPointerDirectionByFeatures(instance, ptr, templatePtr, x, y, useTemplate)

    @classmethod
    def FastMatch(cls, instance, ptr, templatePtr, matchVal, _type, angle, scale):
        return cls._dll.FastMatch(instance, ptr, templatePtr, matchVal, _type, angle, scale)

    @classmethod
    def FastROI(cls, instance, ptr):
        return cls._dll.FastROI(instance, ptr)

    @classmethod
    def GetROIRegion(cls, instance, ptr, x1 = None, y1 = None, x2 = None, y2 = None):
        x1 = c_int(0)
        y1 = c_int(0)
        x2 = c_int(0)
        y2 = c_int(0)
        result = cls._dll.GetROIRegion(instance, ptr, byref(x1), byref(y1), byref(x2), byref(y2))
        return result, x1.value, y1.value, x2.value, y2.value

    @classmethod
    def GetForegroundPoints(cls, instance, ptr):
        return cls._dll.GetForegroundPoints(instance, ptr)

    @classmethod
    def ConvertColor(cls, instance, ptr, _type):
        return cls._dll.ConvertColor(instance, ptr, _type)

    @classmethod
    def Threshold(cls, instance, ptr, thresh, maxVal, _type):
        return cls._dll.Threshold(instance, ptr, thresh, maxVal, _type)

    @classmethod
    def RemoveIslands(cls, instance, ptr, minArea):
        return cls._dll.RemoveIslands(instance, ptr, minArea)

    @classmethod
    def MorphGradient(cls, instance, ptr, kernelSize):
        return cls._dll.MorphGradient(instance, ptr, kernelSize)

    @classmethod
    def MorphTophat(cls, instance, ptr, kernelSize):
        return cls._dll.MorphTophat(instance, ptr, kernelSize)

    @classmethod
    def MorphBlackhat(cls, instance, ptr, kernelSize):
        return cls._dll.MorphBlackhat(instance, ptr, kernelSize)

    @classmethod
    def Dilation(cls, instance, ptr, kernelSize):
        return cls._dll.Dilation(instance, ptr, kernelSize)

    @classmethod
    def Erosion(cls, instance, ptr, kernelSize):
        return cls._dll.Erosion(instance, ptr, kernelSize)

    @classmethod
    def GaussianBlur(cls, instance, ptr, kernelSize):
        return cls._dll.GaussianBlur(instance, ptr, kernelSize)

    @classmethod
    def Sharpen(cls, instance, ptr):
        return cls._dll.Sharpen(instance, ptr)

    @classmethod
    def CannyEdge(cls, instance, ptr, kernelSize):
        return cls._dll.CannyEdge(instance, ptr, kernelSize)

    @classmethod
    def Flip(cls, instance, ptr, flipCode):
        return cls._dll.Flip(instance, ptr, flipCode)

    @classmethod
    def MorphOpen(cls, instance, ptr, kernelSize):
        return cls._dll.MorphOpen(instance, ptr, kernelSize)

    @classmethod
    def MorphClose(cls, instance, ptr, kernelSize):
        return cls._dll.MorphClose(instance, ptr, kernelSize)

    @classmethod
    def Skeletonize(cls, instance, ptr):
        return cls._dll.Skeletonize(instance, ptr)

    @classmethod
    def ImageStitchFromPath(cls, instance, path, trajectory = None):
        trajectory = c_int64(0)
        result = cls._dll.ImageStitchFromPath(instance, path.encode("utf-8"), byref(trajectory))
        return result, trajectory.value

    @classmethod
    def ImageStitchCreate(cls, instance):
        return cls._dll.ImageStitchCreate(instance)

    @classmethod
    def ImageStitchAppend(cls, instance, imageStitch, image):
        return cls._dll.ImageStitchAppend(instance, imageStitch, image)

    @classmethod
    def ImageStitchGetResult(cls, instance, imageStitch, trajectory = None):
        trajectory = c_int64(0)
        result = cls._dll.ImageStitchGetResult(instance, imageStitch, byref(trajectory))
        return result, trajectory.value

    @classmethod
    def ImageStitchFree(cls, instance, imageStitch):
        return cls._dll.ImageStitchFree(instance, imageStitch)

    @classmethod
    def CreateDatabase(cls, instance, dbName, password):
        return cls._dll.CreateDatabase(instance, dbName.encode("utf-8"), password.encode("utf-8"))

    @classmethod
    def OpenDatabase(cls, instance, dbName, password):
        return cls._dll.OpenDatabase(instance, dbName.encode("utf-8"), password.encode("utf-8"))

    @classmethod
    def GetDatabaseError(cls, instance, db):
        return cls._dll.GetDatabaseError(instance, db)

    @classmethod
    def CloseDatabase(cls, instance, db):
        return cls._dll.CloseDatabase(instance, db)

    @classmethod
    def GetAllTableNames(cls, instance, db):
        return cls._dll.GetAllTableNames(instance, db)

    @classmethod
    def GetTableInfo(cls, instance, db, tableName):
        return cls._dll.GetTableInfo(instance, db, tableName.encode("utf-8"))

    @classmethod
    def GetTableInfoDetail(cls, instance, db, tableName):
        return cls._dll.GetTableInfoDetail(instance, db, tableName.encode("utf-8"))

    @classmethod
    def ExecuteSql(cls, instance, db, sql):
        return cls._dll.ExecuteSql(instance, db, sql.encode("utf-8"))

    @classmethod
    def ExecuteScalar(cls, instance, db, sql):
        return cls._dll.ExecuteScalar(instance, db, sql.encode("utf-8"))

    @classmethod
    def ExecuteReader(cls, instance, db, sql):
        return cls._dll.ExecuteReader(instance, db, sql.encode("utf-8"))

    @classmethod
    def Read(cls, instance, stmt):
        return cls._dll.Read(instance, stmt)

    @classmethod
    def GetDataCount(cls, instance, stmt):
        return cls._dll.GetDataCount(instance, stmt)

    @classmethod
    def GetColumnCount(cls, instance, stmt):
        return cls._dll.GetColumnCount(instance, stmt)

    @classmethod
    def GetColumnName(cls, instance, stmt, iCol):
        return cls._dll.GetColumnName(instance, stmt, iCol)

    @classmethod
    def GetColumnIndex(cls, instance, stmt, columnName):
        return cls._dll.GetColumnIndex(instance, stmt, columnName.encode("utf-8"))

    @classmethod
    def GetColumnType(cls, instance, stmt, iCol):
        return cls._dll.GetColumnType(instance, stmt, iCol)

    @classmethod
    def Finalize(cls, instance, stmt):
        return cls._dll.Finalize(instance, stmt)

    @classmethod
    def GetDouble(cls, instance, stmt, iCol):
        return cls._dll.GetDouble(instance, stmt, iCol)

    @classmethod
    def GetInt32(cls, instance, stmt, iCol):
        return cls._dll.GetInt32(instance, stmt, iCol)

    @classmethod
    def GetInt64(cls, instance, stmt, iCol):
        return cls._dll.GetInt64(instance, stmt, iCol)

    @classmethod
    def GetString(cls, instance, stmt, iCol):
        return cls._dll.GetString(instance, stmt, iCol)

    @classmethod
    def GetDoubleByColumnName(cls, instance, stmt, columnName):
        return cls._dll.GetDoubleByColumnName(instance, stmt, columnName.encode("utf-8"))

    @classmethod
    def GetInt32ByColumnName(cls, instance, stmt, columnName):
        return cls._dll.GetInt32ByColumnName(instance, stmt, columnName.encode("utf-8"))

    @classmethod
    def GetInt64ByColumnName(cls, instance, stmt, columnName):
        return cls._dll.GetInt64ByColumnName(instance, stmt, columnName.encode("utf-8"))

    @classmethod
    def GetStringByColumnName(cls, instance, stmt, columnName):
        return cls._dll.GetStringByColumnName(instance, stmt, columnName.encode("utf-8"))

    @classmethod
    def InitOlaDatabase(cls, instance, db):
        return cls._dll.InitOlaDatabase(instance, db)

    @classmethod
    def InitOlaImageFromDir(cls, instance, db, _dir, cover):
        return cls._dll.InitOlaImageFromDir(instance, db, _dir.encode("utf-8"), cover)

    @classmethod
    def RemoveOlaImageFromDir(cls, instance, db, _dir):
        return cls._dll.RemoveOlaImageFromDir(instance, db, _dir.encode("utf-8"))

    @classmethod
    def ExportOlaImageDir(cls, instance, db, _dir, exportDir):
        return cls._dll.ExportOlaImageDir(instance, db, _dir.encode("utf-8"), exportDir.encode("utf-8"))

    @classmethod
    def ImportOlaImage(cls, instance, db, _dir, fileName, cover):
        return cls._dll.ImportOlaImage(instance, db, _dir.encode("utf-8"), fileName.encode("utf-8"), cover)

    @classmethod
    def GetOlaImage(cls, instance, db, _dir, fileName):
        return cls._dll.GetOlaImage(instance, db, _dir.encode("utf-8"), fileName.encode("utf-8"))

    @classmethod
    def RemoveOlaImage(cls, instance, db, _dir, fileName):
        return cls._dll.RemoveOlaImage(instance, db, _dir.encode("utf-8"), fileName.encode("utf-8"))

    @classmethod
    def SetDbConfig(cls, instance, db, key, value):
        return cls._dll.SetDbConfig(instance, db, key.encode("utf-8"), value.encode("utf-8"))

    @classmethod
    def GetDbConfig(cls, instance, db, key):
        return cls._dll.GetDbConfig(instance, db, key.encode("utf-8"))

    @classmethod
    def RemoveDbConfig(cls, instance, db, key):
        return cls._dll.RemoveDbConfig(instance, db, key.encode("utf-8"))

    @classmethod
    def SetDbConfigEx(cls, instance, key, value):
        return cls._dll.SetDbConfigEx(instance, key.encode("utf-8"), value.encode("utf-8"))

    @classmethod
    def GetDbConfigEx(cls, instance, key):
        return cls._dll.GetDbConfigEx(instance, key.encode("utf-8"))

    @classmethod
    def RemoveDbConfigEx(cls, instance, key):
        return cls._dll.RemoveDbConfigEx(instance, key.encode("utf-8"))

    @classmethod
    def InitDictFromDir(cls, instance, db, dict_name, dict_path, cover):
        return cls._dll.InitDictFromDir(instance, db, dict_name.encode("utf-8"), dict_path.encode("utf-8"), cover)

    @classmethod
    def ImportDictWord(cls, instance, db, dict_name, pic_file_name, cover):
        return cls._dll.ImportDictWord(instance, db, dict_name.encode("utf-8"), pic_file_name.encode("utf-8"), cover)

    @classmethod
    def ExportDict(cls, instance, db, dict_name, export_dir):
        return cls._dll.ExportDict(instance, db, dict_name.encode("utf-8"), export_dir.encode("utf-8"))

    @classmethod
    def RemoveDict(cls, instance, db, dict_name):
        return cls._dll.RemoveDict(instance, db, dict_name.encode("utf-8"))

    @classmethod
    def RemoveDictWord(cls, instance, db, dict_name, word):
        return cls._dll.RemoveDictWord(instance, db, dict_name.encode("utf-8"), word.encode("utf-8"))

    @classmethod
    def GetDictImage(cls, instance, db, dict_name, word, gap, _dir):
        return cls._dll.GetDictImage(instance, db, dict_name.encode("utf-8"), word.encode("utf-8"), gap, _dir)

    @classmethod
    def SetWindowState(cls, instance, hwnd, state):
        return cls._dll.SetWindowState(instance, hwnd, state)

    @classmethod
    def FindWindow(cls, instance, class_name, title):
        return cls._dll.FindWindow(instance, class_name.encode("utf-8"), title.encode("utf-8"))

    @classmethod
    def GetClipboard(cls, instance):
        return cls._dll.GetClipboard(instance)

    @classmethod
    def SetClipboard(cls, instance, text):
        return cls._dll.SetClipboard(instance, text.encode("utf-8"))

    @classmethod
    def SendPaste(cls, instance, hwnd):
        return cls._dll.SendPaste(instance, hwnd)

    @classmethod
    def GetWindow(cls, instance, hwnd, flag):
        return cls._dll.GetWindow(instance, hwnd, flag)

    @classmethod
    def GetWindowTitle(cls, instance, hwnd):
        return cls._dll.GetWindowTitle(instance, hwnd)

    @classmethod
    def GetWindowClass(cls, instance, hwnd):
        return cls._dll.GetWindowClass(instance, hwnd)

    @classmethod
    def GetWindowRect(cls, instance, hwnd, x1 = None, y1 = None, x2 = None, y2 = None):
        x1 = c_int(0)
        y1 = c_int(0)
        x2 = c_int(0)
        y2 = c_int(0)
        result = cls._dll.GetWindowRect(instance, hwnd, byref(x1), byref(y1), byref(x2), byref(y2))
        return result, x1.value, y1.value, x2.value, y2.value

    @classmethod
    def GetWindowProcessPath(cls, instance, hwnd):
        return cls._dll.GetWindowProcessPath(instance, hwnd)

    @classmethod
    def GetWindowState(cls, instance, hwnd, flag):
        return cls._dll.GetWindowState(instance, hwnd, flag)

    @classmethod
    def GetForegroundWindow(cls, instance):
        return cls._dll.GetForegroundWindow(instance)

    @classmethod
    def GetWindowProcessId(cls, instance, hwnd):
        return cls._dll.GetWindowProcessId(instance, hwnd)

    @classmethod
    def GetClientSize(cls, instance, hwnd, width = None, height = None):
        width = c_int(0)
        height = c_int(0)
        result = cls._dll.GetClientSize(instance, hwnd, byref(width), byref(height))
        return result, width.value, height.value

    @classmethod
    def GetMousePointWindow(cls, instance):
        return cls._dll.GetMousePointWindow(instance)

    @classmethod
    def GetSpecialWindow(cls, instance, flag):
        return cls._dll.GetSpecialWindow(instance, flag)

    @classmethod
    def GetClientRect(cls, instance, hwnd, x1 = None, y1 = None, x2 = None, y2 = None):
        x1 = c_int(0)
        y1 = c_int(0)
        x2 = c_int(0)
        y2 = c_int(0)
        result = cls._dll.GetClientRect(instance, hwnd, byref(x1), byref(y1), byref(x2), byref(y2))
        return result, x1.value, y1.value, x2.value, y2.value

    @classmethod
    def SetWindowText(cls, instance, hwnd, title):
        return cls._dll.SetWindowText(instance, hwnd, title.encode("utf-8"))

    @classmethod
    def SetWindowSize(cls, instance, hwnd, width, height):
        return cls._dll.SetWindowSize(instance, hwnd, width, height)

    @classmethod
    def SetClientSize(cls, instance, hwnd, width, height):
        return cls._dll.SetClientSize(instance, hwnd, width, height)

    @classmethod
    def SetWindowTransparent(cls, instance, hwnd, alpha):
        return cls._dll.SetWindowTransparent(instance, hwnd, alpha)

    @classmethod
    def FindWindowEx(cls, instance, parent, class_name, title):
        return cls._dll.FindWindowEx(instance, parent, class_name.encode("utf-8"), title.encode("utf-8"))

    @classmethod
    def FindWindowByProcess(cls, instance, process_name, class_name, title):
        return cls._dll.FindWindowByProcess(instance, process_name.encode("utf-8"), class_name.encode("utf-8"), title.encode("utf-8"))

    @classmethod
    def MoveWindow(cls, instance, hwnd, x, y):
        return cls._dll.MoveWindow(instance, hwnd, x, y)

    @classmethod
    def GetScaleFromWindows(cls, instance, hwnd):
        return cls._dll.GetScaleFromWindows(instance, hwnd)

    @classmethod
    def GetWindowDpiAwarenessScale(cls, instance, hwnd):
        return cls._dll.GetWindowDpiAwarenessScale(instance, hwnd)

    @classmethod
    def EnumProcess(cls, instance, name):
        return cls._dll.EnumProcess(instance, name.encode("utf-8"))

    @classmethod
    def EnumWindow(cls, instance, parent, title, className, _filter):
        return cls._dll.EnumWindow(instance, parent, title.encode("utf-8"), className.encode("utf-8"), _filter)

    @classmethod
    def EnumWindowByProcess(cls, instance, process_name, title, class_name, _filter):
        return cls._dll.EnumWindowByProcess(instance, process_name.encode("utf-8"), title.encode("utf-8"), class_name.encode("utf-8"), _filter)

    @classmethod
    def EnumWindowByProcessId(cls, instance, pid, title, class_name, _filter):
        return cls._dll.EnumWindowByProcessId(instance, pid, title.encode("utf-8"), class_name.encode("utf-8"), _filter)

    @classmethod
    def EnumWindowSuper(cls, instance, spec1, flag1, type1, spec2, flag2, type2, sort):
        return cls._dll.EnumWindowSuper(instance, spec1.encode("utf-8"), flag1, type1, spec2.encode("utf-8"), flag2, type2, sort)

    @classmethod
    def GetPointWindow(cls, instance, x, y):
        return cls._dll.GetPointWindow(instance, x, y)

    @classmethod
    def GetProcessInfo(cls, instance, pid):
        return cls._dll.GetProcessInfo(instance, pid)

    @classmethod
    def ShowTaskBarIcon(cls, instance, hwnd, show):
        return cls._dll.ShowTaskBarIcon(instance, hwnd, show)

    @classmethod
    def FindWindowByProcessId(cls, instance, process_id, className, title):
        return cls._dll.FindWindowByProcessId(instance, process_id, className.encode("utf-8"), title.encode("utf-8"))

    @classmethod
    def GetWindowThreadId(cls, instance, hwnd):
        return cls._dll.GetWindowThreadId(instance, hwnd)

    @classmethod
    def FindWindowSuper(cls, instance, spec1, flag1, type1, spec2, flag2, type2):
        return cls._dll.FindWindowSuper(instance, spec1.encode("utf-8"), flag1, type1, spec2.encode("utf-8"), flag2, type2)

    @classmethod
    def ClientToScreen(cls, instance, hwnd, x = None, y = None):
        x = c_int(0)
        y = c_int(0)
        result = cls._dll.ClientToScreen(instance, hwnd, byref(x), byref(y))
        return result, x.value, y.value

    @classmethod
    def ScreenToClient(cls, instance, hwnd, x = None, y = None):
        x = c_int(0)
        y = c_int(0)
        result = cls._dll.ScreenToClient(instance, hwnd, byref(x), byref(y))
        return result, x.value, y.value

    @classmethod
    def GetForegroundFocus(cls, instance):
        return cls._dll.GetForegroundFocus(instance)

    @classmethod
    def SetWindowDisplay(cls, instance, hwnd, affinity):
        return cls._dll.SetWindowDisplay(instance, hwnd, affinity)

    @classmethod
    def IsDisplayDead(cls, instance, x1, y1, x2, y2, time):
        return cls._dll.IsDisplayDead(instance, x1, y1, x2, y2, time)

    @classmethod
    def GetWindowsFps(cls, instance, x1, y1, x2, y2):
        return cls._dll.GetWindowsFps(instance, x1, y1, x2, y2)

    @classmethod
    def TerminateProcess(cls, instance, pid):
        return cls._dll.TerminateProcess(instance, pid)

    @classmethod
    def TerminateProcessTree(cls, instance, pid):
        return cls._dll.TerminateProcessTree(instance, pid)

    @classmethod
    def GetCommandLine(cls, instance, hwnd):
        return cls._dll.GetCommandLine(instance, hwnd)

    @classmethod
    def CheckFontSmooth(cls, instance):
        return cls._dll.CheckFontSmooth(instance)

    @classmethod
    def SetFontSmooth(cls, instance, enable):
        return cls._dll.SetFontSmooth(instance, enable)

    @classmethod
    def EnableDebugPrivilege(cls, instance):
        return cls._dll.EnableDebugPrivilege(instance)

    @classmethod
    def SystemStart(cls, instance, applicationName, commandLine):
        return cls._dll.SystemStart(instance, applicationName.encode("utf-8"), commandLine.encode("utf-8"))

    @classmethod
    def CreateChildProcess(cls, instance, applicationName, commandLine, currentDirectory, showType, parentProcessId):
        return cls._dll.CreateChildProcess(instance, applicationName.encode("utf-8"), commandLine.encode("utf-8"), currentDirectory.encode("utf-8"), showType, parentProcessId)


