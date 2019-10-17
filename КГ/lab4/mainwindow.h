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
    enum class Fractal
    {
        MANDELBORT_SET,
        HILBERT_CURVE,
        KOCH_SNOWFLAKE
    };

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;
protected:
    void keyPressEvent(QKeyEvent* event) override;
    void paintEvent(QPaintEvent* event) override;
private:
    void mandelbrotSet();
    void simpleUpdate();
    void clear();
private:
    Ui::MainWindow *ui;

    QImage m_image;
    QGraphicsScene* m_scene;
    QGraphicsPixmapItem* m_pixmapItem;
    Fractal m_fractal;
};

#endif // MAINWINDOW_H
