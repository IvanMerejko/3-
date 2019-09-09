#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <cmath>
#include <iomanip>
#include <chrono>

/*
   TODO
   How calculate a,b,x,m,M ?
   For another two methods need solve the equation f(x)*f(x)'' > 0 
*/

class Task
{
   double m_x;
   double m_a;
   double m_b;
   double m_m;
   double m_M;
   double m_c;
   int m_nForIterationMethod;
   int m_nForBisectionMethod;
   int m_nForChordMethod;
   int m_nForTangentMethod;
public:
   Task(double x , double a, double b, double m, double M);
   Task(double x, double a, double b, double m, double M , double c);
   void createTableForIterationMethod();
   void createTableForBisectionMethod();
   void createTableForChordMethod();
   void createTableForTangentMethod();
   void createThirdTable();
private:
   double getFunctionValue(double x) const;
   

   double getByIterationMethod(double eps);
   double getByBisectionMethod(double a, double b, double eps);
   double getByChordMethod(double eps);
   double getByTangentMethod(double eps);

};

Task::Task(double x, double a, double b, double m, double M , double c)
   : m_x(x) 
   , m_a(a)
   , m_b(b)
   , m_m(m)
   , m_M(M)
   , m_c(c)
   , m_nForIterationMethod(0)
   , m_nForBisectionMethod(0)
   , m_nForChordMethod(0)
   , m_nForTangentMethod(0)
{}
Task::Task(double x, double a, double b, double m, double M)
   : Task(x, a, b, m, M, 0)
{}

void Task::createTableForIterationMethod()
{
   auto step = std::pow(10, -3);
   auto limit = std::pow(10, -14);
   std::cout << "IterationMethod\n";
   std::cout << "\tEps" << "\t\tRoot's value\t" << "\tEstimation accuracy" << std::endl;
   for (auto eps = std::pow(10, -2); eps > limit; eps *= step)
   {
      std::cout << std::fixed << std::setprecision(15) << eps << '\t' << m_x << '\t' << std::abs(getByIterationMethod(eps) - m_x) << std::endl;
   }
}

void Task::createTableForBisectionMethod()
{
   auto step = std::pow(10, -3);
   auto limit = std::pow(10, -14);
   std::cout << "BisectionMethod\n";
   std::cout << "\tEps" << "\t\tRoot's value\t" << "\tEstimation accuracy" << std::endl;
   for (auto eps = std::pow(10, -2); eps > limit; eps *= step)
   {
      std::cout << std::fixed << std::setprecision(15) << eps << '\t' << m_x << '\t' << std::abs(getByBisectionMethod(m_a, m_b, eps) - m_x) << std::endl;
   }
}

void Task::createTableForChordMethod()
{
   auto step = std::pow(10, -3);
   auto limit = std::pow(10, -14);
   std::cout << "ChordMethod\n";
   std::cout << "\tEps" << "\t\tRoot's value\t" << "\tEstimation accuracy" << std::endl;
   for (auto eps = std::pow(10, -2); eps > limit; eps *= step)
   {
      std::cout << std::fixed << std::setprecision(15) << eps << '\t' << m_x << '\t' << std::abs(getByChordMethod(eps) - m_x) << std::endl;
   }
}

void Task::createTableForTangentMethod()
{
   auto step = std::pow(10, -3);
   auto limit = std::pow(10, -14);
   std::cout << "TangentMethod\n";
   std::cout << "\tEps" << "\t\tRoot's value\t" << "\tEstimation accuracy" << std::endl;
   for (auto eps = std::pow(10, -2); eps > limit; eps *= step)
   {
      std::cout << std::fixed << std::setprecision(15) << eps << '\t' << m_x << '\t' << std::abs(getByTangentMethod(eps) - m_x) << std::endl;
   }
}

void Task::createThirdTable()
{
   std::cout << "TASK_3 - Speed tables" << std::endl << std::endl;
   std::cout << std::setw(17) << "eps" << std::setw(17) << "IterationMethod"
                      << std::setw(17)  << "BisectionMethod" 
                      << std::setw(17)  << "ChordMethod" 
                      << std::setw(17)  << "TangentMethod" << std::endl << std::endl;
   
   for (double eps = pow(10, -2); eps > pow(10, -14); eps = eps * pow(10, -3))
   {
      getByIterationMethod(eps);
      getByBisectionMethod(m_a, m_b , eps);
      getByChordMethod(eps);
      getByTangentMethod(eps);
      std::cout << std::fixed << std::setprecision(14) << std::setw(16) << eps 
                              << std::setprecision(0)  << std::setw(17)  << m_nForIterationMethod
                                                       << std::setw(17)  << m_nForBisectionMethod 
                                                       << std::setw(17)  << m_nForChordMethod 
                                                       << std::setw(17)  << m_nForTangentMethod << std::endl;
   }
}

double Task::getByIterationMethod(double eps)
{
   m_nForIterationMethod = 0;
   double lambda = 1 / m_M;
   double q = 1 - m_m / m_M;
   double x = m_a;
   auto getCorrectFunctionValue = [&](double x)
   {
      return x - lambda*getFunctionValue(x);
   };
   auto limit = ((1 - q) * eps / q);
   while (std::abs(getCorrectFunctionValue(x) - x) > limit)
   {
      x = getCorrectFunctionValue(x);
      ++m_nForIterationMethod;
   }
   return x;
}

double Task::getFunctionValue(double x) const
{
   return log(2 + sin(x)) - (x / 10) - 0.5;
}

double Task::getByBisectionMethod(double a, double b, double eps)
{
   m_nForBisectionMethod = 0;
   double x = 0.0;
   while (std::abs(getFunctionValue(x) - eps) > eps)
   {
      x = (a + b) / 2;
      if (getFunctionValue(x) * getFunctionValue(a) < 0)
      {
         b = x;
      }
      else if (getFunctionValue(x) * getFunctionValue(b) < 0)
      {
         a = x;
      }
      ++m_nForBisectionMethod;
   }
   return x;
}

double Task::getByChordMethod(double eps)
{
   m_nForChordMethod = 0;
   double x = std::abs(m_a - m_c) < std::abs(m_b - m_c) ? m_b : m_a;
   double m = m_b;// for current function because min(f`(x)) in [a;b] is when x = b
   while (std::abs(getFunctionValue(x) / m_b) > eps) 
   {
      x = x - (getFunctionValue(x)*(x - m_c)) / (getFunctionValue(x) - getFunctionValue(m_c));
      ++m_nForChordMethod;
   }
   
   return x;
}

double Task::getByTangentMethod(double eps)
{
   auto derivative = [](double x)
   {
      return (cos(x) / (2 + sin(x))) - 1 / 10;
   };//derivative for the given function

   m_nForTangentMethod = 0;

   //x must be equal to tne of the line where f(x)f(x)'' > 0
   //for current function it can be any of two values
   double x = m_a;;
   double m = m_b;// for current function because min(f`(x)) in [a;b] is when x = b
   while (std::abs(getFunctionValue(x) / m_b) > eps)
   {
      x = x - (getFunctionValue(x) / derivative(x));
      ++m_nForTangentMethod;
   }

   return x;
}

int main()
{
   double x1 = -2.3677;
   double a1 = -2.4;
   double b1 = -2.2;
   double c = -2.375; // from f(x)*f(x)`` > 0
   double m1 = -0.593915;
   double M1 = -0.656718;
   Task task(x1 , a1 , b1 , m1 , M1 , c);
   task.createTableForIterationMethod();
   task.createTableForBisectionMethod();
   task.createTableForChordMethod();
   task.createTableForTangentMethod();
   task.createThirdTable();
   std::cin.get();
}