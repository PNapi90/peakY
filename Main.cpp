#include <iostream>
#include <thread>
#include <vector>
#include <string>

#include "PeakFinder.hpp"

int main(int argc,char** argv)
{

    int nthr = 1,Egamma = 661;
    bool threadFlag = false,EFlag = false;
    std::string s;
    
    for(int i = 0;i < argc;++i)
    {
        s = std::string(argv[i]);
        if(s == "-t")
        {
            threadFlag = true;
            continue;
        }
        if(threadFlag)
        {
            nthr = std::stoi(s);
            threadFlag = false;
            continue;
        }
        if (s == "-E")
        {
            EFlag = true;
            continue;
        }
        if (EFlag)
        {
            Egamma = std::stoi(s);
            EFlag = false;
            continue;
        }
    }

    int thetaBin = 181;
    int Ebin = Egamma == 661 ? 175 : Egamma/4 + 1;

    std::vector<std::shared_ptr<PeakFinder>> Finders;
    Finders.reserve(nthr);

    int bin = 600/nthr;
    std::vector<int> d0Range(2,0);

    double MaxArea = Egamma == 661 ? 0.95 : 0.99;

    std::cout << "\n-------------------------------------------------" << std::endl;

    for(int i = 0;i < nthr;++i)
    {
        d0Range[0] = d0Range[1];
        d0Range[1] = d0Range[0] + bin;
        Finders.push_back(std::make_shared<PeakFinder>(d0Range,Ebin,thetaBin,i,Egamma,MaxArea));
    }
    std::cout << "-------------------------------------------------" << std::endl;

    std::thread t[nthr];
    for(int i = 0;i < nthr;++i)
        t[i] = Finders[i]->threading();
    
    for(int i = 0;i < nthr;++i)
        t[i].join();

    return 0;
}