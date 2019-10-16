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
    enum class Algorithm
    {
        FILL4,
        FILL8,
        LINES,
        XOR
    };

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow()override ;

protected:
    void mousePressEvent(QMouseEvent *event) override;
    void keyPressEvent(QKeyEvent* event) override;
private:
    void fillByRec4(const QPoint&);
    void fillByRec8(const QPoint&);
    void fillByLines();
    void fillByXOR(QPainter&);
    void simpleUpdate();
    void clear();
private:
    Ui::MainWindow *ui;
    QVector<QPoint> m_points;
    QImage m_image;
    QGraphicsScene* m_scene;
    QGraphicsPixmapItem* m_pixmapItem;
    Algorithm m_currentAlgorithm;
};
#endif // MAINWINDOW_H
