#include <iostream>
#include <cmath>
#include <iomanip>
#include <tuple>
#include <thread>

using returnableTuple = std::tuple<double, double, int>;


class Task
{
private:
   enum class NumberOfTask
   {
      First,
      Second
   };
private:
   double m_a;
   double m_b;
   const double m_PI;
   double m_x;
   mutable double m_nForSecondTask;

public:

   Task();
   Task(const double a, const double b);
   void createFirstTable() const;
   void createSecondTable() const;
private:
   returnableTuple getSinFunctionValue(NumberOfTask task, double x = 0.0, double eps = 0.0 ) const;
};

Task::Task()
   : Task(0, 0)
{}
Task::Task(const double a, const double b)
   : m_a(a)
   , m_b(b)
   , m_PI(3.14159265)
   , m_x( ((m_a + m_b) /2) * m_PI / 180)
   , m_nForSecondTask(0)
{}
void Task::createFirstTable() const
{
   std::cout << "First Table\n\n";
   std::cout << "eps"
      << std::setw(10) << "n"
      << std::setw(12) << "abs_delta"
      << std::setw(21) << "last (R)"
      << std::endl << std::endl;
   const auto step = 1e-3;
   const auto limit = 1e-14;
   for (auto eps = 1e-2; eps > limit; eps *= step)
   {
      double R;
      int n;
      double result;
      std::tie(result, R, n) = getSinFunctionValue(NumberOfTask::First,m_x, eps);
      std::cout << std::setprecision(2) << std::scientific
         << std::setw(6)  << eps
         << std::setw(6)  << n
         << std::setw(12) << abs(abs(sin(m_x)) - abs(result))
         << std::setw(18) << R
         << std::endl;

      if (eps == 1e-8)
         m_nForSecondTask = n;
   }

}
returnableTuple Task::getSinFunctionValue(NumberOfTask task, double x,  double eps) const
{
   auto U = x, result = x;
   auto k = 1;
   auto lambda = [=](const double x, const int k,const double U)
   {
      return -x * x / ( (2*k + 1)* 2*k)  * U;
   };
   if (task == NumberOfTask::First)
   {
      do
      {
         U = lambda(m_x, k, U);
         result += U;
         k += 1;
      } while (abs(lambda(m_x, k, U)) > eps);

   }
   else
   {
      for(; k < m_nForSecondTask ; ++k)
      {
         U = lambda(x, k, U);
         result += U;
      }
   }
   return std::make_tuple(result, lambda(x, k, U), k);
}
void Task::createSecondTable() const
{
   std::cout << "\n\nSecond Table\n" << std::endl;
   const auto h = (m_b - m_a) / 10;
   std::cout << "x_i"
      << std::setw(21) << "abs_delta"
      << std::setw(21) << "last (R)"
      << std::endl << std::endl;
   for (int i = 0; i < 10; i++)
   {
      const auto x = m_a + h * i;
      double R;
      double result;
      int unused;
      std::tie(result, R, unused) = getSinFunctionValue(NumberOfTask::Second, x*m_PI / 180);
      std::cout << std::defaultfloat << std::setw(7) << std::setprecision(4) << x
         << std::setw(17) << abs(abs(sin(x*m_PI / 180)) - abs(result))
         << std::setw(22) << abs(R) << std::endl;
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