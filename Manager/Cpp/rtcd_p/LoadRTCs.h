// -*-C++-*-
/*!
 * @file  LoadRTCs.h
 * @brief 
 *
 */



#ifndef LOADRTCS_H
#define LOADRTCS_H



#include <rtm/Manager.h>
#include <rtm/DataFlowComponentBase.h>
#include <coil/DynamicLib.h>
 
typedef void (*RTCInitFunction)(RTC::Manager* pManager);


class compParam
{
public:
	compParam(std::string name, std::string filename, std::string filepath, RTCInitFunction func, std::vector<RTC::RtcBase *> compList);
	std::string m_name;
	std::string m_filename;
	std::string m_filepath;
	RTCInitFunction m_func;
	std::vector<RTC::RtcBase *> m_compList;
};


class LoadRTCs
{
 private:


 public:
  
  LoadRTCs(RTC::Manager* manager);
  
  virtual ~LoadRTCs();

   void updateCompList();
   
   bool createComp(const char* name, const char* filename, const char* filepath);
   bool removeComp(const char* name);
   
   compParam *getCompFromName(std::string name);
   RTCInitFunction getFunc(std::string filename,std::string filepath);
   void openFile();

  template <class T>
    void getProperty(coil::Properties& prop, const char* key, T& value)
    {
    if (prop.findNode(key) != 0)
      {
        T tmp;
        if (coil::stringTo(tmp, prop[key].c_str()))
          {
            value = tmp;
          }
      }
    }


	std::vector<coil::DynamicLib*> dllList;
	std::vector<compParam> compList;
	RTC::Manager* mgr;

private:

};



#endif // RTCCONTROLSVC_IMPL_H


