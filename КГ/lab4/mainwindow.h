#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QGraphicsSceneMouseEvent>
#include <QGraphicsPixmapItem>
#include <QVector>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    enum class  Algorithm
    {
        KOCH_1,
        KOCH_SNOWFLAKE,
        LEAF, //лист
        CARPET, //килим
        NAPKIN,//серветка
        MANDELBORT_SET,

    };

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;
protected:
    void keyPressEvent(QKeyEvent* event) override;
    void paintEvent(QPaintEvent* event) override;
private:
    void mandelbrotSet();
    void drawLeaf(int num);
    void drawSnow(int iter, int x1, int y1, int x5, int y5);
    void simpleUpdate();

    template<typename F>
    void drawCarpet(double x1,double y1,double x2,double y2,int n, F&& func);
    template<typename F>
    void drawNapkin(int x1, int y1, int x2, int y2, int x3, int y3, int n, F&& func);
    void clear();
private:
    Ui::MainWindow *ui;

    QImage m_image;
    QGraphicsScene* m_scene;
    QGraphicsPixmapItem* m_pixmapItem;
    Algorithm m_algorithm;
};

#endif // MAINWINDOW_H
