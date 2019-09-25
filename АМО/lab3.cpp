#include <iostream>
#include <vector>
#include <array>
#include <algorithm>

constexpr int LineNumber = 4;
constexpr int ColumnNumber = 5;
using Line = std::array<double, ColumnNumber>;
using SLAR = std::array<Line, LineNumber>;
using solutionType = std::array<double, LineNumber>;
class Task
{

   SLAR m_system;
public:
   explicit Task(const SLAR& system);
   void solveByGaussJordanExclusion() const;
   void solveBySimpleIteration() const;
   void printSlar() const;
private:
   //for SingleDivisionScheme
   void simplifyMatrixByLine(SLAR& system, int line) const;
   //for GaussJordanExclusion
   void subtractionTwoLinesToReduceVariable(SLAR& system, int from, int which) const;
};

int main()
{
   SLAR slar =
   {
      10,	2,	0,	19,	44,
      2,	24,	7,	14,	114,
      10,	14,	29,	4,	108,
      20,	13,	3,	8,	61

   };
   Task task(slar);
   task.printSlar();
   task.solveByGaussJordanExclusion();
   task.solveBySimpleIteration();

   std::cin.get();
}

Task::Task(const SLAR & system)
   : m_system(system)
{
}
void Task::solveBySimpleIteration() const
{
   std::cout << "\nSolveBySimpleIteration\n";
   auto matrix = m_system;
   solutionType  solution{};

   for (int i = 0; i < LineNumber; ++i)
   {
      for (int k = 0; k < LineNumber; ++k)
      {
         if (abs(matrix[i][i]) < abs(matrix[k][i]))
         {
            for (int j = 0; j < ColumnNumber; ++j)
            {
               std::swap(matrix[i][j], matrix[k][j]);
            }
         }
      }
   }
   int readySolutions{ 0 };
   int y{ 0 };
   do
   {
      for (int i = 0; i < LineNumber; ++i)
      {
         y = solution[i];
         solution[i] = matrix[i][LineNumber];
         for (int j = 0; j < LineNumber; ++j)
         {
            if (i != j)
            {
               solution[i] -= matrix[i][j] * solution[j];
            }
         }
         solution[i] /= matrix[i][i];

         if (abs(solution[i] - y) <= 1e-8)
         {
            ++readySolutions;
         }
      }
   } while (readySolutions < LineNumber);


   std::cout << "Result: \n";
   std::copy(solution.begin(), solution.end(), std::ostream_iterator<double>(std::cout, " "));

}

void Task::solveByGaussJordanExclusion() const
{
   std::cout << "\nSolveByGaussJordanExclusion\n";
   auto matrix = m_system;
   simplifyMatrixByLine(matrix, 0);
   simplifyMatrixByLine(matrix, 1);
   simplifyMatrixByLine(matrix, 2);
   simplifyMatrixByLine(matrix, 3);

   subtractionTwoLinesToReduceVariable(matrix, 0, 1);
   subtractionTwoLinesToReduceVariable(matrix, 0, 2);
   subtractionTwoLinesToReduceVariable(matrix, 0, 3);

   subtractionTwoLinesToReduceVariable(matrix, 1, 2);
   subtractionTwoLinesToReduceVariable(matrix, 1, 3);

   subtractionTwoLinesToReduceVariable(matrix, 2, 3);

   solutionType solution;
   solution[0] = matrix[0][ColumnNumber - 1];//< x1
   solution[1] = matrix[1][ColumnNumber - 1];//< x2
   solution[2] = matrix[2][ColumnNumber - 1];//< x3
   solution[3] = matrix[3][ColumnNumber - 1];//< x4
   std::cout << "Result: \n";
   std::copy(solution.begin(), solution.end(), std::ostream_iterator<double>(std::cout, " "));
}

void Task::simplifyMatrixByLine(SLAR& system, int line) const
{
   //divide the first row into the first element
   std::for_each(system[line].begin(), system[line].end(), [firstElement = system[line][line]](double& value)
   {
      value /= firstElement;
   });
   for (int row = line + 1; row < m_system.size(); ++row)
   {
      auto firstElement = system[row][line];
      for (int column = 0; column < m_system[0].size(); ++column)
      {
         system[row][column] -= firstElement * system[line][column];
      }
   }
}

void Task::subtractionTwoLinesToReduceVariable(SLAR& system, int from, int which) const
{
   auto coefficient = system[from][which];
   for (auto i = which; i < ColumnNumber; ++i)
   {
      system[from][i] -= system[which][i] * coefficient;
   }
}

void Task::printSlar() const
{
   for (const auto& line : m_system)
   {
      std::copy(line.begin(), line.end(), std::ostream_iterator<double>(std::cout, " "));
      std::cout << std::endl;
   }
}