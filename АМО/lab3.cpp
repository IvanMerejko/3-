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
   void solveBySingleDivisionScheme() const;
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
               43, -5, 32, 0, -15 ,
               12, 32, 18, 3, 114 ,
               20, 1, 27, 5, 3 ,
               -10, -27, -5, 50, -81
   };
   Task task(slar);;
   task.solveBySingleDivisionScheme();
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
   std::cout << "\nSolveByZedelIteration\n";
   auto matrix = m_system;
   solutionType  previousSolution;

   while(true)
   {
      solutionType currentSolution;
      for(int i = 0; i < LineNumber; ++i)
      {
         currentSolution[i] = matrix[i][ColumnNumber - 1];

         for(int j = 0 ; j < LineNumber ; ++j)
         {
            if(i != j)
            {
               currentSolution[i] -= matrix[i][j] * previousSolution[j];
            }
         }
         currentSolution[i] /= matrix[i][i];
      }
      long double error = 0;
      for (int i = 0; i < LineNumber; ++i)
      {
         error += abs(currentSolution[i] - previousSolution[i]);
      }
      if (error < 1e-8)
      {
         break;
      }
      previousSolution = currentSolution;
   }

   std::copy(previousSolution.begin(), previousSolution.end(), std::ostream_iterator<double>(std::cout, " "));

}

void Task::solveBySingleDivisionScheme() const
{
   std::cout << "\nSolveBySingleDivisionScheme\n";
   auto matrix = m_system;
   simplifyMatrixByLine(matrix, 0);
   simplifyMatrixByLine(matrix, 1);
   simplifyMatrixByLine(matrix, 2);
   solutionType solution;
   solution[0] = matrix[LineNumber - 1][ColumnNumber - 1] / matrix[LineNumber - 1][ColumnNumber - 2]; //< x4
   solution[1] = matrix[LineNumber - 2][ColumnNumber - 1] - matrix[LineNumber - 2][ColumnNumber - 2] * solution[0];//< x3
   solution[2] = matrix[LineNumber - 3][ColumnNumber - 1] - matrix[LineNumber - 3][ColumnNumber - 2] * solution[0]//< x2
                                             - matrix[LineNumber - 3][ColumnNumber - 3] * solution[1];
   solution[3] = matrix[LineNumber - 4][ColumnNumber - 1] - matrix[LineNumber - 4][ColumnNumber - 2] * solution[0] //< x1
                                             - matrix[LineNumber - 4][ColumnNumber - 3] * solution[1]
                                             - matrix[LineNumber - 4][ColumnNumber - 4] * solution[2];
   std::reverse(solution.begin(), solution.end());

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

