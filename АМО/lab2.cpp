#include <iostream>
#include <cmath>
#include <iomanip>
#include <vector>

class Task
{
   double m_a;
   double m_b;
   double m_m;
   double m_M;
   double m_step;
   mutable std::vector<int> m_nForIterationMethod;
   mutable std::vector<int>  m_nForBisectionMethod;
   mutable std::vector<double> m_mas;

public:
   Task(double a, double b);
   void createTableForIterationMethod();
   void createTableForBisectionMethod();
   void createThirdTable() const;
private:
   double getFunctionValue(double x) const;
   double getFirstDerivativeValue(double x) const;
   void createMass() const;
   void createConstants(double a, double b);


   std::tuple<double, double> getByIterationMethod(double a, double b, double eps) const;
   std::tuple<double, double> getByBisectionMethod(double a, double b, double eps) const;

};

Task::Task(double a, double b)
   : m_a(a)
   , m_b(b)
   , m_m(0)
   , m_M(0)
   , m_step(0.2)
{

   createMass();
}
void Task::createConstants(double a, double b)
{
   if (fabs(getFirstDerivativeValue(a)) > fabs(getFirstDerivativeValue(b)))
   {
      m_M = getFirstDerivativeValue(a);
      m_m = getFirstDerivativeValue(b);
   }
   else
   {
      m_M = getFirstDerivativeValue(b);
      m_m = getFirstDerivativeValue(a);
   }
}

void Task::createMass() const
{
   for(double a = m_a; a <= m_b; a += m_step)
   {
      if(getFunctionValue(a) * getFunctionValue(a+m_step) < 0)
      {
         m_mas.push_back(a);
      }
   }
}

void Task::createTableForIterationMethod()
{
   const auto step = 1e-3;
   const auto limit = 1e-14;
   std::cout << "-----------------------------------\n" <<"IterationMethod\n";
   double a{};
   double b{};
      
   for(size_t i = 0 ; i < m_mas.size() ; ++i)
   {
      std::cout << "\tEps" << "\t\tRoot_" << i + 1  << "\t\t\taccurately" << std::endl;
      a = m_mas[i];
      b = a + m_step;
      createConstants(a, b);
      for (auto eps = 1e-2; eps > limit; eps *= step)
      {
         double my_x{};
         double accurately{};
         std::tie(my_x, accurately) = getByIterationMethod(a, b, eps);
         std::cout << std::fixed << std::setprecision(15) << eps  << '\t' << my_x << '\t' << accurately << std::endl;
      }
   }
   std::cout << "\n-----------------------------------\n";
}

void Task::createTableForBisectionMethod()
{
   const auto step = 1e-3;
   const auto limit = 1e-14;
   std::cout << "----------------------------------- \n" <<"BisectionMethod\n";
   double a{};
   double b{};

   for (size_t i = 0; i < m_mas.size(); ++i)
   {
      std::cout << "\tEps" << "\t\tRoot_" << i + 1 << "\t\t\taccurately" << std::endl;
      a = m_mas[i];
      b = a + m_step;
      for (auto eps = 1e-2; eps > limit; eps *= step)
      {
         double my_x{};
         double accurately{};
         std::tie(my_x, accurately) = getByBisectionMethod(a, b, eps);
         std::cout << std::fixed << std::setprecision(15) << eps << '\t' << my_x << '\t' << accurately << std::endl;
      }
   }
   std::cout << "\n-----------------------------------\n";
}


void Task::createThirdTable() const
{
   std::cout << "TASK_3 - Speed tables" << std::endl << std::endl;
   std::cout << std::setw(17) << "eps" << std::setw(17) << "IterationMethod"
      << std::setw(17) << "BisectionMethod" << std::endl << std::endl;
   const auto step = 1e-3;
   const auto limit = 1e-14;
   auto i = 0;
   for (auto eps = 1e-2; eps > limit; eps *=step, ++i)
   {
      std::cout << std::fixed << std::setprecision(14) << std::setw(16) << eps
         << std::setprecision(0) << std::setw(17) << m_nForIterationMethod[i]
         << std::setw(17) << m_nForBisectionMethod[i] << std::endl;
   }
}

std::tuple<double, double> Task::getByIterationMethod(double a, double b, double eps) const
{
   auto n = 0;
   const auto lambda = 1 / m_M;
   const auto q = 1 - fabs(m_m / m_M);
   auto x = (b + a)/2;
   auto x1 = x;
   auto getCorrectFunctionValue = [&](double x)
   {
      return x - lambda * getFunctionValue(x);
   };
   const auto limit = ((1 - q) * eps / q);
   do
   {
      x = x1;
      x1= getCorrectFunctionValue(x);
      ++n;
   } while (fabs(x1 - x) > limit);
   m_nForIterationMethod.push_back(n);
   return std::make_tuple(x1, fabs(fabs(x1) - fabs(x)) * limit);
}

double Task::getFunctionValue(double x) const
{
   return log(2 + sin(x)) - (x / 10) - 0.5;
}
double Task::getFirstDerivativeValue(double x) const
{
   return   cos(x) / (2 + sin(x)) - 0.1;
}
std::tuple<double, double> Task::getByBisectionMethod(double a, double b, double eps) const
{
   int n = 0;
   double x = 0.0;
   do
   {
      x = (a + b) / 2;
      if (getFunctionValue(x) * getFunctionValue(a) < 0)
      {
         b = x;
      }
      if(getFunctionValue(x) * getFunctionValue(b) < 0)
      {
         a = x;
      }
      ++n;
   } while (fabs(b - a) >= 2 * eps);
   x =  (a + b) / 2;
   m_nForBisectionMethod.push_back(n);
   return std::make_tuple(x, fabs(b - a)/2);
}




int main()
{
   double a1 = -10;
   double b1 = 10;
   Task task(a1, b1);
   task.createTableForIterationMethod();
   task.createTableForBisectionMethod();
   task.createThirdTable();
   std::cin.get();
}