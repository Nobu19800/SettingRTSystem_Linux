// -*-C++-*-
/*!
 * @file  rtcControlSVC_impl.cpp
 * @brief Service implementation code of rtcControl.idl
 *
 */

#include "rtcControlSVC_impl.h"

/*
 * Example implementational code for IDL interface rtcControl::RTCDataInterface
 */
RTCDataInterfaceSVC_impl::RTCDataInterfaceSVC_impl(RTC::Manager* manager)
{
	mgr = manager;
  // Please add extra constructor code here.
}


RTCDataInterfaceSVC_impl::~RTCDataInterfaceSVC_impl()
{
  // Please add extra destructor code here.
}


/*
 * Methods corresponding to IDL attributes and operations
 */
CORBA::Boolean RTCDataInterfaceSVC_impl::getRTC(rtcControl::rtcPathSeq_out paths)
{
	rtcControl::rtcPathSeq_var paths_var = new rtcControl::rtcPathSeq;
	std::vector<RTC::RtcBase*> comps = mgr->getComponents();
	paths_var->length(comps.size());
	for(int i=0;i < comps.size();i++)
	{
		RTC::ComponentProfile_var prof;
		
		prof = comps[i]->get_component_profile();
		RTC::NVList prop = prof->properties;
		
		//NVUtil::dump(prof->properties);
		
		CORBA::Any value = NVUtil::find(prop, "naming.names");
		const char* ans;
		value >>= ans;
		
		paths_var[i] = ans;
		
		
	}
	paths = paths_var._retn();
  // Please insert your code here and remove the following warning pragma
#ifndef WIN32
  #warning "Code missing in function <CORBA::Boolean RTCDataInterfaceSVC_impl::getRTC(rtcControl::rtcPathSeq_out paths)>"
#endif
  return 0;
}

CORBA::Boolean RTCDataInterfaceSVC_impl::createComp(const char* filename, const char* filepath)
{
  // Please insert your code here and remove the following warning pragma
#ifndef WIN32
  #warning "Code missing in function <CORBA::Boolean RTCDataInterfaceSVC_impl::createComp(const char* filename, const char* filepath)>"
#endif
  return 0;
}

CORBA::Boolean RTCDataInterfaceSVC_impl::removeComp(const char* name)
{
  // Please insert your code here and remove the following warning pragma
#ifndef WIN32
  #warning "Code missing in function <CORBA::Boolean RTCDataInterfaceSVC_impl::removeComp(const char* name)>"
#endif
  return 0;
}



// End of example implementational code



