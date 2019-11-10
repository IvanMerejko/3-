#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QKeyEvent>
#include <complex>
#include <QDebug>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    m_image = QImage(ui->graphicsView->width(), ui->graphicsView->height(), QImage::Format_RGB32);
    m_image.fill(Qt::white);
    m_scene = new QGraphicsScene(this);
    m_pixmapItem = m_scene->addPixmap(QPixmap::fromImage(m_image));

    ui->graphicsView->setScene(m_scene);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::keyPressEvent(QKeyEvent *event)
{
    switch (event->key())
    {
        case Qt::Key::Key_0:
        {
            m_algorithm = Algorithm::KOCH_1;
            update();
        }break;
        case Qt::Key::Key_1:
        {
            m_algorithm = Algorithm::KOCH_SNOWFLAKE;
            update();
        }break;
        case Qt::Key::Key_2:
        {
            m_algorithm = Algorithm::LEAF;
            update();
        }break;
        case Qt::Key::Key_3:
        {
            m_algorithm = Algorithm::CARPET;
            update();
        }break;
        case Qt::Key::Key_4:
        {
            m_algorithm = Algorithm::NAPKIN;
            update();
        }break;
        case Qt::Key::Key_5:
        {
            m_algorithm = Algorithm::MANDELBORT_SET;
            update();
        }break;
    }
}

void MainWindow::paintEvent(QPaintEvent *event)
{
    clear();
    switch (m_algorithm)
    {
        case Algorithm::KOCH_1:
        {
            drawSnow(5, 530, 380, 270, 380);
        }break;
        case Algorithm::KOCH_SNOWFLAKE:
        {
            drawSnow(5, 270, 380, 530, 380);
            drawSnow(5, 530, 380, 400, 120);
            drawSnow(5, 400, 120, 270, 380);
        }break;
        case Algorithm::LEAF:
        {
            drawLeaf(50);
        }break;
        case Algorithm::CARPET:
        {
            auto drawRect = [this](int A,int B,int C,int D)
            {
                QPainter painter(&m_image);
                QPen pen(Qt::black);
                painter.setPen(pen);

                painter.drawRect(A, B, C-A, D-B);
                painter.end();
            };
            drawRect(90, 10, 550, 470);
            drawCarpet(90, 10, 550, 470,5, drawRect);
        }break;
        case Algorithm::NAPKIN:
        {
            auto trian = [this](int x1, int y1, int x2, int y2, int x3, int y3)
            {
                QPainter painter(&m_image);
                QPen pen(Qt::black);
                painter.setPen(pen);
                painter.drawLine(x1, y1, x2, y2);
                painter.drawLine(x2, y2, x3, y3);
                painter.drawLine(x3, y3, x1, y1);
                painter.end();

            };
            drawNapkin(320,10,600,470,40,470, 5, trian);
            trian(320,10,600,470,40,470);
        }break;
        case Algorithm::MANDELBORT_SET:
        {
            mandelbrotSet();
        }break;
    }

    simpleUpdate();
}

void MainWindow::mandelbrotSet()
{
    const auto width = ui->graphicsView->width();
    const auto height = ui->graphicsView->height();
    const auto calculateValue = [&](auto x, auto y) -> int
    {
        const auto to_double = [](auto& value){ return static_cast<double>(value); };
        std::complex<double> point(to_double(x)/to_double(width)-1.5,
                                  to_double(y)/to_double(height)-0.5);
        // we divide by the image dimensions to get values smaller than 1
        // then apply a translation
        std::complex<double> z(0, 0);
        unsigned int nb_iter = 0;
        while (abs (z) < 2 && nb_iter <= 34)
        {
            z = z * z + point;
            nb_iter++;
        }
        if (nb_iter < 34) return (255*nb_iter)/33;
        else return 0;
    };
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
           auto color = calculateValue(i, j);
           double r = 0.1098+(color*0.00329)*0.45; //расчет
           double g = 0.18824+(color*0.00329)*0.78; //значений
           double b = 0.29412+(color*0.00329)*0.30; //для раскраски м
           QPainter painter(&m_image);
           QColor rgbf; rgbf.setRgbF(r, g, b);
           QPen pen(rgbf);
           painter.setPen(pen);
           painter.drawPoint(i-0.65, j);
        }
    }
}
void MainWindow::simpleUpdate()
{
    m_pixmapItem->setPixmap(QPixmap::fromImage(m_image));
    m_scene->update();
}
void MainWindow::clear()
{
    m_image.fill(Qt::white);
    simpleUpdate();
}

void MainWindow::drawSnow(int iter, int x1, int y1, int x5, int y5)
{
    if (iter == 0) {
        QPainter painter(&m_image);
        QPen pen(Qt::black);
        painter.setPen(pen);
        painter.drawLine(x1, y1, x5, y5);
        painter.end();
        return;
    }

    int deltaX, deltaY, x2, y2, x3, y3, x4, y4;

    deltaX = x5 - x1;
    deltaY = y5 - y1;

    x2 = x1 + deltaX / 3;
    y2 = y1 + deltaY / 3;

    x3 = (int) (0.5 * (x1+x5) + sqrt(3) * (y1-y5)/6);
    y3 = (int) (0.5 * (y1+y5) + sqrt(3) * (x5-x1)/6);

    x4 = x1 + 2 * deltaX / 3;
    y4 = y1 + 2 * deltaY / 3;

    drawSnow(iter-1, x1, y1, x2, y2);
    drawSnow(iter-1, x2, y2, x3, y3);
    drawSnow(iter-1, x3, y3, x4, y4);
    drawSnow(iter-1, x4, y4, x5, y5);
}
void MainWindow::drawLeaf(int num)
{

    QPainter painter(&m_image);
    QPen pen(Qt::green);
    painter.setPen(pen);
    double x = 0, X1;
    double y = 0, Y1;
    double a = 0, b=0, c=0, d=0, e=0, f=0, r=0;
    auto randomBetween = [](auto&& low, auto&& high)
    {
        return (qrand() % ((high + 1) - low) + low);
    };
    for (int i = 1 ;i< 70000;i++)
    {

        r = randomBetween(0,100);
        if ((0<r) && (r<1))
        {
            a = 0; b = 0; c = 0; d = 0.16; e = 0; f = 0;
        }
        else if ((1<r)&&(r<80))
        {
            a = 0.85; b = 0.04; c = -0.04; d = 0.85; e = 0; f = 1.6;
        }
        else if ((80<r)&&(r<90))
        {
            a = 0.2; b = -0.26; c = 0.23; d = 0.22; e = 0; f = 1.6;
        }
        else if ((90<r)&&(r<100))
        {
            a = -0.15; b = 0.28; c = 0.26; d = 0.24; e = 0; f = 0.44;
        }

        X1 = (a * x) + (b * y) + e;
        Y1 = (c * x) + (d * y) + f;
        x = X1;
        y = Y1;
        painter.drawPoint((10+x)*num, (11-y)*num);
        //image.setPixelColor(floor( x + 10 ),floor( 11 - y ), Qt::green);
    }

    painter.end();
}
template <typename F>
void MainWindow::drawCarpet(double x1,double y1,double x2,double y2,int n, F&& func)
{
    double x1n, y1n, x2n, y2n;
    if(n > 0)
    {
        x1n= 2*x1/3+x2 / 3;
        x2n= x1/3+2*x2 / 3;
        y1n= 2*y1/3+y2 / 3;
        y2n= y1/3+2*y2 / 3;

        func(floor(x1n),floor(y1n),floor(x2n),floor(y2n));

        drawCarpet(x1, y1, x1n, y1n, n-1, func);
        drawCarpet(x1n, y1, x2n, y1n, n-1,func);
        drawCarpet(x2n, y1, x2, y1n, n-1, func);
        drawCarpet(x1, y1n, x1n, y2n, n-1, func);
        drawCarpet(x2n, y1n, x2, y2n, n-1, func);
        drawCarpet(x1, y2n, x1n, y2, n-1, func);
        drawCarpet(x1n, y2n, x2n, y2, n-1, func);
        drawCarpet(x2n, y2n, x2, y2, n-1, func);
    }
}
template <typename F>
void MainWindow::drawNapkin(int x1, int y1, int x2, int y2, int x3, int y3, int n, F&& func)
{
    double x1n, y1n, x2n, y2n, x3n, y3n;
    if  (n > 0)
    {
        x1n = (x1 + x2) / 2;
        y1n = (y1 + y2) / 2;
        x2n = (x2 + x3) / 2;
        y2n = (y2 + y3) / 2;
        x3n = (x3 + x1) / 2;
        y3n = (y3 + y1) / 2;
        func(x1n, y1n, x2n, y2n, x3n, y3n);

        drawNapkin(x1, y1, x1n, y1n, x3n, y3n, n - 1, func);
        drawNapkin(x2, y2, x1n, y1n, x2n, y2n, n - 1, func);
        drawNapkin( x3, y3, x2n, y2n, x3n, y3n, n - 1, func);
    }

}
