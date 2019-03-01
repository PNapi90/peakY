#include "PeakFinder.hpp"

//------------------------------------------

PeakFinder::PeakFinder(std::vector<int> &d0s,
                       int _binsE,
                       int _binsX,
                       int _thrNum,
                       int _Egamma,
                       double _MaxArea)
    : binsE(_binsE),
      binsX(_binsX),
      thrNum(_thrNum),
      Egamma(_Egamma),
      MaxArea(_MaxArea)
{
    d0Range = std::vector<int>(2,0);
    
    for(int i = 0;i < 2;++i)
        d0Range[i] = d0s[i];
    
    Histogram = std::vector<std::vector<std::vector<double>>>(150,
                std::vector<std::vector<double>>(binsE,
                std::vector<double>(binsX,0)));
    
    HistogramMax = std::vector<std::vector<int>>(150,
                   std::vector<int>(binsE,-1));
                
    Norm = std::vector<std::vector<double>>(150,
           std::vector<double>(binsE,0));

    HistogramLimits = std::vector<std::vector<std::vector<int>>>(150,
                      std::vector<std::vector<int>>(binsE,
                      std::vector<int>(2,0)));

    folder = "Histograms/ExpEGamma_" + std::to_string(Egamma) + "/d0_";
    
    std::cout << "Created PeakFinder # " << thrNum << " with d0 in [" << d0Range[0] << "," << d0Range[1] << ")" << std::endl;
}

//------------------------------------------

PeakFinder::~PeakFinder()
{}

//------------------------------------------

void PeakFinder::DoIt()
{

    int iter = 0;
    saveCalled = false;

    double NormConst = 1;//(2./((double)binsX));

    std::ifstream DATA;
    std::string name,nameF;
    for (int i = d0Range[0]; i < d0Range[1]; ++i)
    {
        if (i % 4 != 0)
            continue;

        iter = 0;
        nameF = folder + std::to_string(i);
        for (int j = 0; j < 600; ++j)
        {
            if(j % 4 != 0)
                continue;
            
            name = nameF + "/d12_" + std::to_string(j);
            DATA.open(name);

            if (DATA.fail())
            {
                std::cerr << "Could not open " << name << std::endl;
                exit(1);
            }
            if(thrNum == 0 && j % 10 == 0)
            {
                std::cout << "\rFile " << name << " opened";
                std::cout.flush();
            }
            for(int o = 0;o < binsE;++o)
            {
                for(int k = 0;k < binsX;++k)
                {
                    DATA >> Histogram[iter][o][k];
                    Norm[iter][o] += Histogram[iter][o][k]*NormConst;
                }
                    
            }
            ++iter;

            DATA.close();
            DATA.clear();
        }
        FindMaxima(iter);
        if(thrNum == 0)
            std::cout << "\n-> Maxima set" << std::endl;
        FindThreshold(iter);
        if(thrNum == 0)
            std::cout << "-> Thresholds set" << std::endl;
        SAVE(nameF);
        saveCalled = true;
        if(thrNum == 0)
        {
            std::cout << "d0_" << i << " saved and fully processed" << std::endl;
            std::cout << "-------------------------------------------------" << std::endl;
        }
    }
}

//------------------------------------------

void PeakFinder::FindMaxima(int iter)
{
    if(iter != Histogram.size())
    {
        std::cerr << "Length mismatch: " << iter << " <-> " << Histogram.size() << std::endl;
        exit(1);
    }

    double maximum = 0;
    int maxPos = 0;

    for(int i = 0;i < iter;++i)
    {
        for(int j = 0;j < Histogram[0].size();++j)
        {   

            maxPos = -1;
            maximum = 0;

            if(Norm[i][j] == 0)
                continue;

            for(int k = 0;k < Histogram[0][0].size();++k)
            {
                Histogram[i][j][k] /= Norm[i][j];
                if(maximum <= Histogram[i][j][k])
                {
                    maximum = Histogram[i][j][k];
                    maxPos = k;
                }
            }
            HistogramMax[i][j] = maxPos;
        }
    }
}

//------------------------------------------

void PeakFinder::FindThreshold(int iter)
{
    int left = 0,right = 0,iterator = 0,posP = 0,posM = 0;
    double area = 0;

    int posPM[2] = {0,0};

    bool Escape = false;


    

    double binwidth = 1;//180./((double) binsX);

    std::vector<int> CalledPos(Histogram[0][0].size(),0);

    for(int i = 0;i < Histogram.size();++i)
    {
        for(int j = 0;j < Histogram[0].size();++j)
        {   
            left = 0;
            right = 0;
            iterator = 0;
            area = 0;

            posPM[0] = 0;
            posPM[1] = 0;

            Escape = false;

            for(int o = 0;o < CalledPos.size();++o)
                CalledPos[o] = 0;

            if(Norm[i][j] == 0 || HistogramMax[i][j] == -1)
                continue;

            RecheckNorm(i, j);

            while(!Escape)
            {
                
                for(int o = 0;o < 2;++o)
                {
                    posPM[o] = HistogramMax[i][j] + pow(-1,o)*iterator;
                    
                    //only allow values inside defined range
                    if(posPM[o] <= 0)
                        posPM[o] = 0;
                    if(posPM[o] >= binsX - 1)
                        posPM[o] = binsX - 1;
                    
                    ++CalledPos[posPM[o]];

                }
                
                if(iterator == 0)
                    area += binwidth * Histogram[i][j][posPM[0]];

                else
                {   
                    //add area left and right to peak
                    //(boolean operation: only add area for each bin once)
                    for(int o = 0;o < 2;++o)
                        area += binwidth * Histogram[i][j][posPM[o]]*(CalledPos[posPM[o]] == 1);
                }
                
                if(thrNum == 0 && iter > 0 && saveCalled && false)
                    std::cout << area << " " << posPM[1] << " " << posPM[0] << " " << HistogramMax[i][j] << " " << Norm[i][j]<< std::endl;


                if(area >= MaxArea)
                {
                    Escape = true;
                    continue;
                }
                ++iterator;
            }
            //if(thrNum == 0)
            //    std::cout << "Bin_i " << i << " Bin_j " << j << " done " << std::endl;
            for(int o = 0;o < 2;++o)
                HistogramLimits[i][j][o] = posPM[1-o];
        }
    }
} 

//------------------------------------------

void PeakFinder::SAVE(std::string nameF)
{
    std::string name;
    std::ofstream DATA;
    
    for(int j = 0;j < Histogram.size();++j)
    {
        name = nameF + "/d12_" + std::to_string(j * 4) + "_Ranges";
        DATA.open(name);

        if (DATA.fail())
        {
            std::cerr << "Could not open output file " << name << std::endl;
            exit(1);
        }

        for(int k = 0;k < Histogram[0].size();++k)
        {
            for(int o = 0;o < 2;++o)
                DATA << HistogramLimits[j][k][o] << " ";
            DATA << std::endl;

            //reset norms
            Norm[j][k] = 0;
        }
        DATA.close();
        DATA.clear();
    }


}

//------------------------------------------

std::thread PeakFinder::threading()
{
    return std::thread([=]{DoIt();});
}

//------------------------------------------

inline void PeakFinder::RecheckNorm(int i,int j)
{   
    double n = 0;

    for(auto X : Histogram[i][j])
    {
        n += X;
    }

    if(n < 0.99)
    {
        std::cerr << "\nBad norm in (i,j) = (" << i << "," << j << ") with n = " << n << " encountered!" << std::endl;
        exit(1);
    }
}

//------------------------------------------