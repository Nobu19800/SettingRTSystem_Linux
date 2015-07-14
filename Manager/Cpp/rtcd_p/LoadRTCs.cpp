// -*-C++-*-
/*!
 * @file  LoadRTCs.cpp
 * @brief 
 *
 */

#include <coil/stringutil.h>
#include "CompSearch.h"
#include "LoadRTCs.h"

using namespace std;



compParam::compParam(std::string filename, std::string filepath, RTCInitFunction func, std::vector<RTC::RtcBase *> compList)
{
	m_filename = filename;
	m_filepath = filepath;
	m_func = func;
	m_compList = compList;
}


LoadRTCs::LoadRTCs(RTC::Manager* manager)
{
	mgr = manager;

}


LoadRTCs::~LoadRTCs()
{

}

void LoadRTCs::openFile()
{
	coil::Properties& prop(::RTC::Manager::instance().getConfig());
	std::string value = "";
	getProperty(prop, "manager.modules.loadRTCs", value);
	coil::eraseBlank(value);

	if(value == "")
	{
		return;
	}

	

#ifdef _WINDOWS
	coil::replaceString(value, "/", "\\");
#else
	coil::replaceString(value, "\\", "/");
#endif

	std::ifstream ifs( value.c_str() , ios::in | ios::binary );

	int m;
	ifs.read( (char*)&m, sizeof(m) );
	
	for(int i=0;i < m;i++)
	{
		string name;
		name = ReadString( ifs );
		int d;
		ifs.read( (char*)&d, sizeof(d) );
		string path;
		path = ReadString( ifs );
		string dir;
		dir = ReadString( ifs );

		for(int j=0;j < d;j++)
		{
			createComp(name.c_str(),dir.c_str());
		}
	}

	ifs.close();
}


RTCInitFunction LoadRTCs::getFunc(std::string filename,std::string filepath)
{
#ifdef _WINDOWS
	char szFullPath[MAX_PATH];
	_fullpath(szFullPath, filepath.c_str(), sizeof(szFullPath)/sizeof(szFullPath[0]));
	std::string path = "PATH=";
	path += getenv("PATH");
	path += ";";
	path += szFullPath;
	putenv(path.c_str());


	coil::replaceString(filepath, "/", "\\");
	std::string fn = filename + ".dll";


#else
	coil::replaceString(filepath, "\\", "/");
	std::string fn = filename + ".so";

#endif


	coil::DynamicLib *dl = new coil::DynamicLib();

	

	int ret = dl->open(fn.c_str());
	if (ret != 0) {
		
		return NULL;
	}
	dllList.push_back(dl);


	std::string fun = filename + "Init";

	RTCInitFunction InInitFunc = (RTCInitFunction)RTCInitFunction(dl->symbol(fun.c_str()));
	
	return InInitFunc;
}

compParam *LoadRTCs::getCompFromName(std::string name)
{
	for(int i=0;i < compList.size();i++)
	{
		
		if(compList[i].m_filename == name)
		{
			return &compList[i];
		}
	}
	return NULL;
}


class RTC_FinalizeListener
    : public RTC::PostComponentActionListener
{
public:
	RTC_FinalizeListener(RTC::RtcBase * rtc, compParam *list)
	{
		m_rtc = rtc;
		m_list = list;
	};
	void operator()(RTC::UniqueId ec_id, RTC::ReturnCode_t ret)
	{
		//std::cout << m_list->m_filename << coil::otos<int>(ec_id) << std::endl;
		//m_list->m_compList.clear();
		m_list->m_compList.erase(std::remove(m_list->m_compList.begin(), m_list->m_compList.end(), m_rtc), m_list->m_compList.end());
	};
	RTC::RtcBase * m_rtc;
	compParam *m_list;
};


bool LoadRTCs::createComp(const char* filename, const char* filepath)
{
	
	updateCompList();
	
	RTCInitFunction InInitFunc = NULL;
	compParam *preLoadComp = getCompFromName(filename);
	if(preLoadComp)
	{
		InInitFunc = preLoadComp->m_func;
		
	}

	if(preLoadComp == NULL)
	{
		
		InInitFunc = getFunc(filename, filepath);
		if(InInitFunc == NULL)
		{
			return false;
		}
		
		InInitFunc(mgr);
	}

	if(InInitFunc)
	{
		
		RTC::RtcBase *comp = mgr->createComponent(filename);
		
		if(!comp)
			return false;
		

		compParam *cp;

		if(preLoadComp)
		{
			preLoadComp->m_compList.push_back(comp);
			cp = preLoadComp;
		}
		else
		{
			std::vector<RTC::RtcBase *> rl;
			rl.push_back(comp);

			
			
			compList.push_back(compParam(filename, filepath, InInitFunc, rl));
			cp = &compList[compList.size()-1];
			
		}
		comp->addPostComponentActionListener(RTC::POST_ON_FINALIZE, new RTC_FinalizeListener(comp,cp));
		
		return true;
	}
	else
	{
		return false;
	}
	return false;

}

bool LoadRTCs::removeComp(const char* filename)
{
	updateCompList();
	compParam *c = getCompFromName(filename);
	
	if(c)
	{
		if(c->m_compList.size() != 0)
		{
			c->m_compList[c->m_compList.size()-1]->exit();
			c->m_compList.pop_back();
		}
		else
		{
			return false;
		}
		
	}
	else
	{
		return false;
	}
	return true;

}

void LoadRTCs::updateCompList()
{
	/*std::cout << "test2" << std::endl;
	for (std::vector<compParam>::iterator it = compList.begin(); it != compList.end(); ++it)
	{
		for (std::vector<RTC::RtcBase *>::iterator rtc = (*it).m_compList.begin(); rtc != (*it).m_compList.end();)
		{
			
			try
			{
				//(*rtc)->getObjRef()->get_owned_contexts();
				(*rtc)->getObjRef();
				++rtc;
			}
			catch (...)
			{
				std::cout << "test" << std::endl;
				rtc = (*it).m_compList.erase(rtc);
				//++rtc;
			}
			
		}
		
	}*/
}



// End of example implementational code



