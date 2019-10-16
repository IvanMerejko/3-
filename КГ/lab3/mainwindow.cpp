#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QPen>
#include <QPainter>
#include <QMouseEvent>
#include <QStack>
#include <QDebug>
#include <QGraphicsScene>
#include <QVector>
#include <QElapsedTimer>
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    clearFocus();
    m_image = QImage(width(), height(), QImage::Format_RGB32);
    m_image.fill(Qt::white);
    m_scene = new QGraphicsScene(this);
    m_pixmapItem = m_scene->addPixmap(QPixmap::fromImage(m_image));

    ui->graphicsView->setScene(m_scene);
}

MainWindow::~MainWindow()
{
    delete ui;
}
void MainWindow::mousePressEvent(QMouseEvent *event)
{
    const auto buttonEvent = event->button();
    QPainter painter(&m_image);
    QPen pen(Qt::black);
    painter.setPen(pen);
    if( buttonEvent == Qt::LeftButton)
    {
        m_image.fill(Qt::white);
        m_points.push_back(event->pos());
        painter.drawPolyline(m_points.data(), m_points.size());

        if (m_points.size() >=3)
        {
            painter.drawLine(m_points.front(), m_points.back());
        }

    }
    else
    {
        QElapsedTimer timer;
        timer.start();
        switch (m_currentAlgorithm)
        {
            case Algorithm::FILL4:
            {
                qDebug() << "FILL 4";
                fillByRec4(event->pos());
            }break;
            case Algorithm::FILL8:
            {
                qDebug() << "FILL 8";
                fillByRec8(event->pos());
            }break;
            case Algorithm::XOR:
            {
                qDebug() << "XOR";
                m_image.fill(Qt::white);
                simpleUpdate();
                fillByXOR(painter);
            }break;
            case Algorithm::LINES:
            {
                qDebug() << "LINES";
                fillByLines();
            }break;
        }
        auto time = timer.elapsed();
        qDebug() << "Time: " << time;
    }
    painter.end();
    simpleUpdate();
}

void MainWindow::keyPressEvent(QKeyEvent *event)
{
    switch (event->key())
    {
        case Qt::Key_1:
        {
            m_currentAlgorithm = Algorithm::FILL4;
        }break;
        case Qt::Key_2:
        {
            m_currentAlgorithm = Algorithm::FILL8;
        }break;
        case Qt::Key_3:
        {
            m_currentAlgorithm = Algorithm::LINES;
        }break;
        case Qt::Key_4:
        {
            m_currentAlgorithm = Algorithm::XOR;
        }break;
    case Qt::Key_Escape:
        {
            clear();
        }break;
    }
}

void MainWindow::fillByRec4(const QPoint& startPoint)
{
    QStack<QPoint> to_draw;
    to_draw.push(startPoint);
    QPoint top;

    while (!to_draw.empty())
    {
       top = to_draw.pop();
       if (top.x() < 0 || top.x() >= m_image.width() ||
           top.y() < 0 || top.y() >= m_image.height() ||
           m_image.pixelColor(top.x(), top.y()) != Qt::white)
       {
          continue;
       }
       m_image.setPixelColor(top.x(), top.y(), Qt::black);
       to_draw.push({top.x(), top.y() + 1});
       to_draw.push({top.x(), top.y() - 1});
       to_draw.push({top.x() + 1, top.y()});
       to_draw.push({top.x() - 1, top.y()});
    }
}

void MainWindow::fillByRec8(const QPoint &start_point)
{
    QStack<QPoint> to_draw;
    to_draw.push_back(start_point);
    QPoint top;

    while (!to_draw.empty())
    {
        top = to_draw.pop();

        if (top.x() < 0 || top.x() >= m_image.width()  ||
            top.y() < 0 || top.y() >= m_image.height() ||
            m_image.pixelColor(top.x(), top.y()) != Qt::white) {
            continue;
        }
        m_image.setPixelColor(top.x(), top.y(), Qt::black);
        to_draw.push({top.x() + 1, top.y()});
        to_draw.push({top.x(), top.y() + 1});
        to_draw.push({top.x() - 1, top.y()});
        to_draw.push({top.x(), top.y() - 1});

//        to_draw.push({top.x() - 1, top.y() - 1});
//        to_draw.push({top.x() - 1, top.y() + 1});
//        to_draw.push({top.x() + 1, top.y() - 1});
//        to_draw.push({top.x() + 1, top.y() + 1});
    }
}

void MainWindow::fillByLines()
{
    QPoint line;
    int i = 0, j = 0;

    while (i < m_image.height())
    {
        j = 0;
        while (j < m_image.width())
        {
            if (m_image.pixelColor(j, i) != Qt::white)
            {
                while (j < m_image.width() && m_image.pixelColor(j, i) != Qt::white)
                {
                    j++;
                }
                line.setX(j);

                if (j >= m_image.width()) {
                    break;
                }

                while (j < m_image.width() && m_image.pixelColor(j, i) == Qt::white)
                {
                    j++;
                }

                if (j >= m_image.width()) {
                    break;
                }

                line.setY(j);
                for (int k = line.x(); k < line.y(); k++)
                {

                    m_image.setPixelColor(k, i, Qt::black);
                }
            }
            j++;
        }
        i++;
    }
}

void MainWindow::fillByXOR(QPainter& painter)
{
    int i = 0, j = 0;
    bool fl;
    while (i < m_image.height())
    {
        fl = false;
        j = 0;
        while (j < m_image.width())
        {
            if (m_image.pixelColor(j, i) != Qt::white) {
                if (fl == false)
                {
                    do
                    {
                        j++;
                    } while (j < m_image.width() && m_image.pixelColor(j, i) != Qt::white);
                }
                else
                {
                    do
                    {
                        j++;
                    } while (j < m_image.width() && m_image.pixelColor(j, i) == Qt::white);
                }
                fl = !fl;
                j++;
            }
            if (fl)
            {
                int k = j;
                do
                {
                    k++;
                } while (k < m_image.width() && m_image.pixelColor(k, i) == Qt::white);
                if (k > m_image.width())
                {
                    break;
                }
                m_image.setPixelColor(j, i, Qt::black);
            }
            j++;
        }
        i++;
    }
    QBrush brush;
    brush.setColor(Qt::black);
    brush.setStyle(Qt::SolidPattern);

    QPolygonF poly(m_points);
    // Fill polygon
    QPainterPath path;
    path.addPolygon(poly);

    // Draw polygon
    painter.drawPolygon(poly);
    painter.fillPath(path, brush);
}

void MainWindow::simpleUpdate()
{
    m_pixmapItem->setPixmap(QPixmap::fromImage(m_image));
    m_scene->update();
}

void MainWindow::clear()
{
    m_image.fill(Qt::white);
    m_points.clear();
    simpleUpdate();
}


