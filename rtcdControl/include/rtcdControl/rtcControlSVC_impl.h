// -*-C++-*-
/*!
 * @file  rtcControlSVC_impl.h
 * @brief Service implementation header of rtcControl.idl
 *
 */

#include <rtm/DataFlowComponentBase.h>
#include "BasicDataTypeSkel.h"

#include "rtcControlSkel.h"

#ifndef RTCCONTROLSVC_IMPL_H
#define RTCCONTROLSVC_IMPL_H

#include <rtm/Manager.h>

#include "LoadRTCs.h"
 





/*!
 * @class RTCDataInterfaceSVC_impl
 * Example class implementing IDL interface rtcControl::RTCDataInterface
 */
class RTCDataInterfaceSVC_impl
 : public virtual POA_rtcControl::RTCDataInterface,
   public virtual PortableServer::RefCountServantBase
{
 private:
   // Make sure all instances are built on the heap by making the
   // destructor non-public
   //virtual ~RTCDataInterfaceSVC_impl();

 public:
  /*!
   * @brief standard constructor
   */
	 RTCDataInterfaceSVC_impl(RTC::Manager* manager);
  /*!
   * @brief destructor
   */
   virtual ~RTCDataInterfaceSVC_impl();

   // attributes and operations
   CORBA::Boolean getRTC(rtcControl::rtcPathSeq_out paths);
   CORBA::Boolean createComp(const char* filename, const char* filepath);
   CORBA::Boolean removeComp(const char* filename);
   CORBA::Boolean getCompList(rtcControl::RTC_List_out names);
   

private:
	LoadRTCs *loadRTCsObject;
	RTC::Manager* mgr;

};



#endif // RTCCONTROLSVC_IMPL_H


