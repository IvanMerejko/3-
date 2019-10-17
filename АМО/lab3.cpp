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
	bool solveByGaussJordanExclusion() const;
	bool solveBySimpleIteration(double eps) const;
	void printSlar() const;
private:
	//for GaussJordanExclusion
	bool simplifyMatrixByLine(SLAR& system, int line) const;
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
	if ( task.solveByGaussJordanExclusion() )
	{
		std::cout << "\n Solved \n";
	}
	else
	{
		std::cout << "\n Can not solve because one of the supporting element equal to 0 \n";
	}

	if ( task.solveBySimpleIteration(1e-8) )
	{
		std::cout << "\n Solved \n";
	}
	else
	{
		std::cout << "Solution not found";
	}
	std::cin.get();
}

Task::Task(const SLAR & system)
	: m_system(system)
{
}
bool Task::solveBySimpleIteration(double eps) const
{
	std::cout << "\nSolveBySimpleIteration\n";
	auto matrix = m_system;
	solutionType  solution{};
	const auto iteration_thresholder = 1000;
	auto current_iteration = 0;
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
		++current_iteration;
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
			solution[i] /= !matrix[i][i] ? 1.0 : matrix[i][i];

			if (abs(solution[i] - y) <= eps)
			{
				++readySolutions;
			}
		}
		if ( current_iteration > iteration_thresholder)
		{
			return false;
		}
	} while (readySolutions < LineNumber);


	std::cout << "Result: \n";
	
	for( const auto result: solution)
	{
		printf("%25.16ef", result);
	}

	return true;
}

bool Task::solveByGaussJordanExclusion() const
{
	std::cout << "\nSolveByGaussJordanExclusion\n";
	auto matrix = m_system;
	if ( !simplifyMatrixByLine(matrix, 0) )
	{
		return false;
	}
	if ( !simplifyMatrixByLine(matrix, 1) )
	{
		return false;
	}
	if( !simplifyMatrixByLine(matrix, 2) )
	{
		return false;
	}
	if ( !simplifyMatrixByLine(matrix, 3) )
	{
		return false;
	}

	subtractionTwoLinesToReduceVariable(matrix, 0, 1);
	subtractionTwoLinesToReduceVariable(matrix, 0, 2);
	subtractionTwoLinesToReduceVariable(matrix, 0, 3);

	subtractionTwoLinesToReduceVariable(matrix, 1, 2);
	subtractionTwoLinesToReduceVariable(matrix, 1, 3);

	subtractionTwoLinesToReduceVariable(matrix, 2, 3);

	solutionType solution;
	for(auto i = 0u; i< matrix.size(); ++i)
	{
		solution[i] = matrix[i][ColumnNumber - 1];
	}
	std::cout << "Result: \n";
	for (const auto result : solution)
	{
		printf("%25.16ef", result);
	}
	return true;
}

bool Task::simplifyMatrixByLine(SLAR& system, int line) const
{
	//divide the first row into the first element
	if ( !system[line][line] )
	{
		return false;
	}
	std::for_each(system[line].begin(), system[line].end(), [firstElement = system[line][line]](double& value)
	{
		value /= !firstElement ? 1.0 : firstElement;
	});
	for (int row = line + 1; row < m_system.size(); ++row)
	{
		auto firstElement = system[row][line];
		for (int column = 0; column < m_system[0].size(); ++column)
		{
			system[row][column] -= firstElement * system[line][column];
		}
	}
	return true;
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