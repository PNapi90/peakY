#ifndef PEAK_FINDER_H
#define PEAK_FINDER_H

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <thread>
#include <cmath>

class PeakFinder
{
private:

    bool saveCalled;
    int binsE,binsX,thrNum;

    std::string folder;
    std::vector<int> d0Range;
    std::vector<std::vector<int>> HistogramMax;
    std::vector<std::vector<double>> Norm;
    std::vector<std::vector<std::vector<int>>> HistogramLimits;
    std::vector<std::vector<std::vector<double>>> Histogram;

    void DoIt();
    void FindThreshold(int iter);
    void FindMaxima(int iter);
    void SAVE(std::string nameF);

    inline void RecheckNorm(int i,int j);

public:
    PeakFinder(std::vector<int> &d0s,
               int _binsE,
               int _binsX,
               int _thrNum);
    ~PeakFinder();

    std::thread threading();
};


#endif
