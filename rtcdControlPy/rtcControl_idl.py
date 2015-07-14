# Python stubs generated by omniidl from idl/rtcControl.idl

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA

_omnipy.checkVersion(3,0, __file__)

# #include "BasicDataType.idl"
import BasicDataType_idl
_0_RTC = omniORB.openModule("RTC")
_0_RTC__POA = omniORB.openModule("RTC__POA")

#
# Start of module "rtcControl"
#
__name__ = "rtcControl"
_0_rtcControl = omniORB.openModule("rtcControl", r"idl/rtcControl.idl")
_0_rtcControl__POA = omniORB.openModule("rtcControl__POA", r"idl/rtcControl.idl")


# typedef ... rtcPathSeq
class rtcPathSeq:
    _NP_RepositoryId = "IDL:rtcControl/rtcPathSeq:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_rtcControl.rtcPathSeq = rtcPathSeq
_0_rtcControl._d_rtcPathSeq  = (omniORB.tcInternal.tv_sequence, (omniORB.tcInternal.tv_string,0), 0)
_0_rtcControl._ad_rtcPathSeq = (omniORB.tcInternal.tv_alias, rtcPathSeq._NP_RepositoryId, "rtcPathSeq", (omniORB.tcInternal.tv_sequence, (omniORB.tcInternal.tv_string,0), 0))
_0_rtcControl._tc_rtcPathSeq = omniORB.tcInternal.createTypeCode(_0_rtcControl._ad_rtcPathSeq)
omniORB.registerType(rtcPathSeq._NP_RepositoryId, _0_rtcControl._ad_rtcPathSeq, _0_rtcControl._tc_rtcPathSeq)
del rtcPathSeq

# struct RTC_Data
_0_rtcControl.RTC_Data = omniORB.newEmptyClass()
class RTC_Data (omniORB.StructBase):
    _NP_RepositoryId = "IDL:rtcControl/RTC_Data:1.0"

    def __init__(self, name, num):
        self.name = name
        self.num = num

_0_rtcControl.RTC_Data = RTC_Data
_0_rtcControl._d_RTC_Data  = (omniORB.tcInternal.tv_struct, RTC_Data, RTC_Data._NP_RepositoryId, "RTC_Data", "name", (omniORB.tcInternal.tv_string,0), "num", omniORB.tcInternal.tv_short)
_0_rtcControl._tc_RTC_Data = omniORB.tcInternal.createTypeCode(_0_rtcControl._d_RTC_Data)
omniORB.registerType(RTC_Data._NP_RepositoryId, _0_rtcControl._d_RTC_Data, _0_rtcControl._tc_RTC_Data)
del RTC_Data

# typedef ... RTC_List
class RTC_List:
    _NP_RepositoryId = "IDL:rtcControl/RTC_List:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_rtcControl.RTC_List = RTC_List
_0_rtcControl._d_RTC_List  = (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:rtcControl/RTC_Data:1.0"], 0)
_0_rtcControl._ad_RTC_List = (omniORB.tcInternal.tv_alias, RTC_List._NP_RepositoryId, "RTC_List", (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:rtcControl/RTC_Data:1.0"], 0))
_0_rtcControl._tc_RTC_List = omniORB.tcInternal.createTypeCode(_0_rtcControl._ad_RTC_List)
omniORB.registerType(RTC_List._NP_RepositoryId, _0_rtcControl._ad_RTC_List, _0_rtcControl._tc_RTC_List)
del RTC_List

# interface RTCDataInterface
_0_rtcControl._d_RTCDataInterface = (omniORB.tcInternal.tv_objref, "IDL:rtcControl/RTCDataInterface:1.0", "RTCDataInterface")
omniORB.typeMapping["IDL:rtcControl/RTCDataInterface:1.0"] = _0_rtcControl._d_RTCDataInterface
_0_rtcControl.RTCDataInterface = omniORB.newEmptyClass()
class RTCDataInterface :
    _NP_RepositoryId = _0_rtcControl._d_RTCDataInterface[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_rtcControl.RTCDataInterface = RTCDataInterface
_0_rtcControl._tc_RTCDataInterface = omniORB.tcInternal.createTypeCode(_0_rtcControl._d_RTCDataInterface)
omniORB.registerType(RTCDataInterface._NP_RepositoryId, _0_rtcControl._d_RTCDataInterface, _0_rtcControl._tc_RTCDataInterface)

# RTCDataInterface operations and attributes
RTCDataInterface._d_getRTC = ((), (omniORB.tcInternal.tv_boolean, omniORB.typeMapping["IDL:rtcControl/rtcPathSeq:1.0"]), None)
RTCDataInterface._d_createComp = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0)), (omniORB.tcInternal.tv_boolean, ), None)
RTCDataInterface._d_removeComp = (((omniORB.tcInternal.tv_string,0), ), (omniORB.tcInternal.tv_boolean, ), None)
RTCDataInterface._d_getCompList = ((), (omniORB.tcInternal.tv_boolean, omniORB.typeMapping["IDL:rtcControl/RTC_List:1.0"]), None)

# RTCDataInterface object reference
class _objref_RTCDataInterface (CORBA.Object):
    _NP_RepositoryId = RTCDataInterface._NP_RepositoryId

    def __init__(self):
        CORBA.Object.__init__(self)

    def getRTC(self, *args):
        return _omnipy.invoke(self, "getRTC", _0_rtcControl.RTCDataInterface._d_getRTC, args)

    def createComp(self, *args):
        return _omnipy.invoke(self, "createComp", _0_rtcControl.RTCDataInterface._d_createComp, args)

    def removeComp(self, *args):
        return _omnipy.invoke(self, "removeComp", _0_rtcControl.RTCDataInterface._d_removeComp, args)

    def getCompList(self, *args):
        return _omnipy.invoke(self, "getCompList", _0_rtcControl.RTCDataInterface._d_getCompList, args)

    __methods__ = ["getRTC", "createComp", "removeComp", "getCompList"] + CORBA.Object.__methods__

omniORB.registerObjref(RTCDataInterface._NP_RepositoryId, _objref_RTCDataInterface)
_0_rtcControl._objref_RTCDataInterface = _objref_RTCDataInterface
del RTCDataInterface, _objref_RTCDataInterface

# RTCDataInterface skeleton
__name__ = "rtcControl__POA"
class RTCDataInterface (PortableServer.Servant):
    _NP_RepositoryId = _0_rtcControl.RTCDataInterface._NP_RepositoryId


    _omni_op_d = {"getRTC": _0_rtcControl.RTCDataInterface._d_getRTC, "createComp": _0_rtcControl.RTCDataInterface._d_createComp, "removeComp": _0_rtcControl.RTCDataInterface._d_removeComp, "getCompList": _0_rtcControl.RTCDataInterface._d_getCompList}

RTCDataInterface._omni_skeleton = RTCDataInterface
_0_rtcControl__POA.RTCDataInterface = RTCDataInterface
omniORB.registerSkeleton(RTCDataInterface._NP_RepositoryId, RTCDataInterface)
del RTCDataInterface
__name__ = "rtcControl"

#
# End of module "rtcControl"
#
__name__ = "rtcControl_idl"

_exported_modules = ( "rtcControl", )

# The end.
