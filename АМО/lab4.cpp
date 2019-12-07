#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>
#include <algorithm>
#include <vector>


class Task
{
private:
   const double m_a;
   const double m_b;
   std::vector<double> m_errors;
public:
   Task(double a, double b);
   void createFirstTable();
   void createSecondTable();
private:
   double getH(double eps);
   double getIntegral(double x);
   double getPrimitive(double x);
   double getSecondDerivative(double x);
   double getValueByNewtonLeibniz();
   double trapezoid(double h);
};

Task::Task(double a, double b)
   : m_a(a)
   , m_b(b)
{
}

void Task::createFirstTable()
{
   double value, ex_value = getValueByNewtonLeibniz(), h, error;
   printf("First Table\nEps\t\tStep\t\tExact value\t     Error\n");
   for (double eps = 0.1; eps > std::pow(10, -10); eps *= 0.01)
   {
      h = getH(eps);
      value = trapezoid(h);
      error = std::fabs(value - ex_value);
      printf("%.12lf  %.12lf  %.15lf  %.16lf\n", eps, h, ex_value, error);
      m_errors.push_back(error);
   }
}

void Task::createSecondTable()
{
   printf("\n\nRunge principle\nExpected error\t    Step\t    Prodused error\n");
   double eps = 0.1;
   const auto helper = [&](auto&& eps, auto&& error)
   {
      double n = 1 / std::sqrt(eps);
      double R;
      double val_n, val_2n;
      do
      {
         val_n = trapezoid((m_b - m_a) / n);
         val_2n = trapezoid((m_b - m_a) / (2 * n));
         R = std::fabs(val_n - val_2n) / 3;
         n *= 2;
      } while (R > eps);

      double ex_value = getValueByNewtonLeibniz();
      printf("%.16lf  %.12lf  %.16lf\n", error, (m_b - m_a) / n, std::abs(val_2n - ex_value));
   };
   for (const auto error : m_errors)
   {
      helper(eps, error);
      eps *= 0.01;
   }
}

double Task::getH(double eps)
{
   auto max = 0.0, cur = 0.0;
   for (auto i = m_a; i <= m_b; i += 0.1)
   {
      cur = std::abs(getSecondDerivative(i));
      max = std::max(cur, max);
   }
   return std::sqrt((12 * eps) / ( (m_b-m_a)*max));
}

double Task::getIntegral(double x)
{
   return (x / 3 + 0.0001*std::pow(M_E, x));
}

double Task::getPrimitive(double x)
{
   return x*x / 6 + 0.0001*std::pow(M_E, x);
}

double Task::getSecondDerivative(double x)
{
   return 0.0001*std::pow(M_E, x);
}

double Task::getValueByNewtonLeibniz()
{
   return getPrimitive(m_b) - getPrimitive(m_a);
}

double Task::trapezoid(double h)
{
   double psum = getIntegral(m_a) + getIntegral(m_b);
   int n = static_cast<int>((m_b - m_a) / h);
   for (int i = 1; i < n; ++i)
      psum = psum + 2.0*getIntegral(m_a + i*h);

   psum = (h / 2.0)*psum;

   return psum;
}

int main()
{
   Task task(1, 15);
   task.createFirstTable();
   task.createSecondTable();
   std::cin.get();
}