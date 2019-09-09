#include <iostream>
#include <stdio.h>
#include <math.h>
#include <iomanip>
#include <tuple>
#include <functional>
#include <thread>


/*
   TODO
   write function to count value for sin, sh, exp, ln

*/

using returnableTuple = std::tuple<double, double, int>;
class Task
{
private:
   enum class NumberOfTask
   {
      First , 
      Second
   };
private:
   double m_a;
   double m_b;
   double m_x;
   double m_PI;
   double m_nForSecondTask;
public:
  
   Task();
   Task(const double a, const double b);
   void createFirstTable();
   void createSecondTable() const;
private:
   returnableTuple getCosFunctionValue(double x, NumberOfTask task, double eps = 0.0) const;
   returnableTuple getSinFunctionValue(double x, NumberOfTask task, double eps = 0.0) const;
   returnableTuple getShFunctionValue(double x, NumberOfTask task, double eps = 0.0) const;
   returnableTuple getChFunctionValue(double x, NumberOfTask task, double eps = 0.0) const;
   returnableTuple getExpFunctionValue(double x, NumberOfTask task, double eps = 0.0) const;
   returnableTuple getLnFunctionValue(double x, NumberOfTask task, double eps = 0.0) const;
};

Task::Task()
   : Task(0 , 0)
{}
Task::Task(const double a, const double b)
   : m_a(a)
   , m_b(b)
   , m_x((m_a + m_b) / 2)
   , m_PI(3.14159265)
{}
void Task::createFirstTable()
{
   std::cout <<                  "eps" 
             << std::setw(17) << "n"   
             << std::setw(8)  << "fluff" 
             << std::setw(21) << "last (R)" 
             << std::endl << std::endl;
   auto step = std::pow(10, -3);
   auto limit = std::pow(10, -14);
   for (auto eps = std::pow(10, -2); eps > limit; eps *= step)
   {
      double R;
      int n;
      double fluff;
      std::tie(fluff, R, n) = getSinFunctionValue(m_PI / 2 - m_x , NumberOfTask::First, eps);
      fluff = fabs(cos(m_PI / 2 - m_x) - fluff);
      std::cout << std::setw(6)  << eps 
                << std::setw(4)  << n 
                << std::setw(18) << fluff 
                << std::setw(18) << R 
                << std::endl;

      if (eps == pow(10, -8))
         m_nForSecondTask = n;
   }

}
returnableTuple Task::getCosFunctionValue(double x, NumberOfTask task, double eps) const
{
   double U = 1.0, result = 1.0;
   int k = 1;
   auto lambda = [](double x , int k , double U)
   {
      return -(std::pow(x, 2) / (2 * k * (2 * k - 1))) * U;
   };
   if (task == NumberOfTask::First)
   {
      while (std::fabs(U) > eps)
      {
         U = lambda(x, k, U);
         result += U;
         k++;
      }
   } 
   else
   {
      for (; k < m_nForSecondTask; ++k)
      {
         U = lambda(x, k, U);
         result += U;
      }
   }
   return std::make_tuple(result , U , k);
}
returnableTuple Task::getSinFunctionValue(double x, NumberOfTask task, double eps) const
{
   double U = x, result = 1.0;
   int k = 1;
   auto lambda = [](double x, int k, double U)
   {
      return -(std::pow(x, 2) / (2 * k * (2 * k + 1))) * U;
   };
   if (task == NumberOfTask::First)
   {
      while (std::fabs(lambda(x, k, U)) > eps)
      {
         U = lambda(x, k, U);
         result += U;
         k++;
      }
   }
   else
   {
      for (; k < m_nForSecondTask; ++k)
      {
         U = lambda(x, k, U);
         result += U;
      }
   }
   return std::make_tuple(result, U, k);
}
returnableTuple Task::getChFunctionValue(double x, NumberOfTask task, double eps) const
{
   double U = x, result = 1.0;
   int k = 1;
   auto lambda = [](double x, int k, double U)
   {
      return -(std::pow(x, 2) / (2 * k * (2 * k - 1))) * U;
   };
   if (task == NumberOfTask::First)
   {
      while (std::fabs(U) > eps)
      {
         U = lambda(x, k, U);
         result += U;
         k++;
      }
   }
   else
   {
      for (; k < m_nForSecondTask; ++k)
      {
         U = lambda(x, k, U);
         result += U;
      }
   }
   return std::make_tuple(result, U / 3, k);
}
void Task::createSecondTable() const
{
   double h = (m_b - m_a) / 10;
   std::cout <<                  "x_i" 
             << std::setw(21) << "fluff" 
             << std::setw(21) << "last (R)" 
             << std::endl << std::endl;
   for (int i = 0; i < 10; i++) 
   {
      double x = m_a + h * i;
      double R;
      double fluff;
      int unused;
      std::tie(fluff, R, unused) = getSinFunctionValue(m_PI / 2 - x, NumberOfTask::Second);
      fluff = fabs(cos(m_PI / 2 - x) - fluff);
      std::cout << std::setw(7)  << std::setprecision(4) << x
                << std::setw(22) << std::setprecision(14) << fluff
                << std::setw(22)  << fabs(R) << std::endl;
   }
   std::cout << std::endl;
}

int main()
{
   std::cout.precision(14);
   std::cout.setf(std::ios::fixed | std::ios::right);
   Task task(-3.3, 24.9);
   task.createFirstTable();
   task.createSecondTable();

   std::cin.get();
}