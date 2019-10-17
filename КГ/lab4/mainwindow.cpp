#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QKeyEvent>
#include <complex>

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
        case Qt::Key::Key_1:
        {
            m_fractal = Fractal::MANDELBORT_SET;
            update();
        }break;
        case Qt::Key::Key_Escape:
        {
            clear();
        }break;
    }
}

void MainWindow::paintEvent(QPaintEvent *event)
{
    clear();
    switch (m_fractal)
    {
        case Fractal::MANDELBORT_SET:
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
        std::complex<float> point(to_double(x)/to_double(width)-1.5,
                                  to_double(y)/to_double(height)-0.5);
        // we divide by the image dimensions to get values smaller than 1
        // then apply a translation
        std::complex<float> z(0, 0);
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
